import React, { useState, useEffect } from "react";
import "./App.css";
import Dashboard from "./Dashboard";

const App = () => {
  const [systemInfo, setSystemInfo] = useState(null);
  const [networkConnections, setNetworkConnections] = useState([]);
  const [memoryInfo, setMemoryInfo] = useState(null);
  const [susProcess, setSusProcess] = useState([]);

  useEffect(() => {
    const fetchData = async (endpoint, setData) => {
      try {
        const response = await fetch(`http://localhost:5000/${endpoint}`);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log(`Data from ${endpoint}:`, data);
        setData(data);
      } catch (error) {
        console.error(`Error fetching ${endpoint}:`, error);
      }
    };

    fetchData("system_info.json", setSystemInfo);
    fetchData("network_connections.json", setNetworkConnections);
    fetchData("memory_info.json", setMemoryInfo);
    fetchData("suspicious_processes.json", setSusProcess);
  }, []);

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-blue-600 text-white p-4">
        <h1 className="text-2xl font-bold">Forensic Data Visualization</h1>
      </header>
      <main className="p-4">
        <Dashboard 
          systemInfo={systemInfo}
          networkConnections={networkConnections}
          memoryInfo={memoryInfo}
          susProcess={susProcess}
        />
      </main>
    </div>
  );
};

export default App;