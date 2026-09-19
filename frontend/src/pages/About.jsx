import { motion } from 'framer-motion';
import { Leaf, Database, Layers, CheckCircle } from 'lucide-react';

const About = () => {
  const techStack = [
    { name: 'FastAPI', category: 'Backend', description: 'High-performance Python framework for building APIs with data validation.' },
    { name: 'TensorFlow', category: 'AI Engine', description: 'Deep learning framework used to train and run the plant disease detection model.' },
    { name: 'React + Vite', category: 'Frontend', description: 'Modern frontend development toolkit for a responsive, lightning-fast UI.' },
    { name: 'Tailwind CSS', category: 'Design', description: 'Utility-first CSS framework for custom, premium visual aesthetics.' },
  ];

  return (
    <div className="max-w-5xl mx-auto py-12 px-6">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="space-y-4 mb-16"
      >
        <span className="text-agro-terminal font-bold font-grotesk tracking-widest text-xs uppercase">The Technology</span>
        <h1 className="text-5xl font-black font-grotesk text-agro-text leading-tight">
          Next-Gen Diagnostics for <br /> Future Farmers.
        </h1>
        <p className="text-agro-text/60 text-lg max-w-3xl leading-relaxed">
          AEROFARM is a full-stack plant disease detection platform designed to mitigate crop loss through early pathological detection. Built during Week 1 of our development cycle, this project demonstrates the synergy between Computer Vision and High-Performance Web Services.
        </p>
      </motion.div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-20">
        <motion.div 
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="glass-card p-10 space-y-6"
        >
          <div className="w-12 h-12 bg-agro-terminal/20 rounded-xl flex items-center justify-center">
            <Database className="w-6 h-6 text-agro-terminal" />
          </div>
          <h3 className="text-2xl font-bold font-grotesk text-agro-text">The Dataset</h3>
          <p className="text-agro-text/50 leading-relaxed font-inter">
            Our model is trained on the PlanetVillage dataset, featuring over 54,000 images of healthy and diseased crop leaves across 14 diverse species. It covers 38 distinct class labels including bacterial spots, blights, rusts, and more.
          </p>
          <ul className="space-y-2">
            {['14 Crop Species', '38 Disease Classes', '224px Image Resolution'].map((item) => (
              <li key={item} className="flex items-center gap-2 text-agro-text/70 text-sm italic">
                <CheckCircle className="w-4 h-4 text-agro-terminal" /> {item}
              </li>
            ))}
          </ul>
        </motion.div>

        <motion.div 
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          className="glass-card p-10 space-y-6 border-agro-amber/10"
        >
          <div className="w-12 h-12 bg-agro-amber/20 rounded-xl flex items-center justify-center">
            <Layers className="w-6 h-6 text-agro-amber" />
          </div>
          <h3 className="text-2xl font-bold font-grotesk text-agro-text">Model Architecture</h3>
          <p className="text-agro-text/50 leading-relaxed font-inter">
            We utilize a transfer learning approach with <strong>MobileNetV2</strong> as our base architecture. This allows for high-accuracy predictions while maintaining a lightweight footprint suitable for real-time mobile and web deployment.
          </p>
          <div className="pt-4 p-4 bg-agro-dark/50 rounded-xl border border-white/5 space-y-2">
            <div className="flex justify-between text-[10px] font-bold text-agro-text/40 tracking-widest uppercase">
              <span>Optimized For</span>
              <span>Performance</span>
            </div>
            <div className="h-1 w-full bg-white/5 rounded-full overflow-hidden">
              <div className="h-full w-full bg-agro-amber shadow-glow-amber opacity-60" />
            </div>
          </div>
        </motion.div>
      </div>

      <div className="mt-20">
        <h3 className="text-xl font-bold font-grotesk text-agro-text/40 uppercase tracking-widest text-center mb-10">AEROFARM Tech Stack</h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {techStack.map((tech) => (
            <div key={tech.name} className="glass-card p-6 border-white/5 hover:border-agro-terminal/20 transition-colors group">
              <span className="text-[10px] font-bold text-agro-terminal group-hover:text-agro-text transition-colors">{tech.category}</span>
              <h4 className="text-lg font-bold font-grotesk text-agro-text mt-1">{tech.name}</h4>
              <p className="text-xs text-agro-text/40 mt-2 leading-relaxed">{tech.description}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default About;
