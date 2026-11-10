# import os
# from PIL import Image

# # --- PIL COMPATIBILITY FIX FOR MOVIEPY ---
# if not hasattr(Image, 'ANTIALIAS'):
#     Image.ANTIALIAS = Image.LANCZOS
# # ----------------------------------------

# from moviepy.editor import VideoFileClip, concatenate_videoclips

# def create_long_form_video(input_path: str, output_path: str, target_duration: int = 600) -> bool:
#     """
#     Safely stitches a short clip into a long-form video by concatenating safe subclips.
#     """
#     clip = None
#     final_clip = None
#     try:
#         print(f"   -> Processing Long-Form (16:9, {target_duration}s) for {input_path}...")
#         clip = VideoFileClip(input_path)
        
#         # Trim slightly shorter than actual duration to avoid boundary frame errors
#         safe_duration = max(clip.duration - 0.3, 1.0)
#         sub = clip.subclip(0, safe_duration)
        
#         # Concatenate clips repeatedly until target duration is reached
#         clips_list = []
#         current_dur = 0
#         while current_dur < target_duration:
#             clips_list.append(sub)
#             current_dur += safe_duration
            
#         final_clip = concatenate_videoclips(clips_list).subclip(0, target_duration)
        
#         final_clip.write_videofile(
#             output_path,
#             fps=24,
#             codec="libx264",
#             audio_codec="aac",
#             logger=None
#         )
#         return True
#     except Exception as e:
#         print(f"❌ Long-Form Rendering Error: {e}")
#         return False
#     finally:
#         if final_clip: final_clip.close()
#         if clip: clip.close()

# def create_short_video(input_path: str, output_path: str, target_duration: int = 30) -> bool:
#     """
#     Safely converts and crops a short clip into a vertical 9:16 Short.
#     """
#     clip = None
#     vertical_clip = None
#     try:
#         print(f"   -> Processing Short (9:16 vertical, {target_duration}s) for {input_path}...")
#         clip = VideoFileClip(input_path)
        
#         safe_duration = max(clip.duration - 0.3, 1.0)
#         sub = clip.subclip(0, safe_duration)
        
#         clips_list = []
#         current_dur = 0
#         while current_dur < target_duration:
#             clips_list.append(sub)
#             current_dur += safe_duration
            
#         looped = concatenate_videoclips(clips_list).subclip(0, target_duration)
        
#         # Crop 16:9 horizontal to 9:16 vertical center crop
#         w, h = looped.size
#         new_w = int(h * (9 / 16))
#         x_center = w / 2
        
#         vertical_clip = looped.crop(
#             x1=x_center - new_w/2, 
#             y1=0, 
#             x2=x_center + new_w/2, 
#             y2=h
#         ).resize((1080, 1920))

#         vertical_clip.write_videofile(
#             output_path,
#             fps=24,
#             codec="libx264",
#             audio_codec="aac",
#             logger=None
#         )
#         return True
#     except Exception as e:
#         print(f"❌ Short Rendering Error: {e}")
#         return False
#     finally:
#         if vertical_clip: vertical_clip.close()
#         if clip: clip.close()