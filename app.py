"""Flask web interface for the LEX Legal AI chatbot.

Run with:  python app.py
Then open: http://localhost:5000
"""

import os
import sys
import traceback

# Ensure the Legal directory is on the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)


@app.route("/")
def index():
    """Serve the chatbot UI."""
    here = os.path.dirname(os.path.abspath(__file__))
    return send_from_directory(here, "style2.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    """
    Receive a user query and return the AI response.
    Expects JSON: { "query": "..." }
    Returns JSON: { "response": "...", "disclaimer": true/false }
    """
    data = request.get_json(force=True)
    user_query = (data.get("query") or "").strip()

    if not user_query:
        return jsonify({"error": "Empty query"}), 400

    try:
        # Import here so the heavy CrewAI imports only happen on first request
        from crew import run_query

        print(f"\n📩 Web query: {user_query}")
        answer = run_query(user_query)
        print(f"✅ Response generated ({len(answer)} chars)")

        return jsonify({
            "response": answer,
            "disclaimer": True,
        })

    except Exception as e:
        traceback.print_exc()
        return jsonify({
            "error": f"An error occurred while processing your query: {str(e)}"
        }), 500


if __name__ == "__main__":
    print("=" * 52)
    print("  LEX — Legal AI  |  Web Interface")
    print("  Open http://localhost:5000 in your browser")
    print("=" * 52)
    app.run(host="0.0.0.0", port=5000, debug=False)
