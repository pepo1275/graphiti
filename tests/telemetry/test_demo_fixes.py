"""
Tests for fixes made to the token monitoring demo and utilities.
"""

import pytest
import subprocess
import os
from pathlib import Path


class TestDemoFixes:
    """Test fixes made to the demo system."""
    
    def test_run_script_exists_and_executable(self):
        """Test that run.sh script exists and is executable."""
        script_path = Path("/Users/pepo/graphiti-pepo-local/run.sh")
        
        assert script_path.exists(), "run.sh script should exist"
        assert os.access(script_path, os.X_OK), "run.sh should be executable"
        
        # Test basic functionality
        result = subprocess.run([str(script_path)], capture_output=True, text=True)
        assert "Usage:" in result.stdout, "run.sh should show usage when called without args"
    
    def test_confirm_flag_logic(self):
        """Test that --confirm flag logic is correctly implemented."""
        # Read the demo file content
        demo_file = Path("/Users/pepo/graphiti-pepo-local/examples/token_monitoring_real_demo.py")
        content = demo_file.read_text()
        
        # Check that main function accepts skip_confirmation parameter
        assert "async def main(skip_confirmation=False):" in content, \
            "main function should accept skip_confirmation parameter"
        
        # Check that --confirm flag passes skip_confirmation=True
        assert "asyncio.run(main(skip_confirmation=True))" in content, \
            "--confirm flag should pass skip_confirmation=True"
        
        # Check that confirmation is skipped when flag is True
        assert "if not skip_confirmation:" in content, \
            "should check skip_confirmation before asking for input"
    
    def test_method_signature_fixes(self):
        """Test that method signatures are correctly fixed."""
        demo_file = Path("/Users/pepo/graphiti-pepo-local/examples/token_monitoring_real_demo.py")
        content = demo_file.read_text()
        
        # Check that monitored_llm_generate has correct signature
        expected_signature = "async def monitored_llm_generate(self, messages, response_model=None, max_tokens=DEFAULT_MAX_TOKENS, model_size=ModelSize.medium)"
        assert expected_signature in content, \
            "monitored_llm_generate should have correct signature matching _generate_response"
        
        # Check that required imports are present
        assert "from graphiti_core.llm_client.config import DEFAULT_MAX_TOKENS, ModelSize" in content, \
            "should import required constants"
        
        # Check that original method is called with correct parameters
        assert "await original_llm_generate(self, messages, response_model, max_tokens, model_size)" in content, \
            "should call original method with all parameters"
    
    def test_attribute_name_fixes(self):
        """Test that attribute names are correctly fixed."""
        demo_file = Path("/Users/pepo/graphiti-pepo-local/examples/token_monitoring_real_demo.py")
        content = demo_file.read_text()
        
        # Check that self.model is used instead of self.llm_config.model
        assert "self.model" in content, "should use self.model"
        assert "self.llm_config.model" not in content, "should not use self.llm_config.model"
        
        # Count occurrences to ensure all were fixed
        model_usages = content.count("self.model")
        assert model_usages >= 3, f"should have at least 3 usages of self.model, found {model_usages}"
    
    def test_embedder_parameter_fixes(self):
        """Test that embedder parameter names are correctly fixed."""
        demo_file = Path("/Users/pepo/graphiti-pepo-local/examples/token_monitoring_real_demo.py")
        content = demo_file.read_text()
        
        # Check that input_data is used instead of input_text
        assert "async def monitored_embedder_create(self, input_data, **kwargs):" in content, \
            "monitored_embedder_create should use input_data parameter"
        
        assert "isinstance(input_data, list)" in content, \
            "should check isinstance on input_data, not input_text"
        
        assert "await original_embedder_create(self, input_data, **kwargs)" in content, \
            "should call original embedder with input_data parameter"


class TestConvenienceImprovements:
    """Test convenience improvements made to the project."""
    
    def test_run_script_functionality(self):
        """Test the run.sh script functionality."""
        script_path = Path("/Users/pepo/graphiti-pepo-local/run.sh")
        content = script_path.read_text()
        
        # Check basic structure
        assert "#!/bin/bash" in content, "should have bash shebang"
        assert "exec uv run python" in content, "should use uv run python"
        assert "Usage:" in content, "should have usage instructions"
        
        # Check parameter handling
        assert '"$@"' in content, "should pass all arguments through"


class TestModelNameFixes:
    """Test fixes for model names in OpenAI client."""
    
    def test_correct_model_names(self):
        """Test that model names are correct."""
        client_file = Path("/Users/pepo/graphiti-pepo-local/graphiti_core/llm_client/openai_base_client.py")
        content = client_file.read_text()
        
        # Check model names are valid
        assert "DEFAULT_MODEL = 'gpt-4o-mini'" in content, "DEFAULT_MODEL should be gpt-4o-mini"
        assert "DEFAULT_SMALL_MODEL = 'gpt-3.5-turbo'" in content, "DEFAULT_SMALL_MODEL should be gpt-3.5-turbo"
        
        # Ensure invalid names are not present
        assert "gpt-4.1-mini" not in content, "Invalid model name should not be present"
        assert "gpt-4.1-nano" not in content, "Invalid model name should not be present"


class TestAnalysisPromptFixes:
    """Test fixes for analysis prompt to include JSON keyword."""
    
    def test_json_keyword_in_prompt(self):
        """Test that analysis prompt includes 'json' keyword."""
        demo_file = Path("/Users/pepo/graphiti-pepo-local/examples/token_analysis_demo.py")
        content = demo_file.read_text()
        
        # Check that prompt includes json keyword
        assert "json-like organization" in content, "Prompt should mention json to satisfy OpenAI requirements"
    
    def test_project_structure_consistency(self):
        """Test that project structure remains consistent."""
        # Key files should still exist
        key_files = [
            "/Users/pepo/graphiti-pepo-local/examples/token_monitoring_real_demo.py",
            "/Users/pepo/graphiti-pepo-local/graphiti_core/telemetry/token_monitor.py",
            "/Users/pepo/graphiti-pepo-local/graphiti_core/telemetry/token_integration.py",
            "/Users/pepo/graphiti-pepo-local/docs/SESSION_HANDOFF.md"
        ]
        
        for file_path in key_files:
            assert Path(file_path).exists(), f"Key file should exist: {file_path}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])