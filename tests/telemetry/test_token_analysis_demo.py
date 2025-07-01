"""
Tests for the token analysis demo that uses LLM to analyze monitoring data.
This ensures the demo will work correctly before implementation.
"""

import pytest
import asyncio
import os
import tempfile
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, AsyncMock
from pathlib import Path


class TestTokenAnalysisDemoPrerequisites:
    """Test prerequisites for the token analysis demo."""
    
    def test_required_imports_available(self):
        """Test that all required imports are available."""
        # Test token monitoring imports
        try:
            from graphiti_core.telemetry import (
                get_usage_report,
                get_token_monitor,
                _TOKEN_MONITORING_AVAILABLE
            )
            assert _TOKEN_MONITORING_AVAILABLE, "Token monitoring should be available"
        except ImportError as e:
            pytest.fail(f"Required token monitoring imports failed: {e}")
        
        # Test Graphiti imports
        try:
            from graphiti_core import Graphiti
            from graphiti_core.prompts.models import Message
        except ImportError as e:
            pytest.fail(f"Required Graphiti imports failed: {e}")
    
    def test_token_monitoring_data_available(self):
        """Test that token monitoring has some data to analyze."""
        from graphiti_core.telemetry import get_usage_report, get_token_monitor
        
        # Check usage report
        usage_report = get_usage_report("openai", days=1)
        assert isinstance(usage_report, dict), "Usage report should be a dictionary"
        
        # Check that we have some usage data from previous demos
        total_requests = usage_report.get('total_requests', 0)
        assert total_requests > 0, "Should have some requests from previous demos"
        
        # Check comprehensive report functionality
        monitor = get_token_monitor()
        comprehensive_report = monitor.get_comprehensive_report()
        assert isinstance(comprehensive_report, dict), "Comprehensive report should be a dictionary"
        assert 'summary' in comprehensive_report, "Report should have summary section"
    
    def test_api_key_available(self):
        """Test that OpenAI API key is available for LLM analysis."""
        api_key = os.getenv("OPENAI_API_KEY")
        assert api_key, "OPENAI_API_KEY should be set for LLM analysis"
        assert api_key.startswith("sk-"), "API key should be valid format"


class TestTokenAnalysisDemoLogic:
    """Test the core logic that will be used in the demo."""
    
    def test_usage_report_formatting_for_analysis(self):
        """Test formatting usage report data for LLM analysis."""
        # Mock usage report data (based on real structure)
        mock_usage_report = {
            'provider': 'openai',
            'total_requests': 25,
            'total_tokens': 1500,
            'total_cost_usd': 0.05,
            'by_service_type': {
                'embedding': {'requests': 15, 'tokens': 500, 'cost_usd': 0.001},
                'llm': {'requests': 10, 'tokens': 1000, 'cost_usd': 0.049}
            },
            'by_model': [
                {'model': 'text-embedding-3-small', 'requests': 15, 'tokens': 500},
                {'model': 'gpt-4o', 'requests': 10, 'tokens': 1000}
            ]
        }
        
        # Test formatting function (we'll implement this)
        def format_usage_for_analysis(usage_report):
            if not usage_report:
                return "No usage data found."
            
            formatted = f"""
            Provider: {usage_report.get('provider', 'unknown')}
            Total Requests: {usage_report.get('total_requests', 0)}
            Total Tokens: {usage_report.get('total_tokens', 0):,}
            Total Cost: ${usage_report.get('total_cost_usd', 0):.4f}
            
            By Service Type:
            """
            
            for service, stats in usage_report.get('by_service_type', {}).items():
                formatted += f"- {service}: {stats['requests']} requests, {stats['tokens']} tokens\n"
            
            return formatted.strip()
        
        result = format_usage_for_analysis(mock_usage_report)
        
        assert "Provider: openai" in result
        assert "Total Requests: 25" in result
        assert "Total Tokens: 1,500" in result
        assert "$0.0500" in result
        assert "embedding: 15 requests" in result
        assert "llm: 10 requests" in result
    
    def test_entity_structure_creation(self):
        """Test creation of structured entities from analysis."""
        # Mock usage report
        mock_usage_report = {
            'total_requests': 25,
            'total_tokens': 1500,
            'total_cost_usd': 0.05,
            'by_service_type': {
                'embedding': {'tokens': 500},
                'llm': {'tokens': 1000}
            }
        }
        
        mock_recent_ops = [{'operation': 'test'}] * 10
        
        # Test entity structure creation
        def create_entity_structure(usage_report, num_requests):
            return {
                "analysis_session": {
                    "id": f"token_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    "timestamp": datetime.now().isoformat(),
                    "data_period": "24_hours",
                    "requests_analyzed": num_requests
                },
                "usage_metrics": {
                    "total_requests": usage_report.get('total_requests', 0),
                    "total_tokens": usage_report.get('total_tokens', 0),
                    "total_cost": usage_report.get('total_cost_usd', 0),
                    "primary_service": max(usage_report.get('by_service_type', {}).items(), 
                                         key=lambda x: x[1]['tokens'], default=('unknown', {'tokens': 0}))[0]
                }
            }
        
        entity_structure = create_entity_structure(mock_usage_report, 25)
        
        # Verify structure
        assert "analysis_session" in entity_structure
        assert "usage_metrics" in entity_structure
        assert entity_structure["analysis_session"]["requests_analyzed"] == 25
        assert entity_structure["usage_metrics"]["total_tokens"] == 1500
        assert entity_structure["usage_metrics"]["primary_service"] == "llm"
    
    def test_analysis_prompt_generation(self):
        """Test generation of analysis prompt for LLM."""
        mock_usage_report = {
            'total_requests': 25,
            'total_tokens': 1500,
            'total_cost_usd': 0.05,
            'by_service_type': {'embedding': {'tokens': 500}},
            'by_model': {'gpt-4o': {'tokens': 1000}}
        }
        
        # Test prompt creation
        def create_analysis_prompt(usage_report):
            return f"""
            Analyze the following token monitoring data:
            
            USAGE SUMMARY:
            - Total Requests: {usage_report.get('total_requests', 0)}
            - Total Tokens: {usage_report.get('total_tokens', 0):,}
            - Total Cost: ${usage_report.get('total_cost_usd', 0):.4f}
            - By Service: {usage_report.get('by_service_type', {})}
            
            Please provide insights about usage patterns and optimization opportunities.
            """
        
        prompt = create_analysis_prompt(mock_usage_report)
        
        assert "Total Requests: 25" in prompt
        assert "Total Tokens: 1,500" in prompt
        assert "$0.0500" in prompt
        assert "insights about usage patterns" in prompt
        assert "By Service:" in prompt


class TestTokenAnalysisDemoIntegration:
    """Test integration aspects of the demo."""
    
    @pytest.mark.asyncio
    async def test_graphiti_connection_works(self):
        """Test that Graphiti connection works for the demo."""
        from graphiti_core import Graphiti
        
        uri = "bolt://localhost:7687"
        username = "neo4j"
        password = "pepo_graphiti_2025"
        
        try:
            graphiti = Graphiti(uri, username, password)
            await graphiti.build_indices_and_constraints()
            await graphiti.close()
            # If we get here, connection works
            assert True
        except Exception as e:
            pytest.fail(f"Graphiti connection failed: {e}")
    
    def test_episode_parameters_correct(self):
        """Test that add_episode is called with correct parameters."""
        # This test validates the fix for add_episode parameters
        required_params = ['name', 'episode_body', 'source_description', 'reference_time']
        
        # Check the demo file has correct parameters
        demo_file = Path("/Users/pepo/graphiti-pepo-local/examples/token_analysis_demo.py")
        if demo_file.exists():
            content = demo_file.read_text()
            assert 'name="Token Usage Analysis Report"' in content
            assert 'source_description="LLM-generated analysis of token monitoring data"' in content
            assert 'reference_time=datetime.now()' in content
    
    @pytest.mark.asyncio
    async def test_llm_client_available(self):
        """Test that LLM client is available for analysis."""
        from graphiti_core import Graphiti
        from graphiti_core.prompts.models import Message
        
        uri = "bolt://localhost:7687" 
        username = "neo4j"
        password = "pepo_graphiti_2025"
        
        try:
            graphiti = Graphiti(uri, username, password)
            
            # Test that llm_client exists and has required methods
            assert hasattr(graphiti, 'llm_client'), "Graphiti should have llm_client"
            assert hasattr(graphiti.llm_client, '_generate_response'), "LLM client should have _generate_response"
            
            await graphiti.close()
            
        except Exception as e:
            pytest.fail(f"LLM client test failed: {e}")
    
    def test_patching_function_available(self):
        """Test that token monitoring patching is available."""
        try:
            from examples.token_monitoring_real_demo import patch_graphiti_for_monitoring
            
            # Function should exist and be callable
            assert callable(patch_graphiti_for_monitoring), "Patching function should be callable"
            
        except ImportError as e:
            pytest.fail(f"Patching function not available: {e}")


class TestDemoFileStructure:
    """Test the planned demo file structure."""
    
    def test_demo_script_location(self):
        """Test that demo script exists in correct location."""
        expected_path = Path("/Users/pepo/graphiti-pepo-local/examples/token_analysis_demo.py")
        
        # The file should now exist
        assert expected_path.exists(), "Demo script should exist"
        assert expected_path.is_file(), "Demo script should be a file"
    
    def test_demo_script_functions(self):
        """Test that all required functions are in the demo script."""
        demo_file = Path("/Users/pepo/graphiti-pepo-local/examples/token_analysis_demo.py")
        content = demo_file.read_text()
        
        # Check all main functions exist
        required_functions = [
            "def format_usage_for_analysis",
            "def create_analysis_prompt",
            "def create_entity_structure",
            "async def analyze_token_usage_with_llm",
            "async def main"
        ]
        
        for func in required_functions:
            assert func in content, f"Demo should contain {func}"
    
    def test_demo_script_imports(self):
        """Test that all required imports are in the demo script."""
        demo_file = Path("/Users/pepo/graphiti-pepo-local/examples/token_analysis_demo.py")
        content = demo_file.read_text()
        
        # Check critical imports
        required_imports = [
            "from graphiti_core.telemetry import",
            "from graphiti_core import Graphiti",
            "from graphiti_core.prompts.models import Message",
            "from examples.token_monitoring_real_demo import patch_graphiti_for_monitoring"
        ]
        
        for imp in required_imports:
            assert imp in content, f"Demo should import {imp}"
    
    def test_required_dependencies_structure(self):
        """Test that all required dependencies are properly structured."""
        # Test imports work from examples directory context
        examples_dir = Path("/Users/pepo/graphiti-pepo-local/examples")
        
        # Test that we can import from parent directory (this is what the script will do)
        import sys
        original_path = sys.path.copy()
        
        try:
            sys.path.insert(0, str(examples_dir.parent))
            
            # These imports should work from the demo script
            from graphiti_core.telemetry import get_usage_report
            from graphiti_core import Graphiti
            from graphiti_core.prompts.models import Message
            
            # Test passed if no ImportError
            assert True
            
        except ImportError as e:
            pytest.fail(f"Demo dependencies not properly structured: {e}")
        finally:
            sys.path = original_path


if __name__ == "__main__":
    pytest.main([__file__, "-v"])