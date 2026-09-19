import { Link } from 'react-router-dom';
import { Leaf, Github, BarChart3, Info } from 'lucide-react';

const Navbar = () => {
  return (
    <nav className="sticky top-0 z-50 w-full glass-card rounded-none border-x-0 border-t-0 border-b-agro-terminal/20 backdrop-blur-md">
      <div className="container mx-auto px-6 h-16 flex items-center justify-between">
        <Link to="/" className="flex items-center gap-2 group">
          <Leaf className="w-8 h-8 text-agro-terminal transition-transform group-hover:scale-110 group-hover:rotate-12" />
          <span className="text-xl font-black font-grotesk tracking-tighter text-agro-terminal">
            AERO<span className="text-agro-text">FARM</span>
          </span>
        </Link>

        <div className="flex items-center gap-8">
          <Link 
            to="/" 
            className="flex items-center gap-2 text-agro-text/70 hover:text-agro-terminal transition-colors"
          >
            <BarChart3 className="w-4 h-4" />
            <span className="text-sm font-medium">Detector</span>
          </Link>
          <Link 
            to="/about" 
            className="flex items-center gap-2 text-agro-text/70 hover:text-agro-terminal transition-colors"
          >
            <Info className="w-4 h-4" />
            <span className="text-sm font-medium">About</span>
          </Link>
          <a 
            href="https://github.com" 
            target="_blank" 
            rel="noopener noreferrer"
            className="p-2 glass-card border-none hover:bg-agro-terminal/10 transition-colors"
          >
            <Github className="w-5 h-5 text-agro-terminal" />
          </a>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
