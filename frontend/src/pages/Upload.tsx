import React, { useState } from "react";
import axios from "axios";
import { API_UPLOAD_URL } from "../config";
import type { BackendResponse } from "../types/types";

function Upload() {
  const [file, setFile] = useState<File | null>(null);
  const [status, setStatus] = useState<string | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
      setStatus(null);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setStatus("⚠️ Please select a JSON file first.");
      return;
    }

    const formData = new FormData();
    formData.append("quiz_json", file);

    try {
      const response = await axios.post<BackendResponse>(
        `${API_UPLOAD_URL}`,
        formData
      );

      if (response.data.success === true) {
        setStatus("✅ File uploaded successfully!");
      } else {
        setStatus(
          `❌ Upload failed: ${response.data.error || "Unknown error"}`
        );
      }
    } catch (error: any) {
      setStatus(`❌ An error occurred: ${error}`);
    }
  };

  return (
    <div>
      <h1>Upload Quiz</h1>
      <p>Select a JSON quiz file to upload.</p>

      <input type="file" accept=".json" onChange={handleFileChange} />

      <div>
        <button onClick={handleUpload} disabled={!file}>
          Upload
        </button>
      </div>

      {status && <p>{status}</p>}
    </div>
  );
}

export default Upload;
