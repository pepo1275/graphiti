# Token Monitoring API Reference

## TokenMonitor Class

The main class for managing token usage tracking.

### Constructor

```python
TokenMonitor(storage_dir: Optional[str] = None)
```

**Parameters:**
- `storage_dir`: Custom storage directory (default: `~/.graphiti/token_monitor`)

### Methods

#### log_usage()

```python
def log_usage(
    provider: str,
    service_type: ServiceType,
    model: str,
    operation: str,
    input_tokens: int,
    output_tokens: int = 0,
    api_key: Optional[str] = None,
    metadata: Optional[Dict] = None,
    error: bool = False,
    error_message: Optional[str] = None
) -> Dict[str, Any]
```

Log token usage for a specific operation.

**Parameters:**
- `provider`: Provider name (e.g., "openai", "anthropic")
- `service_type`: Type of service (LLM, EMBEDDING, RERANKING)
- `model`: Model name (e.g., "gpt-4o", "claude-3-sonnet")
- `operation`: Operation name (e.g., "extract_nodes", "generate_embeddings")
- `input_tokens`: Number of input tokens
- `output_tokens`: Number of output tokens (default: 0)
- `api_key`: API key for identification (optional)
- `metadata`: Additional metadata (optional)
- `error`: Whether the operation failed (default: False)
- `error_message`: Error message if failed (optional)

**Returns:**
Dictionary containing:
- `logged`: Boolean indicating success
- `record`: The logged record details
- `usage_summary`: Current usage summary
- `alerts`: List of triggered alerts

#### get_provider_summary()

```python
def get_provider_summary(provider: str, days: int = 30) -> Dict[str, Any]
```

Get usage summary for a specific provider.

**Parameters:**
- `provider`: Provider name
- `days`: Number of days to include (default: 30)

**Returns:**
Dictionary containing:
- `provider`: Provider name
- `period_days`: Number of days covered
- `total_requests`: Total number of requests
- `total_input_tokens`: Total input tokens
- `total_output_tokens`: Total output tokens
- `total_tokens`: Total tokens (input + output)
- `total_cost_usd`: Total estimated cost
- `by_service_type`: Breakdown by service type
- `by_model`: Breakdown by model

#### get_comprehensive_report()

```python
def get_comprehensive_report(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> Dict[str, Any]
```

Generate comprehensive usage report across all providers.

**Parameters:**
- `start_date`: ISO format start date (default: 30 days ago)
- `end_date`: ISO format end date (default: now)

**Returns:**
Dictionary containing:
- `report_period`: Start and end dates
- `summary`: Overall statistics
- `by_provider`: Breakdown by provider
- `subscription_status`: Current subscription status

#### set_subscription_limit()

```python
def set_subscription_limit(provider: str, limit_type: str, value: int)
```

Update subscription limits for a provider.

**Parameters:**
- `provider`: Provider name
- `limit_type`: Type of limit (e.g., "max_plan_tokens", "prepaid_credits")
- `value`: Limit value

#### export_to_csv()

```python
def export_to_csv(
    output_path: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
)
```

Export usage data to CSV file.

**Parameters:**
- `output_path`: Path for output CSV file
- `start_date`: ISO format start date
- `end_date`: ISO format end date

## Decorators

### @track_llm_usage

```python
@track_llm_usage(provider: str, model: str, operation: str = "inference")
```

Decorator to automatically track LLM token usage.

**Parameters:**
- `provider`: LLM provider name
- `model`: Model name
- `operation`: Operation name (default: "inference")

**Example:**
```python
@track_llm_usage(provider="openai", model="gpt-4o", operation="summarize")
async def summarize_text(text: str) -> str:
    # Your LLM call here
    pass
```

### @track_embedding_usage

```python
@track_embedding_usage(provider: str, model: str, operation: str = "embed")
```

Decorator to automatically track embedding token usage.

**Parameters:**
- `provider`: Embedding provider name
- `model`: Model name
- `operation`: Operation name (default: "embed")

**Example:**
```python
@track_embedding_usage(provider="openai", model="text-embedding-3-small")
async def generate_embeddings(texts: List[str]) -> List[List[float]]:
    # Your embedding call here
    pass
```

## Helper Functions

### get_token_monitor()

```python
def get_token_monitor() -> TokenMonitor
```

Get or create the global token monitor instance.

**Returns:** TokenMonitor instance

### log_llm_usage()

```python
def log_llm_usage(
    provider: str,
    model: str,
    input_tokens: int,
    output_tokens: int,
    operation: str = "manual",
    api_key: Optional[str] = None,
    **metadata
)
```

Manually log LLM usage.

### log_embedding_usage()

```python
def log_embedding_usage(
    provider: str,
    model: str,
    input_tokens: int,
    operation: str = "manual",
    api_key: Optional[str] = None,
    **metadata
)
```

Manually log embedding usage.

### get_usage_report()

```python
def get_usage_report(
    provider: Optional[str] = None,
    days: int = 30
) -> Dict[str, Any]
```

Get usage report for provider or all providers.

**Parameters:**
- `provider`: Specific provider or None for all
- `days`: Number of days to include

### set_provider_limit()

```python
def set_provider_limit(provider: str, limit_type: str, value: int)
```

Set subscription limit for a provider.

## Enums

### ServiceType

```python
class ServiceType(str, Enum):
    LLM = "llm"
    EMBEDDING = "embedding"
    RERANKING = "reranking"
```

### Provider

```python
class Provider(str, Enum):
    # LLM Providers
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GEMINI = "gemini"
    AZURE_OPENAI = "azure_openai"
    GROQ = "groq"
    
    # Embedding Providers
    OPENAI_EMBED = "openai_embed"
    VERTEX_AI = "vertex_ai"
    GEMINI_EMBED = "gemini_embed"
    VOYAGE = "voyage"
    AZURE_OPENAI_EMBED = "azure_openai_embed"
```

## Data Models

### TokenUsageRecord

```python
@dataclass
class TokenUsageRecord:
    timestamp: str
    provider: str
    service_type: str
    model: str
    operation: str
    input_tokens: int
    output_tokens: int
    total_tokens: int
    api_key_id: str
    cost_usd: float = 0.0
    metadata: Dict[str, Any] = None
    error: bool = False
    error_message: str = None
```

## Database Schema

### token_usage Table

```sql
CREATE TABLE token_usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    provider TEXT NOT NULL,
    service_type TEXT NOT NULL,
    model TEXT NOT NULL,
    operation TEXT NOT NULL,
    input_tokens INTEGER NOT NULL,
    output_tokens INTEGER NOT NULL,
    total_tokens INTEGER NOT NULL,
    api_key_id TEXT NOT NULL,
    cost_usd REAL DEFAULT 0.0,
    metadata TEXT,
    error BOOLEAN DEFAULT FALSE,
    error_message TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
)
```

## Configuration File Format

```json
{
    "subscription_limits": {
        "anthropic": {
            "max_plan_tokens": 5000000,
            "billing_cycle": "monthly"
        },
        "openai": {
            "prepaid_credits": 100,
            "monthly_limit": 0
        },
        "gemini": {
            "free_tier_tokens": 1000000,
            "paid_tier_tokens": 0
        }
    },
    "api_keys": {},
    "alerts": {
        "warn_at_percentage": 80,
        "critical_at_percentage": 95
    }
}
```