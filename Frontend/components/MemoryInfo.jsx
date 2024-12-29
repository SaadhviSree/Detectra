import React, { useEffect, useState } from "react";

const MemoryInfo = () => {
  const [memoryInfo, setMemoryInfo] = useState(null);

  useEffect(() => {
    fetch("http://localhost:3000/memory_info") // Replace with your Flask endpoint
      .then((response) => response.json())
      .then((data) => setMemoryInfo(data));
  }, []);

  if (!memoryInfo) return <div>Loading...</div>;

  return (
    <div className="p-4 bg-gray-100 rounded-lg shadow-md">
      <h2 className="text-xl font-bold">Memory Information</h2>
      <ul>
        {Object.entries(memoryInfo).map(([key, value]) => (
          <li key={key}>
            <strong>{key}:</strong> {value}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default MemoryInfo;
