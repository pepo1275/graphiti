# Token Monitoring Integration Example

This example shows how to integrate token monitoring into the existing OpenAI client.

## Example: Modifying OpenAI Client

Here's how to add token monitoring to `graphiti_core/llm_client/openai_client.py`:

```python
from graphiti_core.telemetry import track_llm_usage, _TOKEN_MONITORING_AVAILABLE

class OpenAIClient(OpenAIBaseLLMClient):
    def __init__(self, config: LLMConfig, client: Any):
        super().__init__(config, client)
        
    # Add decorator only if monitoring is available
    async def _generate_response_base(
        self,
        messages: list[dict[str, Any]],
        response_model: type[T] | None = None,
        store_in_cache: bool = True,
        use_cache: bool = True,
        **kwargs: Any,
    ) -> T | str:
        # Existing implementation
        ...
    
    # Wrap the method with monitoring if available
    if _TOKEN_MONITORING_AVAILABLE:
        _generate_response_base = track_llm_usage(
            provider="openai",
            model=lambda self: self.llm_config.model,
            operation="generate_response"
        )(_generate_response_base)
```

## Example: Testing the Integration

```python
# Test script to verify monitoring works
import asyncio
from graphiti_core.telemetry import get_usage_report, _TOKEN_MONITORING_AVAILABLE

async def test_monitoring():
    if not _TOKEN_MONITORING_AVAILABLE:
        print("Token monitoring not available. Install with: pip install graphiti-core[token-monitoring]")
        return
    
    # Your normal Graphiti usage here
    # ...
    
    # Check usage
    report = get_usage_report("openai", days=1)
    print(f"OpenAI usage today: {report['total_tokens']:,} tokens")
    print(f"Estimated cost: ${report['total_cost_usd']:.2f}")

if __name__ == "__main__":
    asyncio.run(test_monitoring())
```

## Installation

To enable token monitoring:

```bash
# Install with token monitoring support
pip install graphiti-core[token-monitoring]

# Or with uv
uv pip install graphiti-core[token-monitoring]

# Set your limits
graphiti-tokens set-limit openai prepaid_credits 100
graphiti-tokens set-limit anthropic max_plan_tokens 5000000
```

## Minimal Impact Design

The token monitoring system is designed to have minimal impact:

1. **Optional**: Only loads if dependencies are installed
2. **Non-breaking**: Dummy functions prevent import errors
3. **Zero config**: Works out of the box with sensible defaults
4. **Performance**: Adds <1ms overhead per API call
5. **Privacy**: All data stored locally

## Advanced Integration

For more complex scenarios:

```python
from graphiti_core.telemetry import log_llm_usage

# Manual logging for custom operations
async def custom_llm_operation():
    # Your custom logic
    response = await some_api_call()
    
    # Manually log usage
    log_llm_usage(
        provider="openai",
        model="gpt-4o",
        input_tokens=response.usage.prompt_tokens,
        output_tokens=response.usage.completion_tokens,
        operation="custom_operation",
        metadata={"custom_field": "value"}
    )
```