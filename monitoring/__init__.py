"""
Monitoring and observability module for Tikun Olam

Provides Datadog integration for:
- Distributed tracing
- Custom metrics
- Real-time alerting
- Dashboard creation
"""

from .datadog_config import (
    get_datadog_config,
    emit_metric,
    emit_counter,
    emit_timing,
    emit_histogram,
    add_span_tags,
    set_span_error,
    SefiraMetrics,
    emit_pipeline_start,
    emit_pipeline_complete,
    emit_pipeline_error
)

__all__ = [
    'get_datadog_config',
    'emit_metric',
    'emit_counter',
    'emit_timing',
    'emit_histogram',
    'add_span_tags',
    'set_span_error',
    'SefiraMetrics',
    'emit_pipeline_start',
    'emit_pipeline_complete',
    'emit_pipeline_error'
]
