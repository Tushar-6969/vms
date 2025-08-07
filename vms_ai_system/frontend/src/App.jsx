import { useEffect, useState } from "react";
import axios from "axios";
import StreamCard from "./components/StreamCard";

export default function App() {
  const [streams, setStreams] = useState({});
  const [newUrl, setNewUrl] = useState("");
  const [loading, setLoading] = useState(false);

  const BACKEND_URL = "http://localhost:5000/api/streams"; // Update if deployed

  useEffect(() => {
    fetchStatus();
    const interval = setInterval(fetchStatus, 10000);
    return () => clearInterval(interval);
  }, []);

  const fetchStatus = async () => {
    try {
      const res = await axios.get(`${BACKEND_URL}/status`);
      setStreams(res.data);
    } catch (err) {
      console.error("❌ Error fetching stream status", err);
    }
  };

  const handleAddStream = async () => {
    if (!newUrl.trim()) return;
    try {
      setLoading(true);
      const res = await axios.post(`${BACKEND_URL}/add`, { url: newUrl.trim() });
      console.log("✅ Stream added:", res.data.message);
      setNewUrl("");
      await fetchStatus();
    } catch (err) {
      console.error("❌ Failed to add stream:", err);
    } finally {
      setLoading(false);
    }
  };

  return (<div className="min-h-screen bg-gray-100 p-6" style={{ marginLeft: "500px" }}>

      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-4 text-center">🎥 AI VMS Dashboard</h1>

        <div className="flex gap-2 mb-6 justify-center">
          <input
            type="text"
            value={newUrl}
            onChange={(e) => setNewUrl(e.target.value)}
            placeholder="Enter stream URL (e.g. test.mp4 or 0)"
            className="border border-gray-400 px-4 py-2 rounded w-96"
          />
          <button
            onClick={handleAddStream}
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50"
            disabled={loading}
          >
            {loading ? "Adding..." : "Add Stream"}
          </button>
        </div>

        {Object.keys(streams).length === 0 ? (
          <p className="text-center text-gray-500">No streams active yet.</p>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {Object.entries(streams).map(([id, stream]) => (
              <StreamCard
                key={id}
                streamId={id}
                url={stream.url}
                running={stream.running}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
