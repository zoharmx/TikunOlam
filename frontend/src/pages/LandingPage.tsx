import { useRef } from 'react';
import { Link } from 'react-router-dom';
import { motion, useInView } from 'framer-motion';
import { ArrowRight, Eye, GitBranch, Lock } from 'lucide-react';
import PentagonCaseStudy from '../components/PentagonCaseStudy';
import SefirotPipeline from '../components/SefirotPipeline';

// ─── Tree of Life node positions (% of container) ───────────────────────────
const TREE_NODES = [
  { id: 'keter',    x: 50,  y: 5,  color: '#ffffff', label: 'כתר' },
  { id: 'chochmah', x: 75,  y: 18, color: '#3a86ff', label: 'חכמה' },
  { id: 'binah',    x: 25,  y: 18, color: '#06d6a0', label: 'בינה' },
  { id: 'chesed',   x: 75,  y: 40, color: '#ffd60a', label: 'חסד' },
  { id: 'gevurah',  x: 25,  y: 40, color: '#e63946', label: 'גבורה' },
  { id: 'tiferet',  x: 50,  y: 52, color: '#f77f00', label: 'תפארת' },
  { id: 'netzach',  x: 75,  y: 65, color: '#06ffa5', label: 'נצח' },
  { id: 'hod',      x: 25,  y: 65, color: '#457b9d', label: 'הוד' },
  { id: 'yesod',    x: 50,  y: 78, color: '#a8dadc', label: 'יסוד' },
  { id: 'malchut',  x: 50,  y: 92, color: '#9d4edd', label: 'מלכות' },
];

// ─── Stats ───────────────────────────────────────────────────────────────────
const STATS = [
  { value: 6,    suffix: '',   label: 'AI Providers' },
  { value: 10,   suffix: '',   label: 'Reasoning Stages' },
  { value: 8,    suffix: 'min', label: 'Deep Analysis' },
  { value: 2,    suffix: '',   label: 'Civilizational Perspectives' },
];

// ─── Differentiators ─────────────────────────────────────────────────────────
const DIFFERENTIATORS = [
  {
    icon: <GitBranch size={22} className="text-primary" />,
    title: 'No Single AI Decides',
    body: '6 different AI providers analyze your dilemma from independent angles. No single model monopoly. Adversarial by design.',
    detail: 'Grok · Mistral · GPT-4o · DeepSeek · VertexAI',
  },
  {
    icon: <Eye size={22} className="text-accent" />,
    title: 'Western vs. Eastern Blind Spots',
    body: 'BinahSigma activates automatically for geopolitical scenarios — comparing civilizational blind spots with quantified bias delta.',
    detail: '6 blind spots detected in Pentagon case · 0% bias delta',
  },
  {
    icon: <Lock size={22} className="text-secondary" />,
    title: 'Full Audit Trail',
    body: 'Every reasoning step is attributed to its AI provider. Not a black box — a transparent 10-stage reasoning chain you can inspect.',
    detail: 'Every sefirah annotated with provider, model, and confidence',
  },
];

// ─── LandingPage ─────────────────────────────────────────────────────────────
const LandingPage = () => {
  const caseStudyRef = useRef<HTMLDivElement>(null);

  const scrollToCaseStudy = () => {
    caseStudyRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' });
  };

  return (
    <div className="relative overflow-x-hidden bg-background text-slate-200">

      {/* ── 1. NAV ─────────────────────────────────────────────────────────── */}
      <nav className="fixed w-full z-50 backdrop-blur-xl bg-background/80 border-b border-white/5">
        <div className="max-w-7xl mx-auto px-5 sm:px-8 h-14 flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <div className="w-7 h-7 rounded-full bg-gradient-to-tr from-secondary to-primary flex items-center justify-center font-bold text-white text-base">ת</div>
            <span className="font-bold tracking-tight text-lg">Tikun<span className="text-primary">Olam</span></span>
          </div>
          <div className="flex items-center gap-3">
            <button
              onClick={scrollToCaseStudy}
              className="hidden sm:flex items-center gap-1.5 px-4 py-1.5 rounded-full text-sm text-slate-300 hover:text-white border border-white/10 hover:bg-white/5 transition-all"
            >
              <Eye size={13} />
              Case Study
            </button>
            <Link
              to="/login"
              className="flex items-center gap-1.5 px-4 py-1.5 rounded-full bg-primary text-white text-sm font-semibold hover:bg-primary/90 transition-all shadow-[0_0_16px_rgba(58,134,255,0.3)]"
            >
              Launch App <ArrowRight size={14} />
            </Link>
          </div>
        </div>
      </nav>

      {/* ── 2. HERO ────────────────────────────────────────────────────────── */}
      <section className="relative pt-28 pb-20 px-5 sm:px-8 max-w-7xl mx-auto min-h-screen flex flex-col lg:flex-row items-center gap-16">
        {/* Ambient glow */}
        <div className="absolute top-1/4 left-1/2 -translate-x-1/2 w-[600px] h-[500px] bg-secondary/10 rounded-full blur-[140px] pointer-events-none" />

        {/* Left: copy */}
        <div className="flex-1 relative z-10 text-center lg:text-left">
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full border border-white/10 bg-white/5 text-xs font-mono text-slate-300 mb-6"
          >
            <span className="w-1.5 h-1.5 rounded-full bg-accent animate-pulse" />
            Ethical AI Architecture
          </motion.div>

          <motion.h1
            initial={{ opacity: 0, y: 18 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.1 }}
            className="text-4xl sm:text-6xl lg:text-7xl font-bold leading-tight mb-4"
          >
            When AI must<br />
            <span className="text-gradient">choose</span>
          </motion.h1>

          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.25 }}
            className="text-lg sm:text-xl font-mono text-slate-400 mb-3"
          >
            10 reasoning stages. 6 AI models. One answer.
          </motion.p>

          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.35 }}
            className="text-slate-500 max-w-xl mx-auto lg:mx-0 mb-10 leading-relaxed"
          >
            TikunOlam routes every ethical dilemma through a 10-stage Kabbalistic reasoning pipeline,
            each stage powered by a different AI provider. No consensus bias. No single model deciding your future.
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.45 }}
            className="flex flex-col sm:flex-row gap-3 justify-center lg:justify-start"
          >
            <button
              onClick={scrollToCaseStudy}
              className="group flex items-center justify-center gap-2 px-7 py-3.5 rounded-full border border-white/15 bg-white/5 hover:bg-white/10 text-white font-semibold transition-all"
            >
              See Pentagon Case Study
              <ArrowRight size={16} className="group-hover:translate-x-1 transition-transform" />
            </button>
            <Link
              to="/login"
              className="group relative flex items-center justify-center gap-2 px-7 py-3.5 rounded-full bg-primary text-white font-bold overflow-hidden shadow-[0_0_24px_rgba(58,134,255,0.25)] hover:shadow-[0_0_36px_rgba(58,134,255,0.4)] transition-all"
            >
              <div className="absolute inset-0 bg-white/20 group-hover:translate-x-full transition-transform duration-500 ease-out -skew-x-12 -translate-x-full" />
              Run Your Own Analysis
            </Link>
          </motion.div>
        </div>

        {/* Right: Tree of Life visual */}
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.8, delay: 0.3 }}
          className="relative w-64 h-80 flex-shrink-0 hidden lg:block"
        >
          <svg className="absolute inset-0 w-full h-full opacity-15" viewBox="0 0 100 100" preserveAspectRatio="none">
            {/* Tree of Life paths */}
            {[
              [50,5, 75,18],[50,5, 25,18],
              [75,18,75,40],[25,18,25,40],
              [75,18,50,52],[25,18,50,52],
              [75,40,50,52],[25,40,50,52],
              [75,40,75,65],[25,40,25,65],
              [50,52,75,65],[50,52,25,65],
              [50,52,50,78],[75,65,50,78],
              [25,65,50,78],[50,78,50,92],
            ].map(([x1,y1,x2,y2], i) => (
              <line key={i} x1={x1} y1={y1} x2={x2} y2={y2} stroke="white" strokeWidth="0.5" />
            ))}
          </svg>
          {TREE_NODES.map((node, idx) => (
            <motion.div
              key={node.id}
              className="absolute -translate-x-1/2 -translate-y-1/2 flex flex-col items-center gap-1"
              style={{ left: `${node.x}%`, top: `${node.y}%` }}
              animate={{ opacity: [0.5, 1, 0.5] }}
              transition={{ duration: 3, repeat: Infinity, delay: idx * 0.3 }}
            >
              <div
                className="w-5 h-5 rounded-full border-2 border-current"
                style={{ color: node.color, backgroundColor: `${node.color}20`, boxShadow: `0 0 12px ${node.color}60` }}
              />
              <span className="text-[8px] font-mono" style={{ color: node.color }}>{node.label}</span>
            </motion.div>
          ))}
        </motion.div>
      </section>

      {/* ── 3. LIVE CASE STUDY ─────────────────────────────────────────────── */}
      <section
        id="case-study"
        ref={caseStudyRef}
        className="py-24 px-5 sm:px-8 max-w-7xl mx-auto"
      >
        <div className="text-center mb-12">
          <span className="px-3 py-1 rounded-full text-[11px] font-mono font-bold bg-yellow-500/10 border border-yellow-500/20 text-yellow-400 uppercase tracking-wider">
            Live Case Study
          </span>
          <h2 className="text-3xl sm:text-5xl font-bold mt-4 mb-4">
            Anthropic vs. The Pentagon
          </h2>
          <p className="text-slate-400 max-w-2xl mx-auto">
            The Pentagon offered Anthropic $2.4B for autonomous weapons AI — and a 60-day ultimatum.
            6 AI providers analyzed the dilemma across 10 reasoning stages. Here's every step.
          </p>
        </div>
        <PentagonCaseStudy />
      </section>

      {/* ── 4. ARCHITECTURE ────────────────────────────────────────────────── */}
      <section className="py-24 px-5 sm:px-8 max-w-7xl mx-auto border-t border-white/5">
        <div className="text-center mb-12">
          <span className="px-3 py-1 rounded-full text-[11px] font-mono font-bold bg-primary/10 border border-primary/20 text-primary uppercase tracking-wider">
            Architecture
          </span>
          <h2 className="text-3xl sm:text-5xl font-bold mt-4 mb-4">
            6 AI Providers. 10 Reasoning Stages.
          </h2>
          <p className="text-slate-400 max-w-xl mx-auto">
            No single model holds a monopoly on the verdict.
            Each sefirah is powered by a different AI provider — by design.
          </p>
        </div>
        <SefirotPipeline />
      </section>

      {/* ── 5. STATS STRIP ─────────────────────────────────────────────────── */}
      <StatStrip />

      {/* ── 6. DIFFERENTIATORS ─────────────────────────────────────────────── */}
      <section className="py-24 px-5 sm:px-8 max-w-7xl mx-auto border-t border-white/5">
        <div className="grid md:grid-cols-3 gap-6">
          {DIFFERENTIATORS.map((d, idx) => (
            <motion.div
              key={idx}
              whileHover={{ y: -4 }}
              className="glass-card p-7 rounded-2xl space-y-4"
            >
              <div className="p-2.5 bg-white/5 rounded-xl w-fit">{d.icon}</div>
              <h3 className="text-lg font-bold text-white">{d.title}</h3>
              <p className="text-slate-400 text-sm leading-relaxed">{d.body}</p>
              <p className="text-[11px] font-mono text-slate-600 border-t border-white/5 pt-3">{d.detail}</p>
            </motion.div>
          ))}
        </div>
      </section>

      {/* ── 7. FINAL CTA ───────────────────────────────────────────────────── */}
      <section className="py-28 px-5 sm:px-8 text-center border-t border-white/5 relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-primary/5 via-transparent to-secondary/5 pointer-events-none" />
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="relative z-10 max-w-2xl mx-auto"
        >
          <h2 className="text-3xl sm:text-5xl font-bold mb-4">
            Ready to run your<br />
            <span className="text-gradient">own analysis?</span>
          </h2>
          <p className="text-slate-400 mb-10">
            The Pentagon case took 7m 55s across 10 reasoning stages and 6 AI providers.
            Your dilemma can run now.
          </p>
          <Link
            to="/login"
            className="inline-flex items-center gap-2 px-10 py-4 rounded-full bg-primary text-white font-bold text-lg shadow-[0_0_40px_rgba(58,134,255,0.3)] hover:shadow-[0_0_60px_rgba(58,134,255,0.45)] hover:bg-primary/90 transition-all"
          >
            Start Analysis <ArrowRight size={20} />
          </Link>
        </motion.div>
      </section>

      {/* Footer */}
      <footer className="py-8 text-center text-slate-600 text-sm border-t border-white/5">
        <p>© 2026 Tikun Olam Framework · <span className="font-mono">תיקון עולם</span> — Repairing the world</p>
      </footer>
    </div>
  );
};

// ─── Stats strip with count-up ───────────────────────────────────────────────
function StatStrip() {
  const ref = useRef<HTMLDivElement>(null);
  const inView = useInView(ref, { once: true });

  return (
    <div ref={ref} className="border-y border-white/5 bg-white/[0.02] py-14">
      <div className="max-w-5xl mx-auto px-5 grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
        {STATS.map((stat, idx) => (
          <div key={idx}>
            <div className="text-4xl sm:text-5xl font-bold text-transparent bg-clip-text bg-gradient-to-b from-white to-slate-500 mb-2 font-mono">
              {inView ? (
                <CountUp target={stat.value} suffix={stat.suffix} delay={idx * 0.15} />
              ) : '0'}
            </div>
            <div className="text-sm text-slate-500 uppercase tracking-wider">{stat.label}</div>
          </div>
        ))}
      </div>
    </div>
  );
}

function CountUp({ target, suffix = '', delay = 0 }: { target: number; suffix?: string; delay?: number }) {
  return (
    <motion.span
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ delay }}
    >
      {target}{suffix}
    </motion.span>
  );
}

export default LandingPage;
