import { motion } from 'framer-motion';

interface HeaderProps {
  isAnalyzing?: boolean;
}

function Header({ isAnalyzing = false }: HeaderProps) {
  return (
    <div className="mb-8">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-4xl font-bold text-gradient mb-2">
            תיקון עולם
          </h1>
          <p className="text-slate-400 text-sm">
            Ethical AI Reasoning Framework
          </p>
        </div>

        <div className="flex gap-3 items-center flex-wrap justify-end">
          <div className="px-4 py-2 rounded-full bg-accent/10 border border-accent/20 text-accent text-xs font-medium">
            BinahSigma Active
          </div>
          <div className="px-4 py-2 rounded-full bg-primary/10 border border-primary/20 text-primary text-xs font-medium">
            10 Sefirot
          </div>
          {isAnalyzing && (
            <motion.div
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              className="flex items-center gap-2 px-4 py-2 rounded-full bg-yellow-500/10 border border-yellow-500/20 text-yellow-400 text-xs font-medium"
            >
              <motion.span
                className="w-1.5 h-1.5 rounded-full bg-yellow-400"
                animate={{ opacity: [1, 0.3, 1] }}
                transition={{ duration: 1.2, repeat: Infinity }}
              />
              Processing...
            </motion.div>
          )}
        </div>
      </div>

      <div className="glass-panel p-4 rounded-xl text-sm text-slate-300">
        Multi-civilizational AI ethical reasoning based on Kabbalistic Sefirot.
        Detects biases between Western and Eastern perspectives.
      </div>
    </div>
  );
}

export default Header;
