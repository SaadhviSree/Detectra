import React, { useEffect, useState } from "react";

const Processes = () => {
  const [processes, setProcesses] = useState([]);

  useEffect(() => {
    fetch("http://localhost:3000/processes") // Replace with your Flask endpoint
      .then((response) => response.json())
      .then((data) => setProcesses(data));
  }, []);

  if (!processes.length) return <div>Loading...</div>;

  return (
    <div className="p-4 bg-gray-100 rounded-lg shadow-md">
      <h2 className="text-xl font-bold">Running Processes</h2>
      <ul className="overflow-y-auto h-64">
        {processes.map((process, index) => (
          <li key={index}>
            {process.name} (PID: {process.pid}) - {process.username}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Processes;
