#!/usr/bin/env python3
"""
Initialize token monitoring for Graphiti
Sets up default configurations and subscription limits
"""

import os
from pathlib import Path
from graphiti_core.telemetry import (
    get_token_monitor, 
    set_provider_limit,
    _TOKEN_MONITORING_AVAILABLE
)

def init_token_monitoring():
    """Initialize token monitoring with sensible defaults."""
    
    if not _TOKEN_MONITORING_AVAILABLE:
        print("❌ Token monitoring not available. Install dependencies:")
        print("   pip install graphiti-core[token-monitoring]")
        print("   # or")
        print("   uv pip install graphiti-core[token-monitoring]")
        return False
    
    print("🚀 Initializing Graphiti Token Monitoring System")
    print("=" * 50)
    
    monitor = get_token_monitor()
    storage_dir = Path(os.path.expanduser("~/.graphiti/token_monitor"))
    
    # Create directories
    storage_dir.mkdir(parents=True, exist_ok=True)
    
    # Set default limits (users should update these)
    defaults = {
        "anthropic": ("max_plan_tokens", 5_000_000, "5M tokens (Max plan)"),
        "openai": ("prepaid_credits", 0, "No limit set"),
        "gemini": ("free_tier_tokens", 1_000_000, "1M tokens (free tier)"),
    }
    
    print("\n📊 Setting default subscription limits:")
    for provider, (limit_type, value, description) in defaults.items():
        set_provider_limit(provider, limit_type, value)
        print(f"  • {provider}: {description}")
    
    print("\n✅ Token monitoring initialized successfully!")
    print(f"📁 Data stored in: {storage_dir}")
    
    print("\n🔧 Next steps:")
    print("1. Update your subscription limits:")
    print("   graphiti-tokens set-limit anthropic max_plan_tokens 5000000")
    print("   graphiti-tokens set-limit openai prepaid_credits 100")
    print("\n2. Check current usage:")
    print("   graphiti-tokens summary")
    print("   graphiti-tokens status")
    print("\n3. View all commands:")
    print("   graphiti-tokens --help")
    
    return True

def check_monitoring_status():
    """Check if monitoring is properly configured."""
    if not _TOKEN_MONITORING_AVAILABLE:
        return False
    
    try:
        monitor = get_token_monitor()
        # Try to get a report to verify it works
        monitor.get_comprehensive_report()
        return True
    except Exception as e:
        print(f"❌ Error checking monitoring status: {e}")
        return False

if __name__ == "__main__":
    # Run initialization when called directly
    success = init_token_monitoring()
    
    if success:
        print("\n🔍 Verifying installation...")
        if check_monitoring_status():
            print("✅ Token monitoring is working correctly!")
        else:
            print("⚠️ Token monitoring initialized but verification failed")