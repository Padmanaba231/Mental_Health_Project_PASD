import { Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Chatbot from './pages/Chatbot';
import Profile from './pages/Profile';
import Login from './pages/Login';

function App() {
  return (
    <>
      <Navbar />
      <div className="pt-24 px-4 min-h-screen bg-gray-50">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/chatbot" element={<Chatbot />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/login" element={<Login />} />
          <Route path="*" element={<div className="text-center text-red-500 text-xl mt-10">404 - Halaman tidak ditemukan</div>} />
        </Routes>
      </div>
    </>
  );
}

export default App;
