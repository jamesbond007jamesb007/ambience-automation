import os
from google import genai

def generate_ambience_metadata(filename: str, is_short: bool = False) -> dict:
    """
    Uses Gemini to analyze the filename and generate tailored metadata, 
    titles, descriptions, and trending hashtags for ambience videos.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    
    # Extract clean topic name from filename (e.g., 'rain_window.mp4' -> 'rain window')
    clean_name = os.path.splitext(filename)[0].replace("_", " ").title()

    if not api_key:
        print("⚠️ Warning: GEMINI_API_KEY missing. Using fallback metadata.")
        return get_fallback_metadata(clean_name, is_short)

    try:
        client = genai.Client(api_key=api_key)
        
        format_type = "YouTube Short (under 60s, vertical)" if is_short else "Long-form Ambience Video (10 minutes, horizontal)"
        
        prompt = (
            f"Generate YouTube metadata for a relaxing ambience video in the '{clean_name}' theme. "
            f"This video format is a {format_type}. "
            "Return the response strictly in this exact format: "
            "TITLE: [Catchy title with emojis] \n"
            "DESCRIPTION: [Relaxing description with a call to subscribe] \n"
            "TAGS: tag1, tag2, tag3, tag4, tag5"
        )

        response = client.models.generate_content(
            model="gemini-flash-lite-latest",
            contents=prompt,
        )

        if not response.text:
            return get_fallback_metadata(clean_name, is_short)

        lines = response.text.strip().split("\n")
        title = f"Relaxing {clean_name} Ambience 🌧️"
        description = f"Immerse yourself in this soothing {clean_name} soundscape. Perfect for sleep, study, and deep relaxation."
        tags = [clean_name.lower(), "ambience", "relaxation", "sleep sounds", "study music"]

        for line in lines:
            if line.startswith("TITLE:"):
                title = line.replace("TITLE:", "").strip()
            elif line.startswith("DESCRIPTION:"):
                description = line.replace("DESCRIPTION:", "").strip()
            elif line.startswith("TAGS:"):
                tags = [t.strip() for t in line.replace("TAGS:", "").split(",")]

        # Append trending hashtags for shorts or long form
        if is_short:
            title = f"{title} #shorts #relax"
            tags.extend(["shorts", "ambience"])
        else:
            tags.extend(["ambient sounds", "deep sleep"])

        return {
            "title": title[:100],  # YouTube max title length constraint
            "description": description,
            "tags": tags
        }

    except Exception as e:
        print(f"❌ Gemini API Error: {e}")
        return get_fallback_metadata(clean_name, is_short)

def get_fallback_metadata(name: str, is_short: bool) -> dict:
    if is_short:
        return {
            "title": f"Peaceful {name} #shorts #ambience",
            "description": f"Relaxing {name} moment. Subscribe for daily ambience!",
            "tags": [name.lower(), "shorts", "ambience", "relax"]
        }
    else:
        return {
            "title": f"Relaxing {name} Ambience for Sleep and Study (10 Hours)",
            "description": f"Enjoy the soothing soundscape of {name}. Designed for deep focus, stress relief, and falling asleep.",
            "tags": [name.lower(), "ambience", "sleep sounds", "study music", "relaxation"]
        }