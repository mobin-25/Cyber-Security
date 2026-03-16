import { useState } from "react";

export default function DropZone({ setFile }) {

  const [dragging, setDragging] = useState(false);

  const handleDrop = (e) => {
    e.preventDefault();
    setDragging(false);

    const file = e.dataTransfer.files[0];
    setFile(file);
  };

  return (
    <div
      className={`border-2 border-dashed p-8 text-center rounded-lg 
      ${dragging ? "border-purple-600 bg-purple-50" : "border-gray-300"}`}
      onDragOver={(e) => {
        e.preventDefault();
        setDragging(true);
      }}
      onDragLeave={() => setDragging(false)}
      onDrop={handleDrop}
    >

      <p className="text-gray-600">
        Drag & Drop audio file here
      </p>

      <p className="text-sm text-gray-400 mt-2">
        or click to upload
      </p>

      <input
        type="file"
        accept="audio/*"
        className="mt-3"
        onChange={(e) => setFile(e.target.files[0])}
      />

    </div>
  );
}