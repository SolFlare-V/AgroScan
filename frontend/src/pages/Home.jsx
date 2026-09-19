import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import UploadZone from '../components/UploadZone';
import ResultCard from '../components/ResultCard';
import { ShieldCheck, Cpu, Zap, Activity } from 'lucide-react';

const Home = () => {
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);

  return (
    <div className="flex flex-col items-center">
      {/* Hero Section */}
      <section className="text-center py-16 md:py-24 space-y-6 max-w-4xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-agro-terminal/10 border border-agro-terminal/30 text-agro-terminal text-[10px] font-bold uppercase tracking-[0.3em] shadow-glow-green mb-4"
        >
          <Zap className="w-3 h-3 fill-agro-terminal" />
          Powered by MobileNetV2 AI
        </motion.div>

        <motion.h1 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="text-5xl md:text-7xl font-black font-grotesk text-agro-text leading-[1.1] tracking-tight"
        >
          Detect Plant Disease <br />
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-agro-terminal via-agro-terminal to-agro-text">Instantly.</span>
        </motion.h1>

        <motion.p 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="text-agro-text/50 max-w-2xl mx-auto text-lg md:text-xl font-inter leading-relaxed"
        >
          Precision agriculture at your fingertips. Upload a high-resolution photo of your crop's leaf and let our neural network provide a professional diagnostic in real-time.
        </motion.p>

        {/* Dynamic Badges */}
        <motion.div 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4 }}
          className="flex flex-wrap justify-center gap-6 pt-8"
        >
          <div className="flex items-center gap-2 text-agro-text/30 text-xs font-semibold uppercase tracking-widest">
            <ShieldCheck className="w-4 h-4 text-agro-terminal/50" />
            98.5% Accuracy
          </div>
          <div className="flex items-center gap-2 text-agro-text/30 text-xs font-semibold uppercase tracking-widest">
            <Cpu className="w-4 h-4 text-agro-terminal/50" />
            V3 Core Engine
          </div>
          <div className="flex items-center gap-2 text-agro-text/30 text-xs font-semibold uppercase tracking-widest">
            <Activity className="w-4 h-4 text-agro-terminal/50" />
            Real-time I/O
          </div>
        </motion.div>
      </section>

      {/* Main Interaction Area */}
      <section className="w-full max-w-4xl px-4 flex flex-col items-center">
        <UploadZone 
          onResult={(res) => setPrediction(res)} 
          onLoading={(l) => setLoading(l)}
        />

        <AnimatePresence>
          {prediction && !loading && (
            <ResultCard result={prediction} />
          )}
        </AnimatePresence>
      </section>
      
      {/* Background Glows */}
      <div className="fixed top-1/2 left-1/4 -translate-y-1/2 w-[500px] h-[500px] bg-agro-terminal/5 rounded-full blur-[120px] pointer-events-none -z-10 animate-pulse" />
      <div className="fixed top-1/4 right-1/4 w-[400px] h-[400px] bg-agro-amber/5 rounded-full blur-[100px] pointer-events-none -z-10" />
    </div>
  );
};

export default Home;
