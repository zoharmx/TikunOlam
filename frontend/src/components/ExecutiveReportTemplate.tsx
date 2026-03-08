import { forwardRef, useMemo } from 'react';
import type { AnalysisResponse } from '../types';
import { calculateERI, getERILabel } from '../utils/ethicalRiskIndex';
import { INDUSTRY_BENCHMARKS } from '../data/benchmarks';

interface Props {
  analysis: AnalysisResponse;
  industry?: string;
}

const DECISION_COLORS: Record<string, string> = {
  GO: '#10b981',
  NO_GO: '#ef4444',
  CONDITIONAL_GO: '#f59e0b',
};

export const ExecutiveReportTemplate = forwardRef<HTMLDivElement, Props>(
  ({ analysis, industry }, ref) => {
    const { sefirot_results: s, summary, metadata, case_name } = analysis;
    const eri = useMemo(() => calculateERI(s), [s]);
    const benchmark = industry ? INDUSTRY_BENCHMARKS[industry] : null;
    const date = new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
    const decision = s.malchut?.decision || summary?.final_decision || 'PENDING';
    const decisionColor = DECISION_COLORS[decision] ?? '#6b7280';

    const sefirotScores = [
      { label: 'Keter — Ethical Alignment', score: Number(s.keter?.alignment_percentage ?? 0), weight: '30%' },
      { label: 'Tiferet — Harmony & Balance', score: Number(s.tiferet?.balance_score ?? 0), weight: '20%' },
      { label: 'Yesod — Readiness', score: Number(s.yesod?.readiness_score ?? 0), weight: '20%' },
      { label: 'Chochmah — Confidence', score: Number(s.chochmah?.confidence_level ?? 0), weight: '15%' },
      { label: 'Chesed — Opportunity', score: Number(s.chesed?.opportunity_score ?? 0), weight: '15%' },
      { label: 'Gevurah — Risk (inverted)', score: 100 - Number(s.gevurah?.risk_score ?? 50), weight: '—' },
      { label: 'Netzach — Strategy', score: Number(s.netzach?.strategy_score ?? 0), weight: '—' },
      { label: 'Hod — Communication', score: Number(s.hod?.communication_score ?? 0), weight: '—' },
      { label: 'Malchut — Decisiveness', score: Number(s.malchut?.confidence_level ?? 0), weight: '—' },
      { label: 'Binah — Contextual Depth', score: Number(s.binah?.contextual_depth_score ?? 0), weight: '—' },
    ];

    const risks = s.gevurah?.risks ?? [];
    const opportunities = s.chesed?.opportunities ?? [];
    const actionItems = s.malchut?.action_items ?? [];

    // page styles
    const page: React.CSSProperties = {
      width: '794px',
      minHeight: '1123px',
      padding: '60px',
      background: '#ffffff',
      fontFamily: 'Georgia, "Times New Roman", serif',
      color: '#1a1a2e',
      boxSizing: 'border-box',
      pageBreakAfter: 'always',
      breakAfter: 'page',
      position: 'relative',
      overflow: 'hidden',
    };
    const hr: React.CSSProperties = { border: 'none', borderTop: '1px solid #e2e8f0', margin: '20px 0' };
    const h1: React.CSSProperties = { fontSize: 26, fontWeight: 'bold', margin: 0, color: '#1a1a2e' };
    const h2: React.CSSProperties = { fontSize: 16, fontWeight: 'bold', margin: '0 0 12px', color: '#312e81', borderLeft: '4px solid #7c3aed', paddingLeft: 10 };
    const label: React.CSSProperties = { fontSize: 10, color: '#64748b', textTransform: 'uppercase', letterSpacing: 1, marginBottom: 2 };
    const value: React.CSSProperties = { fontSize: 22, fontWeight: 'bold', color: '#1a1a2e' };
    const metricBox: React.CSSProperties = { textAlign: 'center', padding: '16px', border: '1px solid #e2e8f0', borderRadius: 8, flex: 1 };
    const riskItem: React.CSSProperties = { display: 'flex', alignItems: 'flex-start', gap: 8, marginBottom: 8 };

    return (
      <div ref={ref} style={{ background: '#fff', width: '794px' }}>
        {/* ── PAGE 1: Header + ERI + Decision + Summary ── */}
        <div style={page}>
          {/* Header */}
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 24 }}>
            <div>
              <p style={{ fontSize: 11, color: '#7c3aed', fontFamily: 'sans-serif', margin: '0 0 4px', letterSpacing: 2, textTransform: 'uppercase' }}>
                Tikun Olam — Ethical AI Reasoning
              </p>
              <h1 style={h1}>{case_name || 'Ethical Analysis Report'}</h1>
              <p style={{ fontSize: 12, color: '#64748b', fontFamily: 'sans-serif', margin: '6px 0 0' }}>
                Executive Board Report · {date}
              </p>
            </div>
            <div style={{ textAlign: 'right' }}>
              <div style={{ display: 'inline-block', padding: '8px 18px', borderRadius: 20, background: decisionColor + '22', border: `2px solid ${decisionColor}` }}>
                <span style={{ fontSize: 14, fontWeight: 'bold', color: decisionColor, fontFamily: 'sans-serif', letterSpacing: 1 }}>
                  {decision.replace('_', ' ')}
                </span>
              </div>
              <p style={{ fontSize: 10, color: '#94a3b8', fontFamily: 'sans-serif', margin: '6px 0 0' }}>
                Final Recommendation
              </p>
            </div>
          </div>
          <hr style={hr} />

          {/* Key Metrics Row */}
          <div style={{ display: 'flex', gap: 16, marginBottom: 28 }}>
            <div style={{ ...metricBox, borderColor: eri.hexColor + '44', background: eri.hexColor + '0A' }}>
              <p style={label}>Ethical Risk Index</p>
              <p style={{ ...value, color: eri.hexColor }}>{eri.score}</p>
              <p style={{ fontSize: 11, color: '#64748b', fontFamily: 'sans-serif', margin: '2px 0 0' }}>{getERILabel(eri.score)}</p>
            </div>
            <div style={metricBox}>
              <p style={label}>Ethical Alignment</p>
              <p style={value}>{s.keter?.alignment_percentage ?? '—'}%</p>
              <p style={{ fontSize: 11, color: '#64748b', fontFamily: 'sans-serif', margin: '2px 0 0' }}>Keter Score</p>
            </div>
            <div style={metricBox}>
              <p style={label}>Harmony Score</p>
              <p style={value}>{s.tiferet?.balance_score ?? '—'}</p>
              <p style={{ fontSize: 11, color: '#64748b', fontFamily: 'sans-serif', margin: '2px 0 0' }}>Tiferet</p>
            </div>
            <div style={metricBox}>
              <p style={label}>Readiness</p>
              <p style={value}>{s.yesod?.readiness_score ?? '—'}</p>
              <p style={{ fontSize: 11, color: '#64748b', fontFamily: 'sans-serif', margin: '2px 0 0' }}>Yesod Score</p>
            </div>
          </div>

          {/* Executive Summary */}
          <h2 style={h2}>Executive Summary</h2>
          <p style={{ fontSize: 13, lineHeight: 1.7, color: '#334155', marginBottom: 20 }}>
            {summary?.recommendation || s.malchut?.raw_decision?.slice(0, 500) || 'Analysis completed.'}
          </p>

          {/* Synthesis statement */}
          {s.tiferet?.synthesis && (
            <blockquote style={{ borderLeft: '3px solid #7c3aed', paddingLeft: 16, margin: '0 0 20px', fontStyle: 'italic', color: '#475569', fontSize: 12 }}>
              "{s.tiferet.synthesis}"
            </blockquote>
          )}

          {/* Industry benchmark note */}
          {benchmark && (
            <div style={{ background: '#f8fafc', border: '1px solid #e2e8f0', borderRadius: 8, padding: '12px 16px' }}>
              <p style={{ ...label, marginBottom: 6 }}>Industry Benchmark · {benchmark.label}</p>
              <div style={{ display: 'flex', gap: 24, fontFamily: 'sans-serif' }}>
                <span style={{ fontSize: 12, color: '#475569' }}>Avg ERI: <strong>{benchmark.riskIndex}</strong></span>
                <span style={{ fontSize: 12, color: '#475569' }}>Avg Alignment: <strong>{benchmark.alignment}%</strong></span>
                <span style={{ fontSize: 12, color: eri.score <= benchmark.riskIndex ? '#10b981' : '#ef4444', fontWeight: 'bold' }}>
                  {eri.score <= benchmark.riskIndex ? '▼ Below industry avg (better)' : '▲ Above industry avg (worse)'}
                </span>
              </div>
            </div>
          )}

          {/* Models footer */}
          <div style={{ position: 'absolute', bottom: 40, left: 60, right: 60 }}>
            <hr style={hr} />
            <p style={{ fontSize: 9, color: '#94a3b8', fontFamily: 'sans-serif' }}>
              Models: {Object.entries(metadata?.models_used ?? {}).map(([k, v]) => `${k}: ${v}`).join(' · ')} · Duration: {metadata?.total_duration_seconds?.toFixed(1)}s
            </p>
          </div>
        </div>

        {/* ── PAGE 2: Scoring Table ── */}
        <div style={page}>
          <h2 style={{ ...h2, marginBottom: 20 }}>Quantitative Scoring by Dimension</h2>
          <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 12, fontFamily: 'sans-serif' }}>
            <thead>
              <tr style={{ borderBottom: '2px solid #e2e8f0' }}>
                <th style={{ textAlign: 'left', padding: '8px 0', color: '#475569', fontWeight: 600 }}>Dimension (Sefirah)</th>
                <th style={{ textAlign: 'center', padding: '8px 0', color: '#475569', fontWeight: 600 }}>Weight</th>
                <th style={{ textAlign: 'right', padding: '8px 0', color: '#475569', fontWeight: 600 }}>Score</th>
                <th style={{ textAlign: 'left', padding: '8px 16px', color: '#475569', fontWeight: 600 }}>Visual</th>
                {benchmark && <th style={{ textAlign: 'right', padding: '8px 0', color: '#475569', fontWeight: 600 }}>Benchmark</th>}
              </tr>
            </thead>
            <tbody>
              {sefirotScores.map((row, i) => (
                <tr key={i} style={{ borderBottom: '1px solid #f1f5f9', background: i % 2 === 0 ? '#fafafa' : '#fff' }}>
                  <td style={{ padding: '10px 0', color: '#1e293b' }}>{row.label}</td>
                  <td style={{ textAlign: 'center', padding: '10px 0', color: '#7c3aed', fontWeight: 600 }}>{row.weight}</td>
                  <td style={{ textAlign: 'right', padding: '10px 0', fontWeight: 700, color: row.score >= 70 ? '#10b981' : row.score >= 40 ? '#f59e0b' : '#ef4444' }}>
                    {row.score}
                  </td>
                  <td style={{ padding: '10px 16px' }}>
                    <div style={{ height: 8, background: '#e2e8f0', borderRadius: 4, overflow: 'hidden' }}>
                      <div style={{ height: '100%', width: `${row.score}%`, background: row.score >= 70 ? '#10b981' : row.score >= 40 ? '#f59e0b' : '#ef4444', borderRadius: 4 }} />
                    </div>
                  </td>
                  {benchmark && (
                    <td style={{ textAlign: 'right', padding: '10px 0', color: '#94a3b8' }}>
                      {[benchmark.alignment, benchmark.harmony, benchmark.readiness, benchmark.confidence, benchmark.riskIndex, 55, 65, 68, 70, 70][i] ?? '—'}
                    </td>
                  )}
                </tr>
              ))}
            </tbody>
          </table>

          <div style={{ marginTop: 28, display: 'flex', gap: 16 }}>
            <div style={{ flex: 1, background: '#f0fdf4', border: '1px solid #bbf7d0', borderRadius: 8, padding: 16 }}>
              <p style={{ ...label, color: '#166534' }}>ERI Formula</p>
              <p style={{ fontFamily: 'monospace', fontSize: 11, color: '#166534', lineHeight: 1.8 }}>
                ERI = 100 − (<br />
                &nbsp;&nbsp;Keter × 0.30 +<br />
                &nbsp;&nbsp;Tiferet × 0.20 +<br />
                &nbsp;&nbsp;Yesod × 0.20 +<br />
                &nbsp;&nbsp;Chochmah × 0.15 +<br />
                &nbsp;&nbsp;Chesed × 0.15<br />
                ) = <strong>{eri.score}</strong>
              </p>
            </div>
            <div style={{ flex: 1, background: '#faf5ff', border: '1px solid #e9d5ff', borderRadius: 8, padding: 16 }}>
              <p style={{ ...label, color: '#6b21a8' }}>ERI Interpretation</p>
              <div style={{ fontSize: 11, fontFamily: 'sans-serif', lineHeight: 1.9, color: '#4c1d95' }}>
                <div>0 – 25 &nbsp;→&nbsp; <span style={{ color: '#10b981', fontWeight: 700 }}>Low Risk</span></div>
                <div>26 – 50 →&nbsp; <span style={{ color: '#f59e0b', fontWeight: 700 }}>Moderate Risk</span></div>
                <div>51 – 75 →&nbsp; <span style={{ color: '#f97316', fontWeight: 700 }}>High Risk</span></div>
                <div>76 – 100 →&nbsp; <span style={{ color: '#ef4444', fontWeight: 700 }}>Critical Risk</span></div>
              </div>
              <p style={{ marginTop: 10, fontSize: 12, fontWeight: 700, color: eri.hexColor }}>
                This scenario: {eri.score} — {eri.label}
              </p>
            </div>
          </div>
        </div>

        {/* ── PAGE 3: Risks + Opportunities ── */}
        <div style={page}>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 40 }}>
            {/* Risks */}
            <div>
              <h2 style={h2}>Key Risks (Gevurah)</h2>
              {risks.length === 0 && summary?.key_risks?.map((r, i) => (
                <div key={i} style={riskItem}>
                  <span style={{ color: '#ef4444', fontSize: 14, marginTop: 1 }}>⚠</span>
                  <span style={{ fontSize: 12, color: '#334155', lineHeight: 1.5 }}>{r}</span>
                </div>
              ))}
              {risks.slice(0, 6).map((r: any, i: number) => (
                <div key={i} style={{ ...riskItem, borderBottom: '1px solid #f1f5f9', paddingBottom: 8 }}>
                  <div>
                    <div style={{ display: 'flex', gap: 8, alignItems: 'center', marginBottom: 2 }}>
                      <span style={{ fontSize: 10, background: r.severity === 'critical' ? '#fef2f2' : '#fff7ed', color: r.severity === 'critical' ? '#991b1b' : '#9a3412', padding: '1px 6px', borderRadius: 4, fontFamily: 'sans-serif' }}>
                        {r.severity ?? 'medium'}
                      </span>
                    </div>
                    <p style={{ fontSize: 11, color: '#334155', margin: 0, lineHeight: 1.5 }}>{r.description ?? r}</p>
                  </div>
                </div>
              ))}
            </div>

            {/* Opportunities */}
            <div>
              <h2 style={h2}>Key Opportunities (Chesed)</h2>
              {opportunities.length === 0 && summary?.key_opportunities?.map((o, i) => (
                <div key={i} style={riskItem}>
                  <span style={{ color: '#10b981', fontSize: 14, marginTop: 1 }}>✦</span>
                  <span style={{ fontSize: 12, color: '#334155', lineHeight: 1.5 }}>{o}</span>
                </div>
              ))}
              {opportunities.slice(0, 6).map((o: any, i: number) => (
                <div key={i} style={{ ...riskItem, borderBottom: '1px solid #f1f5f9', paddingBottom: 8 }}>
                  <div>
                    <p style={{ fontSize: 11, color: '#334155', margin: 0, lineHeight: 1.5 }}>{o.description ?? o}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Communication strategy */}
          {s.hod?.messages && Object.keys(s.hod.messages).length > 0 && (
            <div style={{ marginTop: 28 }}>
              <h2 style={h2}>Stakeholder Communication (Hod)</h2>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
                {Object.entries(s.hod.messages).slice(0, 4).map(([audience, msg]) => (
                  <div key={audience} style={{ background: '#f8fafc', border: '1px solid #e2e8f0', borderRadius: 6, padding: '10px 12px' }}>
                    <p style={{ ...label, marginBottom: 4 }}>{audience}</p>
                    <p style={{ fontSize: 11, color: '#334155', margin: 0, lineHeight: 1.5 }}>{String(msg).slice(0, 120)}{String(msg).length > 120 ? '…' : ''}</p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* ── PAGE 4: Action Plan ── */}
        <div style={{ ...page, pageBreakAfter: 'auto' }}>
          <h2 style={h2}>Implementation Action Plan (Malchut)</h2>
          {actionItems.length > 0 ? (
            <ol style={{ paddingLeft: 20, margin: '0 0 24px' }}>
              {actionItems.map((item, i) => (
                <li key={i} style={{ fontSize: 12, color: '#334155', lineHeight: 1.7, marginBottom: 4 }}>{item}</li>
              ))}
            </ol>
          ) : (
            <p style={{ fontSize: 12, color: '#64748b', fontStyle: 'italic' }}>No specific action items defined.</p>
          )}

          {s.netzach?.strategies && s.netzach.strategies.length > 0 && (
            <div style={{ marginTop: 20 }}>
              <h2 style={h2}>Strategic Roadmap (Netzach)</h2>
              {s.netzach.strategies.slice(0, 5).map((st: any, i: number) => (
                <div key={i} style={{ display: 'flex', gap: 12, marginBottom: 12, paddingBottom: 12, borderBottom: '1px solid #f1f5f9' }}>
                  <div style={{ width: 24, height: 24, borderRadius: '50%', background: '#7c3aed', color: '#fff', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 11, fontFamily: 'sans-serif', flexShrink: 0 }}>
                    {i + 1}
                  </div>
                  <div>
                    <p style={{ fontWeight: 700, fontSize: 12, margin: '0 0 2px' }}>{st.name ?? `Strategy ${i + 1}`}</p>
                    <p style={{ fontSize: 11, color: '#475569', margin: 0, lineHeight: 1.5 }}>{st.description ?? st}</p>
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* Footer */}
          <div style={{ marginTop: 40, padding: '16px 0', borderTop: '2px solid #e2e8f0' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <p style={{ fontSize: 10, color: '#94a3b8', fontFamily: 'sans-serif', margin: 0 }}>
                Generated by Tikun Olam — Ethical Reasoning Architecture · {date}
              </p>
              <p style={{ fontSize: 10, color: '#94a3b8', fontFamily: 'sans-serif', margin: 0 }}>
                CONFIDENTIAL — Board Use Only
              </p>
            </div>
          </div>
        </div>
      </div>
    );
  }
);

ExecutiveReportTemplate.displayName = 'ExecutiveReportTemplate';
