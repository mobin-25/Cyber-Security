import { useState } from "react";

export default function UploadPage({ startAnalysis }) {

  const [file, setFile] = useState(null);
  const [text, setText] = useState("");
  const [language, setLanguage] = useState("auto");

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">

      <div className="bg-white p-8 rounded-xl shadow-lg w-full max-w-xl">

        <h1 className="text-3xl font-bold text-center mb-6">
          Phishing Shield
        </h1>

        {/* Upload audio */}
        <div className="border-2 border-dashed p-6 text-center rounded-lg">

          <input
            type="file"
            accept="audio/*"
            onChange={(e) => setFile(e.target.files[0])}
          />

          <p className="text-gray-500 mt-2">
            Upload scam call audio (.mp3 .wav .ogg)
          </p>

        </div>

        <div className="text-center my-4">OR</div>

        {/* Text input */}

        <textarea
          className="w-full border p-3 rounded-lg"
          rows="4"
          placeholder="Paste suspicious message..."
          value={text}
          onChange={(e) => setText(e.target.value)}
        />

        {/* Language select */}

        <div className="mt-4">

          <label className="font-medium">Language</label>

          <select
            className="w-full border p-2 rounded mt-1"
            value={language}
            onChange={(e) => setLanguage(e.target.value)}
          >

            <option value="auto">Auto Detect</option>
            <option value="hi">Hindi</option>
            <option value="mr">Marathi</option>
            <option value="ta">Tamil</option>

          </select>

        </div>

        {/* Analyze button */}

        <button
          onClick={() => startAnalysis(file, text, language)}
          className="w-full mt-6 bg-purple-600 text-white py-3 rounded-lg hover:bg-purple-700"
        >
          Analyze
        </button>

      </div>

    </div>
  );
}