import { motion } from 'framer-motion';

const StatusBadge = ({ isHealthy }) => {
  return (
    <motion.div
      initial={{ scale: 0.9, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      className={`inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider ${
        isHealthy 
          ? 'bg-agro-terminal/10 text-agro-terminal border border-agro-terminal/30 shadow-glow-green' 
          : 'bg-agro-amber/10 text-agro-amber border border-agro-amber/30 shadow-glow-amber'
      }`}
    >
      <span className={`w-2 h-2 rounded-full animate-pulse ${isHealthy ? 'bg-agro-terminal' : 'bg-agro-amber'}`}></span>
      {isHealthy ? 'Healthy' : 'Diseased'}
    </motion.div>
  );
};

export default StatusBadge;
