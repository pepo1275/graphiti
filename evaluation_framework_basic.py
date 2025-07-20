"""
Basic Evaluation Framework - Minimal Version for Testing
Phase 1: Just structure and basic metrics
"""

from dataclasses import dataclass
from typing import Dict, Any
import time
import json
from datetime import datetime

@dataclass
class BasicMetrics:
    """Simple metrics for initial testing."""
    node_count: int
    edge_count: int
    response_time_ms: float
    success: bool
    timestamp: str
    
    def to_dict(self):
        return {
            "node_count": self.node_count,
            "edge_count": self.edge_count,
            "response_time_ms": self.response_time_ms,
            "success": self.success,
            "timestamp": self.timestamp
        }

class BasicEvaluator:
    """Minimal evaluator for testing approach."""
    
    def __init__(self, graphiti_instance=None):
        self.graphiti = graphiti_instance
        
    def evaluate_basic(self) -> BasicMetrics:
        """Run basic evaluation - just check if it works."""
        start_time = time.time()
        
        try:
            # Mock basic operations
            node_count = 10  # Would get from graphiti
            edge_count = 20  # Would get from graphiti
            success = True
            
        except Exception as e:
            print(f"Evaluation failed: {e}")
            node_count = 0
            edge_count = 0
            success = False
        
        response_time = (time.time() - start_time) * 1000
        
        return BasicMetrics(
            node_count=node_count,
            edge_count=edge_count,
            response_time_ms=response_time,
            success=success,
            timestamp=datetime.now().isoformat()
        )

def test_basic_framework():
    """Test the basic framework works."""
    print("Testing basic evaluation framework...")
    
    evaluator = BasicEvaluator()
    result = evaluator.evaluate_basic()
    
    print(f"Result: {result}")
    print(f"JSON: {json.dumps(result.to_dict(), indent=2)}")
    
    assert result.success, "Basic evaluation should succeed"
    assert result.response_time_ms > 0, "Should measure response time"
    
    print("✅ Basic framework test passed!")
    return result

if __name__ == "__main__":
    test_basic_framework()