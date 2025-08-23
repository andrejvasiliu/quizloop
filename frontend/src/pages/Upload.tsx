import React, { useState } from "react";
import axios from "axios";
import { API_UPLOAD_URL } from "../config";
import type { BackendResponse } from "../types/types";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardHeader,
  CardTitle,
  CardContent,
  CardFooter,
} from "@/components/ui/card";
import { Alert, AlertDescription } from "@/components/ui/alert";

function Upload() {
  const [file, setFile] = useState<File | null>(null);
  const [status, setStatus] = useState<string | null>(null);
  const [uploaded, setUploaded] = useState(false);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
      setUploaded(false);
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
        setUploaded(true);
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
      <Card>
        <CardHeader>
          <CardTitle>Upload a Quiz</CardTitle>
        </CardHeader>
        <CardContent>
          <div>
            <Label htmlFor="quiz_file">
              Select a JSON quiz file to upload.
            </Label>
            <Input
              id="quiz_file"
              type="file"
              accept=".json"
              onChange={handleFileChange}
            />
          </div>
          {status && (
            <Alert>
              <AlertDescription>{status}</AlertDescription>
            </Alert>
          )}
        </CardContent>
        <CardFooter>
          <Button onClick={handleUpload} disabled={!file || uploaded}>
            Upload
          </Button>
        </CardFooter>
      </Card>
    </div>
  );
}

export default Upload;
