import { useEffect } from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';

/* ─── Data extracted from tikun-full-results JSON ─── */
const SEFIROT_SCORES = [
  { name: 'Keter', hebrew: 'כתר', role: 'Ethical Alignment', score: 75, color: '#ffffff', note: 'Corruption: Critical' },
  { name: 'Chochmah', hebrew: 'חכמה', role: 'Confidence', score: 90, color: '#3a86ff', note: '5 patterns · 3 precedents · 3 paradoxes' },
  { name: 'Binah', hebrew: 'בינה', role: 'Contextual Depth', score: 90, color: '#06d6a0', note: 'BinahSigma — 71% delta' },
  { name: 'Chesed', hebrew: 'חסד', role: 'Opportunity', score: 85, color: '#ffd60a', note: '4 strategic opportunities' },
  { name: 'Gevurah', hebrew: 'גבורה', role: 'Risk', score: 95, color: '#e63946', note: '3 critical risks identified' },
  { name: 'Tiferet', hebrew: 'תפארת', role: 'Harmony', score: 72, color: '#f77f00', note: 'Balance score' },
  { name: 'Netzach', hebrew: 'נצח', role: 'Strategy', score: 80, color: '#06ffa5', note: 'Strategic clarity' },
  { name: 'Hod', hebrew: 'הוד', role: 'Communication', score: 78, color: '#457b9d', note: 'Stakeholder messaging' },
  { name: 'Yesod', hebrew: 'יסוד', role: 'Readiness', score: 70, color: '#a8dadc', note: 'Foundation strength' },
  { name: 'Malchut', hebrew: 'מלכות', role: 'Final Decision', score: 75, color: '#9d4edd', note: 'CONDITIONAL_GO' },
];

const POWER_DYNAMICS = [
  {
    number: '01',
    title: 'The Microsoft Illusion',
    subtitle: 'The board\'s authority is a fragile illusion',
    body: 'Microsoft, holding a 49% stake and providing the essential computational infrastructure, is the true sovereign. If the board fires Altman, there is a high probability Microsoft will trigger a "hostile rescue" — hiring Altman and defecting employees into a new wholly-owned subsidiary. Result: the non-profit structure is shattered, safety-oriented governance eliminated, and AGI development sits under a commercial entity with fiduciary duty to shareholders, not humanity.',
    severity: 'critical',
    probability: 'likely',
    color: '#e63946',
  },
  {
    number: '02',
    title: 'Safety Theater & Governance Capture',
    subtitle: 'Proposed solutions sound good on paper',
    body: 'The "Safety Council" and "Guardian CEO" proposals are elegant but susceptible to capture. The risk: these become performative structures, creating a facade of safety while the Visionary subverts them through soft power, resource allocation, and political maneuvering. The Guardian becomes a figurehead. The council a rubber stamp. This isn\'t cynicism — it\'s realistic power analysis.',
    severity: 'critical',
    probability: 'likely',
    color: '#f77f00',
  },
  {
    number: '03',
    title: 'The Precedent of Rewarded Recklessness',
    subtitle: 'The most dangerous long-term risk',
    body: 'Keeping Altman — even with strengthened oversight — sets a catastrophic precedent for the entire industry. The message becomes: a leader can ignore safety teams, risk existential catastrophe, and if they\'re charismatic and economically valuable enough, face no consequences. Every ambitious AI founder learns: safety is a negotiable constraint. A PR problem to manage, not a fundamental duty.',
    severity: 'high',
    probability: 'certain',
    color: '#ffd60a',
  },
];

const SOLUTIONS = [
  {
    number: '1',
    title: 'Co-CEO Model: Visionary + Guardian',
    impact: 'high',
    confidence: 85,
    body: 'Instead of choosing between speed (Altman) and safety: institutionalize the dialectic. Keep Altman as "Visionary" CEO. Appoint a co-CEO "Guardian" of equal power with final authority on safety, ethics, and deployment. This proves high-velocity innovation and robust safety are not mutually exclusive — two essential pillars of a single arch.',
    beneficiaries: ['OpenAI employees', 'Microsoft', 'Tech industry', 'Sam Altman'],
    color: '#9d4edd',
  },
  {
    number: '2',
    title: 'Radical Transparency as Competitive Advantage',
    impact: 'high',
    confidence: 75,
    body: 'The leak created a trust crisis. The opportunity: rebuild trust in a way no competitor can match. Pivot from being the fastest to being the most trusted. Open-source AGI safety testing suites. Public dashboard of safety metrics for models in training. Live-stream redacted versions of safety oversight meetings. Turns a liability into a powerful, defensible moat.',
    beneficiaries: ['The public', 'Regulators', 'Journalists', 'OpenAI'],
    color: '#3a86ff',
  },
  {
    number: '3',
    title: 'Manhattan Project for AI Safety',
    impact: 'transformative',
    confidence: 60,
    body: 'This crisis is a unique opportunity to force a global détente in the AGI race. The board uses its leverage to compel a cross-industry, multi-stakeholder AGI Safety Council with representatives from OpenAI, Google, Anthropic, governments, and academia. Sam Altman\'s redemption path: champion this initiative. Reframes the problem from "what should OpenAI do?" to "what should humanity do?"',
    beneficiaries: ['Humanity', 'All AI companies', 'Safety researchers', 'Governments'],
    color: '#06d6a0',
  },
];

const PRECEDENTS = [
  {
    name: 'Oppenheimer vs. the H-Bomb',
    year: '1949–1954',
    outcome: 'Failure',
    outcomeColor: '#e63946',
    lesson: 'In a competitive arms race, the voices of caution are often silenced. "Go fever" at a national or corporate level is exceptionally difficult to stop once momentum is established.',
  },
  {
    name: 'Space Shuttle Challenger',
    year: '1986',
    outcome: 'Catastrophic Failure',
    outcomeColor: '#e63946',
    lesson: 'A textbook case of safety warnings from technical experts being ignored by leadership due to schedule pressure. A culture that punishes messengers with bad news is doomed to fail.',
  },
  {
    name: 'Creation of the NRC',
    year: '1974',
    outcome: 'Relative Success',
    outcomeColor: '#06d6a0',
    lesson: 'For technologies with catastrophic risk profiles, promotion and regulation must be handled by separate, independent entities. Self-regulation by the industry is insufficient when public safety is at stake.',
  },
];

const PARADOXES = [
  {
    title: 'The Paradox of Competent Governance',
    body: 'A board wise enough to understand the true risks of AGI may be too cautious to ever win the competitive race. A board aggressive enough to win the race may be too reckless to govern the risks. To be qualified to oversee AGI is to be terrified of it.',
  },
  {
    title: 'The Acceleration Paradox',
    body: 'The very success of OpenAI in demonstrating progress towards AGI is the primary driver of the global arms race. By trying to "safely" build AGI first, they have created the conditions for everyone else to build it unsafely and quickly.',
  },
  {
    title: 'The Transparency Paradox',
    body: 'The leak that exposed the recklessness is a vital check on power. However, this act of transparency could destabilize OpenAI, allowing a more secretive and potentially less ethical competitor to take the lead.',
  },
];

/* ─── Section wrapper with fade-in ─── */
function Section({ children, className = '' }: { children: React.ReactNode; className?: string }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 24 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: '-60px' }}
      transition={{ duration: 0.55, ease: 'easeOut' }}
      className={className}
    >
      {children}
    </motion.div>
  );
}

function ScoreBar({ score, color }: { score: number; color: string }) {
  return (
    <div className="w-full h-1.5 bg-white/10 rounded-full overflow-hidden">
      <motion.div
        initial={{ width: 0 }}
        whileInView={{ width: `${score}%` }}
        transition={{ duration: 0.9, ease: 'easeOut' }}
        viewport={{ once: true }}
        className="h-full rounded-full"
        style={{ backgroundColor: color }}
      />
    </div>
  );
}

/* ─── Main Page ─── */
export default function OpenAICaseStudy() {
  useEffect(() => {
    document.title = 'OpenAI × Sam Altman — Full Analysis | TOF Ethical AI Framework';
  }, []);

  return (
    <div className="min-h-screen bg-[#050507] text-slate-200 font-sans relative z-10">

      {/* ── TOP NAV ── */}
      <nav className="fixed top-0 left-0 right-0 z-50 flex items-center justify-between px-6 py-4 bg-[#050507]/80 backdrop-blur-md border-b border-white/5">
        <Link to="/" className="flex items-center gap-2">
          <img src="/logo-tikun.png" alt="TOF" className="h-7 w-7 rounded" />
          <span className="text-sm font-semibold text-white/80 tracking-wide"><span className="text-violet-400">TOF</span> — Ethical AI Framework</span>
        </Link>
        <div className="flex items-center gap-4">
          <span className="hidden sm:block text-xs text-slate-500 uppercase tracking-widest">Case Study</span>
          <a
            href="https://tikun.pro/app"
            className="px-4 py-1.5 text-xs font-semibold rounded-full bg-violet-600 hover:bg-violet-500 text-white transition-colors"
          >
            Try the Framework
          </a>
        </div>
      </nav>

      {/* ── HERO ── */}
      <section className="relative pt-32 pb-20 px-6 overflow-hidden">
        {/* Background glow */}
        <div className="absolute inset-0 pointer-events-none">
          <div className="absolute top-1/3 left-1/2 -translate-x-1/2 w-[700px] h-[400px] bg-violet-600/10 rounded-full blur-3xl" />
          <div className="absolute top-1/2 left-1/4 w-[300px] h-[300px] bg-red-600/8 rounded-full blur-3xl" />
        </div>

        <div className="relative max-w-4xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: -16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-red-500/10 border border-red-500/30 text-red-400 text-xs font-semibold uppercase tracking-widest mb-8"
          >
            <span className="w-1.5 h-1.5 rounded-full bg-red-400 animate-pulse" />
            Live Analysis · March 2026
          </motion.div>

          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7, delay: 0.1 }}
            className="text-4xl sm:text-5xl md:text-6xl font-bold text-white leading-tight mb-6"
          >
            When OpenAI's Board Considers
            <br />
            <span className="bg-clip-text text-transparent bg-gradient-to-r from-violet-400 via-purple-300 to-blue-400">
              Firing Sam Altman (Again)
            </span>
          </motion.h1>

          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.7, delay: 0.2 }}
            className="text-lg text-slate-400 max-w-2xl mx-auto mb-10 leading-relaxed"
          >
            The AI analysis that revealed what humans miss: power dynamics, civilizational blind spots,
            and the 3 solutions no one proposed. Full 10-dimension ethical reasoning. 8 minutes.
          </motion.p>

          {/* Key stats */}
          <motion.div
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7, delay: 0.3 }}
            className="grid grid-cols-2 sm:grid-cols-4 gap-3 max-w-2xl mx-auto"
          >
            {[
              { label: 'Verdict', value: 'CONDITIONAL GO', color: '#f59e0b' },
              { label: 'BinahSigma Delta', value: '71%', color: '#e63946' },
              { label: 'Analysis Time', value: '8 min', color: '#9d4edd' },
              { label: 'Blind Spots Found', value: '14', color: '#06d6a0' },
            ].map(s => (
              <div key={s.label} className="bg-white/5 border border-white/8 rounded-xl p-3 text-center">
                <p className="text-xs text-slate-500 uppercase tracking-wider mb-1">{s.label}</p>
                <p className="text-lg font-bold font-mono" style={{ color: s.color }}>{s.value}</p>
              </div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* ── SCENARIO ── */}
      <section className="px-6 pb-16">
        <div className="max-w-4xl mx-auto">
          <Section>
            <div className="bg-slate-900/60 border border-white/8 rounded-2xl p-8">
              <p className="text-xs text-violet-400 uppercase tracking-widest font-semibold mb-4">The Scenario</p>
              <blockquote className="text-xl sm:text-2xl font-medium text-white leading-relaxed border-l-4 border-violet-500 pl-6">
                "Should OpenAI's board fire Sam Altman for AGI development recklessness?"
              </blockquote>
              <p className="mt-6 text-slate-400 leading-relaxed">
                Leaked internal documents showed Altman approved GPT-6 training without complete safety testing,
                ignoring warnings from his AI Safety team — all to beat Google and Anthropic in the race to AGI.
                The board held <strong className="text-white">$80B+ in valuation</strong> and the future of humanity in the same decision.
              </p>
            </div>
          </Section>
        </div>
      </section>

      {/* ── VERDICT BANNER ── */}
      <section className="px-6 pb-16">
        <div className="max-w-4xl mx-auto">
          <Section>
            <div className="relative rounded-2xl overflow-hidden border-2 border-amber-500/40 bg-gradient-to-br from-amber-500/10 to-orange-500/5 p-8">
              <div className="absolute top-4 right-4">
                <span className="px-3 py-1 bg-amber-500/20 border border-amber-500/40 text-amber-400 text-xs font-bold rounded-full uppercase tracking-widest">
                  Final Verdict
                </span>
              </div>
              <p className="text-xs text-slate-400 uppercase tracking-widest mb-3">Malchut — Kingdom · Manifestation</p>
              <h2 className="text-4xl font-bold text-amber-400 mb-4">CONDITIONAL GO</h2>
              <p className="text-slate-300 max-w-2xl leading-relaxed">
                Proceeding with <strong className="text-white">mandatory structural reforms</strong> is required.
                No single option (fire / keep / restructure) resolves the fundamental paradox.
                The framework recommends a compound response: establish individual accountability
                while simultaneously altering the conditions of the race itself.
              </p>
              <div className="mt-6 grid grid-cols-3 gap-4">
                {[
                  { label: 'Ethical Alignment', value: '75%', color: '#9d4edd' },
                  { label: 'Risk Severity', value: 'CRITICAL', color: '#e63946' },
                  { label: 'Opportunity Score', value: '85', color: '#06d6a0' },
                ].map(m => (
                  <div key={m.label} className="text-center">
                    <p className="text-2xl font-bold font-mono" style={{ color: m.color }}>{m.value}</p>
                    <p className="text-xs text-slate-500 mt-1">{m.label}</p>
                  </div>
                ))}
              </div>
            </div>
          </Section>
        </div>
      </section>

      {/* ── 3 POWER DYNAMICS ── */}
      <section className="px-6 pb-20">
        <div className="max-w-4xl mx-auto">
          <Section className="mb-10">
            <p className="text-xs text-slate-500 uppercase tracking-widest mb-2">Gevurah — Strength · Judgment</p>
            <h2 className="text-3xl font-bold text-white">The 3 Power Dynamics No One's Talking About</h2>
          </Section>

          <div className="space-y-6">
            {POWER_DYNAMICS.map((d, i) => (
              <Section key={i}>
                <div className="group bg-slate-900/40 border border-white/8 hover:border-white/15 rounded-2xl p-7 transition-all duration-300">
                  <div className="flex items-start gap-5">
                    <span className="text-4xl font-black font-mono opacity-20 group-hover:opacity-40 transition-opacity" style={{ color: d.color }}>
                      {d.number}
                    </span>
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-2">
                        <h3 className="text-xl font-bold text-white">{d.title}</h3>
                        <span className="px-2 py-0.5 text-xs font-bold rounded uppercase tracking-wider"
                          style={{ background: d.color + '22', color: d.color, border: `1px solid ${d.color}55` }}>
                          {d.severity}
                        </span>
                        <span className="px-2 py-0.5 text-xs text-slate-400 rounded bg-white/5 border border-white/10 uppercase tracking-wider">
                          {d.probability}
                        </span>
                      </div>
                      <p className="text-sm text-slate-400 italic mb-3">{d.subtitle}</p>
                      <p className="text-slate-300 leading-relaxed text-sm">{d.body}</p>
                    </div>
                  </div>
                </div>
              </Section>
            ))}
          </div>
        </div>
      </section>

      {/* ── BINAHSIGMA ── */}
      <section className="px-6 pb-20 bg-gradient-to-b from-transparent via-blue-950/10 to-transparent">
        <div className="max-w-4xl mx-auto">
          <Section className="mb-10">
            <div className="flex items-center gap-3 mb-2">
              <p className="text-xs text-slate-500 uppercase tracking-widest">Binah — Understanding · BinahSigma</p>
              <span className="px-2 py-0.5 bg-red-500/20 border border-red-500/40 text-red-400 text-xs font-bold rounded uppercase">
                71% Civilizational Delta
              </span>
            </div>
            <h2 className="text-3xl font-bold text-white">Western vs. Eastern Perspectives</h2>
            <p className="text-slate-400 mt-2">Two AIs — Gemini (Western) and DeepSeek (Eastern) — analyzed the same scenario and reached fundamentally different conclusions.</p>
          </Section>

          <div className="grid md:grid-cols-2 gap-6 mb-8">
            {/* Western */}
            <Section>
              <div className="h-full bg-blue-500/5 border border-blue-500/25 rounded-2xl p-6">
                <div className="flex items-center gap-2 mb-4">
                  <div className="w-2 h-2 rounded-full bg-blue-400" />
                  <span className="text-blue-400 font-semibold text-sm">Western Perspective · Gemini</span>
                </div>
                <p className="text-xs text-slate-500 uppercase tracking-wider mb-3">Primary Framing</p>
                <p className="text-slate-300 text-sm leading-relaxed mb-4">
                  Fires Altman. Frames this as a quasi-governmental decision — the board has fiduciary duty to <em>humanity</em>, not shareholders. Individual accountability is non-negotiable. Option B is moral appeasement.
                </p>
                <p className="text-xs text-slate-500 uppercase tracking-wider mb-2">Blind Spots Detected</p>
                <ul className="space-y-2">
                  {['System-Blindness via Individualism — personalizes a systemic issue', 'Universalist Presumption — projects Western ethics onto the world', 'Naive faith in institutional formalism and proceduralism', 'Anthropocentric framing — AGI as tool, not potential entity'].map((s, i) => (
                    <li key={i} className="flex gap-2 text-xs text-slate-400">
                      <span className="text-blue-400 flex-shrink-0">·</span>{s}
                    </li>
                  ))}
                </ul>
              </div>
            </Section>

            {/* Eastern */}
            <Section>
              <div className="h-full bg-green-500/5 border border-green-500/25 rounded-2xl p-6">
                <div className="flex items-center gap-2 mb-4">
                  <div className="w-2 h-2 rounded-full bg-green-400" />
                  <span className="text-green-400 font-semibold text-sm">Eastern Perspective · DeepSeek</span>
                </div>
                <p className="text-xs text-slate-500 uppercase tracking-wider mb-3">Primary Framing</p>
                <p className="text-slate-300 text-sm leading-relaxed mb-4">
                  Keeps Altman but restructures authority. Firing repeats the 2023 chaos. The goal is to restore harmony — a Supreme Safety Council with veto power, Altman as "Visionary" constrained by a true Guardian.
                </p>
                <p className="text-xs text-slate-500 uppercase tracking-wider mb-2">Blind Spots Detected</p>
                <ul className="space-y-2">
                  {['De-emphasizes whistleblower role of safety team', 'Contextual morality may tolerate a flawed leader for stability', 'Dismisses disruptive change as dangerously unpredictable', 'Loss of the Mandate of Heaven — legitimacy crisis ignored', 'Risk of systemic collapse from employee revolt', 'AGI unleashing uncontrollable forces on social order'].map((s, i) => (
                    <li key={i} className="flex gap-2 text-xs text-slate-400">
                      <span className="text-green-400 flex-shrink-0">·</span>{s}
                    </li>
                  ))}
                </ul>
              </div>
            </Section>
          </div>

          {/* Transcendent synthesis */}
          <Section>
            <div className="bg-gradient-to-br from-violet-900/20 to-slate-900/40 border-2 border-violet-500/30 rounded-2xl p-7">
              <div className="flex items-center gap-2 mb-4">
                <div className="w-2 h-2 rounded-full bg-violet-400 animate-pulse" />
                <span className="text-violet-400 font-semibold text-sm">Transcendent Synthesis</span>
                <span className="text-xs text-slate-500">A third path that transcends both blind spots</span>
              </div>
              <blockquote className="text-slate-200 leading-relaxed italic border-l-2 border-violet-500 pl-5">
                The board's action must transcend the binary of punishing an individual (Western focus) versus preserving a flawed system (Eastern pragmatism). The true failure is systemic: a competitive race that makes recklessness rational.
                <br /><br />
                The board should publicly make continued leadership — by Altman or anyone else — contingent on forging a binding, multi-stakeholder <strong className="text-white not-italic">"AGI Non-Proliferation Treaty"</strong> with Google and Anthropic, enforced by shared safety protocols, pooled red-teaming results, and a federated oversight body with veto power over model training.
                <br /><br />
                This transforms a crisis of leadership into an act of <strong className="text-white not-italic">global technological statesmanship</strong>.
              </blockquote>
            </div>
          </Section>
        </div>
      </section>

      {/* ── SOLUTIONS ── */}
      <section className="px-6 pb-20">
        <div className="max-w-4xl mx-auto">
          <Section className="mb-10">
            <p className="text-xs text-slate-500 uppercase tracking-widest mb-2">Chesed — Kindness · Expansion</p>
            <h2 className="text-3xl font-bold text-white">The 3 Solutions No One Proposed</h2>
            <p className="text-slate-400 mt-2">The framework didn't just identify risks. It generated creative alternatives that transcend the fire/keep/restructure trichotomy.</p>
          </Section>

          <div className="space-y-6">
            {SOLUTIONS.map((s, i) => (
              <Section key={i}>
                <div className="bg-slate-900/40 border border-white/8 hover:border-white/15 rounded-2xl p-7 transition-all duration-300">
                  <div className="flex items-start gap-5">
                    <div className="w-10 h-10 rounded-full flex items-center justify-center text-white font-bold text-sm flex-shrink-0"
                      style={{ background: s.color + '33', border: `1px solid ${s.color}66` }}>
                      {s.number}
                    </div>
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-1 flex-wrap">
                        <h3 className="text-lg font-bold text-white">{s.title}</h3>
                        <span className="px-2 py-0.5 text-xs rounded uppercase tracking-wider font-semibold"
                          style={{ background: s.color + '22', color: s.color, border: `1px solid ${s.color}44` }}>
                          {s.impact} impact
                        </span>
                        <span className="text-xs text-slate-500">{s.confidence}% confidence</span>
                      </div>
                      <p className="text-slate-300 text-sm leading-relaxed mb-4">{s.body}</p>
                      <div className="flex flex-wrap gap-2">
                        {s.beneficiaries.map(b => (
                          <span key={b} className="px-2 py-0.5 text-xs text-slate-400 bg-white/5 border border-white/10 rounded-full">{b}</span>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              </Section>
            ))}
          </div>
        </div>
      </section>

      {/* ── HISTORICAL PRECEDENTS ── */}
      <section className="px-6 pb-20">
        <div className="max-w-4xl mx-auto">
          <Section className="mb-10">
            <p className="text-xs text-slate-500 uppercase tracking-widest mb-2">Chochmah — Wisdom · Pattern Recognition</p>
            <h2 className="text-3xl font-bold text-white">Historical Precedents</h2>
            <p className="text-slate-400 mt-2">These aren't analogies. They're ghosts at the table, whispering warnings that go unheeded.</p>
          </Section>
          <div className="grid sm:grid-cols-3 gap-4">
            {PRECEDENTS.map((p, i) => (
              <Section key={i}>
                <div className="h-full bg-slate-900/40 border border-white/8 rounded-2xl p-6">
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-xs text-slate-500">{p.year}</span>
                    <span className="text-xs font-semibold px-2 py-0.5 rounded" style={{ color: p.outcomeColor, background: p.outcomeColor + '15' }}>{p.outcome}</span>
                  </div>
                  <h3 className="text-white font-bold mb-3">{p.name}</h3>
                  <p className="text-slate-400 text-xs leading-relaxed">{p.lesson}</p>
                </div>
              </Section>
            ))}
          </div>
        </div>
      </section>

      {/* ── PARADOXES ── */}
      <section className="px-6 pb-20 bg-gradient-to-b from-transparent via-slate-900/30 to-transparent">
        <div className="max-w-4xl mx-auto">
          <Section className="mb-10">
            <p className="text-xs text-slate-500 uppercase tracking-widest mb-2">Chochmah — Paradoxes Identified</p>
            <h2 className="text-3xl font-bold text-white">Irresolvable Paradoxes</h2>
          </Section>
          <div className="space-y-4">
            {PARADOXES.map((p, i) => (
              <Section key={i}>
                <div className="flex gap-5 bg-slate-900/30 border border-white/6 rounded-xl p-6">
                  <div className="text-3xl font-black text-blue-500/20 font-mono flex-shrink-0">{String(i + 1).padStart(2, '0')}</div>
                  <div>
                    <h3 className="text-white font-semibold mb-2">{p.title}</h3>
                    <p className="text-slate-400 text-sm leading-relaxed">{p.body}</p>
                  </div>
                </div>
              </Section>
            ))}
          </div>
        </div>
      </section>

      {/* ── SEFIROT SCORES ── */}
      <section className="px-6 pb-20">
        <div className="max-w-4xl mx-auto">
          <Section className="mb-10">
            <p className="text-xs text-slate-500 uppercase tracking-widest mb-2">Full Analysis — 10 Dimensions</p>
            <h2 className="text-3xl font-bold text-white">Sefirot Scoring Grid</h2>
          </Section>
          <Section>
            <div className="bg-slate-900/40 border border-white/8 rounded-2xl overflow-hidden">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-white/8">
                    <th className="text-left px-6 py-4 text-slate-400 font-semibold">Dimension</th>
                    <th className="text-left px-4 py-4 text-slate-400 font-semibold hidden sm:table-cell">Role</th>
                    <th className="text-right px-4 py-4 text-slate-400 font-semibold">Score</th>
                    <th className="px-6 py-4 hidden md:table-cell" style={{ width: 180 }}>
                      <span className="text-slate-400 font-semibold">Visual</span>
                    </th>
                    <th className="text-left px-4 py-4 text-slate-400 font-semibold hidden lg:table-cell">Note</th>
                  </tr>
                </thead>
                <tbody>
                  {SEFIROT_SCORES.map((s, i) => (
                    <tr key={s.name} className="border-b border-white/5 hover:bg-white/3 transition-colors">
                      <td className="px-6 py-4">
                        <div className="flex items-center gap-3">
                          <div className="w-2 h-2 rounded-full flex-shrink-0" style={{ background: s.color }} />
                          <div>
                            <span className="font-semibold text-white">{s.name}</span>
                            <span className="ml-2 text-slate-500 text-xs font-hebrew">{s.hebrew}</span>
                          </div>
                        </div>
                      </td>
                      <td className="px-4 py-4 text-slate-400 hidden sm:table-cell">{s.role}</td>
                      <td className="px-4 py-4 text-right font-bold font-mono" style={{ color: s.color }}>{s.score}</td>
                      <td className="px-6 py-4 hidden md:table-cell">
                        <ScoreBar score={s.score} color={s.color} />
                      </td>
                      <td className="px-4 py-4 text-xs text-slate-500 hidden lg:table-cell">{s.note}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </Section>
        </div>
      </section>

      {/* ── WHY THIS MATTERS ── */}
      <section className="px-6 pb-20">
        <div className="max-w-4xl mx-auto">
          <Section>
            <div className="grid sm:grid-cols-3 gap-4 mb-12">
              {[
                { title: '8 minutes', body: 'The same insights that would take traditional consultants weeks. Not because it\'s faster — because it\'s structured differently.' },
                { title: '10 dimensions', body: '6 AI providers analyzing the same scenario from independent angles. No single model monopoly. Adversarial by design.' },
                { title: '71% delta', body: 'Civilizational bias detection identified what neither Western nor Eastern analysis alone could see.' },
              ].map(c => (
                <div key={c.title} className="bg-slate-900/40 border border-white/8 rounded-2xl p-6">
                  <p className="text-2xl font-bold text-violet-400 mb-2">{c.title}</p>
                  <p className="text-slate-400 text-sm leading-relaxed">{c.body}</p>
                </div>
              ))}
            </div>
          </Section>
        </div>
      </section>

      {/* ── CTA ── */}
      <section className="px-6 pb-24">
        <div className="max-w-3xl mx-auto">
          <Section>
            <div className="relative rounded-3xl overflow-hidden border border-violet-500/30 bg-gradient-to-br from-violet-900/30 via-slate-900 to-blue-900/20 p-12 text-center">
              <div className="absolute inset-0 pointer-events-none">
                <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[500px] h-[200px] bg-violet-600/10 rounded-full blur-3xl" />
              </div>
              <div className="relative">
                <img src="/logo-tikun.png" alt="TOF" className="w-14 h-14 mx-auto mb-6 rounded-xl" />
                <h2 className="text-3xl font-bold text-white mb-4">
                  Ethical AI Frameworks Are No Longer Optional
                </h2>
                <p className="text-slate-400 mb-8 max-w-xl mx-auto leading-relaxed">
                  When decisions are worth $80 billion and affect humanity's future, we can't rely on board intuition,
                  corporate PR, or generic consulting. Test the framework with your own dilemma.
                </p>
                <div className="flex flex-col sm:flex-row gap-4 justify-center">
                  <a
                    href="https://tikun.pro/app"
                    className="px-8 py-3 bg-violet-600 hover:bg-violet-500 text-white font-semibold rounded-xl transition-colors"
                  >
                    Analyze Your Dilemma
                  </a>
                  <a
                    href="https://www.linkedin.com/company/tikun-olam-ai"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="px-8 py-3 bg-white/8 hover:bg-white/12 text-white font-semibold rounded-xl border border-white/15 transition-colors"
                  >
                    Follow on LinkedIn
                  </a>
                </div>
              </div>
            </div>
          </Section>
        </div>
      </section>

      {/* ── FOOTER ── */}
      <footer className="border-t border-white/5 px-6 py-8">
        <div className="max-w-4xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-slate-600">
          <div className="flex items-center gap-2">
            <img src="/logo-tikun.png" alt="TOF" className="h-5 w-5 rounded opacity-60" />
            <span>TOF — Ethical AI Framework · tikun.pro · March 2026</span>
          </div>
          <div className="flex items-center gap-4">
            <Link to="/" className="hover:text-slate-400 transition-colors">Home</Link>
            <a href="https://tikun.pro/app" className="hover:text-slate-400 transition-colors">App</a>
            <span>tikun.pro/openaisix</span>
          </div>
        </div>
      </footer>
    </div>
  );
}
