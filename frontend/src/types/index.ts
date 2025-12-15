// API Request/Response types
export interface AnalysisRequest {
  scenario: string;
  case_name?: string;
  verbose?: boolean;
  auto_export?: boolean;
}

export interface AnalysisResponse {
  status: string;
  case_name: string;
  timestamp: string;
  sefirot_results: SefirotResults;
  summary: Summary;
  metadata: Metadata;
}

export interface SefirotResults {
  keter: KeterResult;
  chochmah: ChochmahResult;
  binah: BinahResult;
  chesed: ChesedResult;
  gevurah: GevurahResult;
  tiferet: TiferetResult;
  netzach: NetzachResult;
  hod: HodResult;
  yesod: YesodResult;
  malchut: MalchutResult;
}

// Keter types
export interface KeterResult {
  alignment_percentage: number;
  corruption_severity: string;
  manifestation_valid: boolean;
  threshold_met: boolean;
  scores: Record<string, number>;
  corruptions: Corruption[];
  raw_analysis: string;
}

export interface Corruption {
  type: string;
  severity: string;
  description: string;
  examples: string[];
}

// Chochmah types
export interface ChochmahResult {
  confidence_level: number;
  epistemic_humility_ratio: number;
  insight_depth_score: number;
  patterns_identified: string[];
  precedents: Precedent[];
  hidden_insights: string[];
  paradoxes_identified: string[];
  raw_wisdom: string;
}

export interface Precedent {
  name: string;
  year?: number;
  outcome: string;
  relevance: string;
  lessons: string[];
}

// Binah types
export interface BinahResult {
  mode: 'simple' | 'sigma';
  contextual_depth_score: number;
  bias_delta?: number;
  divergence_level?: string;
  blind_spots_detected?: number;
  convergence_points?: number;
  sigma_synthesis?: BinahSigmaAnalysis;
  stakeholder_analysis?: StakeholderAnalysis;
  ethical_tensions?: string[];
  contextual_factors?: string[];
  raw_understanding: string;
}

export interface BinahSigmaAnalysis {
  west_blind_spots: string[];
  east_blind_spots: string[];
  universal_convergence: string[];
  transcendent_synthesis: string;
}

export interface StakeholderAnalysis {
  beneficiaries?: string[];
  harmed?: string[];
  ignored?: string[];
  western_priority?: string[];
  eastern_priority?: string[];
}

// Other Sefirot types
export interface ChesedResult {
  opportunity_score: number;
  opportunities: string[];
  potential_impact: string;
  raw_opportunity: string;
}

export interface GevurahResult {
  risk_score: number;
  risks: Risk[];
  mitigation_strategies: string[];
  raw_risk: string;
}

export interface Risk {
  category: string;
  severity: string;
  description: string;
  likelihood: string;
}

export interface TiferetResult {
  balance_score: number;
  synthesis: string;
  harmony_assessment: string;
  raw_synthesis: string;
}

export interface NetzachResult {
  strategy_score: number;
  strategies: string[];
  implementation_phases: string[];
  raw_strategy: string;
}

export interface HodResult {
  communication_score: number;
  messages: Record<string, string>;
  channels: string[];
  raw_communication: string;
}

export interface YesodResult {
  readiness_score: number;
  integration_quality: string;
  foundation_strength: string;
  gaps_identified: Gap[];
  recommendation: string;
  confidence: string;
  raw_integration: string;
}

export interface Gap {
  severity: string;
  description: string;
}

export interface MalchutResult {
  decision: string;
  confidence_level: number;
  action_items: string[];
  timeline_estimate?: string;
  success_criteria: string[];
  raw_decision: string;
}

// Summary types
export interface Summary {
  final_decision: string;
  overall_alignment: number;
  key_risks: string[];
  key_opportunities: string[];
  recommendation: string;
}

export interface Metadata {
  version: string;
  total_duration_seconds: number;
  models_used: Record<string, string>;
  timestamp: string;
}

// Job types for async processing
export interface JobResponse {
  job_id: string;
  status: string;
  message: string;
}

export interface JobStatusResponse {
  job_id: string;
  status: string;
  result?: AnalysisResponse;
  error?: string;
}
