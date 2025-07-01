"""
Telemetry module for Graphiti.

This module provides anonymous usage analytics to help improve Graphiti.
"""

from .telemetry import capture_event, is_telemetry_enabled

# Token monitoring imports (optional - only if dependencies are available)
try:
    from .token_monitor import TokenMonitor, get_token_monitor
    from .token_integration import (
        track_llm_usage, 
        track_embedding_usage,
        log_llm_usage,
        log_embedding_usage,
        get_usage_report,
        set_provider_limit
    )
    _TOKEN_MONITORING_AVAILABLE = True
except ImportError:
    _TOKEN_MONITORING_AVAILABLE = False
    # Define dummy functions if monitoring not available
    def get_token_monitor():
        raise ImportError("Token monitoring requires additional dependencies: pip install pandas tabulate click")
    track_llm_usage = lambda *args, **kwargs: lambda func: func
    track_embedding_usage = lambda *args, **kwargs: lambda func: func
    log_llm_usage = lambda *args, **kwargs: None
    log_embedding_usage = lambda *args, **kwargs: None
    get_usage_report = lambda *args, **kwargs: {}
    set_provider_limit = lambda *args, **kwargs: None

__all__ = [
    'capture_event', 
    'is_telemetry_enabled',
    'get_token_monitor',
    'track_llm_usage',
    'track_embedding_usage', 
    'log_llm_usage',
    'log_embedding_usage',
    'get_usage_report',
    'set_provider_limit',
    '_TOKEN_MONITORING_AVAILABLE'
]
