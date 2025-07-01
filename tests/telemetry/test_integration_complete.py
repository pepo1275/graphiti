"""
Integration tests for the complete token monitoring and analysis system.
Tests the full workflow from monitoring to analysis.
"""

import pytest
import asyncio
import os
from pathlib import Path
from datetime import datetime


class TestCompleteIntegration:
    """Test the complete integration of token monitoring and analysis."""
    
    def test_all_scripts_exist(self):
        """Test that all main scripts exist."""
        scripts = [
            "run.sh",
            "examples/token_monitoring_real_demo.py",
            "examples/token_analysis_demo.py",
            "graphiti_core/telemetry/token_monitor.py",
            "graphiti_core/telemetry/token_integration.py",
            "graphiti_core/telemetry/token_cli.py"
        ]
        
        for script in scripts:
            script_path = Path(f"/Users/pepo/graphiti-pepo-local/{script}")
            assert script_path.exists(), f"{script} should exist"
    
    def test_token_monitoring_available(self):
        """Test that token monitoring is available and functional."""
        from graphiti_core.telemetry import (
            _TOKEN_MONITORING_AVAILABLE,
            get_token_monitor,
            get_usage_report
        )
        
        assert _TOKEN_MONITORING_AVAILABLE, "Token monitoring should be available"
        
        # Get monitor instance
        monitor = get_token_monitor()
        assert monitor is not None, "Should get monitor instance"
        
        # Get usage report
        report = get_usage_report("openai", days=1)
        assert isinstance(report, dict), "Usage report should be a dictionary"
    
    def test_export_functionality(self):
        """Test that export functionality works."""
        import subprocess
        import tempfile
        
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as tmp:
            result = subprocess.run(
                ['./run.sh', '-m', 'graphiti_core.telemetry.token_cli', 
                 'export', tmp.name, '-d', '1'],
                capture_output=True,
                text=True,
                cwd="/Users/pepo/graphiti-pepo-local"
            )
            
            # Check export succeeded
            assert result.returncode == 0, f"Export should succeed: {result.stderr}"
            assert "Exported" in result.stdout, "Should show export confirmation"
            
            # Check file was created
            assert Path(tmp.name).exists(), "Export file should exist"
            assert Path(tmp.name).stat().st_size > 0, "Export file should have content"
            
            # Cleanup
            Path(tmp.name).unlink()
    
    def test_cli_commands_available(self):
        """Test that all CLI commands are available."""
        import subprocess
        
        # Test help command
        result = subprocess.run(
            ['./run.sh', '-m', 'graphiti_core.telemetry.token_cli', '--help'],
            capture_output=True,
            text=True,
            cwd="/Users/pepo/graphiti-pepo-local"
        )
        
        assert result.returncode == 0, "CLI help should work"
        
        # Check all commands are listed
        required_commands = ['status', 'summary', 'export', 'set-limit', 'cleanup', 'alerts']
        for cmd in required_commands:
            assert cmd in result.stdout, f"CLI should have {cmd} command"
    
    def test_database_initialized(self):
        """Test that token monitoring database is initialized."""
        db_path = Path.home() / ".graphiti" / "token_monitor" / "token_usage.db"
        assert db_path.exists(), "Token usage database should exist"
        assert db_path.stat().st_size > 0, "Database should have content"
    
    def test_config_file_exists(self):
        """Test that monitoring config file exists."""
        config_path = Path.home() / ".graphiti" / "token_monitor" / "monitor_config.json"
        assert config_path.exists(), "Monitor config should exist"
        
        # Check config is valid JSON
        import json
        with open(config_path) as f:
            config = json.load(f)
            assert isinstance(config, dict), "Config should be valid JSON"
    
    def test_fixes_applied(self):
        """Test that all critical fixes have been applied."""
        # Test 1: run.sh exists and is executable
        run_script = Path("/Users/pepo/graphiti-pepo-local/run.sh")
        assert run_script.exists(), "run.sh should exist"
        assert os.access(run_script, os.X_OK), "run.sh should be executable"
        
        # Test 2: Model names are correct
        client_file = Path("/Users/pepo/graphiti-pepo-local/graphiti_core/llm_client/openai_base_client.py")
        content = client_file.read_text()
        assert "gpt-4o-mini" in content, "Should have correct model name"
        assert "gpt-4.1-mini" not in content, "Should not have invalid model name"
        
        # Test 3: Demo flags work correctly
        demo_file = Path("/Users/pepo/graphiti-pepo-local/examples/token_monitoring_real_demo.py")
        content = demo_file.read_text()
        assert "skip_confirmation=True" in content, "Should have skip_confirmation parameter"
        
        # Test 4: Embedder parameter names correct
        assert "input_data" in content, "Should use input_data parameter"
        assert "async def monitored_embedder_create(self, input_text" not in content, \
            "Should not use input_text in embedder"
    
    def test_comprehensive_workflow(self):
        """Test that the complete workflow is functional."""
        # This test verifies the conceptual workflow without running actual demos
        
        # Step 1: Token monitoring can be initialized
        from graphiti_core.telemetry import get_token_monitor
        monitor = get_token_monitor()
        assert monitor is not None
        
        # Step 2: Usage data can be retrieved
        from graphiti_core.telemetry import get_usage_report
        report = get_usage_report("openai", days=1)
        assert 'total_requests' in report
        
        # Step 3: Analysis functions exist
        from examples.token_analysis_demo import (
            format_usage_for_analysis,
            create_analysis_prompt,
            create_entity_structure
        )
        
        # Test formatting
        formatted = format_usage_for_analysis(report)
        assert len(formatted) > 0
        
        # Test prompt creation
        prompt = create_analysis_prompt(report)
        assert "json" in prompt.lower()
        
        # Test entity structure
        entity = create_entity_structure(report, "test analysis")
        assert 'analysis_session' in entity
        assert 'usage_metrics' in entity


if __name__ == "__main__":
    pytest.main([__file__, "-v"])