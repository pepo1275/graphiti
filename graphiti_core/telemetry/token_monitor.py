"""
Comprehensive Token Usage Monitor for Graphiti
Tracks token consumption across all LLM and embedding providers with detailed analytics
"""

import json
import os
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Optional, Any, List, Tuple
from enum import Enum
from dataclasses import dataclass, asdict
import pandas as pd

class ServiceType(str, Enum):
    LLM = "llm"
    EMBEDDING = "embedding"
    RERANKING = "reranking"

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

@dataclass
class TokenUsageRecord:
    """Detailed record of token usage."""
    timestamp: str
    provider: str
    service_type: str
    model: str
    operation: str
    input_tokens: int
    output_tokens: int
    total_tokens: int
    api_key_id: str  # Last 4 chars of API key for identification
    cost_usd: float = 0.0
    metadata: Dict[str, Any] = None
    error: bool = False
    error_message: str = None

class TokenMonitor:
    """Comprehensive token usage monitoring with SQLite backend."""
    
    # Pricing per 1M tokens (updated Jan 2025)
    PRICING = {
        # OpenAI Models
        "gpt-4o": {"input": 2.50, "output": 10.00},
        "gpt-4o-mini": {"input": 0.15, "output": 0.60},
        "gpt-4-turbo": {"input": 10.00, "output": 30.00},
        "gpt-3.5-turbo": {"input": 0.50, "output": 1.50},
        
        # Anthropic Claude Models
        "claude-opus-4-20250514": {"input": 15.00, "output": 75.00},
        "claude-sonnet-4-20250514": {"input": 3.00, "output": 15.00},
        "claude-3-5-sonnet-20241022": {"input": 3.00, "output": 15.00},
        "claude-3-opus-20240229": {"input": 15.00, "output": 75.00},
        "claude-3-sonnet-20240229": {"input": 3.00, "output": 15.00},
        "claude-3-haiku-20240307": {"input": 0.25, "output": 1.25},
        
        # Google Gemini Models
        "gemini-2.5-pro": {"input": 1.25, "output": 10.00},  # ≤200k tokens
        "gemini-2.5-flash": {"input": 0.30, "output": 2.50},  # Text/image/video
        "gemini-2.0-flash": {"input": 0.10, "output": 0.40},
        "gemini-1.5-pro": {"input": 1.25, "output": 5.00},  # ≤128k context
        "gemini-1.5-pro-002": {"input": 1.25, "output": 5.00},
        "gemini-1.5-flash": {"input": 0.075, "output": 0.30},  # ≤128k context
        "gemini-1.5-flash-002": {"input": 0.075, "output": 0.30},
        
        # Embedding Models
        "text-embedding-3-small": {"input": 0.02, "output": 0},
        "text-embedding-3-large": {"input": 0.13, "output": 0},
        "text-embedding-ada-002": {"input": 0.10, "output": 0},
        "text-embedding-004": {"input": 0.05, "output": 0},  # Vertex AI
        "text-embedding-005": {"input": 0.05, "output": 0},  # Vertex AI
        "text-multilingual-embedding-002": {"input": 0.05, "output": 0},  # Vertex AI
        "voyage-large-2": {"input": 0.12, "output": 0},
        "voyage-code-2": {"input": 0.12, "output": 0},
    }
    
    def __init__(self, storage_dir: Optional[str] = None):
        self.storage_dir = Path(storage_dir or os.path.expanduser("~/.graphiti/token_monitor"))
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.db_path = self.storage_dir / "token_usage.db"
        self.config_path = self.storage_dir / "monitor_config.json"
        
        self._init_database()
        self._load_config()
    
    def _init_database(self):
        """Initialize SQLite database with usage tracking table."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS token_usage (
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
            """)
            
            # Create indexes for efficient querying
            conn.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON token_usage(timestamp)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_provider ON token_usage(provider)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_api_key ON token_usage(api_key_id)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_service_type ON token_usage(service_type)")
    
    def _load_config(self):
        """Load monitor configuration including limits and API keys."""
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = {
                "subscription_limits": {
                    "anthropic": {
                        "max_plan_tokens": 5000000,  # 5M tokens
                        "billing_cycle": "monthly"
                    },
                    "openai": {
                        "prepaid_credits": 0,  # Set your prepaid amount
                        "monthly_limit": 0
                    },
                    "gemini": {
                        "free_tier_tokens": 1000000,  # 1M free tokens/month
                        "paid_tier_tokens": 0
                    }
                },
                "api_keys": {},  # Store hashed key identifiers
                "alerts": {
                    "warn_at_percentage": 80,
                    "critical_at_percentage": 95
                }
            }
            self._save_config()
    
    def _save_config(self):
        """Save configuration to disk."""
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def _get_api_key_id(self, api_key: str) -> str:
        """Get identifier for API key (last 4 characters)."""
        return f"...{api_key[-4:]}" if len(api_key) > 4 else "****"
    
    def _calculate_cost(self, model: str, input_tokens: int, output_tokens: int) -> float:
        """Calculate cost in USD based on model pricing."""
        if model not in self.PRICING:
            return 0.0
        
        pricing = self.PRICING[model]
        input_cost = (input_tokens / 1_000_000) * pricing.get("input", 0)
        output_cost = (output_tokens / 1_000_000) * pricing.get("output", 0)
        return round(input_cost + output_cost, 6)
    
    def log_usage(
        self,
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
    ) -> Dict[str, Any]:
        """Log token usage with detailed information."""
        total_tokens = input_tokens + output_tokens
        api_key_id = self._get_api_key_id(api_key) if api_key else "default"
        cost = self._calculate_cost(model, input_tokens, output_tokens)
        
        record = TokenUsageRecord(
            timestamp=datetime.now().isoformat(),
            provider=provider,
            service_type=service_type.value,
            model=model,
            operation=operation,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
            api_key_id=api_key_id,
            cost_usd=cost,
            metadata=metadata,
            error=error,
            error_message=error_message
        )
        
        # Store in database
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO token_usage (
                    timestamp, provider, service_type, model, operation,
                    input_tokens, output_tokens, total_tokens, api_key_id,
                    cost_usd, metadata, error, error_message
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                record.timestamp, record.provider, record.service_type,
                record.model, record.operation, record.input_tokens,
                record.output_tokens, record.total_tokens, record.api_key_id,
                record.cost_usd, json.dumps(record.metadata) if record.metadata else None,
                record.error, record.error_message
            ))
        
        # Check usage alerts
        usage_summary = self.get_provider_summary(provider)
        return {
            "logged": True,
            "record": asdict(record),
            "usage_summary": usage_summary,
            "alerts": self._check_alerts(provider, usage_summary)
        }
    
    def _check_alerts(self, provider: str, usage_summary: Dict) -> List[str]:
        """Check if usage triggers any alerts."""
        alerts = []
        if provider in self.config["subscription_limits"]:
            limit_info = self.config["subscription_limits"][provider]
            
            if "max_plan_tokens" in limit_info:
                limit = limit_info["max_plan_tokens"]
                used = usage_summary.get("total_tokens", 0)
                percentage = (used / limit * 100) if limit > 0 else 0
                
                if percentage >= self.config["alerts"]["critical_at_percentage"]:
                    alerts.append(f"CRITICAL: {provider} usage at {percentage:.1f}% of limit")
                elif percentage >= self.config["alerts"]["warn_at_percentage"]:
                    alerts.append(f"WARNING: {provider} usage at {percentage:.1f}% of limit")
        
        return alerts
    
    def get_provider_summary(self, provider: str, days: int = 30) -> Dict[str, Any]:
        """Get usage summary for a specific provider."""
        cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
        
        with sqlite3.connect(self.db_path) as conn:
            # Total usage
            total_query = """
                SELECT 
                    COUNT(*) as request_count,
                    SUM(input_tokens) as total_input_tokens,
                    SUM(output_tokens) as total_output_tokens,
                    SUM(total_tokens) as total_tokens,
                    SUM(cost_usd) as total_cost
                FROM token_usage
                WHERE provider = ? AND timestamp > ?
            """
            totals = conn.execute(total_query, (provider, cutoff_date)).fetchone()
            
            # By service type
            service_query = """
                SELECT 
                    service_type,
                    COUNT(*) as requests,
                    SUM(total_tokens) as tokens
                FROM token_usage
                WHERE provider = ? AND timestamp > ?
                GROUP BY service_type
            """
            services = conn.execute(service_query, (provider, cutoff_date)).fetchall()
            
            # By model
            model_query = """
                SELECT 
                    model,
                    COUNT(*) as requests,
                    SUM(total_tokens) as tokens,
                    SUM(cost_usd) as cost
                FROM token_usage
                WHERE provider = ? AND timestamp > ?
                GROUP BY model
                ORDER BY tokens DESC
            """
            models = conn.execute(model_query, (provider, cutoff_date)).fetchall()
        
        return {
            "provider": provider,
            "period_days": days,
            "total_requests": totals[0] or 0,
            "total_input_tokens": totals[1] or 0,
            "total_output_tokens": totals[2] or 0,
            "total_tokens": totals[3] or 0,
            "total_cost_usd": round(totals[4] or 0, 2),
            "by_service_type": {row[0]: {"requests": row[1], "tokens": row[2]} for row in services},
            "by_model": [{"model": row[0], "requests": row[1], "tokens": row[2], "cost": round(row[3], 2)} for row in models]
        }
    
    def get_comprehensive_report(self, start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict[str, Any]:
        """Generate comprehensive usage report across all providers."""
        if not start_date:
            start_date = (datetime.now() - timedelta(days=30)).isoformat()
        if not end_date:
            end_date = datetime.now().isoformat()
        
        with sqlite3.connect(self.db_path) as conn:
            # Overall statistics
            overall_query = """
                SELECT 
                    COUNT(DISTINCT provider) as provider_count,
                    COUNT(DISTINCT api_key_id) as api_key_count,
                    COUNT(*) as total_requests,
                    SUM(total_tokens) as total_tokens,
                    SUM(cost_usd) as total_cost,
                    SUM(CASE WHEN error = 1 THEN 1 ELSE 0 END) as error_count
                FROM token_usage
                WHERE timestamp BETWEEN ? AND ?
            """
            overall = conn.execute(overall_query, (start_date, end_date)).fetchone()
            
            # By provider
            provider_query = """
                SELECT 
                    provider,
                    service_type,
                    COUNT(*) as requests,
                    SUM(total_tokens) as tokens,
                    SUM(cost_usd) as cost
                FROM token_usage
                WHERE timestamp BETWEEN ? AND ?
                GROUP BY provider, service_type
                ORDER BY provider, service_type
            """
            provider_data = conn.execute(provider_query, (start_date, end_date)).fetchall()
        
        # Organize provider data
        providers = {}
        for row in provider_data:
            provider, service_type = row[0], row[1]
            if provider not in providers:
                providers[provider] = {}
            providers[provider][service_type] = {
                "requests": row[2],
                "tokens": row[3],
                "cost": round(row[4], 2)
            }
        
        return {
            "report_period": {
                "start": start_date,
                "end": end_date
            },
            "summary": {
                "provider_count": overall[0],
                "api_key_count": overall[1],
                "total_requests": overall[2],
                "total_tokens": overall[3],
                "total_cost_usd": round(overall[4] or 0, 2),
                "error_count": overall[5]
            },
            "by_provider": providers,
            "subscription_status": self._get_subscription_status()
        }
    
    def _get_subscription_status(self) -> Dict[str, Any]:
        """Get current subscription status for all providers."""
        status = {}
        
        for provider, limits in self.config["subscription_limits"].items():
            usage = self.get_provider_summary(provider, days=30)
            
            if "max_plan_tokens" in limits:
                limit = limits["max_plan_tokens"]
                used = usage["total_tokens"]
                remaining = max(0, limit - used)
                percentage = (used / limit * 100) if limit > 0 else 0
                
                status[provider] = {
                    "limit": limit,
                    "used": used,
                    "remaining": remaining,
                    "percentage_used": round(percentage, 2),
                    "status": "critical" if percentage >= 95 else "warning" if percentage >= 80 else "ok"
                }
        
        return status
    
    def export_to_csv(self, output_path: str, start_date: Optional[str] = None, end_date: Optional[str] = None):
        """Export usage data to CSV for external analysis."""
        query = """
            SELECT * FROM token_usage
            WHERE timestamp BETWEEN ? AND ?
            ORDER BY timestamp DESC
        """
        
        if not start_date:
            start_date = (datetime.now() - timedelta(days=30)).isoformat()
        if not end_date:
            end_date = datetime.now().isoformat()
        
        with sqlite3.connect(self.db_path) as conn:
            df = pd.read_sql_query(query, conn, params=(start_date, end_date))
            df.to_csv(output_path, index=False)
        
        return f"Exported {len(df)} records to {output_path}"
    
    def set_subscription_limit(self, provider: str, limit_type: str, value: int):
        """Update subscription limits."""
        if provider not in self.config["subscription_limits"]:
            self.config["subscription_limits"][provider] = {}
        
        self.config["subscription_limits"][provider][limit_type] = value
        self._save_config()
        
        return f"Updated {provider} {limit_type} to {value}"
    
    def cleanup_old_data(self, days_to_keep: int = 90):
        """Remove data older than specified days."""
        cutoff_date = (datetime.now() - timedelta(days=days_to_keep)).isoformat()
        
        with sqlite3.connect(self.db_path) as conn:
            result = conn.execute("DELETE FROM token_usage WHERE timestamp < ?", (cutoff_date,))
            deleted = result.rowcount
        
        return f"Deleted {deleted} records older than {days_to_keep} days"

# Global instance
_token_monitor = None

def get_token_monitor() -> TokenMonitor:
    """Get or create global token monitor instance."""
    global _token_monitor
    if _token_monitor is None:
        _token_monitor = TokenMonitor()
    return _token_monitor