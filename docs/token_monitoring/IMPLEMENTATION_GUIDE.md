# Token Monitoring Implementation Guide

This guide explains how the token monitoring system is designed and how to integrate it into Graphiti.

## System Design

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Graphiti Application                      │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │ LLM Clients │  │  Embedders  │  │ Rerankers   │         │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘         │
│         │                 │                 │                 │
│         └─────────────────┼─────────────────┘                │
│                           │                                   │
│                    ┌──────▼──────┐                           │
│                    │ Decorators  │                           │
│                    │ @track_*    │                           │
│                    └──────┬──────┘                           │
│                           │                                   │
│                    ┌──────▼──────┐                           │
│                    │TokenMonitor │                           │
│                    └──────┬──────┘                           │
│                           │                                   │
└───────────────────────────┼───────────────────────────────────┘
                            │
                     ┌──────▼──────┐
                     │   SQLite    │
                     │  Database   │
                     └─────────────┘
```

### Component Responsibilities

1. **TokenMonitor**: Core logic, database operations, reporting
2. **Decorators**: Intercept API calls, extract token counts
3. **CLI Tool**: User interface for querying and configuration
4. **Integration Layer**: Bridges monitoring with existing code

## Integration Steps

### Step 1: Update LLM Clients

For each LLM client in `graphiti_core/llm_client/`:

```python
# Example: openai_client.py
from graphiti_core.telemetry import track_llm_usage

class OpenAIClient(OpenAIBaseLLMClient):
    def __init__(self, config: LLMConfig, client: Any):
        super().__init__(config, client)
        self.model_name = config.model
    
    @track_llm_usage(provider="openai", model=lambda self: self.model_name)
    async def _generate_response(self, messages: list[dict]) -> dict:
        # Existing implementation
        response = await self.client.chat.completions.create(...)
        return response
```

### Step 2: Update Embedding Clients

For each embedder in `graphiti_core/embedder/`:

```python
# Example: openai.py
from graphiti_core.telemetry import track_embedding_usage

class OpenAIEmbedder(Embedder):
    @track_embedding_usage(
        provider="openai", 
        model=lambda self: self.config.embedding_model
    )
    async def create(self, input: Union[str, List[str]]) -> List[List[float]]:
        # Existing implementation
        response = await self.client.embeddings.create(...)
        return response.data[0].embedding
```

### Step 3: Handle Provider-Specific Response Formats

Update `_extract_token_info()` in `token_integration.py` for each provider:

```python
def _extract_token_info(result: Any, provider: str) -> Optional[Dict[str, int]]:
    """Extract token usage information from API response."""
    
    # OpenAI format
    if provider == "openai" and hasattr(result, 'usage'):
        return {
            'input_tokens': result.usage.prompt_tokens,
            'output_tokens': result.usage.completion_tokens
        }
    
    # Anthropic format
    elif provider == "anthropic" and hasattr(result, 'usage'):
        return {
            'input_tokens': result.usage.input_tokens,
            'output_tokens': result.usage.output_tokens
        }
    
    # Gemini format
    elif provider == "gemini":
        if hasattr(result, 'usage_metadata'):
            return {
                'input_tokens': result.usage_metadata.prompt_token_count,
                'output_tokens': result.usage_metadata.candidates_token_count
            }
        elif hasattr(result, '_result') and hasattr(result._result, 'usage_metadata'):
            # Handle async response wrapper
            metadata = result._result.usage_metadata
            return {
                'input_tokens': metadata.prompt_token_count,
                'output_tokens': metadata.candidates_token_count
            }
    
    return None
```

### Step 4: Add CLI Entry Point

Update `pyproject.toml`:

```toml
[tool.poetry.scripts]
graphiti-tokens = "graphiti_core.telemetry.token_cli:cli"
```

Or for uv:

```toml
[project.scripts]
graphiti-tokens = "graphiti_core.telemetry.token_cli:cli"
```

### Step 5: Initialize Default Configuration

Create initialization script:

```python
# graphiti_core/telemetry/init_token_monitor.py
from graphiti_core.telemetry import get_token_monitor, set_provider_limit

def initialize_token_monitoring():
    """Initialize token monitoring with default limits."""
    monitor = get_token_monitor()
    
    # Set default limits (users should update these)
    set_provider_limit("anthropic", "max_plan_tokens", 5_000_000)
    set_provider_limit("openai", "prepaid_credits", 0)
    set_provider_limit("gemini", "free_tier_tokens", 1_000_000)
    
    print("Token monitoring initialized. Update limits with:")
    print("  graphiti-tokens set-limit <provider> <limit_type> <value>")
```

## Testing the Integration

### Unit Tests

```python
# tests/telemetry/test_token_monitor.py
import pytest
from graphiti_core.telemetry import get_token_monitor, ServiceType

def test_log_usage():
    monitor = get_token_monitor()
    result = monitor.log_usage(
        provider="openai",
        service_type=ServiceType.LLM,
        model="gpt-4o",
        operation="test",
        input_tokens=100,
        output_tokens=200
    )
    
    assert result["logged"] == True
    assert result["record"]["total_tokens"] == 300

def test_usage_summary():
    monitor = get_token_monitor()
    summary = monitor.get_provider_summary("openai", days=1)
    
    assert summary["provider"] == "openai"
    assert summary["total_tokens"] >= 300  # From previous test
```

### Integration Tests

```python
# tests/telemetry/test_integration.py
import pytest
from graphiti_core.telemetry import track_llm_usage

@track_llm_usage(provider="test", model="test-model")
async def mock_llm_call():
    # Simulate API response
    class MockResponse:
        class Usage:
            prompt_tokens = 50
            completion_tokens = 100
        usage = Usage()
    
    return MockResponse()

async def test_decorator_tracking():
    from graphiti_core.telemetry import get_token_monitor
    
    # Clear previous data
    monitor = get_token_monitor()
    
    # Make tracked call
    await mock_llm_call()
    
    # Verify tracking
    summary = monitor.get_provider_summary("test", days=1)
    assert summary["total_requests"] >= 1
    assert summary["total_tokens"] >= 150
```

## Best Practices

### 1. Error Handling

Always wrap API calls to ensure errors are tracked:

```python
@track_llm_usage(provider="openai", model="gpt-4o")
async def call_api(prompt: str):
    try:
        response = await client.chat.completions.create(...)
        return response
    except Exception as e:
        # The decorator will catch and log this
        raise
```

### 2. Custom Metadata

Add context to your tracking:

```python
from graphiti_core.telemetry import log_llm_usage

log_llm_usage(
    provider="openai",
    model="gpt-4o",
    input_tokens=100,
    output_tokens=200,
    operation="extract_entities",
    metadata={
        "user_id": "user123",
        "session_id": "abc123",
        "entity_count": 5
    }
)
```

### 3. Performance Considerations

- Token counting is lightweight (microseconds)
- Database writes are async where possible
- Indexes ensure fast queries
- Regular cleanup prevents database bloat

### 4. Security

- Never log full API keys
- Store data locally only
- Use environment variables for sensitive config
- Implement access controls if needed

## Troubleshooting

### Issue: Decorator Not Tracking

**Symptom**: No usage data appears after API calls

**Solutions**:
1. Verify decorator is applied to the actual method making API calls
2. Check that token extraction works for your provider
3. Enable debug logging to see decorator execution

### Issue: Incorrect Token Counts

**Symptom**: Token counts don't match provider dashboard

**Solutions**:
1. Update token extraction logic for provider's response format
2. Verify model names match exactly
3. Check for response wrapper objects

### Issue: Database Errors

**Symptom**: "Database is locked" or similar errors

**Solutions**:
1. Ensure single TokenMonitor instance
2. Use connection pooling for high-volume apps
3. Consider switching to PostgreSQL for production

## Migration Guide

### From Manual Tracking

If you have existing manual tracking:

```python
# Old way
tokens_used = calculate_tokens(response)
log_to_file(f"Used {tokens_used} tokens")

# New way
from graphiti_core.telemetry import log_llm_usage
log_llm_usage(
    provider="openai",
    model="gpt-4o", 
    input_tokens=tokens_used,
    output_tokens=0
)
```

### From Other Monitoring Tools

Export data from existing tools and import:

```python
import pandas as pd
from graphiti_core.telemetry import get_token_monitor

# Read existing data
df = pd.read_csv("old_token_data.csv")

# Import to new system
monitor = get_token_monitor()
for _, row in df.iterrows():
    monitor.log_usage(
        provider=row["provider"],
        service_type=row["type"],
        model=row["model"],
        operation="imported",
        input_tokens=row["tokens"],
        output_tokens=0,
        metadata={"source": "legacy_system"}
    )
```