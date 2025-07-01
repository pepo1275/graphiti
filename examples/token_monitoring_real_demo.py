#!/usr/bin/env python3
"""
Real Token Monitoring Demo with Actual API Calls
This demonstrates automatic token capture from real API responses
"""

import asyncio
import os
import sys
from datetime import datetime
from graphiti_core import Graphiti
from graphiti_core.nodes import EpisodeType

# Import token monitoring
from graphiti_core.telemetry import (
    _TOKEN_MONITORING_AVAILABLE,
    get_token_monitor,
    get_usage_report,
    track_llm_usage,
    track_embedding_usage
)


def patch_graphiti_for_monitoring():
    """
    Patch Graphiti clients to add automatic token monitoring.
    This modifies the actual clients to capture tokens from real API responses.
    """
    if not _TOKEN_MONITORING_AVAILABLE:
        print("⚠️  Token monitoring not available")
        return False
    
    # Import the clients we need to patch
    from graphiti_core.llm_client.openai_client import OpenAIClient
    from graphiti_core.embedder.openai import OpenAIEmbedder
    from graphiti_core.llm_client.config import DEFAULT_MAX_TOKENS, ModelSize
    from functools import wraps
    
    print("🔧 Patching Graphiti clients for token monitoring...")
    
    # Save original methods
    original_llm_generate = OpenAIClient._generate_response
    original_embedder_create = OpenAIEmbedder.create
    
    # Create monitored version of LLM generation
    @wraps(original_llm_generate)
    async def monitored_llm_generate(self, messages, response_model=None, max_tokens=DEFAULT_MAX_TOKENS, model_size=ModelSize.medium):
        """Wrapper that captures token usage from real OpenAI responses."""
        operation = "generate_response"
        if response_model:
            operation = f"extract_{response_model.__name__.lower()}"
        
        print(f"   📊 Monitoring LLM call ({operation}) with {self.model}...")
        
        try:
            # Call the real OpenAI API
            result = await original_llm_generate(self, messages, response_model, max_tokens, model_size)
            
            # Extract token usage from the actual response
            if hasattr(result, '_raw_response'):
                raw = result._raw_response
                if hasattr(raw, 'usage'):
                    from graphiti_core.telemetry import log_llm_usage
                    log_llm_usage(
                        provider="openai",
                        model=self.model,
                        input_tokens=raw.usage.prompt_tokens,
                        output_tokens=raw.usage.completion_tokens,
                        operation=operation,
                        api_key=getattr(self.client, 'api_key', None),
                        metadata={
                            "response_model": response_model.__name__ if response_model else "text",
                            "timestamp": datetime.now().isoformat(),
                            "messages_count": len(messages)
                        }
                    )
                    print(f"      ✅ Captured: {raw.usage.prompt_tokens} in + {raw.usage.completion_tokens} out = {raw.usage.total_tokens} total tokens")
            
            return result
            
        except Exception as e:
            print(f"      ❌ Error: {str(e)}")
            from graphiti_core.telemetry import log_llm_usage
            log_llm_usage(
                provider="openai",
                model=self.model,
                input_tokens=0,
                output_tokens=0,
                operation=operation,
                metadata={"error": str(e), "timestamp": datetime.now().isoformat()}
            )
            raise
    
    # Create monitored version of embedding creation
    @wraps(original_embedder_create)
    async def monitored_embedder_create(self, input_data, **kwargs):
        """Wrapper that captures token usage from real embedding API calls."""
        print(f"   📊 Monitoring embedding call with {self.config.embedding_model}...")
        
        try:
            # Estimate input tokens (embeddings don't return token counts)
            if isinstance(input_data, list):
                total_chars = sum(len(str(text)) for text in input_data)
                estimated_tokens = max(1, total_chars // 4)  # Rough estimate
            else:
                estimated_tokens = max(1, len(str(input_data)) // 4)
            
            # Call the real embedding API
            result = await original_embedder_create(self, input_data, **kwargs)
            
            # Log the usage
            from graphiti_core.telemetry import log_embedding_usage
            log_embedding_usage(
                provider="openai",
                model=self.config.embedding_model,
                input_tokens=estimated_tokens,
                operation="create_embeddings",
                api_key=getattr(self.client, 'api_key', None),
                metadata={
                    "timestamp": datetime.now().isoformat(),
                    "input_type": "list" if isinstance(input_data, list) else "string",
                    "estimated": True  # Since we're estimating
                }
            )
            print(f"      ✅ Captured: ~{estimated_tokens} tokens (estimated)")
            
            return result
            
        except Exception as e:
            print(f"      ❌ Error: {str(e)}")
            from graphiti_core.telemetry import log_embedding_usage
            log_embedding_usage(
                provider="openai",
                model=self.config.embedding_model,
                input_tokens=0,
                operation="create_embeddings",
                metadata={"error": str(e), "timestamp": datetime.now().isoformat()}
            )
            raise
    
    # Apply the patches
    OpenAIClient._generate_response = monitored_llm_generate
    OpenAIEmbedder.create = monitored_embedder_create
    
    print("   ✅ Monitoring patches applied successfully")
    return True


async def show_token_report(label: str):
    """Display current token usage statistics."""
    if not _TOKEN_MONITORING_AVAILABLE:
        return
    
    print(f"\n{'='*60}")
    print(f"📊 TOKEN USAGE REPORT - {label}")
    print('='*60)
    
    report = get_usage_report("openai", days=1)
    
    print(f"\nOpenAI Usage (Last 24 hours):")
    print(f"  Total Requests: {report.get('total_requests', 0)}")
    print(f"  Total Tokens: {report.get('total_tokens', 0):,}")
    print(f"    - Input: {report.get('total_input_tokens', 0):,}")
    print(f"    - Output: {report.get('total_output_tokens', 0):,}")
    print(f"  Estimated Cost: ${report.get('total_cost_usd', 0):.4f}")
    
    # Show breakdown by model
    if report.get('by_model'):
        print("\n  By Model:")
        for model_info in report['by_model']:
            print(f"    {model_info['model']}: {model_info['tokens']:,} tokens (${model_info['cost']:.4f})")
    
    # Show breakdown by operation
    if report.get('by_service_type'):
        print("\n  By Service Type:")
        for service, stats in report['by_service_type'].items():
            print(f"    {service}: {stats['requests']} requests, {stats['tokens']:,} tokens")


async def main(skip_confirmation=False):
    """Run the real token monitoring demo."""
    
    print("🚀 REAL TOKEN MONITORING DEMO")
    print("⚠️  This will make REAL API calls and cost REAL money!")
    print("="*60)
    
    # Check API key
    if not os.getenv("OPENAI_API_KEY"):
        print("\n❌ Please set OPENAI_API_KEY environment variable")
        return
    
    # Confirm with user (unless skipped)
    if not skip_confirmation:
        print("\nThis demo will:")
        print("  • Make real calls to OpenAI API")
        print("  • Create real data in Neo4j")
        print("  • Cost approximately $0.02-0.05")
        print("\nDo you want to continue? (yes/no): ", end="")
        
        if input().lower() != 'yes':
            print("Demo cancelled.")
            return
    else:
        print("\n✅ Running with --confirm flag (skipping confirmation)")
        print("This demo will:")
        print("  • Make real calls to OpenAI API")
        print("  • Create real data in Neo4j")
        print("  • Cost approximately $0.02-0.05")
    
    # Initialize monitoring
    if not _TOKEN_MONITORING_AVAILABLE:
        print("\n❌ Token monitoring not installed. Run:")
        print("   uv sync --extra token-monitoring")
        return
    
    # Show initial state
    await show_token_report("BEFORE DEMO")
    initial_report = get_usage_report("openai", days=1)
    initial_tokens = initial_report.get('total_tokens', 0)
    initial_cost = initial_report.get('total_cost_usd', 0)
    
    # Apply monitoring patches
    if not patch_graphiti_for_monitoring():
        print("❌ Failed to apply monitoring patches")
        return
    
    # Initialize Graphiti
    print("\n🔧 Initializing Graphiti...")
    uri = "bolt://localhost:7687"
    username = "neo4j"
    password = "pepo_graphiti_2025"
    
    try:
        graphiti = Graphiti(uri, username, password)
        await graphiti.build_indices_and_constraints()
        print("   ✅ Graphiti initialized")
    except Exception as e:
        print(f"   ❌ Failed to initialize Graphiti: {e}")
        return
    
    # Create episode content about the monitoring system itself
    episode_content = """
    The Graphiti Token Monitoring System provides comprehensive tracking of API usage 
    across multiple LLM providers including OpenAI, Anthropic, and Google Gemini. 
    It features automatic token capture from API responses, real-time cost calculation 
    based on current pricing models, and detailed analytics through a CLI interface. 
    The system uses SQLite for local storage, ensuring privacy while providing 
    granular insights into token consumption patterns. Key features include 
    multi-provider support, operation-level tracking, subscription limit management, 
    and CSV export capabilities for external analysis. The monitoring integrates 
    seamlessly with existing code through decorators and provides both automatic 
    and manual tracking options.
    """
    
    print("\n📝 Adding episode to Graphiti...")
    print(f"   Content preview: {episode_content[:100].strip()}...")
    
    try:
        # This will trigger multiple API calls that we'll monitor
        result = await graphiti.add_episode(
            name="Token Monitoring System Overview",
            episode_body=episode_content,
            source_description="Real API monitoring demo",
            reference_time=datetime.now(),
            group_id="token_monitor_demo"
        )
        print("   ✅ Episode added successfully")
        
    except Exception as e:
        print(f"   ❌ Error adding episode: {e}")
    
    # Wait a moment for async operations
    await asyncio.sleep(2)
    
    # Show final state
    await show_token_report("AFTER DEMO")
    
    # Calculate what this demo cost
    final_report = get_usage_report("openai", days=1)
    tokens_used = final_report['total_tokens'] - initial_tokens
    cost_incurred = final_report['total_cost_usd'] - initial_cost
    
    print("\n💰 DEMO COST SUMMARY")
    print("="*60)
    print(f"  Tokens used in this demo: {tokens_used:,}")
    print(f"  Cost of this demo: ${cost_incurred:.4f}")
    
    # Show recent operations from the database
    print("\n📋 CAPTURED OPERATIONS:")
    monitor = get_token_monitor()
    
    # Query for operations in the last 5 minutes
    import sqlite3
    with sqlite3.connect(monitor.db_path) as conn:
        recent_ops = conn.execute("""
            SELECT 
                operation, 
                model, 
                input_tokens,
                output_tokens,
                total_tokens,
                cost_usd,
                timestamp
            FROM token_usage 
            WHERE timestamp > datetime('now', '-5 minutes')
            AND provider = 'openai'
            ORDER BY timestamp DESC
            LIMIT 10
        """).fetchall()
    
    if recent_ops:
        print("\n  Recent operations (last 5 minutes):")
        for op in recent_ops:
            operation, model, inp, out, total, cost, ts = op
            print(f"    • {operation} ({model}): {inp}→{out} = {total} tokens (${cost:.4f})")
            print(f"      at {ts}")
    
    # Verify in Neo4j
    print("\n🔍 Verifying in Neo4j...")
    try:
        nodes = await graphiti.search_nodes("token monitoring", num_results=5)
        print(f"   Found {len(nodes)} nodes about token monitoring:")
        for i, node in enumerate(nodes[:3], 1):
            print(f"   {i}. {node.name} (score: {node.score:.3f})")
    except Exception as e:
        print(f"   ❌ Error searching nodes: {e}")
    
    # Cleanup
    await graphiti.close()
    
    print("\n✅ Real demo completed!")
    print("\n📈 You can now explore the captured data:")
    print("   uv run graphiti-tokens summary -p openai -d 1")
    print("   uv run graphiti-tokens export real_demo_results.csv -d 1")


if __name__ == "__main__":
    # Add safety check
    if len(sys.argv) > 1 and sys.argv[1] == "--confirm":
        asyncio.run(main(skip_confirmation=True))
    else:
        print("📋 REAL DEMO PLAN")
        print("="*60)
        print("\nThis script will:")
        print("1. ✅ Patch Graphiti to capture real token usage")
        print("2. ✅ Make real API calls to OpenAI")
        print("3. ✅ Automatically capture tokens from API responses")
        print("4. ✅ Create real nodes/edges in Neo4j")
        print("5. ✅ Cost real money (estimated $0.02-0.05)")
        print("\n⚠️  To execute: python token_monitoring_real_demo.py --confirm")