export default function ResultsPage() {

  const transcript =
    "Your bank account needs OTP verification immediately";

  const flaggedWords = ["OTP", "verification"];

  const words = transcript.split(" ");

  return (

    <div className="min-h-screen flex items-center justify-center bg-gray-100">

      <div className="bg-white p-8 rounded-xl shadow-lg max-w-xl">

        <h1 className="text-2xl font-bold mb-4">
          Analysis Result
        </h1>

        <div className="mb-4">

          Risk Level:
          <span className="ml-2 px-3 py-1 bg-red-500 text-white rounded">
            High Risk
          </span>

        </div>

        <p className="leading-8">

          {words.map((word, index) =>

            flaggedWords.includes(word) ? (
              <mark key={index} className="bg-red-300 px-1">
                {word}
              </mark>
            ) : (
              " " + word
            )
          )}

        </p>

      </div>

    </div>

  );
}