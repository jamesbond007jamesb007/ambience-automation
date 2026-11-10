# import os
# import sys
# from dotenv import load_dotenv

# load_dotenv()
# sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# from src.script_generator import generate_ambience_metadata
# from src.video_transformer import create_long_form_video, create_short_video
# from src.youtube_uploader import upload_to_youtube

# def main():
#     print("🚀 Starting Hybrid Ambience Automation Pipeline...")

#     input_dir = "input_assets"
#     if not os.path.exists(input_dir):
#         print(f"❌ Error: '{input_dir}' directory not found. Please create it and add your input videos.")
#         return

#     # Find all mp4 files in input_assets/
#     video_files = [f for f in os.listdir(input_dir) if f.endswith(".mp4")]

#     if not video_files:
#         print(f"❌ Error: No .mp4 files found in '{input_dir}'.")
#         return

#     print(f"📁 Found {len(video_files)} input video(s) to process.")

#     for filename in video_files:
#         input_path = os.path.join(input_dir, filename)
#         print(f"\n----------------------------------------")
#         print(f"🎬 Processing input asset: {filename}")
#         print(f"----------------------------------------")

#         # --- 1. PROCESS LONG-FORM VIDEO (10 mins, 16:9) ---
#         long_output_path = "temp_long.mp4"
#         long_success = create_long_form_video(input_path, long_output_path, target_duration=600)

#         if long_success:
#             print("🤖 Generating metadata for Long-Form video via Gemini...")
#             long_meta = generate_ambience_metadata(filename, is_short=False)
            
#             print(f"📤 Uploading Long-Form: {long_meta['title']}")
#             upload_to_youtube(
#                 video_file=long_output_path,
#                 title=long_meta["title"],
#                 description=long_meta["description"],
#                 tags=long_meta["tags"],
#                 is_short=False
#             )

#         if os.path.exists(long_output_path):
#             os.remove(long_output_path)

#         # --- 2. PROCESS SHORT VIDEO (30 secs, 9:16) ---
#         short_output_path = "temp_short.mp4"
#         short_success = create_short_video(input_path, short_output_path, target_duration=30)

#         if short_success:
#             print("🤖 Generating metadata for Short via Gemini...")
#             short_meta = generate_ambience_metadata(filename, is_short=True)
            
#             print(f"📤 Uploading Short: {short_meta['title']}")
#             upload_to_youtube(
#                 video_file=short_output_path,
#                 title=short_meta["title"],
#                 description=short_meta["description"],
#                 tags=short_meta["tags"],
#                 is_short=True
#             )

#         if os.path.exists(short_output_path):
#             os.remove(short_output_path)

#     print("\n✨ All tasks completed successfully!")

# if __name__ == "__main__":
#     main()