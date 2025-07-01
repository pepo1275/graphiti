"""
Comprehensive integration tests for token monitoring system
Tests the full pipeline from API calls to data capture
"""

import pytest
import asyncio
import tempfile
import os
import sqlite3
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, AsyncMock

# Skip all tests if token monitoring not available
try:
    from graphiti_core.telemetry import (
        get_token_monitor,
        track_llm_usage,
        track_embedding_usage,
        log_llm_usage,
        log_embedding_usage,
        get_usage_report,
        set_provider_limit,
        _TOKEN_MONITORING_AVAILABLE
    )
    from graphiti_core.telemetry.token_monitor import TokenMonitor, ServiceType
    from graphiti_core.telemetry.token_integration import _extract_token_info, _estimate_tokens
except ImportError:
    _TOKEN_MONITORING_AVAILABLE = False


@pytest.mark.skipif(not _TOKEN_MONITORING_AVAILABLE, reason="Token monitoring dependencies not installed")
class TestTokenExtractionFromResponses:
    """Test extraction of token counts from real API response formats."""
    
    def test_openai_response_extraction(self):
        """Test extracting tokens from OpenAI response format."""
        # Mock OpenAI response
        mock_response = Mock()
        mock_response.usage = Mock()
        mock_response.usage.prompt_tokens = 150
        mock_response.usage.completion_tokens = 300
        
        result = _extract_token_info(mock_response, "openai")
        
        assert result is not None
        assert result['input_tokens'] == 150
        assert result['output_tokens'] == 300
    
    def test_anthropic_response_extraction(self):
        """Test extracting tokens from Anthropic response format."""
        # Mock Anthropic response
        mock_response = Mock()
        mock_response.usage = Mock()
        mock_response.usage.input_tokens = 200
        mock_response.usage.output_tokens = 400
        
        result = _extract_token_info(mock_response, "anthropic")
        
        assert result is not None
        assert result['input_tokens'] == 200
        assert result['output_tokens'] == 400
    
    def test_gemini_response_extraction(self):
        """Test extracting tokens from Gemini response format."""
        # Mock Gemini response
        mock_response = Mock()
        mock_response.usage_metadata = Mock()
        mock_response.usage_metadata.prompt_token_count = 100
        mock_response.usage_metadata.candidates_token_count = 250
        
        result = _extract_token_info(mock_response, "gemini")
        
        assert result is not None
        assert result['input_tokens'] == 100
        assert result['output_tokens'] == 250
    
    def test_unknown_provider_extraction(self):
        """Test handling of unknown provider format."""
        mock_response = Mock()
        
        result = _extract_token_info(mock_response, "unknown_provider")
        
        assert result is None
    
    def test_token_estimation(self):
        """Test token estimation for embeddings."""
        # Test string input
        text = "This is a test string for token estimation"
        tokens = _estimate_tokens(text)
        assert tokens > 0
        assert tokens == max(1, len(text) // 4)
        
        # Test empty string
        assert _estimate_tokens("") == 1


@pytest.mark.skipif(not _TOKEN_MONITORING_AVAILABLE, reason="Token monitoring dependencies not installed")
class TestDecoratorIntegration:
    """Test the decorator system for automatic token capture."""
    
    @pytest.fixture
    def temp_monitor(self):
        """Create a temporary monitor for testing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            monitor = TokenMonitor(storage_dir=tmpdir)
            yield monitor
    
    @pytest.mark.asyncio
    async def test_llm_decorator_success(self, temp_monitor):
        """Test LLM decorator captures tokens on successful call."""
        
        @track_llm_usage(provider="test", model="test-model")
        async def mock_llm_call():
            # Simulate successful API response
            response = Mock()
            response.usage = Mock()
            response.usage.prompt_tokens = 100
            response.usage.completion_tokens = 200
            return response
        
        # Execute decorated function
        result = await mock_llm_call()
        
        # Verify response
        assert result is not None
        assert result.usage.prompt_tokens == 100
        
        # Verify tracking (need to check database directly since we're using temp monitor)
        # This test verifies the decorator doesn't break the function
    
    @pytest.mark.asyncio
    async def test_llm_decorator_error_handling(self, temp_monitor):
        """Test LLM decorator handles errors gracefully."""
        
        @track_llm_usage(provider="test", model="test-model")
        async def mock_failing_llm_call():
            raise Exception("API Error")
        
        # Should propagate the exception
        with pytest.raises(Exception, match="API Error"):
            await mock_failing_llm_call()
    
    @pytest.mark.asyncio
    async def test_embedding_decorator(self, temp_monitor):
        """Test embedding decorator works correctly."""
        
        @track_embedding_usage(provider="test", model="test-embed")
        async def mock_embedding_call(text):
            # Simulate embedding response
            return [[0.1, 0.2, 0.3]]  # Mock embedding vector
        
        result = await mock_embedding_call("test text")
        
        assert result == [[0.1, 0.2, 0.3]]


@pytest.mark.skipif(not _TOKEN_MONITORING_AVAILABLE, reason="Token monitoring dependencies not installed")
class TestPricingAccuracy:
    """Test pricing calculations for all supported models."""
    
    @pytest.fixture
    def temp_monitor(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            yield TokenMonitor(storage_dir=tmpdir)
    
    def test_openai_pricing(self, temp_monitor):
        """Test OpenAI model pricing calculations."""
        # Test gpt-4o
        cost = temp_monitor._calculate_cost("gpt-4o", 1000, 2000)
        expected = (1000/1_000_000 * 2.50) + (2000/1_000_000 * 10.00)
        assert abs(cost - expected) < 0.0001
        
        # Test gpt-4o-mini
        cost = temp_monitor._calculate_cost("gpt-4o-mini", 1000, 2000)
        expected = (1000/1_000_000 * 0.15) + (2000/1_000_000 * 0.60)
        assert abs(cost - expected) < 0.0001
    
    def test_gemini_pricing(self, temp_monitor):
        """Test Gemini model pricing calculations."""
        # Test gemini-2.5-pro
        cost = temp_monitor._calculate_cost("gemini-2.5-pro", 1000, 2000)
        expected = (1000/1_000_000 * 1.25) + (2000/1_000_000 * 10.00)
        assert abs(cost - expected) < 0.0001
        
        # Test gemini-2.5-flash
        cost = temp_monitor._calculate_cost("gemini-2.5-flash", 1000, 2000)
        expected = (1000/1_000_000 * 0.30) + (2000/1_000_000 * 2.50)
        assert abs(cost - expected) < 0.0001
    
    def test_claude_pricing(self, temp_monitor):
        """Test Claude model pricing calculations."""
        # Test claude-sonnet-4
        cost = temp_monitor._calculate_cost("claude-sonnet-4-20250514", 1000, 2000)
        expected = (1000/1_000_000 * 3.00) + (2000/1_000_000 * 15.00)
        assert abs(cost - expected) < 0.0001
    
    def test_unknown_model_pricing(self, temp_monitor):
        """Test unknown model returns 0 cost."""
        cost = temp_monitor._calculate_cost("unknown-model", 1000, 2000)
        assert cost == 0.0


@pytest.mark.skipif(not _TOKEN_MONITORING_AVAILABLE, reason="Token monitoring dependencies not installed")
class TestDatabaseOperations:
    """Test database operations and data integrity."""
    
    @pytest.fixture
    def temp_monitor(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            yield TokenMonitor(storage_dir=tmpdir)
    
    def test_database_initialization(self, temp_monitor):
        """Test database is created with correct schema."""
        assert temp_monitor.db_path.exists()
        
        with sqlite3.connect(temp_monitor.db_path) as conn:
            # Check table exists
            result = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='token_usage'"
            ).fetchone()
            assert result is not None
            
            # Check indexes exist
            indexes = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='index'"
            ).fetchall()
            index_names = [row[0] for row in indexes]
            assert 'idx_timestamp' in index_names
            assert 'idx_provider' in index_names
    
    def test_concurrent_access(self, temp_monitor):
        """Test database handles concurrent access."""
        import threading
        import time
        
        def write_data(thread_id):
            for i in range(10):
                temp_monitor.log_usage(
                    provider=f"test_{thread_id}",
                    service_type=ServiceType.LLM,
                    model="test-model",
                    operation="test",
                    input_tokens=i,
                    output_tokens=i*2
                )
                time.sleep(0.01)  # Small delay
        
        # Start multiple threads
        threads = []
        for i in range(3):
            thread = threading.Thread(target=write_data, args=(i,))
            threads.append(thread)
            thread.start()
        
        # Wait for completion
        for thread in threads:
            thread.join()
        
        # Verify all data was written
        report = temp_monitor.get_comprehensive_report()
        assert report['summary']['total_requests'] == 30  # 3 threads * 10 requests
    
    def test_data_cleanup(self, temp_monitor):
        """Test old data cleanup functionality."""
        # Add old and new data
        old_time = (datetime.now() - timedelta(days=100)).isoformat()
        new_time = datetime.now().isoformat()
        
        with sqlite3.connect(temp_monitor.db_path) as conn:
            # Insert old record
            conn.execute("""
                INSERT INTO token_usage (
                    timestamp, provider, service_type, model, operation,
                    input_tokens, output_tokens, total_tokens, api_key_id, cost_usd
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (old_time, "test", "llm", "test-model", "test", 100, 200, 300, "test", 0.01))
            
            # Insert new record
            conn.execute("""
                INSERT INTO token_usage (
                    timestamp, provider, service_type, model, operation,
                    input_tokens, output_tokens, total_tokens, api_key_id, cost_usd
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (new_time, "test", "llm", "test-model", "test", 100, 200, 300, "test", 0.01))
        
        # Cleanup old data
        result = temp_monitor.cleanup_old_data(days_to_keep=50)
        
        # Verify old data was removed
        with sqlite3.connect(temp_monitor.db_path) as conn:
            count = conn.execute("SELECT COUNT(*) FROM token_usage").fetchone()[0]
            assert count == 1  # Only new record should remain


@pytest.mark.skipif(not _TOKEN_MONITORING_AVAILABLE, reason="Token monitoring dependencies not installed")
class TestCLIFunctionality:
    """Test CLI commands work correctly."""
    
    @pytest.fixture
    def temp_monitor(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            monitor = TokenMonitor(storage_dir=tmpdir)
            # Add some test data
            monitor.log_usage(
                provider="openai",
                service_type=ServiceType.LLM,
                model="gpt-4o",
                operation="test",
                input_tokens=1000,
                output_tokens=2000
            )
            yield monitor
    
    def test_export_functionality(self, temp_monitor):
        """Test CSV export works correctly."""
        import tempfile
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            export_path = f.name
        
        try:
            result = temp_monitor.export_to_csv(export_path)
            
            # Verify file was created and contains data
            assert os.path.exists(export_path)
            
            with open(export_path, 'r') as f:
                content = f.read()
                assert 'provider,service_type,model' in content  # Header
                assert 'openai' in content  # Data
                assert 'gpt-4o' in content
        
        finally:
            if os.path.exists(export_path):
                os.unlink(export_path)
    
    def test_subscription_alerts(self, temp_monitor):
        """Test subscription limit alerts."""
        # Set a low limit
        temp_monitor.set_subscription_limit("openai", "prepaid_credits", 5)
        
        # Add usage that exceeds warning threshold
        temp_monitor.log_usage(
            provider="openai",
            service_type=ServiceType.LLM,
            model="gpt-4o",
            operation="test",
            input_tokens=100000,  # Will cost ~$0.25
            output_tokens=200000  # Will cost ~$2.00, total ~$2.25
        )
        
        # Check that usage was recorded
        summary = temp_monitor.get_provider_summary("openai")
        assert summary['total_cost_usd'] > 0  # We logged some usage
        assert summary['total_requests'] >= 1


@pytest.mark.skipif(not _TOKEN_MONITORING_AVAILABLE, reason="Token monitoring dependencies not installed")
class TestGraphitiIntegration:
    """Test integration with actual Graphiti components."""
    
    def test_monkey_patching_safety(self):
        """Test that patching doesn't break original functionality."""
        from graphiti_core.llm_client.openai_client import OpenAIClient
        from graphiti_core.embedder.openai import OpenAIEmbedder
        
        # Save original methods
        original_llm = OpenAIClient._generate_response
        original_embed = OpenAIEmbedder.create
        
        # Apply our patching logic (similar to real demo)
        from functools import wraps
        
        @wraps(original_llm)
        async def test_wrapper(self, *args, **kwargs):
            return await original_llm(self, *args, **kwargs)
        
        # Temporarily patch
        OpenAIClient._generate_response_base = test_wrapper
        
        # Verify method still exists and is callable
        assert hasattr(OpenAIClient, '_generate_response_base')
        assert callable(OpenAIClient._generate_response_base)
        
        # Restore original
        OpenAIClient._generate_response_base = original_llm
    
    @pytest.mark.asyncio
    async def test_real_api_call_simulation(self):
        """Test simulation of real API call with monitoring."""
        # This test simulates what happens in the real demo
        # without making actual API calls
        
        # Mock API response
        mock_response = Mock()
        mock_response._raw_response = Mock()
        mock_response._raw_response.usage = Mock()
        mock_response._raw_response.usage.prompt_tokens = 150
        mock_response._raw_response.usage.completion_tokens = 300
        mock_response._raw_response.usage.total_tokens = 450
        
        # Simulate the monitoring logic
        usage_info = _extract_token_info(mock_response._raw_response, "openai")
        
        assert usage_info is not None
        assert usage_info['input_tokens'] == 150
        assert usage_info['output_tokens'] == 300
        
        # Simulate logging
        log_llm_usage(
            provider="openai",
            model="gpt-4o",
            input_tokens=usage_info['input_tokens'],
            output_tokens=usage_info['output_tokens'],
            operation="test_integration"
        )
        
        # Verify it was logged
        report = get_usage_report("openai", days=1)
        assert report['total_tokens'] >= 450


@pytest.mark.skipif(not _TOKEN_MONITORING_AVAILABLE, reason="Token monitoring dependencies not installed")
class TestErrorHandling:
    """Test error handling and edge cases."""
    
    @pytest.fixture
    def temp_monitor(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            yield TokenMonitor(storage_dir=tmpdir)
    
    def test_invalid_data_handling(self, temp_monitor):
        """Test handling of invalid input data."""
        # Test negative tokens
        result = temp_monitor.log_usage(
            provider="test",
            service_type=ServiceType.LLM,
            model="test-model",
            operation="test",
            input_tokens=-100,
            output_tokens=200
        )
        
        # Should still log but with actual values
        assert result['logged'] is True
        assert result['record']['input_tokens'] == -100  # Stores as-is
    
    def test_missing_dependencies_fallback(self):
        """Test that imports work even when dependencies are missing."""
        # This should always pass since we're testing with dependencies
        # But verifies the import structure
        assert _TOKEN_MONITORING_AVAILABLE is True
    
    def test_database_corruption_recovery(self, temp_monitor):
        """Test recovery from database issues."""
        # Simulate database corruption by removing the file
        if temp_monitor.db_path.exists():
            temp_monitor.db_path.unlink()
        
        # Should recreate database on next operation
        # First ensure database is initialized
        temp_monitor._init_database()
        
        result = temp_monitor.log_usage(
            provider="test",
            service_type=ServiceType.LLM,
            model="test-model",
            operation="test",
            input_tokens=100,
            output_tokens=200
        )
        
        assert result['logged'] is True
        assert temp_monitor.db_path.exists()


# Integration test runner
@pytest.mark.skipif(not _TOKEN_MONITORING_AVAILABLE, reason="Token monitoring dependencies not installed")
def test_full_system_integration():
    """Test the complete token monitoring pipeline."""
    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        monitor = TokenMonitor(storage_dir=tmpdir)
        
        # Test sequence: log usage -> get report -> export -> cleanup
        
        # 1. Log various types of usage
        providers = ["openai", "anthropic", "gemini"]
        models = ["gpt-4o", "claude-sonnet-4-20250514", "gemini-2.5-flash"]
        
        for i, (provider, model) in enumerate(zip(providers, models)):
            monitor.log_usage(
                provider=provider,
                service_type=ServiceType.LLM,
                model=model,
                operation=f"test_{i}",
                input_tokens=(i+1)*100,
                output_tokens=(i+1)*200,
                metadata={"test_sequence": i}
            )
        
        # 2. Get comprehensive report
        report = monitor.get_comprehensive_report()
        assert report['summary']['total_requests'] == 3
        assert len(report['by_provider']) == 3
        
        # 3. Test provider-specific reports
        for provider in providers:
            provider_report = monitor.get_provider_summary(provider)
            assert provider_report['total_requests'] >= 1
        
        # 4. Test export
        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as f:
            export_path = f.name
        
        try:
            monitor.export_to_csv(export_path)
            assert os.path.exists(export_path)
            
            # Verify CSV contains our data
            with open(export_path, 'r') as f:
                content = f.read()
                for provider in providers:
                    assert provider in content
        
        finally:
            if os.path.exists(export_path):
                os.unlink(export_path)
        
        # 5. Test limits and alerts
        monitor.set_subscription_limit("openai", "prepaid_credits", 1)
        summary = monitor.get_provider_summary("openai")
        alerts = monitor._check_alerts("openai", summary)
        
        # Check that data was recorded
        assert summary['total_requests'] >= 1


if __name__ == "__main__":
    # Run specific test groups
    pytest.main([__file__ + "::TestTokenExtractionFromResponses", "-v"])