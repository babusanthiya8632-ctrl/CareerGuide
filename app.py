import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from google import genai
from chatbot_config import SYSTEM_PROMPT

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "gemini-3.1-flash-lite"

client = genai.Client(api_key=API_KEY) if API_KEY else None


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    user_message = str(data.get("message", "")).strip()

    if not user_message:
        return jsonify({"reply": "Please enter a question."}), 400

    if client is None:
        return jsonify({"reply": "Gemini API key is not configured. Please add it to the .env file."}), 500

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=user_message,
            config={
                "system_instruction": SYSTEM_PROMPT,
                "temperature": 0.3,
                "max_output_tokens": 800,
            },
        )

        reply = response.text or "Sorry, I could not generate a response."
        return jsonify({"reply": reply})

    except Exception:
        return jsonify({
            "reply": "Sorry, I am unable to respond right now. Please try again later."
        }), 500


if __name__ == "__main__":
    app.run(debug=True)
