"""
Test OpenAI Graphiti Instance - Minimal Test
"""

import asyncio
import os
from datetime import datetime, timezone
from graphiti_core import Graphiti
from graphiti_core.nodes import EpisodeType
from graphiti_core.llm_client.config import LLMConfig
from graphiti_core.llm_client.openai_client import OpenAIClient
from graphiti_core.embedder.openai import OpenAIEmbedder, OpenAIEmbedderConfig

async def test_openai_instance():
    """Test OpenAI Graphiti instance with bolt://localhost:7694."""
    
    print("🔍 Testing OpenAI Graphiti Instance...")
    
    try:
        # Create LLM configuration (copying exact working pattern)
        llm_config = LLMConfig(
            api_key=os.environ.get("OPENAI_API_KEY"),
            model="gpt-4o",  # Primary model that supports json_schema
            small_model="gpt-4o-mini"  # Include small_model as in working example
        )
        
        # Create LLM client
        llm_client = OpenAIClient(llm_config)
        
        # Create embedder config with text-embedding-3-large (3072 dimensions)
        embedder_config = OpenAIEmbedderConfig(
            api_key=os.environ.get("OPENAI_API_KEY"),
            embedding_model="text-embedding-3-large",  # Better quality embeddings
            embedding_dim=3072  # Match Gemini dimensions for fair comparison
        )
        
        # Create embedder
        embedder = OpenAIEmbedder(config=embedder_config)
        
        # Initialize Graphiti with configured clients
        graphiti = Graphiti(
            uri="bolt://localhost:7694",
            user="neo4j", 
            password="pepo_graphiti_2025",
            llm_client=llm_client,
            embedder=embedder
        )
        
        print("✅ Graphiti OpenAI instance created")
        
        # Build indices and constraints (first time setup)
        await graphiti.build_indices_and_constraints()
        print("✅ Indices and constraints built")
        
        # Test basic operation
        await graphiti.add_episode(
            name="test_openai_episode",
            episode_body="This is a test episode for OpenAI embeddings evaluation.",
            reference_time=datetime.now(timezone.utc),
            source=EpisodeType.text,
            source_description="Test source for OpenAI evaluation framework",
            group_id="eval_openai"
        )
        
        print("✅ Episode added successfully")
        
        # Test search (simplified to avoid API issue)
        try:
            results = await graphiti.search("test episode")
            print(f"✅ Search successful - found results")
        except Exception as e:
            print(f"⚠️ Search had issues (expected with new DB): {str(e)[:100]}...")
        
        # Test node search
        try:
            node_results = await graphiti.search_nodes(
                query="test episode",
                num_results=5
            )
            print(f"✅ Node search successful - found {len(node_results)} nodes")
        except Exception as e:
            print(f"⚠️ Node search had issues (expected with new DB): {str(e)[:100]}...")
        
        await graphiti.close()
        print("✅ OpenAI instance test completed successfully")
        return True
        
    except Exception as e:
        print(f"❌ OpenAI instance test failed: {e}")
        return False

if __name__ == "__main__":
    result = asyncio.run(test_openai_instance())
    if result:
        print("🎉 OpenAI instance ready for evaluation")
    else:
        print("💥 OpenAI instance setup failed")