import React, { useEffect, useState } from "react";

const SystemInfo = () => {
  const [systemInfo, setSystemInfo] = useState(null);

  useEffect(() => {
    fetch("http://localhost:3000/system_info") // Replace with your Flask endpoint
      .then((response) => response.json())
      .then((data) => setSystemInfo(data));
  }, []);

  if (!systemInfo) return <div>Loading...</div>;

  return (
    <div className="p-4 bg-gray-100 rounded-lg shadow-md">
      <h2 className="text-xl font-bold">System Information</h2>
      <ul>
        {Object.entries(systemInfo).map(([key, value]) => (
          <li key={key}>
            <strong>{key}:</strong> {value}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default SystemInfo;
