// App.jsx
import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import { FiSearch } from 'react-icons/fi';
import About from "./components/About";

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
      <div className="relative text-left text-white max-w-xl">
        <h1 className="text-4xl md:text-5xl font-bold mb-4 ml-20">Detectra</h1>
        <p className="text-sm md:text-xl ml-20">
          The tool is an intuitive, all-in-one forensics platform designed to streamline evidence processing, automate analysis, and provide actionable insights.
        </p>
        <button className="mt-6 bg-white text-black px-6 py-3 rounded-lg font-semibold hover:bg-blue-300 ml-20">
        ABOUT
      </button>

      </div>
    </div>
  );
}

function ScrollableSection() {
  const tiles = [
    {
      title: "NETWORK ANOMALY",
      description:
        "The Detectra platform is designed to maintain and promote secure and intuitive forensics analysis.",
      button: "LEARN MORE",
    },
    {
      title: "DISK FORENSICS",
      description:
        "Explore our training courses designed to teach effective techniques for evidence analysis and management.",
      button: "LEARN MORE",
    },
    {
      title: "LOG ANOMALY",
      description:
        "Participate in our annual contest to showcase your skills and win exciting prizes while contributing to the community.",
      button: "LEARN MORE",
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
            <button className="bg-red-600 text-white px-4 py-2 rounded hover:bg-blue-300">
              {tile.button}
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}





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

function Contact() {
  return (
    <div className="container mx-auto p-4">
      <h2 className="text-2xl font-bold mb-4">Contact Us</h2>
      <p>If you have any questions, feel free to reach out to us at contact@detectra.com.</p>
    </div>
  );
}

function App() {
  return (
    <Router>
      <div>
        <Navbar />

        <Routes>
          <Route path="/about" element={<About />} />
          <Route path="/login" element={<Login />} />
          <Route path="/contact" element={<Contact />} />
        </Routes>
        <Hero />
        <ScrollableSection />
      </div>
    </Router>
  );
}

export default App;
