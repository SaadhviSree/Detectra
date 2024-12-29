import React from 'react';

// Memory Chart Component
const MemoryPieChart = () => {
  return (
    <div className="rounded-lg border bg-white shadow-sm p-4">
      <h2 className="text-xl font-bold mb-4">Memory Usage</h2>
      <div className="flex item-center">
        <img 
          src="http://localhost:5000/memory-chart" 
          alt="Memory Usage Chart" 
          className="w-full max-w-md" 
        />
      </div>
    </div>
  );
};

// Network Chart Component
const NetworkConnectionsGraph = () => {
  return (
    <div className="rounded-lg border bg-white shadow-sm p-4">
      <h2 className="text-xl font-bold mb-4">Network Connections</h2>
      <div className="flex justify-center">
        <img 
          src="http://localhost:5000/network-chart" 
          alt="Network Connections Chart" 
          className="w-full max-w-md" 
        />
      </div>
    </div>
  );
};

// System Information Table (Unchanged)
const SystemInfoTable = ({ data }) => {
  if (!data) return null;

  return (
    <div className="rounded-lg border bg-white shadow-sm p-4">
      <h2 className="text-xl font-bold mb-4">System Information</h2>
      <div className="overflow-x-auto">
        <table className="w-full border-collapse border border-gray-300">
          <tbody>
            {Object.entries(data).map(([key, value]) => (
              <tr key={key} className="border-b border-gray-300">
                <td className="py-2 px-4 font-medium capitalize">{key.replace(/_/g, ' ')}</td>
                <td className="py-2 px-4">{value}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

// Suspicious Processes Table (Unchanged)
const SuspiciousProcessTable = ({ processes }) => {
  if (!processes?.length) return null;

  return (
    <div className="rounded-lg border bg-white shadow-sm p-4">
      <h2 className="text-xl font-bold mb-4">Suspicious Processes</h2>
      <div className="overflow-x-auto">
        <table className="w-full border-collapse border border-gray-300">
          <thead>
            <tr className="bg-gray-50">
              <th className="py-2 px-4 text-left font-medium border border-gray-300">Process Name</th>
              <th className="py-2 px-4 text-left font-medium border border-gray-300">PID</th>
              <th className="py-2 px-4 text-left font-medium border border-gray-300">Username</th>
              <th className="py-2 px-4 text-left font-medium border border-gray-300">Create Time</th>
            </tr>
          </thead>
          <tbody>
            {processes.map((proc, idx) => (
              <tr key={idx} className="border-t hover:bg-gray-50">
                <td className="py-2 px-4 border border-gray-300">{proc.name}</td>
                <td className="py-2 px-4 border border-gray-300">{proc.pid}</td>
                <td className="py-2 px-4 border border-gray-300">{proc.username}</td>
                <td className="py-2 px-4 border border-gray-300">{proc.create_time}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

// Dashboard Component (Unchanged)
const Dashboard = ({ systemInfo, networkConnections, memoryInfo, susProcess }) => {
  return (
    <div className="container mx-auto p-4">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <SystemInfoTable data={systemInfo} />
        <SuspiciousProcessTable processes={susProcess} />
        <MemoryPieChart />
        <NetworkConnectionsGraph />
      </div>
    </div>
  );
};

export default Dashboard;