import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import About from './pages/About';

function App() {
  return (
    <Router>
      <div className="min-h-screen flex flex-col">
        <Navbar />
        <main className="flex-grow container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/about" element={<About />} />
          </Routes>
        </main>
        <footer className="py-6 border-t border-agro-terminal/10 text-center text-agro-text/40 text-sm">
          <p>© 2026 AEROFARM AI • Futuristic Crop Solutions</p>
        </footer>
      </div>
    </Router>
  );
}

export default App;
