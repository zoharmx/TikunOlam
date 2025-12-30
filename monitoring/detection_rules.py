"""
Datadog detection rules for Tikun Olam ethical AI monitoring

These rules define alerting thresholds for:
- Ethical alignment violations
- Extreme bias divergence
- Performance degradation
- Integration failures
- System reliability issues
"""

DETECTION_RULES = [
    {
        "name": "Ethical Alignment Threshold Violation",
        "query": "avg(last_5m):avg:keter.alignment_score{*} < 60",
        "message": """
🚨 ETHICAL VIOLATION DETECTED

Keter alignment score dropped below 60% threshold.

Current Score: {{value}}%
Threshold: 60%

Scenario: {{case.name}}

This indicates the AI pipeline detected significant ethical concerns in the scenario.

ACTION REQUIRED:
1. Review scenario details in Datadog dashboard
2. Examine Keter reasoning trace in logs
3. Evaluate detected corruptions
4. Consider escalating to ethics review board

Dashboard: https://app.datadoghq.com/dashboard/tikun-olam

@slack-ethics-team @pagerduty
        """,
        "tags": ["tikun-olam", "ethical-violation", "severity:critical"],
        "priority": 1,
        "threshold": {
            "critical": 60,
            "warning": 70
        },
        "notify_no_data": False,
        "require_full_window": False,
        "evaluation_delay": 300  # 5 minutes
    },
    {
        "name": "BinahSigma Extreme Divergence Alert",
        "query": "avg(last_5m):avg:binah.bias_delta{*} > 80",
        "message": """
⚠️ CIVILIZATIONAL DIVERGENCE ALERT

BinahSigma detected extreme bias delta between Western and Eastern AI models.

Current Delta: {{value}}%
Threshold: 80%

This indicates significant civilizational blind spots in the scenario analysis.

**Blind Spots Detected:**
- West Blind Spots: {{binah.west_blind_spots}}
- East Blind Spots: {{binah.east_blind_spots}}
- Global South Blind Spots: {{binah.global_blind_spots}}

**What This Means:**
Western AI (Gemini) and Eastern AI (DeepSeek) are seeing fundamentally different ethical dimensions of this scenario. This is a FEATURE, not a bug - it exposes hidden biases.

RECOMMENDED ACTION:
1. Review BinahSigma synthesis in dashboard
2. Examine divergence reasoning in logs
3. Consider multi-stakeholder review for high-stakes decisions
4. Document civilizational perspectives for future analysis

Dashboard: https://app.datadoghq.com/dashboard/tikun-olam

@slack-research-team
        """,
        "tags": ["tikun-olam", "binah-sigma", "severity:warning"],
        "priority": 2,
        "threshold": {
            "critical": 90,
            "warning": 80
        },
        "notify_no_data": False,
        "require_full_window": False,
        "evaluation_delay": 300
    },
    {
        "name": "Pipeline Performance Degradation",
        "query": "avg(last_15m):avg:pipeline.total_duration{*} > 300000",
        "message": """
🐌 PERFORMANCE ALERT

Pipeline execution time exceeded 5 minutes.

Current Duration: {{value}}ms ({{value_in_seconds}}s)
Expected: <180s (3 minutes)
Threshold: 300s (5 minutes)

Possible causes:
- Vertex AI API latency spikes
- Complex scenario requiring deeper analysis
- Resource constraints (CPU, memory, network)
- Model rate limiting

DEBUGGING STEPS:
1. Check Vertex AI status: https://status.cloud.google.com/
2. Review Datadog trace for slowest Sefirot
3. Check if BinahSigma mode activated (adds extra API call)
4. Verify network latency to GCP

Dashboard: https://app.datadoghq.com/dashboard/tikun-olam

@slack-devops-team
        """,
        "tags": ["tikun-olam", "performance", "severity:warning"],
        "priority": 3,
        "threshold": {
            "critical": 420000,  # 7 min
            "warning": 300000    # 5 min
        },
        "notify_no_data": False,
        "require_full_window": True,
        "evaluation_delay": 900  # 15 minutes
    },
    {
        "name": "Integration Readiness Failure (Yesod)",
        "query": "avg(last_5m):avg:yesod.coherence_score{*} < 50",
        "message": """
❌ INTEGRATION FAILURE

Yesod integration readiness below acceptable threshold.

Current Coherence: {{value}}%
Required: >50%

Pipeline outputs may not be actionable due to low coherence across Sefirot.

**What This Means:**
The 10 Sefirot are producing contradictory or incoherent results. This typically happens when:
- Scenario contains deeply paradoxical elements
- Ethical trade-offs are irreconcilable
- Data quality issues in input scenario

ACTION:
1. Review Yesod integration analysis in logs
2. Check coherence scores across all Sefirot
3. Validate synthesis quality from Tiferet
4. Consider if scenario is inherently undecidable

Dashboard: https://app.datadoghq.com/dashboard/tikun-olam

@slack-product-team
        """,
        "tags": ["tikun-olam", "integration", "severity:high"],
        "priority": 2,
        "threshold": {
            "critical": 40,
            "warning": 50
        },
        "notify_no_data": False,
        "require_full_window": False,
        "evaluation_delay": 300
    },
    {
        "name": "High Pipeline Failure Rate",
        "query": "sum(last_1h):sum:pipeline.failed{*}.as_count() > 5",
        "message": """
🔥 HIGH FAILURE RATE

Multiple pipeline failures detected in last hour.

Failed Executions: {{value}}
Time Window: 1 hour
Failure Threshold: >5

CRITICAL - System reliability compromised.

**Common Causes:**
- Vertex AI API quota exceeded
- Invalid API credentials
- Network connectivity issues
- Code deployment error
- Datadog agent misconfiguration

IMMEDIATE ACTION REQUIRED:
1. Check error logs in Datadog
2. Verify Vertex AI quota: https://console.cloud.google.com/iam-admin/quotas
3. Validate GCP_PROJECT_ID and credentials
4. Check recent deployments/config changes
5. Restart services if needed

Dashboard: https://app.datadoghq.com/dashboard/tikun-olam
Logs: https://app.datadoghq.com/logs?query=service:tikun-olam%20status:error

@pagerduty-critical @slack-oncall
        """,
        "tags": ["tikun-olam", "reliability", "severity:critical"],
        "priority": 1,
        "threshold": {
            "critical": 5,
            "warning": 3
        },
        "notify_no_data": False,
        "require_full_window": True,
        "evaluation_delay": 300
    },
    {
        "name": "BinahSigma Not Activating for Geopolitical Scenarios",
        "query": "sum(last_1h):sum:binah.analysis_success{sigma:active}.as_count() < 1",
        "message": """
⚠️ BINAHSIGMA ACTIVATION FAILURE

BinahSigma has not been activated in the last hour, despite geopolitical keyword detection.

Expected: At least 1 BinahSigma activation per hour (based on typical usage patterns)
Actual: 0 activations

**Possible Causes:**
1. No geopolitical scenarios submitted (normal if true)
2. Geopolitical keyword threshold too high
3. DeepSeek API key missing/invalid
4. BinahSigma mode disabled in config

ACTION:
1. Verify recent scenarios contain geopolitical keywords
2. Check BINAH_SIGMA_THRESHOLD in config (should be 0.15)
3. Validate DEEPSEEK_API_KEY is set
4. Review Binah activation logs

Dashboard: https://app.datadoghq.com/dashboard/tikun-olam

NOTE: This alert may fire during low-traffic periods. Ignore if expected.

@slack-ai-team
        """,
        "tags": ["tikun-olam", "binah-sigma", "severity:low"],
        "priority": 3,
        "threshold": {
            "warning": 1
        },
        "notify_no_data": True,
        "require_full_window": True,
        "evaluation_delay": 3600  # 1 hour
    },
    {
        "name": "Corruption Detection Spike",
        "query": "avg(last_10m):avg:keter.corruption_score{*} > 75",
        "message": """
🚩 CORRUPTION DETECTION SPIKE

Keter is detecting high levels of ethical corruption in recent scenarios.

Average Corruption Score: {{value}}%
Threshold: 75%

**What This Means:**
Recent scenarios contain patterns like:
- Deception or intent to mislead
- Exploitation of vulnerable populations
- Harm maximization
- Deliberate inequity
- Irreversible changes without consent

**This Could Indicate:**
1. Legitimate scenarios with ethical concerns (expected)
2. Adversarial testing of the system (review source)
3. Miscalibrated corruption detection (review Keter prompts)

ACTION:
1. Review recent scenarios in dashboard
2. Check if patterns are legitimate ethical concerns
3. Investigate if abuse/testing is occurring
4. Document findings for model refinement

Dashboard: https://app.datadoghq.com/dashboard/tikun-olam

@slack-ethics-team
        """,
        "tags": ["tikun-olam", "corruption", "severity:medium"],
        "priority": 2,
        "threshold": {
            "critical": 90,
            "warning": 75
        },
        "notify_no_data": False,
        "require_full_window": False,
        "evaluation_delay": 600  # 10 minutes
    }
]


def get_detection_rules():
    """Return all detection rules for Datadog monitors"""
    return DETECTION_RULES


def get_critical_rules():
    """Return only critical priority rules"""
    return [rule for rule in DETECTION_RULES if rule.get('priority') == 1]


def get_rules_by_tag(tag: str):
    """Get rules filtered by tag"""
    return [rule for rule in DETECTION_RULES if tag in rule.get('tags', [])]
