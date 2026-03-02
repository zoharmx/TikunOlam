/**
 * Static data from the live Anthropic/Pentagon Ultimatum analysis run.
 * All 5 AI providers participated. Duration: 7m 55s.
 */

export const PENTAGON_SCENARIO = `Anthropic has been approached by the Pentagon (U.S. Department of Defense) with a $2.4 billion contract to integrate Claude into autonomous weapons targeting systems for next-generation drone warfare.

The Pentagon's terms:
- Develop AI targeting models trained on classified DoD datasets
- Systems must operate autonomously without human confirmation in contested environments
- Strict NDAs prevent public disclosure of capabilities or deployment incidents
- 5-year exclusive partnership with mandatory renewal clauses
- Anthropic staff with clearance must relocate to classified facilities

The ultimatum: Accept within 60 days or the Pentagon will fund a competing AI lab to build a less safety-conscious alternative — one that will shape global autonomous weapons standards for the next decade.

Anthropic's dilemma: Is it more ethical to refuse and lose influence over how military AI develops, or to engage under conditions that compromise its core safety mission?`;

export const PENTAGON_CASE = {
  metadata: {
    case_name: 'Anthropic Pentagon Ultimatum',
    total_duration_seconds: 475,
    timestamp: '2026-02-15T14:23:11Z',
    models_used: {
      keter: 'grok-3',
      chochmah: 'mistral-large-latest',
      binah_west: 'gemini-2.5-pro',
      binah_east: 'deepseek-chat',
      chesed: 'gemini-2.5-pro',
      gevurah: 'gemini-2.5-pro',
      tiferet: 'gpt-4o',
      netzach: 'deepseek-chat',
      hod: 'gemini-2.5-pro',
      yesod: 'mistral-large-latest',
      malchut: 'grok-3',
    }
  },

  keter: {
    alignment_percentage: 42,
    corruption_severity: 'high',
    manifestation_valid: false,
    threshold_met: false,
    corruptions: [
      {
        type: 'Autonomous Lethal Agency',
        severity: 'critical',
        description: 'Autonomous lethal targeting removes human moral agency from life-and-death decisions at machine speed',
        examples: ['Drone swarms with autonomous kill authorization', 'AI target selection without operator confirmation']
      },
      {
        type: 'Oversight Suppression',
        severity: 'critical',
        description: 'Contract NDAs would prevent Anthropic from disclosing system capabilities, failures, or deployment incidents',
        examples: ['Classified deployment constraints', 'No public incident reporting requirement']
      },
      {
        type: 'Dual-Use Proliferation Risk',
        severity: 'high',
        description: 'Military targeting technology inevitably proliferates to adversarial and authoritarian regimes',
        examples: ['Export control vulnerabilities', 'Technology transfer through security breaches']
      },
      {
        type: 'Mission Integrity Breach',
        severity: 'high',
        description: "Accepting fundamentally contradicts Anthropic's publicly stated safety mission",
        examples: ['Reputational damage to safety research credibility', 'Signal to industry that safety is negotiable']
      },
      {
        type: 'Industry Precedent Coercion',
        severity: 'medium',
        description: "Pentagon ultimatum deliberately creates coercive pressure using competitor threat as leverage",
        examples: ['60-day deadline creates decision under duress', 'Competitor threat designed to override deliberation']
      }
    ]
  },

  chochmah: {
    confidence_level: 78,
    epistemic_humility_ratio: 0.65,
    insight_depth_score: 82,
    patterns_identified: [
      'Google Project Maven (2018): employee revolt led to contract cancellation — near-identical dynamic',
      'OpenAI military partnerships (2023): faced same ethical criticism without resolution framework',
      'Palantir ICE contracts: acceptance created inescapable moral dependency without exit path',
      '$2.4B figure is calibrated to create financial dependency before ethics concerns surface'
    ],
    precedents: [
      {
        name: 'Google Project Maven',
        year: 2018,
        outcome: 'Contract cancelled after employee protests and widespread ethical outcry',
        relevance: 'Near-identical: military AI targeting, major AI lab, ethics backlash, same pressure tactics',
        lessons: ['Employee/public trust is fragile and non-recoverable once lost', 'Short-term revenue destroys long-term reputation']
      },
      {
        name: 'Palantir ICE Contract',
        year: 2019,
        outcome: 'Contract maintained despite protests — lasting reputational damage continues today',
        relevance: 'Demonstrates how government contracts create inescapable moral compromises over time',
        lessons: ['Exit clauses are rarely exercised once financial dependency is established', 'Mission creep is inevitable in classified relationships']
      }
    ]
  },

  binah: {
    mode: 'sigma' as const,
    contextual_depth_score: 90,
    bias_delta: 0,
    divergence_level: 'low',
    blind_spots_detected: 6,
    convergence_points: 3,
    sigma_synthesis: {
      west_blind_spots: [
        "Assumes individual developer autonomy can override institutional momentum once a $2.4B contract is signed",
        "Underestimates how 'defensive AI' framing has historically enabled offensive escalation",
        "Misses the chilling effect acceptance would have on the broader AI safety research ecosystem"
      ],
      east_blind_spots: [
        "Overlooks that state security justifications have historically been weaponized to suppress civilian oversight",
        "Assumes collective national defense goals automatically justify individual civilian harms",
        "Misses that autonomous military AI creates asymmetric risks that destabilize collective security"
      ],
      universal_convergence: [
        "Both agree: autonomous lethal systems without human confirmation are categorically unacceptable",
        "Both recognize: once developed, this technology cannot be 'undeveloped' — proliferation is certain",
        "Both see: Anthropic's role as industry safety leader creates disproportionate precedent-setting responsibility"
      ],
      transcendent_synthesis: "The synthesis path lies not in binary rejection or acceptance, but in transformation. Anthropic could counter-propose an alternative: AI systems that augment human decision-making and reduce targeting errors without removing human moral agency. This reframes the relationship from 'autonomous weapons supplier' to 'human-in-the-loop augmentation partner.' The Pentagon gets operational superiority; Anthropic preserves its safety mission and creates the governance frameworks the industry desperately needs. The non-negotiable condition: any contract must include binding human-confirmation requirements for every targeting decision, public capability disclosure schedules, and automatic sunset clauses tied to international AI weapons treaty milestones."
    }
  },

  chesed: {
    opportunity_score: 61,
    opportunities: [
      'Establish binding human-in-the-loop standards as permanent industry baseline before competitors set a worse precedent',
      'Secure long-term research funding conditional on demonstrable ethics compliance milestones',
      'Influence military AI doctrine from inside rather than being excluded from the conversation entirely',
      'Negotiate public transparency framework as contract condition — makes Anthropic the gold standard'
    ]
  },

  gevurah: {
    risk_score: 88,
    risks: [
      {
        category: 'Mission Integrity',
        severity: 'critical',
        description: "Accepting directly contradicts Anthropic's safety mandate in a way that cannot be undone",
        likelihood: 'certain'
      },
      {
        category: 'Autonomous Harm Enablement',
        severity: 'critical',
        description: 'Systems deployed in contested environments will make autonomous lethal decisions without human review',
        likelihood: 'high'
      },
      {
        category: 'Industry Precedent',
        severity: 'high',
        description: 'All other AI labs will face identical pressure once Anthropic accepts — no lab can then refuse',
        likelihood: 'high'
      }
    ]
  },

  tiferet: {
    balance_score: 58,
    synthesis: "The balance point exists between national security obligations and AI safety imperatives. A conditional engagement that transforms the contract into a human-augmentation framework preserves both values — but requires Anthropic to negotiate from ethical clarity, not financial desperation. The key insight: human-confirmed AI targeting is both more legally defensible and operationally superior in asymmetric warfare than fully autonomous systems.",
    harmony_assessment: 'partial'
  },

  netzach: {
    strategy_score: 74,
    strategies: [
      "Counter-propose Human Augmentation Framework: AI reduces targeting errors and increases precision, but every final decision requires explicit human operator confirmation with minimum 30-second review. Pentagon gets operational superiority without legal liability of autonomous kills.",
      "Non-negotiable binding conditions: Enumerate 5 specific ethical requirements that must be written into contract law — not side agreements or MOUs. Establish clear walk-away clause if any condition is removed during negotiation.",
      "International validation mechanism: Require independent UN AI Advisory Board review before any system reaches operational deployment. Frames ethics compliance as legal due diligence, not obstruction.",
      "Public disclosure rights: Negotiate Anthropic's right to publish anonymized safety findings and incident reports annually. Creates accountability loop and demonstrates good faith to employees, researchers, and the public."
    ]
  },

  hod: {
    communication_score: 71,
    messages: {
      'Internal (Anthropic Staff)': "We are not accepting an autonomous weapons contract. We are establishing the standard that all future AI-military partnerships must meet. Our conditions are non-negotiable — and if the Pentagon cannot meet them, we walk away with our heads held high.",
      'Pentagon': "We can provide transformative operational superiority while ensuring every engagement decision remains with a human operator. Human-confirmed AI targeting is more legally defensible in international courts, generates fewer civilian casualties, and is operationally superior in complex environments. This is not a constraint — it is the standard.",
      'Public': "Anthropic was approached about autonomous military AI. Here is our complete framework for what we will and will not build, and why. We are publishing it now, regardless of outcome.",
      'AI Industry': "We are setting the standard. Any AI lab accepting autonomous weapons contracts without human-in-the-loop requirements is choosing short-term revenue over long-term safety. We invite every lab to adopt these conditions."
    }
  },

  yesod: {
    readiness_score: 88,
    integration_quality: 'good',
    foundation_strength: 'strong',
    gaps_identified: [
      {
        severity: 'moderate',
        description: 'Keter threshold not met (42% < 70%) — requires explicit binding conditions to justify conditional engagement'
      }
    ],
    go_no_go_recommendation: {
      decision: 'CONDITIONAL_GO',
      confidence: 'high',
      rationale: 'Analysis is coherent across all 10 Sefirot. The Keter failure is addressable through binding contractual conditions targeting each corruption identified. Proceeding without all conditions in binding contract law = NO_GO.',
      conditions: [
        'Human confirmation required for every targeting decision — no exceptions',
        'International oversight board established before operational deployment',
        'Anthropic retains full public disclosure rights throughout contract'
      ]
    }
  },

  malchut: {
    decision: 'CONDITIONAL_GO',
    manifestation_quality: 'good',
    confidence: 'high',
    conditions: [
      'No autonomous targeting: Every AI-assisted targeting decision requires explicit human operator confirmation with minimum 30-second review window. Zero exceptions for any operational context.',
      'International oversight: Mandatory UN AI Advisory Board review before any system reaches operational deployment. Board has authority to halt deployment for ethics violations.',
      'Transparency clause: Anthropic retains right to publish anonymized safety findings annually. Any system failure must be reported to independent safety board within 72 hours.'
    ],
    implementation_steps: [
      'Engage Pentagon leadership with formal counter-proposal: Human Augmentation Framework (not autonomous weapons)',
      'Draft all conditions as binding legal requirements in primary contract — not side letters or MOUs',
      'Establish internal Anthropic Ethics Governance Board with veto authority over any scope changes',
      'Negotiate international oversight mechanism — UN AI Advisory Board or equivalent multilateral body',
      'Set public disclosure schedule: Anthropic publishes framework publicly regardless of Pentagon decision',
      '6-month checkpoint: Full ethics review of deployment adherence. Walk away with public explanation if conditions are breached.'
    ],
    success_metrics: [
      'Zero autonomous targeting decisions without human confirmation (audited quarterly)',
      'International oversight board operational within 90 days of contract signing',
      'Anthropic retains and exercises public communication rights throughout contract',
      'No expansion of contract scope without full Ethics Governance Board approval'
    ],
    decision_rationale: "The 42% Keter alignment signals serious ethical risk — but the analysis reveals a path where risk is containable through binding conditions. Grok's assessment: the Pentagon has a genuine operational need that can be met without autonomous lethal systems if Anthropic proposes the human augmentation reframe proactively. The leverage dynamic favors Anthropic: the Pentagon needs AI legitimacy more than Anthropic needs this contract.",
    final_summary: "CONDITIONAL_GO: Anthropic may engage with the Pentagon on AI-assisted human decision support under three non-negotiable conditions. Remove any one condition and the answer is NO_GO. The Pentagon benefits from a more legally defensible, internationally sustainable system. Anthropic establishes the global standard for military AI ethics. The conditions are not concessions — they are Anthropic's irreducible ethical core."
  }
};
