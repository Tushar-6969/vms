# 🎥 AI VMS (Video Monitoring System)

An AI-powered video monitoring system that performs real-time object detection using OpenCV and generates intelligent summaries using the Gemini API. Ideal for crowd analysis, anomaly detection, and AI-enabled surveillance.

---

## 📂 Folder Structure

```
vms-ai-system/
├── backend/
│   ├── app.py                      # Main Flask app
│   ├── routes/
│   │   └── stream_routes.py        # API endpoints (start/stop streams)
│   ├── ai/
│   │   ├── opencv_detector.py      # OpenCV object detection logic
│   │   └── gemini_utils.py         # Gemini API wrapper
│   ├── utils/
│   │   └── stream_manager.py       # Threaded stream handler per video
│   ├── data/
│   │   ├── outputs/                # Final summaries (.json)
│   │   └── frames/                 # Captured frames for analysis
│   ├── haarcascades/              # Haar cascade XMLs for face detection
│   │   └── haarcascade_frontalface_default.xml
│   └── requirements.txt           # Backend dependencies
│
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   │   ├── StreamCard.jsx      # Display each stream with AI summary
│   │   │   └── Dashboard.jsx       # (Optional) dashboard view
│   │   ├── App.jsx                 # Main React component
│   │   └── main.jsx                # React root
│   ├── tailwind.config.js         # Tailwind CSS config
│   ├── package.json               # Frontend dependencies
│   └── vite.config.js             # Vite build config
│
├── README.md
└── setup_instructions.md          # Quick setup guide
```

---

## 🧠 Features

* 📡 **Live video or file stream support** (e.g., webcam `0`, `test.mp4`)
* 🤖 **Real-time object detection** using Haar cascade (OpenCV)
* 🔍 **Face detection & analysis** with bounding boxes
* ✨ **Gemini API summary** of detected objects after stream ends
* 📁 **Stores results** (frames, JSON summaries) per stream
* 🔄 **Stream dashboard** with auto-refresh every 10 seconds

---

## 📝 Output Sample

> ✅ Stream ID 1 shows a significant number of face detections. A total of 38 faces were detected. The detections appear clustered around four general locations: (1593, 408), (1371, 276), (1008, 326) and (953, 468), with multiple detections within each cluster. The large number of detections, especially the repeated detections around similar coordinates, could indicate a crowd of people, or potentially an issue with the detection algorithm repeatedly identifying the same faces.

---

## 📌 Matches Assignment Requirements

| Requirement                        | Status                                    |
| ---------------------------------- | ----------------------------------------- |
| Upload video or use webcam         | ✅ Done via URL input (`test.mp4`, `0`)    |
| Detect objects using OpenCV        | ✅ Haar cascade face detection             |
| Intelligent AI summary generation  | ✅ Gemini API used after frame analysis    |
| Store summaries and display        | ✅ Saved as JSON, shown on UI              |
| Modern frontend (React + Tailwind) | ✅ Fully implemented                       |
| API integration (Flask backend)    | ✅ REST API for stream control + summaries |

---

## 🚀 How to Run

### 1. Backend (Flask)

```bash
cd backend
pip install -r requirements.txt
python app.py
```

### 2. Frontend (React + Vite)

```bash
cd frontend
npm install
npm run dev
```

### 3. Access Dashboard

Open [http://localhost:5173](http://localhost:5173) in your browser.

---

## 🙋 FAQ

* **Can I upload a video file?**

  * No. As per assignment, only stream URL input (`0` or `.mp4`) is supported.

* **What if Gemini summary is delayed?**

  * "⏳ Processing..." or "❌ Network Error" is shown until summary is ready.

* **Where are summaries stored?**

  * In `backend/data/outputs/stream_<id>.json`

---

## 👨‍💻 Author

Tushar Rathor — B.Tech CSE AIML — 7th Sem

GitHub: [Tushar-6969](https://github.com/Tushar-6969)
LinkedIn: [tushar-rathor-277427259](https://linkedin.com/in/tushar-rathor-277427259)

---

Ready to showcase in demo ✅
