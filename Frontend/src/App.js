import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import { FiSearch } from 'react-icons/fi';
import About from "./components/About";
import Login from "./components/Login"; // Ensure correct casing for filenames (case-sensitive in most OS)
import Contact from "./components/Contact"; // If Contact.js exists as a component
//import NetworkAnomaly from "./components/NetworkAnomaly"; // Import NetworkAnomaly component

// Components
function Navbar() {
  return (
    <nav className="bg-black p-4">
      <div className="container mx-auto flex justify-between items-center">
        <div className="flex items-center">
          <img src="/icon2.png" alt="Detectra Icon" className="w-10 h-10 mr-2 ml-[5px]" />
          <h1 className="text-blue-600 text-2xl font-bold">Detectra</h1>
        </div>
        <ul className="flex space-x-8 mr-20">
          <li>
            <Link to="/" className="text-blue-600 hover:text-gray-300">Home</Link>
          </li>
          <li>
            <Link to="/about" className="text-blue-600 hover:text-gray-300">About</Link>
          </li>
          <li>
            <Link to="/login" className="text-blue-600 hover:text-gray-300">Login</Link>
          </li>
          <li>
            <Link to="/contact" className="text-blue-600 hover:text-gray-300">Contact</Link>
          </li>
          <li>
            <FiSearch className="text-white hover:text-gray-300 cursor-pointer" />
          </li>
        </ul>
      </div>
    </nav>
  );
}


function Hero() {
  return (
    <div
      className="relative bg-cover bg-center h-screen flex items-center justify-start px-10"
      style={{
        backgroundImage: "url('/img.jpg')",
      }}
    >
      <div className="absolute inset-0 bg-gradient-to-b from-black via-transparent to-black opacity-500"></div>
      <div className="relative text-left text-white max-w-xl ml-24">
        <h1 className="text-5xl md:text-5xl font-bold mb-4">Detectra</h1>
        <p className="text-m md:text-xl text-justify">
          The tool is an intuitive, all-in-one forensics platform designed to streamline evidence processing, automate analysis, and provide actionable insights. 
          With a focus on simplicity and innovation, Detectra transforms complex forensic investigations into streamlined workflows. Whether you're uncovering anomalies, tracking down suspicious activities, or generating reports, Detectra has your back—so you can focus on solving the case, not fighting with the tools.
        </p>
        <button className="mt-6 bg-white text-black px-6 py-3 rounded-lg font-semibold hover:bg-blue-300">
          ABOUT
        </button>
      </div>
    </div>
  );
}

function ScrollableSection() {
  //const navigate = useNavigate(); // Use useNavigate hook for navigation

  const tiles = [
    {
      title: "Network Anomaly Analysis",
      description:
        "Check for Network Anomalities with Network traffic analysis wireshark files.",
      button: "TRY OUT",
      action: () => window.location.href = "/main.html", // Navigate to main.html
    },
    {
      title: "Disk Image Analysis & Forensics",
      description:
        "Effortlessly process forensic disk images to extract, analyze, and uncover critical evidence with unparalleled precision and speed.",
      button: "TRY OUT",
    },
    {
      title: "Log Anomaly Detection",
      description:
        "Quickly identify suspicious patterns and irregularities in system logs with AI-powered anomaly detection, ensuring no threat goes unnoticed.",
      button: "TRY OUT",
    },
  ];

  return (
    <div className="bg-gray-200 py-20">
      <div className="container mx-auto grid grid-cols-1 sm:grid-cols-3 gap-1">
        {tiles.map((tile, index) => (
          <div
            key={index}
            className="bg-white shadow-lg p-10 rounded-lg flex flex-col items-center justify-center text-center ml-20 mr-10"
          >
            <img
              src="/na.png"
              alt="Icon"
              className="w-50 h-20 mb-4"
            />
            <h2 className="text-xl font-bold mb-2">{tile.title}</h2>
            <p className="text-gray-600 mb-4">{tile.description}</p>
            <button
              className="bg-red-600 text-white px-4 py-2 rounded hover:bg-blue-300"
              onClick={tile.action} // Call the action for navigation
            >
              {tile.button}
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}

function App() {
  return (
    <Router>
      <Routes>
        <Route
          path="/"
          element={
            <>
              <Navbar />
              <Hero />
              <ScrollableSection />
            </>
          }
        />
        <Route
          path="/about"
          element={
            <>
              <Navbar />
              <About />
            </>
          }
        />
        <Route
          path="/login"
          element={
            <>
              <Navbar />
              <Login />
            </>
          }
        />
        <Route
          path="/contact"
          element={
            <>
              <Navbar />
              <Contact />
            </>
          }
        />
        
      </Routes>
    </Router>
  );
}

export default App;
