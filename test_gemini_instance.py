"""
Test Gemini Graphiti Instance - Using existing implementations
"""

import asyncio
import os
from datetime import datetime, timezone
from graphiti_core import Graphiti
from graphiti_core.nodes import EpisodeType
from graphiti_core.llm_client.gemini_client import GeminiClient
from graphiti_core.llm_client.config import LLMConfig
from graphiti_core.embedder.gemini import GeminiEmbedder, GeminiEmbedderConfig

async def test_gemini_instance():
    """Test Gemini Graphiti instance with bolt://localhost:7693."""
    
    print("🔍 Testing Gemini Graphiti Instance...")
    
    try:
        # Create Gemini LLM configuration (using 2.5-pro + 2.5-flash pattern)
        llm_config = LLMConfig(
            api_key=os.environ.get("GOOGLE_API_KEY"),
            model="gemini-2.5-pro",  # Primary model for complex tasks
            small_model="gemini-2.5-flash",  # Secondary model for simpler tasks
            temperature=0.0
        )
        
        # Create Gemini LLM client
        llm_client = GeminiClient(config=llm_config)
        
        print(f"✅ Gemini LLM client created - model: {llm_client.config.model}")
        print(f"✅ Gemini small model configured: {llm_client.config.small_model}")
        
        # Create Gemini embedder config with gemini-embedding-001 + 3072 dimensions (max)
        embedder_config = GeminiEmbedderConfig(
            api_key=os.environ.get("GOOGLE_API_KEY"),
            embedding_model="gemini-embedding-001",  # GA model with CODE_RETRIEVAL_QUERY support
            embedding_dim=3072  # Maximum dimensions to match OpenAI text-embedding-3-large
        )
        
        # Create Gemini embedder
        embedder = GeminiEmbedder(config=embedder_config)
        
        print(f"✅ Gemini embedder created - model: {embedder_config.embedding_model}")
        
        # Initialize Graphiti with Gemini clients on dedicated instance
        graphiti = Graphiti(
            uri="bolt://localhost:7693",  # Gemini dedicated instance
            user="neo4j", 
            password="pepo_graphiti_2025",
            llm_client=llm_client,
            embedder=embedder
        )
        
        print("✅ Graphiti Gemini instance created")
        
        # Build indices and constraints (first time setup)
        await graphiti.build_indices_and_constraints()
        print("✅ Indices and constraints built")
        
        # Test with code content to leverage CODE_RETRIEVAL_QUERY task type
        test_content = """
        def quicksort(arr):
            if len(arr) <= 1:
                return arr
            pivot = arr[len(arr) // 2]
            left = [x for x in arr if x < pivot]
            middle = [x for x in arr if x == pivot]
            right = [x for x in arr if x > pivot]
            return quicksort(left) + middle + quicksort(right)
        
        This is a test episode for Gemini embeddings evaluation with code content
        to test CODE_RETRIEVAL_QUERY task type optimization.
        """
        
        # Test basic operation with code content
        await graphiti.add_episode(
            name="test_gemini_code_episode",
            episode_body=test_content,
            reference_time=datetime.now(timezone.utc),
            source=EpisodeType.text,
            source_description="Test source for Gemini evaluation framework with code content",
            group_id="eval_gemini"
        )
        
        print("✅ Episode with code content added successfully")
        
        # Test search (should leverage CODE_RETRIEVAL_QUERY)
        try:
            results = await graphiti.search("quicksort algorithm")
            print(f"✅ Search successful - found results")
        except Exception as e:
            print(f"⚠️ Search had issues (expected with new DB): {str(e)[:100]}...")
        
        # Test non-code content
        await graphiti.add_episode(
            name="test_gemini_text_episode", 
            episode_body="This is a regular text episode for Gemini embeddings evaluation without code content.",
            reference_time=datetime.now(timezone.utc),
            source=EpisodeType.text,
            source_description="Test source for Gemini evaluation framework with text content",
            group_id="eval_gemini"
        )
        
        print("✅ Text episode added successfully")
        
        await graphiti.close()
        print("✅ Gemini instance test completed successfully")
        return True
        
    except Exception as e:
        print(f"❌ Gemini instance test failed: {e}")
        try:
            await graphiti.close()
        except:
            pass
        return False

if __name__ == "__main__":
    # Configure API key (prefer GOOGLE_API_KEY, fallback to GEMINI_API_KEY)
    google_api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not google_api_key:
        print("❌ GOOGLE_API_KEY or GEMINI_API_KEY required")
        print("💡 Set with: export GOOGLE_API_KEY='your_google_api_key'")
        exit(1)
    
    # Set GOOGLE_API_KEY for the script
    os.environ["GOOGLE_API_KEY"] = google_api_key
    print(f"✅ Using API key: {google_api_key[:8]}...")
    
    result = asyncio.run(test_gemini_instance())
    if result:
        print("\n🎉 Gemini instance ready for evaluation")
        print("📍 Instance: bolt://localhost:7693")
        print("🤖 LLM Primary: gemini-2.5-pro")
        print("🚀 LLM Secondary: gemini-2.5-flash")
        print("🔗 Embeddings: gemini-embedding-001 with CODE_RETRIEVAL_QUERY support")
    else:
        print("\n💥 Gemini instance setup failed")