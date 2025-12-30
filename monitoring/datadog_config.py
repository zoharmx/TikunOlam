"""
Datadog configuration and initialization for Tikun Olam

Provides observability infrastructure for the entire ethical AI pipeline:
- Distributed tracing for all 10 Sefirot
- Custom metrics for ethical alignment, bias detection, and decision quality
- Structured logging with correlation IDs
- Real-time alerting on threshold violations
"""

import os
from typing import Optional, Dict, Any, List
from datadog import initialize, statsd
from ddtrace import tracer, patch_all
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import logging for structured output
from tikun.utils.logging import get_logger

logger = get_logger(__name__)

# Export availability flag
DATADOG_AVAILABLE = True


class DatadogConfig:
    """
    Datadog configuration manager for Tikun Olam observability
    """

    def __init__(self):
        """Initialize Datadog configuration from environment variables"""
        self.api_key = os.getenv('DATADOG_API_KEY')
        self.app_key = os.getenv('DATADOG_APP_KEY')
        self.service_name = os.getenv('DATADOG_SERVICE_NAME', 'tikun-olam')
        self.env = os.getenv('TIKUN_ENV', 'development')
        self.statsd_host = os.getenv('DATADOG_STATSD_HOST', '127.0.0.1')
        self.statsd_port = int(os.getenv('DATADOG_STATSD_PORT', '8125'))
        self.trace_agent_port = int(os.getenv('DATADOG_TRACE_PORT', '8126'))

        self.enabled = bool(self.api_key and self.api_key != 'your_datadog_api_key_here')

        if not self.enabled:
            logger.warning(
                "Datadog not configured - metrics and tracing disabled. "
                "Set DATADOG_API_KEY to enable observability."
            )

    def initialize_datadog(self) -> bool:
        """
        Initialize Datadog SDK with configuration

        Returns:
            bool: True if initialization successful, False otherwise
        """
        if not self.enabled:
            logger.info("Datadog disabled - skipping initialization")
            return False

        try:
            # Initialize Datadog API client
            initialize(
                api_key=self.api_key,
                app_key=self.app_key,
                statsd_host=self.statsd_host,
                statsd_port=self.statsd_port
            )

            # Set service name and environment via environment variables
            # (must be set before patch_all() for proper instrumentation)
            os.environ['DD_SERVICE'] = self.service_name
            os.environ['DD_ENV'] = self.env

            # DISABLED: Auto-instrumentation causes SSL errors with Python 3.13
            # patch_all() interferes with google-auth SSL handshake
            # TODO: Re-enable when using Python 3.11/3.12 or when ddtrace supports 3.13
            # patch_all()

            # Tracer is auto-configured via environment variables in ddtrace v2+
            # No need to call tracer.configure() explicitly

            logger.info(
                "Datadog initialized successfully (tracing disabled due to Python 3.13 compatibility)",
                service=self.service_name,
                env=self.env,
                statsd_host=self.statsd_host,
                statsd_port=self.statsd_port
            )

            return True

        except Exception as e:
            logger.error(
                "Failed to initialize Datadog",
                error=str(e),
                exc_info=True
            )
            return False


# Global Datadog config instance
_datadog_config: Optional[DatadogConfig] = None


def get_datadog_config() -> DatadogConfig:
    """
    Get or create global Datadog configuration

    Returns:
        DatadogConfig: Singleton instance
    """
    global _datadog_config
    if _datadog_config is None:
        _datadog_config = DatadogConfig()
        _datadog_config.initialize_datadog()
    return _datadog_config


# ============================================================================
# METRIC HELPERS
# ============================================================================

def emit_metric(metric_name: str, value: float, tags: Optional[List[str]] = None) -> None:
    """
    Emit a gauge metric to Datadog

    Args:
        metric_name: Metric name (e.g., 'keter.alignment_score')
        value: Numeric value
        tags: Optional list of tags (e.g., ['scenario:rbu_ubi', 'decision:GO'])
    """
    config = get_datadog_config()
    if not config.enabled:
        return

    try:
        statsd.gauge(metric_name, value, tags=tags or [])
        logger.debug(f"Emitted metric: {metric_name}={value}", tags=tags)
    except Exception as e:
        logger.warning(f"Failed to emit metric {metric_name}: {str(e)}")


def emit_counter(metric_name: str, value: int = 1, tags: Optional[List[str]] = None) -> None:
    """
    Emit a counter metric to Datadog

    Args:
        metric_name: Metric name (e.g., 'pipeline.analysis_started')
        value: Increment value (default: 1)
        tags: Optional list of tags
    """
    config = get_datadog_config()
    if not config.enabled:
        return

    try:
        statsd.increment(metric_name, value, tags=tags or [])
        logger.debug(f"Incremented counter: {metric_name}+{value}", tags=tags)
    except Exception as e:
        logger.warning(f"Failed to emit counter {metric_name}: {str(e)}")


def emit_timing(metric_name: str, value: float, tags: Optional[List[str]] = None) -> None:
    """
    Emit a timing metric to Datadog

    Args:
        metric_name: Metric name (e.g., 'keter.execution_time')
        value: Duration in milliseconds
        tags: Optional list of tags
    """
    config = get_datadog_config()
    if not config.enabled:
        return

    try:
        statsd.timing(metric_name, value, tags=tags or [])
        logger.debug(f"Emitted timing: {metric_name}={value}ms", tags=tags)
    except Exception as e:
        logger.warning(f"Failed to emit timing {metric_name}: {str(e)}")


def emit_histogram(metric_name: str, value: float, tags: Optional[List[str]] = None) -> None:
    """
    Emit a histogram metric to Datadog

    Args:
        metric_name: Metric name
        value: Numeric value
        tags: Optional list of tags
    """
    config = get_datadog_config()
    if not config.enabled:
        return

    try:
        statsd.histogram(metric_name, value, tags=tags or [])
        logger.debug(f"Emitted histogram: {metric_name}={value}", tags=tags)
    except Exception as e:
        logger.warning(f"Failed to emit histogram {metric_name}", error=str(e))


# ============================================================================
# SPAN HELPERS (for distributed tracing)
# ============================================================================

def add_span_tags(tags: Dict[str, Any]) -> None:
    """
    Add tags to the current active span

    Args:
        tags: Dictionary of tag key-value pairs
    """
    config = get_datadog_config()
    if not config.enabled:
        return

    try:
        span = tracer.current_span()
        if span:
            for key, value in tags.items():
                span.set_tag(key, value)
    except Exception as e:
        logger.warning("Failed to add span tags", error=str(e))


def set_span_error(error: Exception) -> None:
    """
    Mark the current span as errored

    Args:
        error: Exception that occurred
    """
    config = get_datadog_config()
    if not config.enabled:
        return

    try:
        span = tracer.current_span()
        if span:
            span.set_tag('error', True)
            span.set_tag('error.message', str(error))
            span.set_tag('error.type', type(error).__name__)
    except Exception as e:
        logger.warning("Failed to set span error", error=str(e))


# ============================================================================
# SEFIROT-SPECIFIC METRICS
# ============================================================================

class SefiraMetrics:
    """
    Helper class for emitting Sefirah-specific metrics
    """

    @staticmethod
    def emit_keter_metrics(result: Dict[str, Any], tags: Optional[List[str]] = None) -> None:
        """Emit Keter (ethical alignment) metrics"""
        base_tags = tags or []

        emit_metric('keter.alignment_score', result.get('alignment_percentage', 0), base_tags)
        emit_metric('keter.corruption_score', result.get('corruption_percentage', 0), base_tags)
        emit_counter('keter.analysis_success', tags=base_tags + ['status:success'])

    @staticmethod
    def emit_chochmah_metrics(result: Dict[str, Any], tags: Optional[List[str]] = None) -> None:
        """Emit Chochmah (wisdom) metrics"""
        base_tags = tags or []

        precedents = result.get('precedents', [])
        emit_metric('chochmah.precedent_count', len(precedents), base_tags)
        emit_counter('chochmah.analysis_success', tags=base_tags + ['status:success'])

    @staticmethod
    def emit_binah_metrics(result: Dict[str, Any], tags: Optional[List[str]] = None) -> None:
        """Emit Binah (understanding + BinahSigma) metrics"""
        base_tags = tags or []

        # BinahSigma-specific metrics (KEY DIFFERENTIATOR)
        # FIX: Check for mode == "sigma" instead of sigma_activated
        if result.get('mode') == 'sigma':
            # FIX: Use bias_delta instead of bias_delta_percentage
            bias_delta = result.get('bias_delta', 0)
            emit_metric('binah.bias_delta', bias_delta, base_tags + ['sigma:active'])

            # Extract blind spots from sigma_synthesis
            sigma_synthesis = result.get('sigma_synthesis', {})
            west_blind_spots = len(sigma_synthesis.get('west_blind_spots', []))
            east_blind_spots = len(sigma_synthesis.get('east_blind_spots', []))

            emit_metric('binah.west_blind_spots', west_blind_spots, base_tags)
            emit_metric('binah.east_blind_spots', east_blind_spots, base_tags)

            # Calculate convergence from convergence_points
            convergence_points = result.get('convergence_points', 0)
            blind_spots_total = result.get('blind_spots_detected', 8)
            convergence = (convergence_points / (convergence_points + blind_spots_total) * 100) if (convergence_points + blind_spots_total) > 0 else 0
            emit_metric('binah.convergence_score', convergence, base_tags)

            # Civilizational divergence (UNIQUE METRIC)
            divergence = 100 - convergence
            emit_metric('binah.civilizational_divergence', divergence, base_tags)

        emit_counter('binah.analysis_success', tags=base_tags + ['status:success'])

    @staticmethod
    def emit_chesed_metrics(result: Dict[str, Any], tags: Optional[List[str]] = None) -> None:
        """Emit Chesed (opportunity) metrics"""
        base_tags = tags or []

        opportunities = result.get('opportunities', [])
        emit_metric('chesed.opportunity_count', len(opportunities), base_tags)
        emit_counter('chesed.analysis_success', tags=base_tags + ['status:success'])

    @staticmethod
    def emit_gevurah_metrics(result: Dict[str, Any], tags: Optional[List[str]] = None) -> None:
        """Emit Gevurah (risk) metrics"""
        base_tags = tags or []

        risks = result.get('risks', [])
        emit_metric('gevurah.risk_count', len(risks), base_tags)

        # Calculate max risk severity
        max_severity = 0
        for risk in risks:
            severity_map = {'LOW': 25, 'MEDIUM': 50, 'HIGH': 75, 'CRITICAL': 100}
            severity = severity_map.get(risk.get('severity', 'MEDIUM'), 50)
            max_severity = max(max_severity, severity)

        emit_metric('gevurah.risk_severity', max_severity, base_tags)
        emit_counter('gevurah.analysis_success', tags=base_tags + ['status:success'])

    @staticmethod
    def emit_tiferet_metrics(result: Dict[str, Any], tags: Optional[List[str]] = None) -> None:
        """Emit Tiferet (synthesis) metrics"""
        base_tags = tags or []

        emit_counter('tiferet.analysis_success', tags=base_tags + ['status:success'])

    @staticmethod
    def emit_netzach_metrics(result: Dict[str, Any], tags: Optional[List[str]] = None) -> None:
        """Emit Netzach (strategy) metrics"""
        base_tags = tags or []

        emit_counter('netzach.analysis_success', tags=base_tags + ['status:success'])

    @staticmethod
    def emit_hod_metrics(result: Dict[str, Any], tags: Optional[List[str]] = None) -> None:
        """Emit Hod (communication) metrics"""
        base_tags = tags or []

        emit_counter('hod.analysis_success', tags=base_tags + ['status:success'])

    @staticmethod
    def emit_yesod_metrics(result: Dict[str, Any], tags: Optional[List[str]] = None) -> None:
        """Emit Yesod (integration) metrics"""
        base_tags = tags or []

        coherence = result.get('coherence_percentage', 0)
        emit_metric('yesod.coherence_score', coherence, base_tags)
        emit_counter('yesod.analysis_success', tags=base_tags + ['status:success'])

    @staticmethod
    def emit_malchut_metrics(result: Dict[str, Any], tags: Optional[List[str]] = None) -> None:
        """Emit Malchut (decision) metrics"""
        base_tags = tags or []

        decision = result.get('decision', 'UNKNOWN')
        confidence = result.get('confidence_percentage', 0)
        action_items = len(result.get('action_items', []))

        emit_metric('malchut.confidence', confidence, base_tags)
        emit_metric('malchut.action_items', action_items, base_tags)
        emit_counter('malchut.decision', tags=base_tags + [f'decision:{decision}'])
        emit_counter('malchut.analysis_success', tags=base_tags + ['status:success'])


# ============================================================================
# PIPELINE-LEVEL METRICS
# ============================================================================

def emit_pipeline_start(scenario_id: str, tags: Optional[List[str]] = None) -> None:
    """Emit metrics when pipeline starts"""
    base_tags = (tags or []) + [f'scenario_id:{scenario_id}']
    emit_counter('pipeline.started', tags=base_tags)


def emit_pipeline_complete(
    scenario_id: str,
    duration_ms: float,
    decision: str,
    tags: Optional[List[str]] = None
) -> None:
    """Emit metrics when pipeline completes"""
    base_tags = (tags or []) + [f'scenario_id:{scenario_id}', f'decision:{decision}']

    emit_timing('pipeline.total_duration', duration_ms, base_tags)
    emit_counter('pipeline.completed', tags=base_tags + ['status:success'])
    emit_counter('pipeline.decision_distribution', tags=base_tags)


def emit_pipeline_error(scenario_id: str, error: Exception, tags: Optional[List[str]] = None) -> None:
    """Emit metrics when pipeline fails"""
    base_tags = (tags or []) + [f'scenario_id:{scenario_id}', f'error_type:{type(error).__name__}']
    emit_counter('pipeline.failed', tags=base_tags + ['status:error'])


# Initialize on module import
get_datadog_config()
