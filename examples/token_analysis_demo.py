#!/usr/bin/env python3
"""
Token Analysis Demo - Uses LLM to analyze token monitoring events
and generate structured entities representing the analysis.

This demo demonstrates:
1. Retrieval of token monitoring data
2. LLM analysis of usage patterns 
3. Entity structure generation
4. Episode creation with analysis results
"""

import asyncio
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from graphiti_core.telemetry import (
        get_usage_report,
        get_token_monitor,
        _TOKEN_MONITORING_AVAILABLE
    )
except ImportError:
    _TOKEN_MONITORING_AVAILABLE = False

from graphiti_core import Graphiti
from graphiti_core.prompts.models import Message


def format_usage_for_analysis(usage_report):
    """Format usage report data for LLM analysis."""
    if not usage_report:
        return "No usage data found."
    
    formatted = f"""
    Provider: {usage_report.get('provider', 'unknown')}
    Total Requests: {usage_report.get('total_requests', 0)}
    Total Tokens: {usage_report.get('total_tokens', 0):,}
    Total Cost: ${usage_report.get('total_cost_usd', 0):.4f}
    
    By Service Type:
    """
    
    for service, stats in usage_report.get('by_service_type', {}).items():
        formatted += f"- {service}: {stats['requests']} requests, {stats['tokens']} tokens, ${stats.get('cost_usd', 0):.4f}\n"
    
    formatted += "\n    By Model:\n"
    for model_data in usage_report.get('by_model', []):
        if isinstance(model_data, dict):
            model = model_data.get('model', 'unknown')
            requests = model_data.get('requests', 0)
            tokens = model_data.get('tokens', 0)
            formatted += f"- {model}: {requests} requests, {tokens:,} tokens\n"
    
    return formatted.strip()


def create_analysis_prompt(usage_report):
    """Create analysis prompt for LLM."""
    formatted_data = format_usage_for_analysis(usage_report)
    
    return f"""
    Analyze the following token monitoring data and provide insights about API usage patterns:

    {formatted_data}

    Please analyze this data and provide:
    1. Key patterns in API usage
    2. Cost optimization opportunities  
    3. Usage efficiency insights
    4. Recommendations for better token management

    Focus on actionable insights that would help a developer optimize their AI API usage.
    Structure your response with clear sections and practical recommendations.
    
    Please provide your analysis in a well-structured format using clear headings and json-like organization.
    """


def create_entity_structure(usage_report, analysis_result):
    """Create structured entities from the analysis."""
    return {
        "analysis_session": {
            "id": f"token_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "timestamp": datetime.now().isoformat(),
            "data_period": "24_hours",
            "requests_analyzed": usage_report.get('total_requests', 0)
        },
        "usage_metrics": {
            "total_requests": usage_report.get('total_requests', 0),
            "total_tokens": usage_report.get('total_tokens', 0),
            "total_cost": usage_report.get('total_cost_usd', 0),
            "primary_service": max(usage_report.get('by_service_type', {}).items(), 
                                 key=lambda x: x[1]['tokens'], default=('unknown', {'tokens': 0}))[0]
        },
        "analysis_insights": {
            "content": analysis_result,
            "generated_by": "llm_analysis",
            "analysis_type": "token_usage_optimization",
            "generated_at": datetime.now().isoformat()
        }
    }


async def analyze_token_usage_with_llm():
    """Use LLM to analyze token monitoring data and generate insights."""
    
    print("🔍 TOKEN USAGE ANALYSIS WITH LLM")
    print("="*50)
    
    # Check if token monitoring is available
    if not _TOKEN_MONITORING_AVAILABLE:
        print("❌ Token monitoring not available. Run:")
        print("   uv sync --extra token-monitoring")
        return
    
    # Get token usage data
    print("\n📊 Retrieving token usage data...")
    usage_report = get_usage_report("openai", days=1)
    monitor = get_token_monitor()
    comprehensive_report = monitor.get_comprehensive_report()
    
    if not usage_report.get('total_requests', 0):
        print("❌ No usage data found. Run the token monitoring demo first:")
        print("   ./run.sh examples/token_monitoring_real_demo.py --confirm")
        return
    
    print(f"   ✅ Found {usage_report.get('total_requests', 0)} requests in last 24h")
    print(f"   ✅ Total tokens: {usage_report.get('total_tokens', 0):,}")
    print(f"   ✅ Total cost: ${usage_report.get('total_cost_usd', 0):.4f}")
    
    # Initialize Graphiti for LLM analysis
    print("\n🤖 Initializing LLM for analysis...")
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
    
    # Apply monitoring patches to capture this LLM usage too
    from examples.token_monitoring_real_demo import patch_graphiti_for_monitoring
    if patch_graphiti_for_monitoring():
        print("   ✅ Token monitoring patches applied")
    
    # Create analysis prompt
    analysis_prompt = create_analysis_prompt(usage_report)
    
    # Perform LLM analysis
    print("\n🧠 Analyzing token usage patterns with LLM...")
    try:
        messages = [Message(role="user", content=analysis_prompt)]
        
        # This will be monitored by our token system
        response = await graphiti.llm_client._generate_response(
            messages=messages,
            response_model=None,
            max_tokens=1000
        )
        
        # Extract content from response
        if isinstance(response, dict):
            # The response structure has the analysis under a key like 'API_Usage_Analysis'
            analysis_result = response.get('content') or response.get('text') or response.get('message') or str(response)
        else:
            analysis_result = str(response)
            
        print(f"   ✅ LLM analysis completed ({len(analysis_result)} characters)")
        
    except Exception as e:
        print(f"   ❌ LLM analysis failed: {e}")
        return
    
    # Create structured entities from the analysis
    print("\n🏗️ Creating structured entities from analysis...")
    
    entity_structure = create_entity_structure(usage_report, analysis_result)
    
    # Create episode with the analysis and entity structure
    episode_content = f"""
TOKEN USAGE ANALYSIS REPORT

Analysis Session: {entity_structure['analysis_session']['id']}
Timestamp: {entity_structure['analysis_session']['timestamp']}

USAGE METRICS ANALYZED:
- Total Requests: {entity_structure['usage_metrics']['total_requests']}
- Total Tokens: {entity_structure['usage_metrics']['total_tokens']:,}
- Total Cost: ${entity_structure['usage_metrics']['total_cost']:.4f}
- Primary Service: {entity_structure['usage_metrics']['primary_service']}

LLM ANALYSIS INSIGHTS:
{analysis_result}

ENTITY STRUCTURE GENERATED:
This analysis created structured entities representing:
- Analysis session metadata (ID: {entity_structure['analysis_session']['id']})
- Usage metrics summary ({entity_structure['usage_metrics']['total_requests']} requests analyzed)
- LLM-generated insights and recommendations

This demonstrates how token monitoring data can be analyzed by LLMs to generate
actionable insights and structured knowledge about API usage patterns.
The analysis was performed at {entity_structure['analysis_insights']['generated_at']} 
using {entity_structure['analysis_insights']['generated_by']}.
"""
    
    try:
        await graphiti.add_episode(
            name="Token Usage Analysis Report",
            episode_body=episode_content,
            source_description="LLM-generated analysis of token monitoring data",
            reference_time=datetime.now()
        )
        print("   ✅ Analysis episode added to Graphiti")
        
    except Exception as e:
        print(f"   ❌ Failed to add episode: {e}")
    
    # Show final results
    print("\n📋 ANALYSIS RESULTS:")
    print("="*50)
    print(analysis_result)
    
    print("\n📊 ENTITY STRUCTURE CREATED:")
    print("="*50)
    for entity_type, entity_data in entity_structure.items():
        print(f"\n{entity_type.upper()}:")
        for key, value in entity_data.items():
            if isinstance(value, str) and len(value) > 100:
                print(f"  {key}: {value[:100]}...")
            else:
                print(f"  {key}: {value}")
    
    # Cleanup
    await graphiti.close()
    
    print("\n✅ Token usage analysis completed!")
    print("📈 You can now explore the updated data:")
    print("   uv run graphiti-tokens summary -p openai -d 1")
    print("   uv run graphiti-tokens export analysis_results.csv -d 1")


async def main(skip_confirmation=False):
    """Run the token analysis demo."""
    
    print("🧠 TOKEN USAGE ANALYSIS DEMO")
    print("⚠️  This will make REAL API calls to analyze token data!")
    print("="*60)
    
    # Check API key
    if not os.getenv("OPENAI_API_KEY"):
        print("\n❌ Please set OPENAI_API_KEY environment variable")
        return
    
    # Confirm with user (unless skipped)
    if not skip_confirmation:
        print("\nThis demo will:")
        print("  • Analyze your token monitoring data")
        print("  • Make LLM calls to generate insights")
        print("  • Create structured entities in Graphiti")
        print("  • Cost approximately $0.01-0.03")
        print("\nDo you want to continue? (yes/no): ", end="")
        
        if input().lower() != 'yes':
            print("Demo cancelled.")
            return
    else:
        print("\n✅ Running with --confirm flag (skipping confirmation)")
        print("This demo will:")
        print("  • Analyze your token monitoring data")
        print("  • Make LLM calls to generate insights")
        print("  • Create structured entities in Graphiti")
        print("  • Cost approximately $0.01-0.03")
    
    await analyze_token_usage_with_llm()


if __name__ == "__main__":
    # Add safety check
    if len(sys.argv) > 1 and sys.argv[1] == "--confirm":
        asyncio.run(main(skip_confirmation=True))
    else:
        print("📋 TOKEN ANALYSIS DEMO PLAN")
        print("="*60)
        print("\nThis script will:")
        print("1. ✅ Retrieve token monitoring data from the last 24 hours")
        print("2. ✅ Use LLM to analyze usage patterns and generate insights")
        print("3. ✅ Create structured entities representing the analysis")
        print("4. ✅ Store the analysis as an episode in Graphiti")
        print("5. ✅ Demonstrate LLM-driven analysis of monitoring data")
        print("\nTo run: ./run.sh examples/token_analysis_demo.py --confirm")