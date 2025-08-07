import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get Gemini API Key from environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found. Please add it to your .env file.")

# Configure Gemini client
genai.configure(api_key=GEMINI_API_KEY)

# Use Gemini 1.5 Flash (fast and optimized)
model = genai.GenerativeModel("gemini-2.0-flash")

def summarize_detections(detections, stream_id):
    """
    Generate a natural language summary of OpenCV detections.
    
    Args:
        detections (list): List of detected objects (e.g., faces).
        stream_id (int): ID of the video stream.

    Returns:
        str: Gemini-generated summary.
    """
    if not detections:
        prompt = f"No objects detected in stream {stream_id}. Generate a brief update for the dashboard."
    else:
        detection_text = "\n".join([
            f"- {d['type']} at (x={d['x']}, y={d['y']}, w={d['width']}, h={d['height']})"
            for d in detections
        ])
        prompt = f"""
You're a security assistant AI. Based on the detections below, generate a clear, human-readable summary.

Stream ID: {stream_id}
Detections:
{detection_text}

Summarize how many faces were detected and note anything unusual or alert-worthy.
"""

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"[Gemini Error] {e}")
        return "⚠️ Unable to generate summary at this time."
