# Token Monitoring System for Graphiti

## Overview

The Token Monitoring System is a comprehensive solution for tracking token usage across all LLM and embedding providers in Graphiti. It provides real-time monitoring, cost tracking, alerts, and detailed analytics to help manage API usage and costs effectively.

## Architecture

The system consists of three main components:

### 1. Core Monitor (`token_monitor.py`)
- **SQLite Database**: Persistent storage for all token usage data
- **Multi-Provider Support**: Tracks OpenAI, Anthropic, Gemini, Azure, Vertex AI, and more
- **Service Type Differentiation**: Separate tracking for LLM, Embeddings, and Reranking
- **Cost Calculation**: Automatic cost estimation based on current pricing
- **Alert System**: Configurable alerts at 80% (warning) and 95% (critical) usage

### 2. Integration Layer (`token_integration.py`)
- **Automatic Tracking**: Decorators for seamless integration
- **Provider-Specific Parsing**: Extracts token counts from each provider's response format
- **Error Handling**: Logs failed requests with error details
- **Async/Sync Support**: Works with both synchronous and asynchronous code

### 3. CLI Tool (`token_cli.py`)
- **Usage Summaries**: View token usage by provider, model, and time period
- **Subscription Status**: Monitor remaining tokens and alerts
- **Data Export**: Export usage data to CSV for external analysis
- **Configuration**: Set subscription limits and manage settings

## Features

### Multi-Provider Token Tracking

Supports all major providers with automatic token extraction:

```python
# LLM Providers
- OpenAI (GPT-4, GPT-3.5)
- Anthropic (Claude 3 Opus, Sonnet, Haiku)
- Google Gemini (Pro, Flash)
- Azure OpenAI
- Groq

# Embedding Providers
- OpenAI Embeddings
- Google Vertex AI
- Gemini Embeddings
- Voyage AI
- Azure OpenAI Embeddings
```

### Comprehensive Data Tracking

Each token usage record captures:
- Timestamp
- Provider and model
- Service type (LLM/Embedding/Reranking)
- Operation name
- Input and output tokens
- Total tokens
- Estimated cost
- API key identifier (last 4 chars)
- Success/error status
- Custom metadata

### Cost Management

Built-in pricing for all major models:
```python
# Example pricing (per 1M tokens)
"gpt-4o": {"input": 2.50, "output": 10.00}
"claude-3-sonnet": {"input": 3.00, "output": 15.00}
"gemini-1.5-flash": {"input": 0.075, "output": 0.30}
```

### Subscription Management

Track usage against your subscription limits:
- Anthropic Max Plan: 5M tokens/month
- OpenAI: Prepaid credits
- Gemini: Free tier + paid tier
- Custom limits for any provider

## Installation

The token monitoring system is included in the Graphiti core telemetry module. No additional installation required.

## Configuration

### Setting Subscription Limits

```bash
# Set Anthropic Max plan limit (5M tokens)
graphiti-tokens set-limit anthropic max_plan_tokens 5000000

# Set OpenAI prepaid credits ($100)
graphiti-tokens set-limit openai prepaid_credits 100

# Set Gemini free tier limit
graphiti-tokens set-limit gemini free_tier_tokens 1000000
```

### Environment Variables

Configure storage location (optional):
```bash
export GRAPHITI_TOKEN_MONITOR_DIR=~/.graphiti/token_monitor
```

## Usage

### Automatic Tracking with Decorators

```python
from graphiti_core.telemetry import track_llm_usage, track_embedding_usage

# Track LLM usage
@track_llm_usage(provider="openai", model="gpt-4o", operation="extract_nodes")
async def call_openai_api(prompt: str):
    # Your API call here
    # Token usage is automatically tracked
    pass

# Track embedding usage
@track_embedding_usage(provider="openai", model="text-embedding-3-small")
async def generate_embeddings(texts: List[str]):
    # Your embedding call here
    pass
```

### Manual Tracking

```python
from graphiti_core.telemetry import log_llm_usage, log_embedding_usage

# Log LLM usage manually
log_llm_usage(
    provider="anthropic",
    model="claude-3-sonnet",
    input_tokens=150,
    output_tokens=500,
    operation="summarize",
    api_key="sk-...wxyz"  # Optional
)

# Log embedding usage
log_embedding_usage(
    provider="openai",
    model="text-embedding-3-small",
    input_tokens=250,
    operation="embed_documents"
)
```

### Querying Usage Data

```python
from graphiti_core.telemetry import get_usage_report, get_token_monitor

# Get usage summary for specific provider
report = get_usage_report("anthropic", days=30)
print(f"Total tokens used: {report['total_tokens']:,}")
print(f"Total cost: ${report['total_cost_usd']:.2f}")

# Get comprehensive report across all providers
full_report = get_usage_report()

# Get subscription status
monitor = get_token_monitor()
status = monitor._get_subscription_status()
for provider, info in status.items():
    print(f"{provider}: {info['percentage_used']:.1f}% used")
```

### CLI Commands

```bash
# View usage summary
graphiti-tokens summary                    # All providers
graphiti-tokens summary -p openai -d 7     # OpenAI last 7 days

# Check subscription status
graphiti-tokens status

# Check for alerts
graphiti-tokens alerts

# Export data
graphiti-tokens export usage_report.csv -d 30

# Clean old data
graphiti-tokens cleanup -d 90
```

## Integration with Graphiti

### Step 1: Import Token Monitoring

```python
from graphiti_core.telemetry import track_llm_usage, track_embedding_usage
```

### Step 2: Add Decorators to Client Methods

Example for OpenAI client:
```python
class OpenAIClient:
    @track_llm_usage(provider="openai", model=self.model_name)
    async def generate_response(self, messages: List[Dict]):
        response = await self.client.chat.completions.create(...)
        return response
```

### Step 3: Configure Limits

Set your subscription limits to enable alerts:
```python
from graphiti_core.telemetry import set_provider_limit

# Set your limits
set_provider_limit("anthropic", "max_plan_tokens", 5_000_000)
set_provider_limit("openai", "prepaid_credits", 100)
```

## Data Storage

All token usage data is stored in:
- **Default location**: `~/.graphiti/token_monitor/`
- **Database**: `token_usage.db` (SQLite)
- **Configuration**: `monitor_config.json`
- **Archives**: Monthly archives of historical data

## Privacy and Security

- **No API Keys Stored**: Only last 4 characters for identification
- **Local Storage**: All data stored locally, no external transmission
- **Configurable**: Can be disabled or redirected to custom location
- **Exportable**: Full control over your data with CSV export

## Troubleshooting

### Common Issues

1. **Database Locked Error**
   - Multiple processes accessing the database
   - Solution: Use single monitor instance

2. **Missing Token Counts**
   - Provider response format changed
   - Solution: Update extraction logic in `_extract_token_info()`

3. **Incorrect Costs**
   - Outdated pricing information
   - Solution: Update `PRICING` dictionary in `token_monitor.py`

### Debug Mode

Enable detailed logging:
```python
import logging
logging.getLogger('graphiti.telemetry').setLevel(logging.DEBUG)
```

## Future Enhancements

- [ ] Web dashboard for visualization
- [ ] Integration with cloud monitoring services
- [ ] Budget alerts via email/webhook
- [ ] Automatic cost optimization suggestions
- [ ] Team usage tracking with multiple API keys

## Demo and Results

See [DEMO_RESULTS.md](./DEMO_RESULTS.md) for a complete demonstration of the system in action, including performance metrics and real usage data.

## API Reference

See [API_REFERENCE.md](./API_REFERENCE.md) for detailed API documentation.