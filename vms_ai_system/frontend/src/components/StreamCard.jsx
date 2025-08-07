import { useEffect, useState } from "react";
import axios from "axios";

export default function StreamCard({ streamId, url, running }) {
  const [summary, setSummary] = useState("⏳ Loading...");
  const BACKEND_URL = "http://localhost:5000";

  useEffect(() => {
    const fetchSummary = async () => {
      try {
        const res = await axios.get(`${BACKEND_URL}/api/streams/summary/${streamId}`);
        const text = res.data.summary?.toLowerCase();

        if (!text || text.includes("no summary") || text.includes("no valid summary")) {
          setSummary("⏳ Summary is being generated... Please wait.");
        } else if (text.includes("error")) {
          setSummary("❌ Backend error while fetching summary.");
        } else {
          setSummary(`✅ ${res.data.summary}`);
        }
      } catch (err) {
        setSummary("❌ Network error while connecting to backend.");
        console.error("[StreamCard] Summary fetch failed:", err.message);
      }
    };

    fetchSummary();
    const interval = setInterval(fetchSummary, 10000); // Refresh every 10s
    return () => clearInterval(interval);
  }, [streamId]);

  return (
    <div className="bg-white shadow-md p-4 rounded border border-gray-200">
      <h2 className="text-xl font-semibold mb-2 text-blue-700">🎥 Stream #{streamId}</h2>
      <p><strong>📡 URL:</strong> {url}</p>
      <p><strong>⚙️ Status:</strong> {running ? "🟢 Running" : "🔴 Stopped"}</p>

      <div className="mt-3 bg-gray-50 p-3 rounded border border-dashed">
        <p className="text-sm font-semibold mb-1 text-gray-700">🧠 AI Summary:</p>
        <p className="text-sm text-gray-800 whitespace-pre-wrap">{summary}</p>
      </div>
    </div>
  );
}
