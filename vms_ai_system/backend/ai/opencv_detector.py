import cv2
import os

# Load the Haar Cascade face detection model
CASCADE_PATH = os.path.join("haarcascades", "haarcascade_frontalface_default.xml")
face_cascade = cv2.CascadeClassifier(CASCADE_PATH)

def detect_objects(frame):
    """
    Detect faces in the given frame using Haar Cascade.

    Returns:
        detections: list of dictionaries with bounding box coordinates.
        annotated_frame: the same frame with rectangles drawn on detected faces.
    """
    detections = []

    # Convert frame to grayscale for detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    # Draw bounding boxes and prepare output
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        detections.append({
            "type": "face",
            "x": int(x),
            "y": int(y),
            "width": int(w),
            "height": int(h)
        })

    return detections, frame
