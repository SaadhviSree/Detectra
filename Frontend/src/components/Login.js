import React from "react";

function Login() {
  return (
    <div className="container mx-auto p-4">
      <h2 className="text-2xl font-bold mb-4">Login</h2>
      <form className="space-y-4">
        <div>
          <label className="block text-gray-700">Email</label>
          <input type="email" className="w-full border border-gray-300 p-2 rounded" placeholder="Enter your email" />
        </div>
        <div>
          <label className="block text-gray-700">Password</label>
          <input type="password" className="w-full border border-gray-300 p-2 rounded" placeholder="Enter your password" />
        </div>
        <button type="submit" className="bg-black text-blue-600 px-4 py-2 rounded hover:bg-blue-700">Login</button>
      </form>
    </div>
  );
}

export default Login;