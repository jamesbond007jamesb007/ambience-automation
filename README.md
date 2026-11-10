# YouTube Hybrid Ambience Automation 🌧️☕

An autonomous Python pipeline that transforms short AI-generated video assets (e.g., from Google Flow) into a full hybrid content strategy: looping them into **10-minute long-form videos (16:9)** and cropping/trimming them into **30-second vertical Shorts (9:16)**. It uses **Gemini Flash-Lite** to automatically generate SEO-optimized titles, relaxing descriptions, and trending hashtags, and leverages the **YouTube Data API v3** to publish everything automatically via **GitHub Actions**.

---

## 📂 Repository Structure

```text
youtube-ambience-automation/
│
├── .github/
│   └── workflows/
│       └── daily_upload.yml       # GitHub Actions automated cron schedule
│
├── input_assets/
│   ├── rain_window.mp4            # Place your Google Flow input videos here (.mp4)
│   ├── cozy_fireplace.mp4
│   └── cafe_night.mp4
│
├── src/
│   ├── __init__.py                # Package initializer
│   ├── script_generator.py        # Gemini API metadata and tag generator
│   ├── video_transformer.py       # MoviePy processing (loops, crops, resizes)
│   └── youtube_uploader.py        # OAuth2 handler & YouTube Data API uploader
│
├── .env.example                   # Local environment variable template
├── .gitignore                     # Excludes temporary builds and credentials
├── main.py                        # Master orchestration script
├── requirements.txt               # Python package dependencies
└── README.md                      # Project documentation