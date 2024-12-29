import React, { useEffect, useState } from "react";

const NetworkConnections = () => {
  const [connections, setConnections] = useState([]);

  useEffect(() => {
    fetch("http://localhost:3000/network_connections") // Replace with your Flask endpoint
      .then((response) => response.json())
      .then((data) => setConnections(data));
  }, []);

  if (!connections.length) return <div>Loading...</div>;

  return (
    <div className="p-4 bg-gray-100 rounded-lg shadow-md">
      <h2 className="text-xl font-bold">Network Connections</h2>
      <table className="table-auto w-full">
        <thead>
          <tr>
            <th>Local Address</th>
            <th>Remote Address</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {connections.map((conn, index) => (
            <tr key={index}>
              <td>{conn.local_address}</td>
              <td>{conn.remote_address}</td>
              <td>{conn.status}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default NetworkConnections;
