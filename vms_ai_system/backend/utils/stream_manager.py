import threading
import cv2
import time
import os
import json
from datetime import datetime
from ai.opencv_detector import detect_objects  # OpenCV detection
from ai.gemini_utils import summarize_detections  # Gemini summary

MAX_FRAMES = 30  # Total frames to process
SAVE_EVERY_N = 15  # Only save every 15th frame

class StreamThread(threading.Thread):
    def __init__(self, stream_id, stream_url):
        super().__init__()
        self.stream_id = stream_id
        self.stream_url = stream_url
        self.running = True

    def run(self):
        print(f"[INFO] Starting thread for Stream {self.stream_id} - URL: {self.stream_url}")
        cap = cv2.VideoCapture(self.stream_url)
        if not cap.isOpened():
            print(f"[ERROR] Failed to open stream {self.stream_url}")
            return

        print(f"[INFO] Stream {self.stream_id} opened successfully.")
        frame_count = 0
        all_detections = []

        while self.running:
            ret, frame = cap.read()
            if not ret:
                print(f"[WARN] Stream {self.stream_id} ended or failed.")
                break

            frame_count += 1
            print(f"[FRAME] Stream {self.stream_id} - Frame {frame_count} captured")

            if frame_count > MAX_FRAMES:
                print(f"[INFO] Reached max frame limit ({MAX_FRAMES}). Ending stream {self.stream_id}.")
                break

            # Step 1: Run detection
            detection_result, annotated_frame = detect_objects(frame)
            print(f"[DETECT] Stream {self.stream_id} - Detected {len(detection_result)} objects")

            all_detections.extend(detection_result)

            # Step 2: Save every 15th frame
            if frame_count % SAVE_EVERY_N == 0:
                frame_path = f"data/frames/stream_{self.stream_id}_frame_{frame_count}.jpg"
                os.makedirs(os.path.dirname(frame_path), exist_ok=True)
                cv2.imwrite(frame_path, annotated_frame)
                print(f"[SAVE] Frame image saved: {frame_path}")

            time.sleep(0.1)  # ~10 FPS control

        cap.release()
        print(f"[INFO] Stream {self.stream_id} stopped.")

        # Step 3: Generate ONE Gemini summary after all frames
        print(f"[GEMINI] Generating final summary for stream {self.stream_id}...")
        summary = summarize_detections(all_detections, self.stream_id)

        # Step 4: Save final summary to JSON
        output_data = {
            "stream_id": self.stream_id,
            "timestamp": datetime.now().isoformat(),
            "frame_count": frame_count,
            "total_detections": len(all_detections),
            "summary": summary
        }

        output_path = f"data/outputs/stream_{self.stream_id}.json"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        try:
            with open(output_path, "w") as f:
                json.dump(output_data, f, indent=2)
            print(f"[SAVE] Final summary JSON saved: {output_path}")
        except Exception as e:
            print(f"[ERROR] Failed to write summary JSON: {e}")


    def stop(self):
        self.running = False


class StreamManager:
    def __init__(self):
        self.streams = {}  # stream_id: thread object

    def start_stream(self, stream_url):
        stream_id = len(self.streams) + 1
        stream_thread = StreamThread(stream_id, stream_url)
        self.streams[stream_id] = stream_thread
        stream_thread.start()
        print(f"[INFO] Started stream {stream_id} with URL: {stream_url}")
        return stream_id

    def get_status(self):
        status = {}
        for stream_id, thread in self.streams.items():
            status[stream_id] = {
                "url": thread.stream_url,
                "running": thread.is_alive()
            }
        return status

    def stop_stream(self, stream_id):
        thread = self.streams.get(stream_id)
        if thread:
            thread.stop()
            return True
        return False
