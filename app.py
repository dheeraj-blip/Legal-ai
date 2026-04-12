"""
Flask web interface for the LEX Legal AI chatbot.

Run (dev):
    python app.py

Run (production - Windows):
    waitress-serve --threads=4 --port=5000 app:app
"""

import os
import sys
import json
import traceback
from functools import lru_cache
from dotenv import load_dotenv
from flask import Flask, request, jsonify, send_from_directory, send_file

# Ensure path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ✅ Load .env BEFORE importing crew/agents (they read keys at import time)
load_dotenv()

# ✅ Load CrewAI ONCE
from crew import run_query
from doc_generator import generate_document

app = Flask(__name__)

# 🔥 Optional: limit request size (prevents abuse)
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024  # 2MB


# ✅ Cache for repeated queries (now handles tuples)
@lru_cache(maxsize=100)
def cached_query(q):
    return run_query(q)


@app.route("/")
def index():
    here = os.path.dirname(os.path.abspath(__file__))
    return send_from_directory(here, "style2.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    user_query = (data.get("query") or "").strip()

    if not user_query:
        return jsonify({"error": "Empty query"}), 400

    try:
        answer, category = cached_query(user_query)

        return jsonify({
            "response": answer,
            "category": category,
            "disclaimer": True,
        })

    except Exception as e:
        traceback.print_exc()
        return jsonify({
            "error": f"Error: {str(e)}"
        }), 500


@app.route("/api/generate-doc", methods=["POST"])
def generate_doc():
    """Generate a legal document PDF based on the chat context."""
    data = request.get_json(force=True)
    user_query = (data.get("query") or "").strip()
    ai_response = (data.get("response") or "").strip()
    category = (data.get("category") or "").strip()

    if not user_query or not ai_response or not category:
        return jsonify({"error": "Missing query, response, or category"}), 400

    try:
        pdf_path = generate_document(category, user_query, ai_response)
        return send_file(
            pdf_path,
            mimetype="application/pdf",
            as_attachment=True,
            download_name=f"legal_document_{category.lower()}.pdf",
        )
    except Exception as e:
        traceback.print_exc()
        return jsonify({
            "error": f"Document generation failed: {str(e)}"
        }), 500



@app.route("/api/translate", methods=["POST"])
def translate():
    """Translate text using translatepy (auto-rotates free services, no AI)."""
    data = request.get_json(force=True)
    text = (data.get("text") or "").strip()
    target = (data.get("target") or "hi").strip()

    if not text:
        return jsonify({"error": "No text to translate"}), 400

    try:
        from translatepy import Translator
        translator = Translator()
        result = translator.translate(text, destination_language=target, source_language="en")
        return jsonify({"translated": str(result), "target": target})

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": f"Translation failed: {str(e)}"}), 500


if __name__ == "__main__":
    print("=" * 52)
    print("  LEX — Legal AI  |  Web Interface")
    print("  Open http://localhost:5000")
    print("=" * 52)

    # ✅ DEV MODE ONLY (not used with waitress)
    app.run(host="0.0.0.0", port=5000, debug=False)