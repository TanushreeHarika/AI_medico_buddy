from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
import base64
from datetime import datetime

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# ===== CONFIG =====
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_KEY", "")

# ===== GEMINI SETUP =====
genai = None
model = None
vision_model = None

try:
    import google.generativeai as google_genai
    if GEMINI_API_KEY:
        google_genai.configure(api_key=GEMINI_API_KEY)
        model = google_genai.GenerativeModel("gemini-2.0-flash")
        vision_model = google_genai.GenerativeModel("gemini-2.0-flash")
        genai = google_genai
        print("✅ Gemini AI initialized successfully")
    else:
        print("⚠ GEMINI_API_KEY not set — AI endpoints will return fallback responses")
except ImportError:
    print("⚠ google-generativeai not installed — run: pip install google-generativeai")

# ===== SUPABASE SETUP =====
supabase_client = None
try:
    from supabase import create_client
    if SUPABASE_URL and SUPABASE_KEY:
        supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("✅ Supabase client initialized successfully")
    else:
        print("⚠ Supabase credentials not set — hospital notifications will be logged locally")
except ImportError:
    print("⚠ supabase not installed — run: pip install supabase")


# ===== EMERGENCY AGENT =====
from agents.emergency_agent import EmergencyAgent
emergency_agent = EmergencyAgent(supabase_client)


# ===== AI CHAT ENDPOINT =====
@app.route("/api/ai/chat", methods=["POST"])
def ai_chat():
    data = request.get_json()
    message = data.get("message", "")

    if not message:
        return jsonify({"error": "Message is required"}), 400

    if model:
        try:
            system_prompt = (
                "You are LifePulse AI, a medical first-aid assistant. "
                "Provide clear, step-by-step first aid guidance. "
                "Always remind users to call emergency services for serious conditions. "
                "Use bullet points and numbered lists for clarity. "
                "Add relevant emojis for visual cues. "
                "Always include a disclaimer that you are not a substitute for professional medical advice."
            )
            response = model.generate_content(f"{system_prompt}\n\nUser question: {message}")
            return jsonify({"response": response.text})
        except Exception as e:
            return jsonify({"response": f"AI processing error: {str(e)}. Please try again."}), 200

    return jsonify({"response": get_fallback_response(message)})


# ===== AI VISION ENDPOINT =====
@app.route("/api/ai/vision", methods=["POST"])
def ai_vision():
    message = request.form.get("message", "Analyze this medical image and provide first aid guidance.")
    image_file = request.files.get("image")

    if not image_file:
        return jsonify({"error": "Image is required"}), 400

    if vision_model:
        try:
            import PIL.Image
            import io

            image_data = image_file.read()
            image = PIL.Image.open(io.BytesIO(image_data))

            system_prompt = (
                "You are LifePulse AI, a medical first-aid assistant with vision capabilities. "
                "Analyze the provided image in a medical context. "
                "Identify any visible injuries, conditions, or medical concerns. "
                "Provide step-by-step first aid guidance based on what you observe. "
                "If the image is unclear or not medically relevant, say so politely. "
                "Always remind users this is not a substitute for professional medical examination."
            )

            response = vision_model.generate_content([f"{system_prompt}\n\nUser message: {message}", image])
            return jsonify({"response": response.text})
        except Exception as e:
            return jsonify({"response": f"Vision analysis error: {str(e)}. Please try again."}), 200

    return jsonify({
        "response": (
            "🔍 **Image Analysis (Demo Mode)**\n\n"
            "The AI vision model is not configured. To enable image analysis:\n\n"
            "1. Set your `GEMINI_API_KEY` environment variable\n"
            "2. Install: `pip install google-generativeai Pillow`\n"
            "3. Restart the Flask server\n\n"
            f"Your message: \"{message}\"\n\n"
            "⚠ For real medical image analysis, always consult a healthcare professional."
        )
    })


# ===== EMERGENCY TRIGGER ENDPOINT =====
@app.route("/api/emergency/trigger", methods=["POST"])
def trigger_emergency():
    data = request.get_json()
    condition = data.get("condition", "Unknown Emergency")
    severity = data.get("severity", "critical")
    lat = data.get("lat", 0)
    lng = data.get("lng", 0)
    address = data.get("address", "Unknown Location")

    result = emergency_agent.trigger(
        condition=condition,
        severity=severity,
        lat=lat,
        lng=lng,
        address=address,
    )

    return jsonify(result)


# ===== HEALTH CHECK =====
@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "LifePulse Backend",
        "gemini_configured": model is not None,
        "supabase_configured": supabase_client is not None,
        "timestamp": datetime.utcnow().isoformat(),
    })


def get_fallback_response(query):
    q = query.lower()
    if "cpr" in q:
        return (
            "🫀 **CPR Steps:**\n\n"
            "1. Call 911 immediately\n"
            "2. Place person on firm, flat surface\n"
            "3. Push hard and fast on center of chest (100-120/min)\n"
            "4. Push at least 2 inches deep\n"
            "5. After 30 compressions, give 2 rescue breaths\n"
            "6. Continue until help arrives\n\n"
            "⚠ Connect your Gemini API key for detailed AI responses."
        )
    if "heart" in q or "chest" in q:
        return (
            "❤️ **Heart Attack Signs:**\n\n"
            "• Chest pain or pressure\n"
            "• Pain in arm, jaw, neck, or back\n"
            "• Shortness of breath\n"
            "• Cold sweat, nausea\n\n"
            "**Action:** Call 911, chew aspirin if not allergic, stay calm.\n\n"
            "⚠ Connect your Gemini API key for detailed AI responses."
        )
    return (
        f"🏥 Thank you for asking about \"{query}\".\n\n"
        "**General First Aid Principles:**\n"
        "1. Stay calm and assess the situation\n"
        "2. Call emergency services if serious\n"
        "3. Do not move injured persons unless in danger\n"
        "4. Monitor breathing and consciousness\n\n"
        "⚠ Set GEMINI_API_KEY for AI-powered responses."
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_ENV", "development") == "development"
    print(f"\n🚀 LifePulse Backend running on http://localhost:{port}")
    print(f"   Gemini AI: {'✅ Ready' if model else '❌ Not configured'}")
    print(f"   Supabase:  {'✅ Ready' if supabase_client else '❌ Not configured'}\n")
    app.run(host="0.0.0.0", port=port, debug=debug)
