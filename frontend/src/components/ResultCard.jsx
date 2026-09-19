import { motion } from 'framer-motion';
import StatusBadge from './StatusBadge';
import ConfidenceBar from './ConfidenceBar';
import { AlertTriangle, CheckCircle2, Wand2, Info, Sparkles } from 'lucide-react';

const ResultCard = ({ result }) => {
  if (!result) return null;

  const { disease, confidence, is_healthy, advice, gemini_advice } = result;

  return (
    <motion.div
      initial={{ y: 20, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      exit={{ y: -20, opacity: 0 }}
      className="w-full max-w-2xl glass-card p-8 mt-12 mb-20 relative overflow-hidden group shadow-2xl"
    >
      <div className={`absolute top-0 right-0 w-32 h-32 opacity-5 pointer-events-none ${is_healthy ? 'text-agro-terminal' : 'text-agro-amber'}`}>
        {is_healthy ? <CheckCircle2 className="w-full h-full" /> : <AlertTriangle className="w-full h-full" />}
      </div>

      <div className="flex flex-col md:flex-row md:items-start justify-between gap-6">
        <div className="flex-1 space-y-4">
          <div className="flex items-center gap-3">
            <StatusBadge isHealthy={is_healthy} />
            <span className="text-agro-text/30 text-[10px] uppercase font-bold tracking-[0.2em]">Analysis Complete</span>
          </div>

          <h2 className={`text-3xl md:text-4xl font-extrabold font-grotesk leading-tight tracking-tight ${is_healthy ? 'text-agro-terminal' : 'text-agro-amber'}`}>
            {disease}
          </h2>

          <div className="p-4 rounded-xl bg-agro-dark/40 border border-agro-terminal/10 space-y-2 mt-6">
            <div className="flex items-center gap-2 text-agro-terminal/60 text-xs font-bold uppercase tracking-widest">
              <Wand2 className="w-3 h-3" />
              <span>Diagnostic Insight</span>
            </div>
            <p className="text-agro-text/80 text-sm leading-relaxed font-inter">
              {advice}
            </p>
          </div>

          {gemini_advice && (
            <div className="mt-10 relative group">
              {/* Glow Effect */}
              <div className="absolute -inset-0.5 bg-gradient-to-r from-agro-terminal/40 via-agro-terminal/20 to-agro-amber/40 rounded-2xl blur opacity-20 group-hover:opacity-40 transition duration-500"></div>
              
              <div className="relative p-6 rounded-2xl bg-agro-dark/40 backdrop-blur-xl border border-white/10 overflow-hidden">
                {/* Background Pattern */}
                <div className="absolute top-0 right-0 p-4 opacity-5 pointer-events-none">
                  <Sparkles className="w-24 h-24 text-agro-terminal rotate-12" />
                </div>

                <div className="flex items-center gap-3 mb-4">
                  <div className="w-8 h-8 rounded-lg bg-agro-terminal/10 flex items-center justify-center border border-agro-terminal/20">
                    <Sparkles className="w-4 h-4 text-agro-terminal" />
                  </div>
                  <div>
                    <h4 className="text-[10px] font-black uppercase tracking-[0.25em] text-agro-terminal/70">Intelligence Insight</h4>
                    <p className="text-xs font-bold text-agro-text/90">AEROFARM AI Suggestion</p>
                  </div>
                </div>
                
                <div className="relative">
                  <div className="prose prose-invert max-w-none">
                    <p className="text-[13px] leading-relaxed font-inter text-agro-text/80 italic pl-5 border-l-2 border-agro-terminal/30 py-1">
                      {gemini_advice}
                    </p>
                  </div>
                </div>

                {/* Micro-interaction line */}
                <div className="mt-4 h-[1px] w-full bg-gradient-to-r from-agro-terminal/20 via-transparent to-transparent"></div>
              </div>
            </div>
          )}
        </div>

        <div className="md:w-64 glass-card bg-agro-terminal/5 border-agro-terminal/10 p-4 rounded-xl flex flex-col items-center self-start">
          <ConfidenceBar confidence={confidence} isHealthy={is_healthy} />
        </div>
      </div>

      <div className="mt-8 pt-6 border-t border-agro-terminal/5 flex items-center justify-between">
        <div className="flex items-center gap-2 text-agro-text/40 text-[9px] font-bold tracking-widest uppercase">
          <Info className="w-3 h-3" />
          <span>Intelligent Diagnostic Engine • AEROFARM v3.2</span>
        </div>
        <div className="flex items-center gap-2 text-agro-text/20 text-[9px] font-medium">
          ML MODEL IDENTIFIED
        </div>
      </div>
    </motion.div>
  );
};

export default ResultCard;
