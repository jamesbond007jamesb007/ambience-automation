import os
import sys
import random
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from src.script_generator import generate_ambience_metadata
from src.video_transformer import create_long_form_video, create_short_video
from src.youtube_uploader import upload_to_youtube

def main():
    print("🚀 Starting Hybrid Ambience Automation Pipeline (Local Mode)...")

    # A rich pool of ambient sub-niches to pull from randomly
    master_topics = [
        "rain window",
        "cozy fireplace",
        "lofi cafe night",
        "snow falling window",
        "thunderstorm night",
        "library ambience",
        "train window night",
        "ocean waves night",
        "autumn forest rain",
        "campfire crackling"
    ]

    # Randomly select 3 different topics for this specific run
    ambience_topics = random.sample(master_topics, 3)
    print(f"🎯 Selected topics for today's run: {ambience_topics}")

    for topic in ambience_topics:
        print(f"\n----------------------------------------")
        print(f"🎬 Processing Ambience Topic: {topic}")
        print(f"----------------------------------------")

        # --- 1. PROCESS LONG-FORM VIDEO (30 mins = 1800s, or 1 hour = 3600s) ---
        long_output_path = "temp_long.mp4"
        
        # Change target_duration to 1800 (30 mins) or 3600 (1 hour) below:
        long_success = create_long_form_video(
            query_keyword=topic, 
            output_path=long_output_path, 
            target_duration=600  # <--- Set your desired length in seconds here
        )

        if long_success:
            print("🤖 Generating metadata for Long-Form video via Gemini...")
            long_meta = generate_ambience_metadata(topic, is_short=False)
            
            print(f"📤 Uploading Long-Form: {long_meta['title']}")
            upload_to_youtube(
                video_file=long_output_path,
                title=long_meta["title"],
                description=long_meta["description"],
                tags=long_meta["tags"],
                is_short=False
            )

        if os.path.exists(long_output_path):
            os.remove(long_output_path)

        # --- 2. PROCESS SHORT VIDEO (30 secs, 9:16) ---
        short_output_path = "temp_short.mp4"
        short_success = create_short_video(
            query_keyword=topic, 
            output_path=short_output_path, 
            target_duration=30
        )

        if short_success:
            print("🤖 Generating metadata for Short via Gemini...")
            short_meta = generate_ambience_metadata(topic, is_short=True)
            
            print(f"📤 Uploading Short: {short_meta['title']}")
            upload_to_youtube(
                video_file=short_output_path,
                title=short_meta["title"],
                description=short_meta["description"],
                tags=short_meta["tags"],
                is_short=True
            )

        if os.path.exists(short_output_path):
            os.remove(short_output_path)

    print("\n✨ All dynamic tasks completed successfully!")

if __name__ == "__main__":
    main()
