import os
import json
from flask import Blueprint, request, jsonify
from utils.stream_manager import StreamManager

stream_bp = Blueprint("stream_routes", __name__)

# Singleton stream manager
stream_manager = StreamManager()

@stream_bp.route("/add", methods=["POST"])
def add_stream():
    data = request.json
    stream_url = data.get("url")

    if not stream_url:
        return jsonify({"error": "Stream URL is required"}), 400

    stream_id = stream_manager.start_stream(stream_url)
    print(f"[ADD] Added stream {stream_id} with URL: {stream_url}")
    return jsonify({"message": "Stream added", "stream_id": stream_id}), 200


@stream_bp.route("/status", methods=["GET"])
def get_status():
    status = stream_manager.get_status()
    return jsonify(status), 200


@stream_bp.route("/stop/<int:stream_id>", methods=["POST"])
def stop_stream(stream_id):
    success = stream_manager.stop_stream(stream_id)
    if success:
        print(f"[STOP] Stopped stream {stream_id}")
        return jsonify({"message": f"Stream {stream_id} stopped"}), 200
    else:
        return jsonify({"error": f"Stream {stream_id} not found or already stopped"}), 404


@stream_bp.route("/summary/<int:stream_id>", methods=["GET"])
def get_latest_summary(stream_id):
    output_file = f"data/outputs/stream_{stream_id}.json"

    if not os.path.exists(output_file):
        print(f"[SUMMARY] Output file not found: {output_file}")
        return jsonify({"summary": "⏳ AI summary still processing..."}), 200

    try:
        with open(output_file, "r") as f:
            content = f.read().strip()
            if not content:
                print(f"[SUMMARY] Output file is empty for stream {stream_id}")
                return jsonify({"summary": "⏳ AI summary still processing..."}), 200

            data = json.loads(content)
            summary = data.get("summary", "")

            if summary and "skipped" not in summary.lower():
                print(f"[SUMMARY] Returning final summary for stream {stream_id}")
                return jsonify({"summary": summary}), 200
            else:
                print(f"[SUMMARY] No valid Gemini summary found for stream {stream_id}")
                return jsonify({"summary": "⏳ AI summary still processing..."}), 200

    except json.JSONDecodeError as jde:
        print(f"[ERROR] JSON decode failed for stream {stream_id}: {jde}")
        return jsonify({"summary": "⏳ AI summary still processing..."}), 200

    except Exception as e:
        print(f"[ERROR] Failed to read summary for stream {stream_id}: {str(e)}")
        return jsonify({"summary": "⏳ AI summary still processing..."}), 200
