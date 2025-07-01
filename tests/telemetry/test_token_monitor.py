"""
Tests for token monitoring system
"""

import pytest
import tempfile
import os
from datetime import datetime
from pathlib import Path

# Import with fallback for when dependencies aren't available
try:
    from graphiti_core.telemetry import (
        get_token_monitor,
        log_llm_usage,
        log_embedding_usage,
        get_usage_report,
        set_provider_limit,
        _TOKEN_MONITORING_AVAILABLE
    )
    from graphiti_core.telemetry.token_monitor import TokenMonitor, ServiceType
except ImportError:
    _TOKEN_MONITORING_AVAILABLE = False


@pytest.mark.skipif(not _TOKEN_MONITORING_AVAILABLE, reason="Token monitoring dependencies not installed")
class TestTokenMonitor:
    """Test token monitoring functionality."""
    
    @pytest.fixture
    def temp_monitor(self):
        """Create a temporary monitor for testing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            monitor = TokenMonitor(storage_dir=tmpdir)
            yield monitor
    
    def test_log_llm_usage(self, temp_monitor):
        """Test logging LLM usage."""
        result = temp_monitor.log_usage(
            provider="openai",
            service_type=ServiceType.LLM,
            model="gpt-4o",
            operation="test",
            input_tokens=100,
            output_tokens=200
        )
        
        assert result["logged"] == True
        assert result["record"]["total_tokens"] == 300
        assert result["record"]["provider"] == "openai"
        assert result["record"]["model"] == "gpt-4o"
    
    def test_log_embedding_usage(self, temp_monitor):
        """Test logging embedding usage."""
        result = temp_monitor.log_usage(
            provider="openai",
            service_type=ServiceType.EMBEDDING,
            model="text-embedding-3-small",
            operation="test_embed",
            input_tokens=50,
            output_tokens=0
        )
        
        assert result["logged"] == True
        assert result["record"]["total_tokens"] == 50
        assert result["record"]["service_type"] == "embedding"
    
    def test_cost_calculation(self, temp_monitor):
        """Test cost calculation."""
        result = temp_monitor.log_usage(
            provider="openai",
            service_type=ServiceType.LLM,
            model="gpt-4o",
            operation="test",
            input_tokens=1000,
            output_tokens=2000
        )
        
        # gpt-4o costs: $2.50/1M input, $10/1M output
        expected_cost = (1000 / 1_000_000 * 2.50) + (2000 / 1_000_000 * 10.00)
        assert abs(result["record"]["cost_usd"] - expected_cost) < 0.0001
    
    def test_provider_summary(self, temp_monitor):
        """Test getting provider summary."""
        # Log some usage
        temp_monitor.log_usage(
            provider="anthropic",
            service_type=ServiceType.LLM,
            model="claude-3-sonnet",
            operation="test",
            input_tokens=1000,
            output_tokens=2000
        )
        
        summary = temp_monitor.get_provider_summary("anthropic", days=1)
        
        assert summary["provider"] == "anthropic"
        assert summary["total_requests"] == 1
        assert summary["total_tokens"] == 3000
        assert summary["total_input_tokens"] == 1000
        assert summary["total_output_tokens"] == 2000
    
    def test_subscription_limits(self, temp_monitor):
        """Test setting and checking subscription limits."""
        temp_monitor.set_subscription_limit("anthropic", "max_plan_tokens", 5_000_000)
        
        # Log usage
        temp_monitor.log_usage(
            provider="anthropic",
            service_type=ServiceType.LLM,
            model="claude-3-sonnet",
            operation="test",
            input_tokens=4_000_000,
            output_tokens=0
        )
        
        status = temp_monitor._get_subscription_status()
        
        assert "anthropic" in status
        assert status["anthropic"]["limit"] == 5_000_000
        assert status["anthropic"]["used"] == 4_000_000
        assert status["anthropic"]["percentage_used"] == 80.0
        assert status["anthropic"]["status"] == "warning"  # 80% triggers warning
    
    def test_error_logging(self, temp_monitor):
        """Test error logging."""
        result = temp_monitor.log_usage(
            provider="openai",
            service_type=ServiceType.LLM,
            model="gpt-4o",
            operation="failed_call",
            input_tokens=0,
            output_tokens=0,
            error=True,
            error_message="API rate limit exceeded"
        )
        
        assert result["logged"] == True
        assert result["record"]["error"] == True
        assert result["record"]["error_message"] == "API rate limit exceeded"


@pytest.mark.skipif(not _TOKEN_MONITORING_AVAILABLE, reason="Token monitoring dependencies not installed")
class TestTokenIntegration:
    """Test integration functions."""
    
    def test_manual_logging_functions(self):
        """Test manual logging helper functions."""
        # Should not raise errors
        log_llm_usage(
            provider="test",
            model="test-model",
            input_tokens=100,
            output_tokens=200,
            operation="test"
        )
        
        log_embedding_usage(
            provider="test",
            model="test-embed",
            input_tokens=50,
            operation="test"
        )
    
    def test_get_usage_report(self):
        """Test getting usage reports."""
        # Log some test data
        log_llm_usage(
            provider="openai",
            model="gpt-4o",
            input_tokens=100,
            output_tokens=200
        )
        
        # Get report
        report = get_usage_report("openai", days=1)
        
        assert "total_tokens" in report
        assert report["total_tokens"] >= 300
    
    def test_set_provider_limit_function(self):
        """Test setting provider limits."""
        result = set_provider_limit("gemini", "free_tier_tokens", 1_000_000)
        assert "Updated gemini" in result


# Test that imports work even without dependencies
def test_imports_without_dependencies():
    """Test that imports don't fail when dependencies are missing."""
    from graphiti_core.telemetry import _TOKEN_MONITORING_AVAILABLE
    
    # This should always work
    if not _TOKEN_MONITORING_AVAILABLE:
        # These should be dummy functions
        from graphiti_core.telemetry import (
            get_token_monitor,
            track_llm_usage,
            log_llm_usage
        )
        
        # Should raise ImportError with helpful message
        with pytest.raises(ImportError, match="Token monitoring requires"):
            get_token_monitor()
        
        # Decorators should be no-ops
        @track_llm_usage(provider="test", model="test")
        def dummy_function():
            return "test"
        
        assert dummy_function() == "test"
        
        # Manual logging should be no-op
        result = log_llm_usage("test", "test", 100, 200)
        assert result is None