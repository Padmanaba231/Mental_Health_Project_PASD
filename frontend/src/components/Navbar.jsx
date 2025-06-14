import { useState } from "react";
import { Link } from "react-router-dom";

export default function Navbar() {
  const [isOpen, setIsOpen] = useState(false);

  const navLinks = [
    { name: "Home", path: "/" },
    { name: "Chatbot", path: "/chatbot" },
    { name: "Profile", path: "/profile" },
  ];

  return (
    <header className="fixed top-0 left-0 right-0 bg-white/80 backdrop-blur border-b border-gray-200 z-50">
      <div className="max-w-7xl mx-auto px-6 py-3 flex justify-between items-center">
        {/* Logo */}
        <Link to="/" className="text-xl font-bold text-teal-700 tracking-wide">
          PASD
        </Link>

        {/* Desktop menu */}
        <nav className="hidden md:flex items-center space-x-6">
          {navLinks.map((link) => (
            <Link
              key={link.name}
              to={link.path}
              className="text-gray-700 hover:text-teal-600 transition"
            >
              {link.name}
            </Link>
          ))}
          <Link
            to="/login"
            className="bg-teal-600 text-white px-4 py-2 rounded hover:bg-teal-700 transition"
          >
            Login
          </Link>
        </nav>

        {/* Mobile menu toggle */}
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="md:hidden text-teal-700 text-2xl"
        >
          ☰
        </button>
      </div>

      {/* Mobile menu */}
      {isOpen && (
        <nav className="md:hidden px-6 pb-4 space-y-2 bg-white">
          {navLinks.map((link) => (
            <Link
              key={link.name}
              to={link.path}
              onClick={() => setIsOpen(false)}
              className="block text-gray-700 hover:text-teal-600"
            >
              {link.name}
            </Link>
          ))}
          <Link
            to="/login"
            onClick={() => setIsOpen(false)}
            className="block bg-teal-600 text-white px-4 py-2 rounded text-center hover:bg-teal-700"
          >
            Login
          </Link>
        </nav>
      )}
    </header>
  );
}
