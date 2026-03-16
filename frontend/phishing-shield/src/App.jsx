import { useState } from "react";
import UploadPage from "./pages/UploadPage";
import LoaderPage from "./pages/Loaderpage";
import ResultsPage from "./pages/ResultsPage";

function App() {
  const [page, setPage] = useState("upload");
  const [analysisData, setAnalysisData] = useState(null); // Stores the AI Result

  const startAnalysis = async (file, text, language) => {
    setPage("loading");
    
    try {
      let textToProcess = text;

      // STEP 1: If it's an audio file, transcribe it first
      if (file) {
        const formData = new FormData();
        formData.append("audio", file);

        const transcribeRes = await fetch("http://127.0.0.1:5000/api/transcribe", {
          method: "POST",
          body: formData,
        });
        const transcribeData = await transcribeRes.json();
        textToProcess = transcribeData.transcript;
      }

      // STEP 2: Send text to your AI Brain
      const analyzeRes = await fetch("http://127.0.0.1:5000/api/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: textToProcess, lang: language }),
      });

      const result = await analyzeRes.json();
      
      // STEP 3: Save the result and show the Results Page
      setAnalysisData(result);
      setPage("result");

    } catch (error) {
      console.error("Connection to AI Backend failed:", error);
      alert("Error: Ensure your Flask server is running on port 5000!");
      setPage("upload"); // Return to start on error
    }
  };

  // Rendering logic
  if (page === "upload") {
    return <UploadPage startAnalysis={startAnalysis} />;
  }

  if (page === "loading") {
    return <LoaderPage />;
  }

  if (page === "result") {
    // Pass the AI data to the Results Page
    return <ResultsPage data={analysisData} onBack={() => setPage("upload")} />;
  }
}

export default App;