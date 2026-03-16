export default function HighlightedText({ text }) {

  const flagged = ["OTP", "bank", "verification", "urgent"];

  const words = text.split(" ");

  return (

    <p className="leading-8">

      {words.map((word, i) =>

        flagged.includes(word) ? (
          <mark key={i} className="bg-red-300 px-1">
            {word}
          </mark>
        ) : (
          " " + word
        )
      )}

    </p>

  );
}