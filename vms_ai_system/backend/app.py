from flask import Flask, send_from_directory
from flask_cors import CORS
from routes.stream_routes import stream_bp
import os

# Create Flask app
app = Flask(__name__)

# Enable CORS for frontend (e.g., React on port 5173)
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

# Ensure required folders exist
os.makedirs("data/outputs", exist_ok=True)
os.makedirs("data/frames", exist_ok=True)

# Register API routes (for stream handling)
app.register_blueprint(stream_bp, url_prefix="/api/streams")

@app.route("/")
def index():
    return {
        "message": "🎥 Video Management System (VMS) Backend is Running!",
        "routes": {
            "Add Stream": "/api/streams/add",
            "Stop Stream": "/api/streams/stop/<stream_id>",
            "Status": "/api/streams/status"
        }
    }

# Serve static files (outputs + frames) so React can access them
@app.route('/data/<path:filename>')
def serve_data(filename):
    return send_from_directory('data', filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
