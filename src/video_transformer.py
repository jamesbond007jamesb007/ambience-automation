import os
import random
import requests
from PIL import Image

if not hasattr(Image, 'ANTIALIAS'):
    Image.ANTIALIAS = Image.LANCZOS

from moviepy.editor import VideoFileClip, concatenate_videoclips

TRACKER_FILE = "used_video_ids.txt"

def load_used_ids():
    if not os.path.exists(TRACKER_FILE):
        return set()
    with open(TRACKER_FILE, "r") as f:
        return set(line.strip() for line in f if line.strip())

def save_used_id(video_id):
    with open(TRACKER_FILE, "a") as f:
        f.write(f"{video_id}\n")

def fetch_specific_pixabay_video(query: str, output_path: str) -> bool:
    """Fetches a unique, audio-verified video from Pixabay that hasn't been used yet."""
    api_key = os.environ.get("PIXABAY_API_KEY")
    if not api_key:
        print("⚠️ PIXABAY_API_KEY missing.")
        return False

    url = "https://pixabay.com/api/videos/"
    params = {"key": api_key, "q": query, "video_type": "film", "per_page": 20}

    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            hits = data.get("hits", [])
            
            used_ids = load_used_ids()
            fresh_hits = [h for h in hits if str(h["id"]) not in used_ids]
            if not fresh_hits:
                fresh_hits = hits

            random.shuffle(fresh_hits)

            for hit in fresh_hits:
                video_id = str(hit["id"])
                video_url = hit["videos"]["medium"]["url"]
                
                vid_data = requests.get(video_url)
                with open(output_path, "wb") as f:
                    f.write(vid_data.content)

                try:
                    temp_clip = VideoFileClip(output_path)
                    has_audio = temp_clip.audio is not None
                    temp_clip.close()

                    if has_audio:
                        save_used_id(video_id)
                        return True
                except Exception:
                    pass

                if os.path.exists(output_path):
                    os.remove(output_path)
    except Exception as e:
        print(f"❌ Pixabay API Error: {e}")
    
    return False

def create_long_form_video(query_keyword: str, output_path: str, target_duration: int = 600) -> bool:
    print(f"   -> [Long-Form] Searching fresh Pixabay asset for '{query_keyword}'...")
    if not fetch_specific_pixabay_video(query_keyword, output_path):
        return False

    clip = None
    final_clip = None
    try:
        print(f"   -> Processing Long-Form (16:9, {target_duration}s)...")
        clip = VideoFileClip(output_path)
        safe_duration = max(clip.duration - 0.3, 1.0)
        sub = clip.subclip(0, safe_duration)
        
        clips_list = []
        current_dur = 0
        while current_dur < target_duration:
            clips_list.append(sub)
            current_dur += safe_duration
            
        final_clip = concatenate_videoclips(clips_list).subclip(0, target_duration)
        final_clip.write_videofile("temp_long_final.mp4", fps=24, codec="libx264", audio_codec="aac", logger=None)
        
        os.replace("temp_long_final.mp4", output_path)
        return True
    except Exception as e:
        print(f"❌ Long-Form Rendering Error: {e}")
        return False
    finally:
        if final_clip: final_clip.close()
        if clip: clip.close()

def create_short_video(query_keyword: str, output_path: str, target_duration: int = 30) -> bool:
    print(f"   -> [Short] Searching SEPARATE fresh Pixabay asset for '{query_keyword}'...")
    
    # Use a temporary filename so it doesn't overwrite anything else
    temp_short_source = "temp_short_source.mp4"
    if not fetch_specific_pixabay_video(query_keyword, temp_short_source):
        return False

    clip = None
    vertical_clip = None
    try:
        print(f"   -> Processing Short (9:16 vertical, {target_duration}s)...")
        clip = VideoFileClip(temp_short_source)
        safe_duration = max(clip.duration - 0.3, 1.0)
        sub = clip.subclip(0, safe_duration)
        
        clips_list = []
        current_dur = 0
        while current_dur < target_duration:
            clips_list.append(sub)
            current_dur += safe_duration
            
        looped = concatenate_videoclips(clips_list).subclip(0, target_duration)
        
        w, h = looped.size
        new_w = int(h * (9 / 16))
        x_center = w / 2
        
        vertical_clip = looped.crop(
            x1=x_center - new_w/2, y1=0, x2=x_center + new_w/2, y2=h
        ).resize((1080, 1920))

        vertical_clip.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac", logger=None)
        return True
    except Exception as e:
        print(f"❌ Short Rendering Error: {e}")
        return False
    finally:
        if vertical_clip: vertical_clip.close()
        if clip: clip.close()
        if os.path.exists(temp_short_source): os.remove(temp_short_source)