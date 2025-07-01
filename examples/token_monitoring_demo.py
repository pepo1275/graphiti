#!/usr/bin/env python3
"""
Token Monitoring Demo for Graphiti
Shows real-time token usage tracking while adding memories
"""

import asyncio
import os
from datetime import datetime
from graphiti_core import Graphiti
from graphiti_core.nodes import EpisodeType
from neo4j import AsyncGraphDatabase

# Import token monitoring - will use dummy functions if not available
from graphiti_core.telemetry import (
    _TOKEN_MONITORING_AVAILABLE,
    get_token_monitor,
    get_usage_report,
    log_llm_usage,
    set_provider_limit
)

# For demonstration, we'll patch the OpenAI client to add monitoring
from graphiti_core.llm_client.openai_client import OpenAIClient
from graphiti_core.llm_client.config import LLMConfig
from graphiti_core.embedder.openai import OpenAIEmbedder
from functools import wraps


def add_monitoring_to_openai():
    """Monkey-patch OpenAI client to add token monitoring."""
    if not _TOKEN_MONITORING_AVAILABLE:
        print("⚠️  Token monitoring not available - install with: pip install graphiti-core[token-monitoring]")
        return
    
    # Save original method
    original_generate = OpenAIClient._generate_response_base
    
    @wraps(original_generate)
    async def monitored_generate(self, messages, response_model=None, **kwargs):
        """Wrapper that adds monitoring."""
        print(f"🔍 Monitoring LLM call to {self.llm_config.model}...")
        
        try:
            # Call original method
            result = await original_generate(self, messages, response_model, **kwargs)
            
            # Extract token usage from response
            if hasattr(result, '_raw_response'):
                raw = result._raw_response
                if hasattr(raw, 'usage'):
                    log_llm_usage(
                        provider="openai",
                        model=self.llm_config.model,
                        input_tokens=raw.usage.prompt_tokens,
                        output_tokens=raw.usage.completion_tokens,
                        operation="generate_response",
                        metadata={
                            "response_model": response_model.__name__ if response_model else "text",
                            "timestamp": datetime.now().isoformat()
                        }
                    )
                    print(f"   ✅ Logged: {raw.usage.prompt_tokens} input + {raw.usage.completion_tokens} output tokens")
            
            return result
            
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            log_llm_usage(
                provider="openai",
                model=self.llm_config.model,
                input_tokens=0,
                output_tokens=0,
                operation="generate_response",
                metadata={"error": str(e)}
            )
            raise
    
    # Replace method
    OpenAIClient._generate_response_base = monitored_generate
    print("✅ Token monitoring added to OpenAI client")


async def show_token_usage():
    """Display current token usage statistics."""
    if not _TOKEN_MONITORING_AVAILABLE:
        return
    
    print("\n" + "="*60)
    print("📊 TOKEN USAGE REPORT")
    print("="*60)
    
    report = get_usage_report("openai", days=1)
    
    print(f"\nOpenAI Usage (Last 24 hours):")
    print(f"  Total Requests: {report.get('total_requests', 0)}")
    print(f"  Total Tokens: {report.get('total_tokens', 0):,}")
    print(f"    - Input: {report.get('total_input_tokens', 0):,}")
    print(f"    - Output: {report.get('total_output_tokens', 0):,}")
    print(f"  Estimated Cost: ${report.get('total_cost_usd', 0):.4f}")
    
    # Show by model
    if report.get('by_model'):
        print("\n  By Model:")
        for model_info in report['by_model']:
            print(f"    {model_info['model']}: {model_info['tokens']:,} tokens (${model_info['cost']:.4f})")
    
    print("="*60 + "\n")


async def demo_graphiti_with_monitoring():
    """Run a demonstration of Graphiti with token monitoring."""
    
    print("🚀 GRAPHITI TOKEN MONITORING DEMO")
    print("="*60)
    
    # Setup monitoring
    if _TOKEN_MONITORING_AVAILABLE:
        print("\n1️⃣ Setting up token monitoring...")
        monitor = get_token_monitor()
        
        # Set a demo limit
        set_provider_limit("openai", "prepaid_credits", 10)  # $10 limit for demo
        print("   ✅ Set OpenAI limit to $10 (demo)")
        
        # Add monitoring to OpenAI
        add_monitoring_to_openai()
    else:
        print("\n⚠️  Token monitoring not installed - continuing without monitoring")
    
    # Initialize Graphiti
    print("\n2️⃣ Initializing Graphiti...")
    
    # Neo4j connection
    uri = "bolt://localhost:7687"
    username = "neo4j"
    password = "pepo_graphiti_2025"
    
    try:
        # Create driver to test connection
        driver = AsyncGraphDatabase.driver(uri, auth=(username, password))
        await driver.verify_connectivity()
        await driver.close()
        print("   ✅ Neo4j connection successful")
    except Exception as e:
        print(f"   ❌ Neo4j connection failed: {e}")
        print("   Please ensure Neo4j is running on bolt://localhost:7687")
        return
    
    # Initialize Graphiti
    graphiti = Graphiti(uri, username, password)
    await graphiti.build_indices_and_constraints()
    print("   ✅ Graphiti initialized")
    
    # Show initial usage
    await show_token_usage()
    
    # Add test episodes
    print("\n3️⃣ Adding test episodes to demonstrate token usage...")
    
    test_episodes = [
        {
            "content": "Dr. Sarah Chen presented groundbreaking research on quantum computing applications in medicine at the Stanford AI Conference 2024. Her work focuses on using quantum algorithms to accelerate drug discovery.",
            "name": "Quantum Medicine Research"
        },
        {
            "content": "The new ElectricFlow X5 vehicle from TechnoMotors features a revolutionary 800-mile range battery and can charge to 80% in just 10 minutes using their proprietary UltraCharge technology.",
            "name": "EV Technology Update"
        },
        {
            "content": "Chef Marco Rossi opened his third restaurant 'Sapori Moderni' in downtown Seattle, bringing his fusion of traditional Italian cuisine with Pacific Northwest ingredients to a new audience.",
            "name": "Restaurant Opening"
        }
    ]
    
    for i, episode_data in enumerate(test_episodes, 1):
        print(f"\n   📝 Episode {i}: {episode_data['name']}")
        print(f"      Content: {episode_data['content'][:80]}...")
        
        # Add episode
        result = await graphiti.add_episode(
            name=episode_data["name"],
            episode_body=episode_data["content"],
            source_description="Token monitoring demo",
            reference_time=datetime.now()
        )
        
        print(f"      ✅ Added successfully")
        
        # Show usage after each episode
        if _TOKEN_MONITORING_AVAILABLE and i == 1:  # Show detailed after first
            await show_token_usage()
    
    # Search demonstration
    print("\n4️⃣ Performing searches to demonstrate embedding token usage...")
    
    search_queries = [
        "quantum computing medical applications",
        "electric vehicle battery technology",
        "Italian restaurant Seattle"
    ]
    
    for query in search_queries:
        print(f"\n   🔍 Searching: '{query}'")
        
        # Search nodes
        results = await graphiti.search_nodes(
            query=query,
            num_results=3
        )
        
        print(f"      Found {len(results)} results")
        for result in results[:2]:  # Show first 2
            print(f"      - {result.name} (score: {result.score:.3f})")
    
    # Final usage report
    print("\n5️⃣ Final Token Usage Summary")
    await show_token_usage()
    
    # Show subscription status
    if _TOKEN_MONITORING_AVAILABLE:
        monitor = get_token_monitor()
        status = monitor._get_subscription_status()
        
        if "openai" in status:
            info = status["openai"]
            print(f"\n💳 Subscription Status:")
            print(f"   OpenAI: ${info['used']:.4f} of ${info['limit']} used ({info['percentage_used']:.1f}%)")
            print(f"   Status: {info['status']} {'⚠️' if info['status'] == 'warning' else '✅'}")
    
    # Cleanup
    await graphiti.close()
    print("\n✅ Demo completed!")
    
    if _TOKEN_MONITORING_AVAILABLE:
        print("\n📈 You can now use these commands to explore the data:")
        print("   graphiti-tokens summary         # View usage summary")
        print("   graphiti-tokens status          # Check subscription status")
        print("   graphiti-tokens export demo.csv # Export data for analysis")


async def main():
    """Main entry point."""
    try:
        await demo_graphiti_with_monitoring()
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error during demo: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # Check environment
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Please set OPENAI_API_KEY environment variable")
        exit(1)
    
    # Run demo
    asyncio.run(main())