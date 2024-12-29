import React, { useState } from "react";

function NetworkAnomaly() {
  const [data, setData] = useState([]); // State to store fetched data
  const [isFetching, setIsFetching] = useState(false); // Loading state

  const fetchData = async () => {
    try {
      setIsFetching(true);
      const response = await fetch("http://localhost:3000/api/data");
      if (!response.ok) {
        throw new Error("Failed to fetch data");
      }
      const result = await response.json();
      setData(result); // Update state with fetched data
    } catch (error) {
      console.error("Error fetching data:", error);
    } finally {
      setIsFetching(false);
    }
  };

  const tiles = [
    {
      title: "Network Analysis",
      description: "Analyze network traffic and detect anomalies.",
    },
    {
      title: "Network Reports",
      description: "View reports on network traffic and anomalies.",
    },
  ];

  const columns = [
    "duration", "protocol_type", "service", "flag", "src_bytes", "dst_bytes", "land",
    "wrong_fragment", "urgent", "hot", "num_failed_logins", "logged_in",
    "num_compromised", "root_shell", "su_attempted", "num_root", "num_file_creations",
    "num_shells", "num_access_files", "num_outbound_cmds", "is_host_login",
    "is_guest_login", "count", "srv_count", "serror_rate", "srv_serror_rate",
    "rerror_rate", "srv_rerror_rate", "same_srv_rate", "diff_srv_rate", "srv_diff_host_rate",
    "dst_host_count", "dst_host_srv_count", "dst_host_same_srv_rate", "dst_host_diff_srv_rate",
    "dst_host_same_src_port_rate", "dst_host_srv_diff_host_rate", "dst_host_serror_rate",
    "dst_host_srv_serror_rate", "dst_host_rerror_rate", "dst_host_srv_rerror_rate" ];

  return (
    <div className="bg-gray-200 h-screen flex flex-col items-center justify-start">
      <h1 className="text-3xl font-bold text-center mt-8">
        Network Anomaly Section
      </h1>

      {/* Tile Section */}
      <div className="flex justify-center gap-20 mt-6">
        {tiles.map((tile, index) => (
          <div
            key={index}
            className="w-1/4 bg-white shadow-lg p-6 rounded-lg text-center hover:shadow-2xl transition-shadow duration-200"
          >
            <h2 className="text-xl font-bold mb-4">{tile.title}</h2>
            <p className="text-gray-600">{tile.description}</p>
            {index === 0 && (
              <button
                onClick={fetchData}
                className="mt-4 bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-700 transition-colors duration-200"
              >
                Execute
              </button>
            )}
          </div>
        ))}
      </div>

      {/* Display Data */}
      <div className="mt-8 w-3/4 bg-white shadow-md rounded-lg p-4">
        <h2 className="text-2xl font-bold mb-4">Analysis Results</h2>
        {isFetching ? (
          <p>Loading...</p>
        ) : (
          <table className="w-full border-collapse border border-gray-300">
            <thead>
              <tr>
                {columns.map((column, index) => (
                  <th key={index} className="border border-gray-300 p-2">{column}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {data.map((row, index) => (
                <tr key={index}>
                  {columns.map((column, colIndex) => (
                    <td key={colIndex} className="border border-gray-300 p-2">{row[column]}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

export default NetworkAnomaly;
