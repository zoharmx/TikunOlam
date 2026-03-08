import { useEffect, useState } from 'react';
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

/* ─── Section wrapper — content always visible, subtle y-slide on enter ─── */
function Section({ children, className = '' }: { children: React.ReactNode; className?: string }) {
  return (
    <motion.div
      initial={{ y: 16 }}
      whileInView={{ y: 0 }}
      viewport={{ once: true, amount: 0.05 }}
      transition={{ duration: 0.5, ease: 'easeOut' }}
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

/* ─── PDF Report generator — popup window approach (most reliable cross-browser) ─── */
function generateReportHTML(caseName: string): string {
  const date = new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
  const risksHTML = POWER_DYNAMICS.map(d => `
    <div class="risk-card">
      <div class="risk-header">
        <span class="risk-num">${d.number}</span>
        <div>
          <strong>${d.title}</strong>
          <span class="badge badge-${d.severity}">${d.severity}</span>
          <span class="badge badge-neutral">${d.probability}</span>
        </div>
      </div>
      <p class="body-text">${d.body}</p>
    </div>`).join('');

  const solsHTML = SOLUTIONS.map(s => `
    <div class="sol-card">
      <div class="sol-header">
        <span class="sol-num">${s.number}</span>
        <div>
          <strong>${s.title}</strong>
          <span class="badge badge-purple">${s.impact} impact · ${s.confidence}% confidence</span>
        </div>
      </div>
      <p class="body-text">${s.body}</p>
      <div class="tags">${s.beneficiaries.map(b => `<span class="tag">${b}</span>`).join('')}</div>
    </div>`).join('');

  const scoresHTML = SEFIROT_SCORES.map(s => `
    <div class="score-row">
      <span class="score-dot" style="background:${s.color}"></span>
      <span class="score-name">${s.name} <small>${s.hebrew}</small></span>
      <span class="score-role">${s.role}</span>
      <strong class="score-val" style="color:${s.color}">${s.score}</strong>
      <div class="score-bar-bg"><div class="score-bar-fill" style="width:${s.score}%;background:${s.color}"></div></div>
    </div>`).join('');

  const precsHTML = PRECEDENTS.map(p => `
    <div class="prec-card">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px">
        <strong>${p.name}</strong>
        <span style="font-size:11px;color:${p.outcomeColor};font-weight:700">${p.outcome} · ${p.year}</span>
      </div>
      <p class="body-text">${p.lesson}</p>
    </div>`).join('');

  return `<!DOCTYPE html><html lang="en"><head>
<meta charset="UTF-8">
<title>${caseName} — Tikun Olam Report</title>
<style>
  *{box-sizing:border-box;margin:0;padding:0}
  body{font-family:'Georgia',serif;color:#1a1a2e;background:#fff;font-size:13px;line-height:1.6}
  @page{size:A4 portrait;margin:16mm 14mm}
  @media print{body{-webkit-print-color-adjust:exact;print-color-adjust:exact}}

  /* ── Layout ── */
  .page{max-width:780px;margin:0 auto;padding:24px 32px}
  .section{margin-bottom:28px}
  .two-col{display:grid;grid-template-columns:1fr 1fr;gap:16px}

  /* ── Header ── */
  .header{display:flex;justify-content:space-between;align-items:flex-start;
    padding-bottom:16px;border-bottom:3px solid #7c3aed;margin-bottom:28px}
  .header-left .tag{display:inline-block;background:#fef3c7;border:1px solid #f59e0b;
    color:#92400e;font-size:10px;font-weight:700;padding:3px 10px;border-radius:20px;
    text-transform:uppercase;letter-spacing:.8px;margin-bottom:8px}
  .header-left h1{font-size:22px;color:#1a1a2e;line-height:1.2;margin-bottom:4px}
  .header-left .sub{font-size:12px;color:#64748b}
  .header-right{text-align:right;font-size:11px;color:#64748b}
  .header-right .logo{font-size:14px;font-weight:700;color:#7c3aed;margin-bottom:4px}

  /* ── Verdict ── */
  .verdict-box{background:linear-gradient(135deg,#fef3c7,#fde68a22);
    border:2px solid #f59e0b;border-radius:10px;padding:20px 24px;margin-bottom:28px}
  .verdict-label{font-size:11px;color:#92400e;text-transform:uppercase;
    letter-spacing:1px;font-weight:700;margin-bottom:4px}
  .verdict-value{font-size:32px;font-weight:900;color:#b45309;font-family:monospace;
    letter-spacing:2px}
  .verdict-meta{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:16px}
  .verdict-stat{text-align:center;background:#fff;border-radius:8px;padding:10px}
  .verdict-stat .v{font-size:20px;font-weight:700;font-family:monospace}
  .verdict-stat .l{font-size:10px;color:#64748b;text-transform:uppercase;margin-top:2px}

  /* ── Section headers ── */
  .sec-title{font-size:15px;font-weight:700;color:#7c3aed;
    border-bottom:2px solid #ede9fe;padding-bottom:6px;margin-bottom:14px;
    display:flex;align-items:center;gap:8px}
  .sec-sub{font-size:10px;color:#94a3b8;text-transform:uppercase;
    letter-spacing:.8px;margin-bottom:14px}

  /* ── Risk cards ── */
  .risk-card{border-left:4px solid #ef4444;background:#fef2f2;
    border-radius:0 8px 8px 0;padding:12px 16px;margin-bottom:10px}
  .risk-header{display:flex;align-items:flex-start;gap:10px;margin-bottom:6px}
  .risk-num{font-size:20px;font-weight:900;color:#ef444433;font-family:monospace;min-width:28px}

  /* ── Solution cards ── */
  .sol-card{border:1px solid #e2e8f0;border-radius:8px;padding:14px 16px;margin-bottom:10px}
  .sol-header{display:flex;align-items:flex-start;gap:10px;margin-bottom:6px}
  .sol-num{width:28px;height:28px;border-radius:50%;background:#7c3aed22;border:1px solid #7c3aed66;
    display:flex;align-items:center;justify-content:center;font-weight:700;
    color:#7c3aed;font-size:13px;flex-shrink:0}

  /* ── Badges ── */
  .badge{font-size:10px;font-weight:700;padding:2px 8px;border-radius:4px;
    text-transform:uppercase;letter-spacing:.5px;margin-left:6px}
  .badge-critical{background:#fee2e2;color:#991b1b}
  .badge-high{background:#fef3c7;color:#92400e}
  .badge-neutral{background:#f1f5f9;color:#475569}
  .badge-purple{background:#ede9fe;color:#6d28d9}

  /* ── Tags ── */
  .tags{display:flex;flex-wrap:wrap;gap:6px;margin-top:8px}
  .tag{font-size:10px;background:#f1f5f9;color:#64748b;
    border:1px solid #e2e8f0;border-radius:20px;padding:2px 8px}

  /* ── BinahSigma ── */
  .binah-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:14px}
  .binah-west{background:#eff6ff;border:1px solid #bfdbfe;border-radius:8px;padding:14px}
  .binah-east{background:#f0fdf4;border:1px solid #bbf7d0;border-radius:8px;padding:14px}
  .binah-label{font-size:10px;font-weight:700;text-transform:uppercase;
    letter-spacing:.8px;margin-bottom:8px}
  .binah-west .binah-label{color:#1d4ed8}
  .binah-east .binah-label{color:#15803d}
  .synthesis-box{background:linear-gradient(135deg,#f5f3ff,#ede9fe22);
    border:1px solid #c4b5fd;border-radius:8px;padding:14px;font-style:italic;
    color:#4c1d95;line-height:1.7}

  /* ── Scores ── */
  .score-row{display:grid;grid-template-columns:12px 90px 1fr 36px 120px;
    align-items:center;gap:8px;padding:5px 0;border-bottom:1px solid #f1f5f9}
  .score-dot{width:10px;height:10px;border-radius:50%;flex-shrink:0}
  .score-name{font-weight:600;font-size:12px} .score-name small{color:#94a3b8;margin-left:4px}
  .score-role{font-size:11px;color:#64748b}
  .score-val{font-family:monospace;font-size:14px}
  .score-bar-bg{height:4px;background:#f1f5f9;border-radius:2px;overflow:hidden}
  .score-bar-fill{height:100%;border-radius:2px}

  /* ── Precedents ── */
  .prec-card{border:1px solid #e2e8f0;border-radius:8px;padding:12px;margin-bottom:8px}

  /* ── Footer ── */
  .footer{margin-top:32px;padding-top:12px;border-top:2px solid #ede9fe;
    display:flex;justify-content:space-between;align-items:center;font-size:10px;color:#94a3b8}
  .footer strong{color:#7c3aed}

  .body-text{font-size:12px;color:#374151;line-height:1.6}
  blockquote{border-left:3px solid #7c3aed;padding-left:14px;color:#4c1d95;
    font-style:italic;line-height:1.7;font-size:12px}
</style></head><body><div class="page">

  <!-- HEADER -->
  <div class="header">
    <div class="header-left">
      <div class="tag">Live Analysis · March 2026</div>
      <h1>When OpenAI's Board Considers<br>Firing Sam Altman (Again)</h1>
      <div class="sub">Case Study · Tikun Olam Ethical AI Framework · ${date}</div>
    </div>
    <div class="header-right">
      <div class="logo">Tikun Olam</div>
      <div>Ethical AI Framework</div>
      <div style="margin-top:6px;color:#94a3b8">tikun.pro/openaisix</div>
    </div>
  </div>

  <!-- VERDICT -->
  <div class="verdict-box">
    <div class="verdict-label">Malchut — Kingdom · Final Verdict</div>
    <div class="verdict-value">CONDITIONAL GO</div>
    <div class="verdict-meta">
      <div class="verdict-stat"><div class="v" style="color:#b45309">75%</div><div class="l">Ethical Alignment</div></div>
      <div class="verdict-stat"><div class="v" style="color:#ef4444">71%</div><div class="l">BinahSigma Δ</div></div>
      <div class="verdict-stat"><div class="v" style="color:#7c3aed">~8 min</div><div class="l">Analysis Time</div></div>
    </div>
  </div>

  <!-- SCENARIO -->
  <div class="section">
    <div class="sec-title">The Scenario</div>
    <blockquote>"Should OpenAI's board fire Sam Altman for AGI development recklessness?"</blockquote>
    <p class="body-text" style="margin-top:10px">Leaked internal documents showed Altman approved GPT-6 training without complete safety testing,
    ignoring warnings from the AI Safety team — all to beat Google and Anthropic in the race to AGI.
    The board held <strong>$80B+ in valuation</strong> and the future of humanity in the same decision.</p>
  </div>

  <!-- POWER DYNAMICS -->
  <div class="section">
    <div class="sec-title">Gevurah — The 3 Power Dynamics No One's Talking About</div>
    ${risksHTML}
  </div>

  <!-- BINAHSIGMA -->
  <div class="section">
    <div class="sec-title">Binah — BinahSigma: Western vs. Eastern Perspectives</div>
    <div class="sec-sub">71% civilizational divergence detected · Gemini (Western) vs DeepSeek (Eastern)</div>
    <div class="binah-grid">
      <div class="binah-west">
        <div class="binah-label">Western · Gemini</div>
        <p class="body-text">Fires Altman. Frames this as a quasi-governmental decision —
        individual accountability is non-negotiable. The board has fiduciary duty to <em>humanity</em>, not shareholders.</p>
        <div class="tags" style="margin-top:8px">
          ${['System-blindness via individualism','Universalist presumption','Naive institutional faith','Anthropocentric framing'].map(b => `<span class="tag">${b}</span>`).join('')}
        </div>
      </div>
      <div class="binah-east">
        <div class="binah-label">Eastern · DeepSeek</div>
        <p class="body-text">Keeps Altman but restructures authority. Firing repeats 2023 chaos.
        The goal is harmony — a Supreme Safety Council with veto power, Altman as constrained "Visionary."</p>
        <div class="tags" style="margin-top:8px">
          ${['De-emphasizes whistleblower role','Contextual morality','Dismisses disruptive change','Legitimacy crisis ignored'].map(b => `<span class="tag">${b}</span>`).join('')}
        </div>
      </div>
    </div>
    <div class="synthesis-box">
      <strong style="color:#6d28d9;font-style:normal">Transcendent Synthesis — </strong>
      The board's action must transcend the binary of punishing an individual (Western) versus preserving a flawed system (Eastern).
      The true failure is systemic. Continued leadership should be contingent on forging a binding, multi-stakeholder
      "AGI Non-Proliferation Treaty" with Google and Anthropic. This transforms a crisis of leadership into
      an act of <strong style="font-style:normal">global technological statesmanship</strong>.
    </div>
  </div>

  <!-- SOLUTIONS -->
  <div class="section">
    <div class="sec-title">Chesed — The 3 Solutions No One Proposed</div>
    ${solsHTML}
  </div>

  <!-- SEFIROT SCORES -->
  <div class="section">
    <div class="sec-title">Full Analysis — 10-Dimension Sefirot Scoring Grid</div>
    ${scoresHTML}
  </div>

  <!-- PRECEDENTS -->
  <div class="section">
    <div class="sec-title">Chochmah — Historical Precedents</div>
    <div class="two-col">${precsHTML}</div>
  </div>

  <!-- FOOTER -->
  <div class="footer">
    <div><strong>Tikun Olam</strong> — Ethical AI Framework · tikun.pro · 6 AI Providers · 10 Reasoning Stages</div>
    <div>CONFIDENTIAL — ${date}</div>
  </div>

</div></body></html>`;
}

/* ─── Main Page ─── */
export default function OpenAICaseStudy() {
  const [pdfLoading, setPdfLoading] = useState(false);

  useEffect(() => {
    document.title = 'OpenAI × Sam Altman — Full Analysis | Tikun Olam';
  }, []);

  const handleDownloadReport = () => {
    setPdfLoading(true);
    try {
      const html = generateReportHTML('OpenAI × Sam Altman');
      const printWindow = window.open('', '_blank', 'width=900,height=700');
      if (!printWindow) {
        alert('Allow pop-ups to download the report.');
        return;
      }
      printWindow.document.write(html);
      printWindow.document.close();
      printWindow.focus();
      setTimeout(() => {
        printWindow.print();
        setPdfLoading(false);
      }, 800);
    } catch {
      setPdfLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#050507] text-slate-200 font-sans relative z-10">

      {/* ── TOP NAV ── */}
      <nav className="fixed top-0 left-0 right-0 z-50 flex items-center justify-between px-6 py-4 bg-[#050507]/80 backdrop-blur-md border-b border-white/5">
        <Link to="/" className="flex items-center gap-2">
          <img src="/logo-tikun.png" alt="Tikun Olam" className="h-7 w-7 rounded" />
          <span className="text-sm font-semibold text-white/80 tracking-wide">Tikun Olam</span>
        </Link>
        <div className="flex items-center gap-3">
          <button
            onClick={handleDownloadReport}
            disabled={pdfLoading}
            className="hidden sm:flex items-center gap-1.5 px-4 py-1.5 text-xs font-semibold rounded-full border border-white/15 bg-white/5 hover:bg-white/10 text-white/80 transition-colors disabled:opacity-50"
          >
            {pdfLoading ? '…' : '↓'} Download Report
          </button>
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
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-red-500/10 border border-red-500/30 text-red-400 text-xs font-semibold uppercase tracking-widest mb-8">
            <span className="w-1.5 h-1.5 rounded-full bg-red-400 animate-pulse" />
            Live Analysis · March 2026
          </div>

          <h1 className="text-4xl sm:text-5xl md:text-6xl font-bold text-white leading-tight mb-6">
            When OpenAI's Board Considers
            <br />
            <span className="bg-clip-text text-transparent bg-gradient-to-r from-violet-400 via-purple-300 to-blue-400">
              Firing Sam Altman (Again)
            </span>
          </h1>

          <p className="text-lg text-slate-400 max-w-2xl mx-auto mb-10 leading-relaxed">
            The AI analysis that revealed what humans miss: power dynamics, civilizational blind spots,
            and the 3 solutions no one proposed. Full 10-dimension ethical reasoning. 8 minutes.
          </p>

          {/* Key stats */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 max-w-2xl mx-auto">
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
          </div>
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
                  {SEFIROT_SCORES.map((s) => (
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
                <img src="/logo-tikun.png" alt="Tikun Olam" className="w-14 h-14 mx-auto mb-6 rounded-xl" />
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
                  <button
                    onClick={handleDownloadReport}
                    disabled={pdfLoading}
                    className="px-8 py-3 bg-white/8 hover:bg-white/12 text-white font-semibold rounded-xl border border-white/15 transition-colors disabled:opacity-50"
                  >
                    {pdfLoading ? 'Generating…' : '↓ Download Full Report PDF'}
                  </button>
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
            <img src="/logo-tikun.png" alt="Tikun Olam" className="h-5 w-5 rounded opacity-60" />
            <span>Tikun Olam — Ethical AI Reasoning Framework · March 2026</span>
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
