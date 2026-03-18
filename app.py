"""
Flask web interface for the LEX Legal AI chatbot.

Run (dev):
    python app.py

Run (production - Windows):
    waitress-serve --threads=4 --port=5000 app:app
"""

import os
import sys
import traceback
from functools import lru_cache
from flask import Flask, request, jsonify, send_from_directory

# Ensure path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ✅ Load CrewAI ONCE
from crew import run_query

app = Flask(__name__)

# 🔥 Optional: limit request size (prevents abuse)
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024  # 2MB


# ✅ Cache for repeated queries
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
        answer = cached_query(user_query)

        return jsonify({
            "response": answer,
            "disclaimer": True,
        })

    except Exception as e:
        traceback.print_exc()
        return jsonify({
            "error": f"Error: {str(e)}"
        }), 500


if __name__ == "__main__":
    print("=" * 52)
    print("  LEX — Legal AI  |  Web Interface")
    print("  Open http://localhost:5000")
    print("=" * 52)

    # ✅ DEV MODE ONLY (not used with waitress)
    app.run(host="0.0.0.0", port=5000, debug=False)