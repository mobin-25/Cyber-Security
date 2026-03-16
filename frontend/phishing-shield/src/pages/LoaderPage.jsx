import { useEffect, useState } from "react";

const steps = [
  "Uploading audio...",
  "Converting speech to text...",
  "Analyzing scam patterns...",
  "Generating report..."
];

export default function LoaderPage({ finish }) {

  const [step, setStep] = useState(0);

  useEffect(() => {

    const interval = setInterval(() => {

      setStep((prev) => prev + 1);

    }, 1200);

    if (step === steps.length) {

      clearInterval(interval);

      setTimeout(() => {

        finish();

      }, 500);

    }

    return () => clearInterval(interval);

  }, [step]);

  return (

    <div className="h-screen flex flex-col items-center justify-center">

      <h2 className="text-xl font-semibold mb-4">
        {steps[step] || "Done"}
      </h2>

      <div className="animate-spin text-4xl">⏳</div>

    </div>

  );

}