# import os
# import time
# from google.oauth2.credentials import Credentials
# from googleapiclient.discovery import build
# from googleapiclient.http import MediaFileUpload
# from googleapiclient.errors import HttpError

# def upload_to_youtube(video_file: str, title: str, description: str, tags: list, is_short: bool = False, max_retries: int = 3) -> bool:
#     client_id = os.environ.get("YT_CLIENT_ID")
#     client_secret = os.environ.get("YT_CLIENT_SECRET")
#     refresh_token = os.environ.get("YT_REFRESH_TOKEN")

#     if not client_id or not client_secret or not refresh_token:
#         print("❌ Error: YouTube OAuth credentials missing.")
#         return False

#     credentials = Credentials(
#         token=None,
#         refresh_token=refresh_token,
#         client_id=client_id,
#         client_secret=client_secret,
#         token_uri="https://oauth2.googleapis.com/token"
#     )

#     # Build client with custom socket timeout to prevent network drop drops
#     youtube = build("youtube", "v3", credentials=credentials, http_timeout=60.0)

#     body = {
#         "snippet": {
#             "title": title[:100],
#             "description": description,
#             "tags": tags,
#             "categoryId": "24"  # Entertainment / Ambience
#         },
#         "status": {
#             "privacyStatus": "public",  # Change to "private" if you want to review them first
#             "selfDeclaredMadeForKids": False
#         }
#     }

#     # Use larger chunks (5MB) for stability on long videos
#     media = MediaFileUpload(video_file, chunksize=5 * 1024 * 1024, resumable=True)

#     print(f"   -> Uploading {'Short' if is_short else 'Long-Form'} video to YouTube...")
    
#     # Retry loop to handle minor network/SSL interruptions automatically
#     for attempt in range(1, max_retries + 1):
#         try:
#             request = youtube.videos().insert(
#                 part="snippet,status",
#                 body=body,
#                 media_body=media
#             )

#             response = None
#             while response is None:
#                 status, response = request.next_chunk()
#                 if status:
#                     print(f"   -> Progress: {int(status.progress() * 100)}%")

#             print(f"✅ Successfully uploaded! Video ID: {response.get('id')}")
#             return True

#         except (HttpError, Exception) as e:
#             print(f"⚠️ Upload attempt {attempt} failed due to error: {e}")
#             if attempt < max_retries:
#                 wait_time = attempt * 5
#                 print(f"   -> Retrying upload in {wait_time} seconds...")
#                 time.sleep(wait_time)
#             else:
#                 print("❌ All upload retry attempts failed.")
#                 return False

#     return False