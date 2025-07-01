#!/usr/bin/env python3
"""
Token Monitoring Simulation
Demonstrates the monitoring system without making real API calls
"""

import asyncio
from datetime import datetime, timedelta
from graphiti_core.telemetry import (
    get_token_monitor,
    log_llm_usage,
    log_embedding_usage,
    get_usage_report,
    set_provider_limit,
    _TOKEN_MONITORING_AVAILABLE
)


async def simulate_graphiti_operations():
    """Simulate various Graphiti operations with token usage."""
    
    print("🚀 TOKEN MONITORING SIMULATION")
    print("="*60)
    
    if not _TOKEN_MONITORING_AVAILABLE:
        print("❌ Token monitoring not available")
        print("   Install with: pip install graphiti-core[token-monitoring]")
        return
    
    # Initialize monitoring
    print("\n1️⃣ Initializing token monitoring...")
    monitor = get_token_monitor()
    
    # Set realistic limits
    set_provider_limit("openai", "prepaid_credits", 50)  # $50
    set_provider_limit("anthropic", "max_plan_tokens", 5_000_000)  # 5M tokens
    print("   ✅ Set provider limits")
    
    # Show initial status
    print("\n2️⃣ Initial Status:")
    await show_status()
    
    # Simulate adding episodes
    print("\n3️⃣ Simulating episode additions...")
    
    episodes = [
        ("Research paper on AI", 500, 800),
        ("News article summary", 300, 500),
        ("Technical documentation", 1000, 1500),
    ]
    
    for i, (description, input_tokens, output_tokens) in enumerate(episodes, 1):
        print(f"\n   📝 Episode {i}: {description}")
        
        # Simulate node extraction
        log_llm_usage(
            provider="openai",
            model="gpt-4o",
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            operation="extract_nodes",
            metadata={
                "episode": description,
                "nodes_extracted": 5,
                "timestamp": datetime.now().isoformat()
            }
        )
        print(f"      ✅ Node extraction: {input_tokens} → {output_tokens} tokens")
        
        # Simulate edge extraction
        edge_input = int(input_tokens * 0.8)
        edge_output = int(output_tokens * 0.6)
        log_llm_usage(
            provider="openai",
            model="gpt-4o",
            input_tokens=edge_input,
            output_tokens=edge_output,
            operation="extract_edges",
            metadata={
                "episode": description,
                "edges_extracted": 8,
                "timestamp": datetime.now().isoformat()
            }
        )
        print(f"      ✅ Edge extraction: {edge_input} → {edge_output} tokens")
        
        # Simulate embeddings
        embedding_tokens = int(input_tokens * 0.3)
        log_embedding_usage(
            provider="openai",
            model="text-embedding-3-small",
            input_tokens=embedding_tokens,
            operation="embed_nodes",
            metadata={
                "episode": description,
                "vectors_created": 5,
                "timestamp": datetime.now().isoformat()
            }
        )
        print(f"      ✅ Embeddings: {embedding_tokens} tokens")
        
        # Show running total
        report = get_usage_report("openai", days=1)
        total_cost = report.get('total_cost_usd', 0)
        print(f"      💰 Running cost: ${total_cost:.4f}")
    
    # Simulate searches
    print("\n\n4️⃣ Simulating search operations...")
    
    searches = [
        ("AI research trends", 50),
        ("quantum computing applications", 80),
        ("sustainable technology", 60),
    ]
    
    for query, tokens in searches:
        print(f"\n   🔍 Search: '{query}'")
        
        # Log embedding for search query
        log_embedding_usage(
            provider="openai",
            model="text-embedding-3-small",
            input_tokens=tokens,
            operation="search_query_embedding",
            metadata={
                "query": query,
                "timestamp": datetime.now().isoformat()
            }
        )
        print(f"      ✅ Query embedding: {tokens} tokens")
        
        # Simulate reranking
        log_llm_usage(
            provider="openai",
            model="gpt-4o-mini",
            input_tokens=tokens * 2,
            output_tokens=20,
            operation="rerank_results",
            metadata={
                "query": query,
                "results_reranked": 10,
                "timestamp": datetime.now().isoformat()
            }
        )
        print(f"      ✅ Result reranking: {tokens * 2} → 20 tokens")
    
    # Show detailed report
    print("\n\n5️⃣ Detailed Usage Report")
    await show_detailed_report()
    
    # Simulate error
    print("\n6️⃣ Simulating API error...")
    log_llm_usage(
        provider="openai",
        model="gpt-4o",
        input_tokens=0,
        output_tokens=0,
        operation="failed_extraction",
        metadata={
            "error": "Rate limit exceeded",
            "timestamp": datetime.now().isoformat()
        }
    )
    print("   ❌ Logged failed operation")
    
    # Show final summary
    print("\n\n7️⃣ Final Summary")
    await show_final_summary()
    
    # Test different providers
    print("\n\n8️⃣ Testing multi-provider tracking...")
    
    # Simulate Anthropic usage
    log_llm_usage(
        provider="anthropic",
        model="claude-3-sonnet",
        input_tokens=1000,
        output_tokens=2000,
        operation="complex_analysis",
        api_key="sk-ant-...wxyz",
        metadata={"task": "Document analysis"}
    )
    print("   ✅ Logged Anthropic usage")
    
    # Simulate Gemini usage
    log_llm_usage(
        provider="gemini",
        model="gemini-1.5-flash",
        input_tokens=500,
        output_tokens=1000,
        operation="quick_summary",
        metadata={"task": "Quick summary"}
    )
    print("   ✅ Logged Gemini usage")
    
    # Show all providers
    print("\n   📊 All Providers Summary:")
    comprehensive = monitor.get_comprehensive_report()
    for provider, services in comprehensive['by_provider'].items():
        total_tokens = sum(s.get('tokens', 0) for s in services.values())
        if total_tokens > 0:
            print(f"      {provider}: {total_tokens:,} tokens")


async def show_status():
    """Show current subscription status."""
    monitor = get_token_monitor()
    status = monitor._get_subscription_status()
    
    print("\n   💳 Subscription Status:")
    for provider, info in status.items():
        if info['limit'] > 0:
            print(f"      {provider}: ${info['used']:.2f} of ${info['limit']} ({info['percentage_used']:.1f}%)")


async def show_detailed_report():
    """Show detailed usage report."""
    print("\n" + "="*60)
    print("📊 DETAILED USAGE REPORT")
    print("="*60)
    
    report = get_usage_report("openai", days=1)
    
    print(f"\nOpenAI Usage Summary:")
    print(f"  Total Requests: {report.get('total_requests', 0)}")
    print(f"  Total Tokens: {report.get('total_tokens', 0):,}")
    print(f"    - Input: {report.get('total_input_tokens', 0):,}")
    print(f"    - Output: {report.get('total_output_tokens', 0):,}")
    print(f"  Total Cost: ${report.get('total_cost_usd', 0):.4f}")
    
    # By operation type
    print("\n  By Service Type:")
    for service, stats in report.get('by_service_type', {}).items():
        print(f"    {service}: {stats['requests']} requests, {stats['tokens']:,} tokens")
    
    # By model
    print("\n  By Model:")
    for model_info in report.get('by_model', []):
        print(f"    {model_info['model']}: {model_info['tokens']:,} tokens (${model_info['cost']:.4f})")


async def show_final_summary():
    """Show final summary with alerts."""
    monitor = get_token_monitor()
    
    # Check alerts
    report = get_usage_report("openai")
    alerts = monitor._check_alerts("openai", report)
    
    if alerts:
        print("\n   ⚠️  ALERTS:")
        for alert in alerts:
            print(f"      {alert}")
    
    # Show subscription status
    status = monitor._get_subscription_status()
    
    print("\n   📈 Usage vs Limits:")
    for provider, info in status.items():
        if info['limit'] > 0:
            bar_length = 30
            filled = int(bar_length * info['percentage_used'] / 100)
            bar = "█" * filled + "░" * (bar_length - filled)
            
            status_emoji = "✅" if info['status'] == 'ok' else "⚠️" if info['status'] == 'warning' else "🚨"
            print(f"      {provider}: [{bar}] {info['percentage_used']:.1f}% {status_emoji}")


async def main():
    """Run the simulation."""
    try:
        await simulate_graphiti_operations()
        
        print("\n\n✅ Simulation completed!")
        print("\n📈 Explore the data with these commands:")
        print("   uv run graphiti-tokens summary         # View usage summary")
        print("   uv run graphiti-tokens status          # Check subscription status")
        print("   uv run graphiti-tokens alerts          # Check for alerts")
        print("   uv run graphiti-tokens export demo.csv # Export data")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())