import { useState } from "react";
import axios from 'axios'

function App() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) return alert("Please upload a PDF");

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);

    axios.post("http://localhost:8000/upload", formData)
    .then(async response => {
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = "output.mp3";
    a.click();
    })
    .catch(error => {
      console.error('Error:', error)
    })

    setLoading(false);
  };

  return (
    <div style={{ padding: 40 }}>
      <h1>PDF → MP3 Converter</h1>

      <input
        type="file"
        accept="application/pdf"
        onChange={(e) => setFile(e.target.files[0])}
      />

      <br /><br />

      <button onClick={handleUpload} disabled={loading}>
        {loading ? "Converting..." : "Convert to MP3"}
      </button>
    </div>
  );
}

export default App;
