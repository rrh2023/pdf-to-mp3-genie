import { useState } from 'react';
import { Upload, File, X, CheckCircle } from 'lucide-react';
import axios from "axios"
import './App.css' 

const App = () => {

  const [file, setFile] = useState(null);
  const [isDragging, setIsDragging] = useState(false);

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile && droppedFile.type === 'application/pdf') {
      setFile(droppedFile);
    }
  };

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile && selectedFile.type === 'application/pdf') {
      setFile(selectedFile);
    }
  };

  const handleRemove = () => {
    setFile(null);
  };

 const handleUpload = async () => {
  if (!file) return alert("Please upload a PDF");

  const formData = new FormData();
  formData.append("file", file);

  // Use environment variable with fallback for local development
  const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";
  
  try {
    const response = await axios.post(
      `http://localhost:8000/upload`,  // Changed from root to /upload endpoint
      formData,
      {
        responseType: "blob", 
      }
    );

    const url = window.URL.createObjectURL(response.data);
    const a = document.createElement("a");
    a.href = url;
    a.download = "output.mp3";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
  } catch (error) {
    if (error.response) {
      console.error('Status:', error.response.status);
      const text = await error.response.data.text();
      console.error('Error message:', text);
      alert('Upload failed: ' + text);
    } else {
      console.error('Request failed:', error.message);
      alert('Upload failed: ' + error.message);
    }
  }
};



  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl shadow-xl p-8 w-full max-w-2xl">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-800 mb-2">Upload PDF Document</h1>
          <p className="text-gray-600">Select or drag and drop your PDF file below</p>
        </div>

        <div
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          className={`border-2 border-dashed rounded-xl p-12 text-center transition-all ${
            isDragging
              ? 'border-indigo-500 bg-indigo-50'
              : 'border-gray-300 bg-gray-50 hover:border-indigo-400 hover:bg-indigo-50'
          }`}
        >
          {!file ? (
            <div className="space-y-4">
              <div className="flex justify-center">
                <Upload className="w-16 h-16 text-indigo-500" />
              </div>
              <div>
                <p className="text-lg font-medium text-gray-700 mb-2">
                  Drop your PDF here, or click to browse
                </p>
                <p className="text-sm text-gray-500">Maximum file size: 10MB</p>
              </div>
              <input
                type="file"
                accept=".pdf,application/pdf"
                onChange={handleFileChange}
                className="hidden"
                id="file-upload"
              />
              <label
                htmlFor="file-upload"
                className="inline-block px-6 py-3 bg-indigo-600 text-white rounded-lg font-medium cursor-pointer hover:bg-indigo-700 transition-colors"
              >
                Choose File
              </label>
            </div>
          ) : (
            <div className="space-y-4">
              <div className="flex justify-center">
                <CheckCircle className="w-16 h-16 text-green-500" />
              </div>
              <div className="bg-white rounded-lg p-4 border border-gray-200">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <File className="w-8 h-8 text-red-500" />
                    <div className="text-left">
                      <p className="font-medium text-gray-800">{file.name}</p>
                      <p className="text-sm text-gray-500">
                        {(file.size / 1024 / 1024).toFixed(2)} MB
                      </p>
                    </div>
                  </div>
                  <button
                    onClick={handleRemove}
                    className="p-2 hover:bg-gray-100 rounded-full transition-colors"
                  >
                    <X className="w-5 h-5 text-gray-600" />
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>

        {file && (
          <div className="mt-6 flex gap-3">
            <button
              onClick={handleUpload}
              className="flex-1 px-6 py-3 bg-indigo-600 text-white rounded-lg font-medium hover:bg-indigo-700 transition-colors"
            >
              Upload File
            </button>
            <button
              onClick={handleRemove}
              className="px-6 py-3 bg-gray-200 text-gray-700 rounded-lg font-medium hover:bg-gray-300 transition-colors"
            >
              Cancel
            </button>
          </div>
        )}
      </div>
    </div>
  );
}


export default App