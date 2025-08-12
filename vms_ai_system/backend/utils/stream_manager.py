import cv2
import os
import threading
import json
from ai.opencv_detector import detect_objects
# import your Gemini API call if needed:
# from your_gemini_module import call_gemini_api

class StreamManager:
    def __init__(self):
        self.streams = {}
        os.makedirs("summaries", exist_ok=True)
        print("[StreamManager] Initialized. 'summaries' folder ready.")

    def add_stream(self, url):
        stream_id = len(self.streams) + 1
        self.streams[stream_id] = {"url": url, "running": True}
        print(f"[StreamManager] Adding stream #{stream_id} with URL: {url}")
        thread = threading.Thread(target=self.process_stream, args=(stream_id, url))
        thread.start()
        return stream_id

    def get_status(self):
        print("[StreamManager] Current stream status requested.")
        return self.streams

    def process_stream(self, stream_id, url):
        print(f"[StreamManager] Starting processing for Stream #{stream_id} ({url})")
        cap = cv2.VideoCapture(url)
        if not cap.isOpened():
            print(f"[StreamManager] ❌ Failed to open stream #{stream_id}: {url}")
            self.streams[stream_id]["running"] = False
            # Always write an error summary
            summary_file_path = os.path.join("summaries", f"{stream_id}.json")
            with open(summary_file_path, "w", encoding="utf-8") as f:
                json.dump({"summary": "Failed to open video stream."}, f, ensure_ascii=False, indent=2)
            print(f"[StreamManager] Summary saved to {summary_file_path}")
            return

        detections_log = []
        frame_count = 0
        max_frames = 30  # or whatever you want
        print(f"[StreamManager] Processing up to {max_frames} frames for Stream #{stream_id}")
        error_message = None

        try:
            while frame_count < max_frames:
                ret, frame = cap.read()
                if not ret:
                    print(f"[StreamManager] No more frames to read for Stream #{stream_id}.")
                    break

                try:
                    detections, _ = detect_objects(frame)
                except Exception as e:
                    print(f"[StreamManager] Detection error on frame {frame_count+1}: {e}")
                    frame_count += 1
                    continue  # Skip this frame and keep processing

                print(f"[StreamManager] Frame {frame_count+1}: Detected {len(detections)} objects.")
                if detections:
                    print(f"[StreamManager] Frame {frame_count+1} Detections: {detections}")
                    detections_log.extend(detections)

                frame_count += 1

        except Exception as main_ex:
            error_message = f"Exception for stream {stream_id}: {str(main_ex)}"
            print(f"[StreamManager] ❌ {error_message}")

        finally:
            cap.release()
            self.streams[stream_id]["running"] = False

            if error_message:
                summary_text = f"❌ Error: {error_message}"
            elif not detections_log:
                summary_text = "No faces or relevant objects were detected in the stream."
                print(f"[StreamManager] No detections found for Stream #{stream_id}.")
            else:
                summary_text = f"A total of {len(detections_log)} faces were detected."
                print(f"[StreamManager] Summary generated for Stream #{stream_id}.")

            # If you want to use Gemini API to summarize, safely add here:
            # if not error_message and detections_log:
            #     try:
            #         summary_text = call_gemini_api(detections_log)
            #     except Exception as e:
            #         summary_text = f"❌ Gemini summary error: {str(e)}"

            summary_file_path = os.path.join("summaries", f"{stream_id}.json")
            with open(summary_file_path, "w", encoding="utf-8") as f:
                json.dump({"summary": summary_text}, f, ensure_ascii=False, indent=2)

            print(f"[StreamManager] Summary saved to {summary_file_path}")
