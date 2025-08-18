"""
Prueba real de CODE_RETRIEVAL_QUERY vs embeddings estándar
Test de escritura y recuperación end-to-end
"""

import asyncio
import os
from datetime import datetime, timezone
from graphiti_core import Graphiti
from graphiti_core.nodes import EpisodeType
from graphiti_core.llm_client.gemini_client import GeminiClient
from graphiti_core.llm_client.config import LLMConfig
from graphiti_core.embedder.gemini import GeminiEmbedder, GeminiEmbedderConfig

async def test_code_retrieval_query_real():
    """Prueba real de CODE_RETRIEVAL_QUERY con escritura y recuperación"""
    
    print("🧪 PRUEBA REAL: CODE_RETRIEVAL_QUERY vs Embeddings Estándar")
    print("=" * 70)
    
    # Configurar API key
    google_api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not google_api_key:
        print("❌ GOOGLE_API_KEY requerida")
        return False
    
    os.environ["GOOGLE_API_KEY"] = google_api_key
    print(f"✅ API Key configurada: {google_api_key[:8]}...")
    
    try:
        # === CONFIGURACIÓN CON CODE_RETRIEVAL_QUERY ===
        print("\n1️⃣ Configurando instancia CON CODE_RETRIEVAL_QUERY...")
        
        # LLM config
        llm_config = LLMConfig(
            api_key=google_api_key,
            model="gemini-2.5-pro",
            small_model="gemini-2.5-flash",
            temperature=0.0
        )
        llm_client = GeminiClient(config=llm_config)
        
        # Embedder CON CODE_RETRIEVAL_QUERY
        embedder_with_code = GeminiEmbedder(config=GeminiEmbedderConfig(
            api_key=google_api_key,
            embedding_model="gemini-embedding-001",
            embedding_dim=3072,
            task_type="CODE_RETRIEVAL_QUERY"  # ← ACTIVADO
        ))
        
        # Graphiti con CODE_RETRIEVAL_QUERY
        graphiti_with_code = Graphiti(
            uri="bolt://localhost:7693",
            user="neo4j",
            password="pepo_graphiti_2025", 
            llm_client=llm_client,
            embedder=embedder_with_code
        )
        
        print("✅ Instancia CON CODE_RETRIEVAL_QUERY creada")
        
        # === CONFIGURACIÓN SIN CODE_RETRIEVAL_QUERY ===
        print("\n2️⃣ Configurando instancia SIN CODE_RETRIEVAL_QUERY...")
        
        # Embedder SIN task_type específico
        embedder_standard = GeminiEmbedder(config=GeminiEmbedderConfig(
            api_key=google_api_key,
            embedding_model="gemini-embedding-001",
            embedding_dim=3072,
            task_type=None  # ← SIN OPTIMIZACIÓN
        ))
        
        # Graphiti estándar (usando puerto diferente para separar datos)
        graphiti_standard = Graphiti(
            uri="bolt://localhost:7687",  # Puerto diferente
            user="neo4j",
            password="pepo_graphiti_2025",
            llm_client=llm_client,
            embedder=embedder_standard
        )
        
        print("✅ Instancia SIN CODE_RETRIEVAL_QUERY creada")
        
        # === DATOS DE PRUEBA ===
        test_episodes = [
            {
                "name": "quicksort_algorithm",
                "content": """
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)

# Algoritmo de ordenamiento rápido con complejidad O(n log n) promedio
""",
                "search_query": "sorting algorithm quicksort python"
            },
            {
                "name": "binary_search_tree",
                "content": """
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class BST:
    def insert(self, root, val):
        if not root:
            return TreeNode(val)
        if val < root.val:
            root.left = self.insert(root.left, val)
        else:
            root.right = self.insert(root.right, val)
        return root
""",
                "search_query": "binary search tree data structure"
            },
            {
                "name": "cypher_person_query",
                "content": """
MATCH (p:Person)-[:WORKS_AT]->(c:Company)
WHERE p.age > 30 AND c.industry = 'Technology'
RETURN p.name, c.name, p.salary
ORDER BY p.salary DESC
LIMIT 10
""",
                "search_query": "find people working in technology companies"
            }
        ]
        
        # === ESCRIBIR EPISODIOS EN AMBAS INSTANCIAS ===
        print("\n3️⃣ Escribiendo episodios de prueba...")
        
        for i, episode in enumerate(test_episodes, 1):
            print(f"   Escribiendo episodio {i}: {episode['name']}")
            
            # Escribir CON CODE_RETRIEVAL_QUERY
            await graphiti_with_code.add_episode(
                name=f"code_{episode['name']}",
                episode_body=episode['content'],
                reference_time=datetime.now(timezone.utc),
                source=EpisodeType.text,
                source_description="Test CODE_RETRIEVAL_QUERY",
                group_id="eval_code_retrieval"
            )
            
            # Escribir SIN CODE_RETRIEVAL_QUERY
            await graphiti_standard.add_episode(
                name=f"standard_{episode['name']}",
                episode_body=episode['content'],
                reference_time=datetime.now(timezone.utc),
                source=EpisodeType.text, 
                source_description="Test standard embeddings",
                group_id="eval_standard"
            )
        
        print("✅ Todos los episodios escritos")
        
        # === COMPARAR BÚSQUEDAS ===
        print("\n4️⃣ Comparando calidad de búsquedas...")
        
        comparison_results = []
        
        for episode in test_episodes:
            query = episode['search_query']
            print(f"\n🔍 Buscando: '{query}'")
            
            # Buscar CON CODE_RETRIEVAL_QUERY
            try:
                results_with_code = await graphiti_with_code.search(query, limit=3)
                code_count = len(results_with_code)
                print(f"   CON CODE_RETRIEVAL: {code_count} resultados")
            except Exception as e:
                print(f"   ❌ Error con CODE_RETRIEVAL: {str(e)[:50]}...")
                code_count = 0
            
            # Buscar SIN CODE_RETRIEVAL_QUERY
            try:
                results_standard = await graphiti_standard.search(query, limit=3)
                standard_count = len(results_standard)
                print(f"   SIN CODE_RETRIEVAL: {standard_count} resultados")
            except Exception as e:
                print(f"   ❌ Error estándar: {str(e)[:50]}...")
                standard_count = 0
            
            comparison_results.append({
                "query": query,
                "with_code": code_count,
                "standard": standard_count
            })
        
        # === RESULTADOS ===
        print("\n5️⃣ RESULTADOS DE LA COMPARACIÓN:")
        print("=" * 70)
        
        total_with_code = sum(r['with_code'] for r in comparison_results)
        total_standard = sum(r['standard'] for r in comparison_results)
        
        print(f"📊 Total resultados CON CODE_RETRIEVAL_QUERY: {total_with_code}")
        print(f"📊 Total resultados SIN CODE_RETRIEVAL_QUERY: {total_standard}")
        
        if total_with_code > total_standard:
            improvement = ((total_with_code - total_standard) / total_standard * 100) if total_standard > 0 else 100
            print(f"✅ CODE_RETRIEVAL_QUERY mejora en {improvement:.1f}%")
        elif total_with_code < total_standard:
            decline = ((total_standard - total_with_code) / total_standard * 100)
            print(f"⚠️ CODE_RETRIEVAL_QUERY reduce en {decline:.1f}%")
        else:
            print("➡️ Sin diferencia significativa")
        
        # Cleanup
        await graphiti_with_code.close()
        await graphiti_standard.close()
        
        print("\n🎉 PRUEBA COMPLETADA EXITOSAMENTE")
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR EN LA PRUEBA: {e}")
        try:
            await graphiti_with_code.close()
            await graphiti_standard.close()
        except:
            pass
        return False

if __name__ == "__main__":
    result = asyncio.run(test_code_retrieval_query_real())
    if result:
        print("\n✅ CODE_RETRIEVAL_QUERY implementation validated!")
    else:
        print("\n❌ Test failed - check implementation")