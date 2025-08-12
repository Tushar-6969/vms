from flask import Blueprint, request, jsonify
import os
import json
from utils.stream_manager import StreamManager

stream_bp = Blueprint("stream_bp", __name__)
manager = StreamManager()

@stream_bp.route("/add", methods=["POST"])
def add_stream():
    data = request.get_json()
    url = data.get("url")
    if not url:
        return jsonify({"error": "URL is required"}), 400

    stream_id = manager.add_stream(url)
    return jsonify({"message": f"Stream {stream_id} added successfully", "id": stream_id})

@stream_bp.route("/status", methods=["GET"])
def status():
    return jsonify(manager.get_status())

@stream_bp.route("/summary/<int:stream_id>", methods=["GET"])
def get_summary(stream_id):
    summary_file = os.path.join("summaries", f"{stream_id}.json")

    if not os.path.exists(summary_file):
        # Return a safe placeholder instead of failing
        return jsonify({"summary": "⏳ AI summary still processing..."}), 200

    try:
        with open(summary_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        return jsonify({"summary": data.get("summary", "⏳ AI summary still processing...")})
    except Exception as e:
        return jsonify({"summary": f"❌ Error reading summary: {str(e)}"}), 500
