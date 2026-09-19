import { motion } from 'framer-motion';

const ConfidenceBar = ({ confidence, isHealthy }) => {
  const percentage = (confidence * 100).toFixed(1);
  const color = isHealthy ? 'bg-agro-terminal' : 'bg-agro-amber';
  const shadow = isHealthy ? 'shadow-glow-green' : 'shadow-glow-amber';

  return (
    <div className="w-full space-y-2 mt-4">
      <div className="flex justify-between items-end">
        <span className="text-agro-text/60 text-xs font-medium uppercase tracking-widest">Model Confidence</span>
        <span className={`text-lg font-bold font-grotesk ${isHealthy ? 'text-agro-terminal' : 'text-agro-amber'}`}>
          {percentage}%
        </span>
      </div>
      <div className="h-2 w-full bg-agro-dark/50 rounded-full overflow-hidden border border-white/5">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${percentage}%` }}
          transition={{ duration: 1, ease: 'easeOut' }}
          className={`h-full ${color} ${shadow}`}
        />
      </div>
    </div>
  );
};

export default ConfidenceBar;
