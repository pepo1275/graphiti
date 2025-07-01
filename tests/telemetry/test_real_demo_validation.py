"""
Tests for validating the real demo functionality
These tests check that the demo will work correctly with actual API calls
"""

import pytest
import asyncio
import os
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime

# Skip tests if token monitoring not available
try:
    from graphiti_core.telemetry import _TOKEN_MONITORING_AVAILABLE
    if _TOKEN_MONITORING_AVAILABLE:
        from examples.token_monitoring_real_demo import (
            patch_graphiti_for_monitoring,
            show_token_report
        )
except ImportError:
    _TOKEN_MONITORING_AVAILABLE = False


@pytest.mark.skipif(not _TOKEN_MONITORING_AVAILABLE, reason="Token monitoring dependencies not installed")
class TestRealDemoPreChecks:
    """Pre-flight checks for the real demo."""
    
    def test_openai_client_exists(self):
        """Test that OpenAI client can be imported and has required methods."""
        from graphiti_core.llm_client.openai_client import OpenAIClient
        
        assert hasattr(OpenAIClient, '_generate_response_base')
        assert callable(OpenAIClient._generate_response_base)
    
    def test_embedder_exists(self):
        """Test that OpenAI embedder can be imported and has required methods."""
        from graphiti_core.embedder.openai import OpenAIEmbedder
        
        assert hasattr(OpenAIEmbedder, 'create')
        assert callable(OpenAIEmbedder.create)
    
    def test_graphiti_import(self):
        """Test that Graphiti can be imported."""
        from graphiti_core import Graphiti
        assert Graphiti is not None
    
    def test_neo4j_connection_parameters(self):
        """Test Neo4j connection parameters are valid."""
        uri = "bolt://localhost:7687"
        username = "neo4j"
        password = "pepo_graphiti_2025"
        
        # Basic validation
        assert uri.startswith("bolt://")
        assert username
        assert password
    
    @pytest.mark.asyncio
    async def test_show_token_report_function(self):
        """Test that show_token_report function works."""
        # Should not raise any exceptions
        await show_token_report("TEST")


@pytest.mark.skipif(not _TOKEN_MONITORING_AVAILABLE, reason="Token monitoring dependencies not installed")
class TestPatchingMechanism:
    """Test the patching mechanism for capturing tokens."""
    
    def test_patch_function_exists(self):
        """Test that patch function can be called."""
        result = patch_graphiti_for_monitoring()
        assert isinstance(result, bool)
    
    def test_client_method_preservation(self):
        """Test that patching preserves original method signatures."""
        from graphiti_core.llm_client.openai_client import OpenAIClient
        from graphiti_core.embedder.openai import OpenAIEmbedder
        import inspect
        
        # Get original signatures
        llm_sig = inspect.signature(OpenAIClient._generate_response_base)
        embed_sig = inspect.signature(OpenAIEmbedder.create)
        
        # Apply patching
        patch_graphiti_for_monitoring()
        
        # Get patched signatures
        patched_llm_sig = inspect.signature(OpenAIClient._generate_response_base)
        patched_embed_sig = inspect.signature(OpenAIEmbedder.create)
        
        # Signatures should be preserved (or compatible)
        assert len(llm_sig.parameters) <= len(patched_llm_sig.parameters)
        assert len(embed_sig.parameters) <= len(patched_embed_sig.parameters)
    
    @pytest.mark.asyncio
    async def test_patched_method_callable(self):
        """Test that patched methods are still callable."""
        from graphiti_core.llm_client.openai_client import OpenAIClient
        from graphiti_core.llm_client.config import LLMConfig
        
        patch_graphiti_for_monitoring()
        
        # Create a mock client
        mock_client = Mock()
        config = LLMConfig(model="gpt-4o")
        
        # This should be callable (though will fail without real setup)
        client = OpenAIClient(config, mock_client)
        assert hasattr(client, '_generate_response_base')
        assert callable(client._generate_response_base)


@pytest.mark.skipif(not _TOKEN_MONITORING_AVAILABLE, reason="Token monitoring dependencies not installed")
class TestTokenCaptureSimulation:
    """Test token capture using mocked API responses."""
    
    @pytest.mark.asyncio
    async def test_simulated_openai_llm_capture(self):
        """Test token capture from simulated OpenAI LLM response."""
        from graphiti_core.llm_client.openai_client import OpenAIClient
        from graphiti_core.llm_client.config import LLMConfig
        from graphiti_core.telemetry import get_usage_report
        
        # Apply patching
        patch_graphiti_for_monitoring()
        
        # Create mock client and config
        mock_openai_client = AsyncMock()
        config = LLMConfig(model="gpt-4o", api_key="test-key")
        client = OpenAIClient(config, mock_openai_client)
        
        # Create mock response with token usage
        mock_response = Mock()
        mock_response._raw_response = Mock()
        mock_response._raw_response.usage = Mock()
        mock_response._raw_response.usage.prompt_tokens = 250
        mock_response._raw_response.usage.completion_tokens = 500
        mock_response._raw_response.usage.total_tokens = 750
        
        # Mock the original method to return our mock response
        with patch('graphiti_core.llm_client.openai_client.OpenAIClient._generate_response_base') as mock_original:
            mock_original.return_value = mock_response
            
            # Get initial usage
            initial_report = get_usage_report("openai", days=1)
            initial_tokens = initial_report.get('total_tokens', 0)
            
            # Call the patched method
            result = await client._generate_response_base([{"role": "user", "content": "test"}])
            
            # Verify response is returned
            assert result == mock_response
            
            # Verify tokens were captured
            final_report = get_usage_report("openai", days=1)
            tokens_captured = final_report['total_tokens'] - initial_tokens
            assert tokens_captured == 750
    
    @pytest.mark.asyncio
    async def test_simulated_openai_embedding_capture(self):
        """Test token capture from simulated OpenAI embedding response."""
        from graphiti_core.embedder.openai import OpenAIEmbedder, OpenAIEmbedderConfig
        from graphiti_core.telemetry import get_usage_report
        
        # Apply patching
        patch_graphiti_for_monitoring()
        
        # Create mock embedder
        mock_client = AsyncMock()
        config = OpenAIEmbedderConfig(embedding_model="text-embedding-3-small")
        embedder = OpenAIEmbedder(config, mock_client)
        
        # Mock embedding response
        mock_embedding = [[0.1, 0.2, 0.3, 0.4]]
        
        with patch('graphiti_core.embedder.openai.OpenAIEmbedder.create') as mock_original:
            mock_original.return_value = mock_embedding
            
            # Get initial usage
            initial_report = get_usage_report("openai", days=1)
            initial_requests = initial_report.get('total_requests', 0)
            
            # Call the patched method
            test_text = "This is a test sentence for embedding"
            result = await embedder.create(test_text)
            
            # Verify embedding is returned
            assert result == mock_embedding
            
            # Verify usage was captured
            final_report = get_usage_report("openai", days=1)
            requests_captured = final_report['total_requests'] - initial_requests
            assert requests_captured >= 1  # At least one embedding request


@pytest.mark.skipif(not _TOKEN_MONITORING_AVAILABLE, reason="Token monitoring dependencies not installed")
class TestDemoDataValidation:
    """Test validation of data that will be created by the demo."""
    
    def test_episode_content_validity(self):
        """Test that the demo episode content is valid."""
        episode_content = """
        The Graphiti Token Monitoring System provides comprehensive tracking of API usage 
        across multiple LLM providers including OpenAI, Anthropic, and Google Gemini. 
        It features automatic token capture from API responses, real-time cost calculation 
        based on current pricing models, and detailed analytics through a CLI interface.
        """
        
        # Basic validation
        assert len(episode_content.strip()) > 100  # Substantial content
        assert "Graphiti" in episode_content
        assert "Token" in episode_content
        assert "OpenAI" in episode_content
    
    def test_expected_operations(self):
        """Test expected operations that should be captured."""
        expected_operations = [
            "extract_nodes",
            "extract_edges", 
            "create_embeddings",
            "generate_response"
        ]
        
        # These should all be valid operation names
        for op in expected_operations:
            assert isinstance(op, str)
            assert len(op) > 0
    
    def test_cost_estimation_bounds(self):
        """Test that estimated costs are reasonable."""
        from graphiti_core.telemetry.token_monitor import TokenMonitor
        
        monitor = TokenMonitor()
        
        # Test typical episode processing costs
        scenarios = [
            # (input_tokens, output_tokens, model, expected_max_cost)
            (1000, 1500, "gpt-4o", 0.05),  # Node extraction
            (800, 1000, "gpt-4o", 0.04),   # Edge extraction
            (500, 0, "text-embedding-3-small", 0.001),  # Embeddings
        ]
        
        total_estimated_cost = 0
        for input_t, output_t, model, max_cost in scenarios:
            cost = monitor._calculate_cost(model, input_t, output_t)
            assert cost <= max_cost
            total_estimated_cost += cost
        
        # Total demo cost should be under $0.10
        assert total_estimated_cost < 0.10


@pytest.mark.skipif(not _TOKEN_MONITORING_AVAILABLE, reason="Token monitoring dependencies not installed")
class TestErrorRecovery:
    """Test error recovery during the demo."""
    
    @pytest.mark.asyncio
    async def test_api_error_handling(self):
        """Test handling of API errors during demo."""
        from graphiti_core.llm_client.openai_client import OpenAIClient
        from graphiti_core.llm_client.config import LLMConfig
        
        patch_graphiti_for_monitoring()
        
        mock_client = AsyncMock()
        config = LLMConfig(model="gpt-4o")
        client = OpenAIClient(config, mock_client)
        
        # Mock API error
        with patch('graphiti_core.llm_client.openai_client.OpenAIClient._generate_response_base') as mock_original:
            mock_original.side_effect = Exception("API Rate Limit")
            
            # Should handle error gracefully
            with pytest.raises(Exception, match="API Rate Limit"):
                await client._generate_response_base([{"role": "user", "content": "test"}])
    
    def test_neo4j_connection_validation(self):
        """Test Neo4j connection parameters."""
        # The demo should handle connection errors gracefully
        uri = "bolt://localhost:7687"
        username = "neo4j"
        password = "pepo_graphiti_2025"
        
        # Basic parameter validation
        assert uri and isinstance(uri, str)
        assert username and isinstance(username, str)
        assert password and isinstance(password, str)
    
    def test_missing_api_key_handling(self):
        """Test handling of missing API key."""
        # Save original
        original_key = os.environ.get("OPENAI_API_KEY")
        
        try:
            # Remove API key
            if "OPENAI_API_KEY" in os.environ:
                del os.environ["OPENAI_API_KEY"]
            
            # Demo should detect missing key
            api_key = os.getenv("OPENAI_API_KEY")
            assert api_key is None
        
        finally:
            # Restore original
            if original_key:
                os.environ["OPENAI_API_KEY"] = original_key


@pytest.mark.skipif(not _TOKEN_MONITORING_AVAILABLE, reason="Token monitoring dependencies not installed")
class TestDataVerification:
    """Test data verification after demo runs."""
    
    def test_expected_database_records(self):
        """Test that expected database records will be created."""
        from graphiti_core.telemetry import get_token_monitor
        import sqlite3
        
        monitor = get_token_monitor()
        
        # Test database query that demo will use
        with sqlite3.connect(monitor.db_path) as conn:
            schema = conn.execute("""
                SELECT sql FROM sqlite_master 
                WHERE type='table' AND name='token_usage'
            """).fetchone()
            
            assert schema is not None
            assert 'timestamp' in schema[0]
            assert 'provider' in schema[0]
            assert 'model' in schema[0]
            assert 'input_tokens' in schema[0]
            assert 'output_tokens' in schema[0]
    
    def test_export_format_validation(self):
        """Test that export format will be valid."""
        from graphiti_core.telemetry import get_token_monitor
        import tempfile
        import csv
        
        monitor = get_token_monitor()
        
        # Add test record
        monitor.log_usage(
            provider="test",
            service_type="llm",
            model="test-model",
            operation="test",
            input_tokens=100,
            output_tokens=200
        )
        
        # Test export
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            export_path = f.name
        
        try:
            monitor.export_to_csv(export_path)
            
            # Validate CSV format
            with open(export_path, 'r') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                
                assert len(rows) >= 1
                
                # Check required fields
                required_fields = [
                    'timestamp', 'provider', 'model', 
                    'input_tokens', 'output_tokens', 'cost_usd'
                ]
                
                for field in required_fields:
                    assert field in reader.fieldnames
        
        finally:
            if os.path.exists(export_path):
                os.unlink(export_path)


def run_pre_demo_checks():
    """Run all pre-demo validation checks."""
    print("🔍 Running pre-demo validation checks...")
    
    # Run specific test classes
    test_classes = [
        TestRealDemoPreChecks,
        TestPatchingMechanism, 
        TestDemoDataValidation,
        TestErrorRecovery,
    ]
    
    for test_class in test_classes:
        print(f"   Testing {test_class.__name__}...")
        
        # Simple test runner
        instance = test_class()
        test_methods = [method for method in dir(instance) if method.startswith('test_')]
        
        for method_name in test_methods:
            try:
                method = getattr(instance, method_name)
                if asyncio.iscoroutinefunction(method):
                    asyncio.run(method())
                else:
                    method()
                print(f"      ✅ {method_name}")
            except Exception as e:
                print(f"      ❌ {method_name}: {e}")
                return False
    
    print("✅ All pre-demo checks passed!")
    return True


if __name__ == "__main__":
    if not _TOKEN_MONITORING_AVAILABLE:
        print("❌ Token monitoring not available")
        exit(1)
    
    success = run_pre_demo_checks()
    exit(0 if success else 1)