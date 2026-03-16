export default function RiskMeter({ level }) {

  let color = "bg-green-500";
  let width = "30%";

  if (level === "Suspicious") {
    color = "bg-yellow-500";
    width = "60%";
  }

  if (level === "High Risk") {
    color = "bg-red-500";
    width = "90%";
  }

  return (

    <div className="mt-4">

      <p className="mb-2 font-medium">
        Risk Level: {level}
      </p>

      <div className="w-full bg-gray-200 rounded h-4">

        <div
          className={`${color} h-4 rounded`}
          style={{ width }}
        ></div>

      </div>

    </div>

  );
}