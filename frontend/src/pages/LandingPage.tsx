import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ShieldCheck, BrainCircuit, Globe, ArrowRight, Zap } from 'lucide-react';

const LandingPage = () => {
  return (
    <div className="relative overflow-hidden">
      {/* Navigation */}
      <nav className="fixed w-full z-50 glass-panel border-b-0 border-white/5">
        <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-secondary to-primary flex items-center justify-center font-bold text-white text-lg">
              ת
            </div>
            <span className="text-xl font-bold tracking-tight">Tikun<span className="text-primary">Olam</span></span>
          </div>
          <div className="flex gap-4">
            <Link to="/app" className="px-6 py-2 rounded-full bg-white/5 hover:bg-white/10 border border-white/10 transition-all text-sm font-medium">
              Documentation
            </Link>
            <Link to="/app" className="px-6 py-2 rounded-full bg-primary hover:bg-primary/90 text-white font-medium text-sm transition-all shadow-[0_0_20px_rgba(58,134,255,0.3)]">
              Launch System
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="pt-32 pb-20 px-6 max-w-7xl mx-auto text-center relative">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="absolute top-20 left-1/2 -translate-x-1/2 w-[600px] h-[600px] bg-secondary/20 rounded-full blur-[120px] pointer-events-none"
        />

        <motion.h1
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-5xl md:text-7xl font-bold leading-tight mb-6 relative z-10"
        >
          Ethical Reasoning <br />
          <span className="text-gradient">Architecture for AI</span>
        </motion.h1>

        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2 }}
          className="text-lg md:text-xl text-slate-400 max-w-2xl mx-auto mb-10"
        >
          Don't just optimize for utility. Optimize for repair.
          Tikun Olam introduces a 10-stage ethical alignment layer with civilizational bias detection (BinahSigma).
        </motion.p>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="flex flex-col sm:flex-row gap-4 justify-center items-center"
        >
          <Link to="/app" className="group relative px-8 py-4 bg-primary rounded-full text-white font-bold text-lg overflow-hidden">
            <div className="absolute inset-0 bg-white/20 group-hover:translate-x-full transition-transform duration-500 ease-out -skew-x-12 -translate-x-full" />
            <span className="flex items-center gap-2">
              Access Console <ArrowRight className="w-5 h-5" />
            </span>
          </Link>
          <button className="px-8 py-4 rounded-full border border-white/10 hover:bg-white/5 text-slate-300 font-medium transition-all">
            Watch UBI/UN Demo
          </button>
        </motion.div>
      </section>

      {/* Features Grid */}
      <section className="py-20 px-6 max-w-7xl mx-auto">
        <div className="grid md:grid-cols-3 gap-8">
          <FeatureCard
            icon={<BrainCircuit className="w-8 h-8 text-accent" />}
            title="10 Sefirot Pipeline"
            desc="Breaks down complex decisions into 10 functional stages, from ethical validation (Keter) to execution (Malchut)."
          />
          <FeatureCard
            icon={<Globe className="w-8 h-8 text-primary" />}
            title="BinahSigma Engine"
            desc="Detects and quantifies civilizational biases by comparing Western (Gemini) vs Eastern (DeepSeek) perspectives."
          />
          <FeatureCard
            icon={<ShieldCheck className="w-8 h-8 text-secondary" />}
            title="Full Auditability"
            desc="Every decision generates an immutable reasoning trail. No more ethical black boxes in critical systems."
          />
        </div>
      </section>

      {/* Stats/Social Proof */}
      <section className="border-y border-white/5 bg-white/[0.02]">
        <div className="max-w-7xl mx-auto py-12 px-6 flex flex-wrap justify-center gap-12 md:gap-24 text-center">
          <Stat number="10" label="Reasoning Stages" />
          <Stat number="3" label="Integrated AI Engines" />
          <Stat number="100%" label="Decision Transparency" />
        </div>
      </section>

      <footer className="py-8 text-center text-slate-600 text-sm">
        <p>© 2025 Tikun Olam Framework. Repairing the world, one byte at a time.</p>
      </footer>
    </div>
  );
};

const FeatureCard = ({ icon, title, desc }: { icon: any, title: string, desc: string }) => (
  <motion.div
    whileHover={{ y: -5 }}
    className="glass-card p-8 rounded-2xl relative overflow-hidden group"
  >
    <div className="absolute top-0 right-0 p-3 opacity-10 group-hover:opacity-20 transition-opacity">
      <Zap className="w-24 h-24" />
    </div>
    <div className="mb-4 p-3 bg-white/5 rounded-xl w-fit">{icon}</div>
    <h3 className="text-xl font-bold mb-3 text-slate-100">{title}</h3>
    <p className="text-slate-400 leading-relaxed">{desc}</p>
  </motion.div>
);

const Stat = ({ number, label }: { number: string, label: string }) => (
  <div>
    <div className="text-4xl md:text-5xl font-bold text-transparent bg-clip-text bg-gradient-to-b from-white to-slate-500 mb-2">{number}</div>
    <div className="text-sm font-medium text-slate-500 uppercase tracking-wider">{label}</div>
  </div>
);

export default LandingPage;
