"""
Tests para validar implementación CODE_RETRIEVAL_QUERY antes de implementar
Siguiendo TDD (Test-Driven Development)
"""

import pytest
import os
from unittest.mock import Mock, patch, AsyncMock
from graphiti_core.embedder.gemini import GeminiEmbedder, GeminiEmbedderConfig

class TestCodeRetrievalQueryImplementation:
    """Tests para validar implementación CODE_RETRIEVAL_QUERY"""
    
    def test_task_type_in_config(self):
        """Test 1: Verificar que task_type está en la configuración"""
        config = GeminiEmbedderConfig(
            embedding_model="gemini-embedding-001",
            task_type="CODE_RETRIEVAL_QUERY"
        )
        assert hasattr(config, 'task_type')
        assert config.task_type == "CODE_RETRIEVAL_QUERY"
    
    def test_task_type_none_by_default(self):
        """Test 2: task_type debe ser None por defecto"""
        config = GeminiEmbedderConfig()
        assert config.task_type is None
    
    def test_detect_content_type_function_exists(self):
        """Test 3: Función de detección de contenido debe existir"""
        # Este test fallará hasta que implementemos la función
        from graphiti_core.embedder.gemini import detect_content_type
        
        # Test con código Python
        python_code = "def quicksort(arr): return sorted(arr)"
        assert detect_content_type(python_code) == "CODE_RETRIEVAL_QUERY"
        
        # Test con query Cypher
        cypher_query = "MATCH (n:Person) WHERE n.age > 30 RETURN n"
        assert detect_content_type(cypher_query) == "CODE_RETRIEVAL_QUERY"
        
        # Test con texto regular
        regular_text = "This is a regular text without code indicators"
        assert detect_content_type(regular_text) == "RETRIEVAL_QUERY"
    
    @pytest.mark.asyncio
    async def test_task_type_passed_to_api(self):
        """Test 4: Verificar que task_type se pasa a la API Gemini"""
        config = GeminiEmbedderConfig(
            task_type="CODE_RETRIEVAL_QUERY"
        )
        embedder = GeminiEmbedder(config)
        
        # Mock del cliente
        with patch.object(embedder.client.aio.models, 'embed_content') as mock_embed:
            mock_result = Mock()
            mock_result.embeddings = [Mock(values=[0.1, 0.2, 0.3])]
            mock_embed.return_value = mock_result
            
            await embedder.create("test code")
            
            # Verificar que se llamó con task_type en el config
            call_args = mock_embed.call_args
            assert 'config' in call_args.kwargs
            config_used = call_args.kwargs['config']
            assert hasattr(config_used, 'task_type')
            assert config_used.task_type == "CODE_RETRIEVAL_QUERY"
    
    @pytest.mark.asyncio
    async def test_automatic_detection_with_python_code(self):
        """Test 5: Detección automática con código Python"""
        config = GeminiEmbedderConfig()  # Sin task_type explícito
        embedder = GeminiEmbedder(config)
        
        python_code = """
        def binary_search(arr, target):
            left, right = 0, len(arr) - 1
            while left <= right:
                mid = (left + right) // 2
                if arr[mid] == target:
                    return mid
                elif arr[mid] < target:
                    left = mid + 1
                else:
                    right = mid - 1
            return -1
        """
        
        with patch.object(embedder.client.aio.models, 'embed_content') as mock_embed:
            mock_result = Mock()
            mock_result.embeddings = [Mock(values=[0.1, 0.2, 0.3])]
            mock_embed.return_value = mock_result
            
            await embedder.create(python_code)
            
            # Debe detectar automáticamente CODE_RETRIEVAL_QUERY
            config_used = mock_embed.call_args.kwargs['config']
            assert config_used.task_type == "CODE_RETRIEVAL_QUERY"

    @pytest.mark.asyncio  
    async def test_automatic_detection_with_cypher_query(self):
        """Test 6: Detección automática con query Cypher"""
        config = GeminiEmbedderConfig()
        embedder = GeminiEmbedder(config)
        
        cypher_query = """
        MATCH (p:Person)-[:WORKS_AT]->(c:Company)
        WHERE p.age > 30 AND c.industry = 'Technology'
        RETURN p.name, c.name, p.salary
        ORDER BY p.salary DESC
        LIMIT 10
        """
        
        with patch.object(embedder.client.aio.models, 'embed_content') as mock_embed:
            mock_result = Mock()
            mock_result.embeddings = [Mock(values=[0.1, 0.2, 0.3])]
            mock_embed.return_value = mock_result
            
            await embedder.create(cypher_query)
            
            # Debe detectar automáticamente CODE_RETRIEVAL_QUERY
            config_used = mock_embed.call_args.kwargs['config']
            assert config_used.task_type == "CODE_RETRIEVAL_QUERY"

    @pytest.mark.asyncio
    async def test_no_task_type_for_regular_text(self):
        """Test 7: No usar task_type para texto regular"""
        config = GeminiEmbedderConfig()
        embedder = GeminiEmbedder(config)
        
        regular_text = "This is a regular text about machine learning and artificial intelligence."
        
        with patch.object(embedder.client.aio.models, 'embed_content') as mock_embed:
            mock_result = Mock()
            mock_result.embeddings = [Mock(values=[0.1, 0.2, 0.3])]
            mock_embed.return_value = mock_result
            
            await embedder.create(regular_text)
            
            # No debe usar CODE_RETRIEVAL_QUERY para texto regular
            config_used = mock_embed.call_args.kwargs['config']
            assert config_used.task_type == "RETRIEVAL_QUERY"

if __name__ == "__main__":
    # Ejecutar tests
    pytest.main([__file__, "-v"])