#!/usr/bin/env python3
"""
TEST DE EVALUACIÓN COMPLETO CON EPISODIO
Prueba el framework de evaluación y registra el proceso como episodio en Graphiti
"""

import asyncio
import json
import time
from datetime import datetime
from typing import Dict, Any
import sys
import os

# Importar los frameworks creados
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from evaluation_framework_complete import (
    ExtendedEvaluationFramework, 
    EvaluationResult,
    PerformanceMetrics,
    GraphQualityMetrics,
    HybridSearchMetrics,
    CodeRetrievalMetrics
)
from test_suites_definition import TestSuiteManager

# Importar Graphiti
from graphiti_core.graphiti import Graphiti
from graphiti_core.llm_client.openai_client import OpenAIClient
from graphiti_core.embedder import OpenAIEmbedder
from graphiti_core.llm_client.config import LLMConfig
from graphiti_core.nodes import EpisodeType
from datetime import timezone

class EvaluationEpisodeCreator:
    """Crea episodios de evaluación en Graphiti"""
    
    def __init__(self, graphiti_instance):
        self.graphiti = graphiti_instance
        
    async def create_evaluation_episode(self, 
                                      evaluation_result: EvaluationResult,
                                      test_summary: Dict[str, Any]) -> Dict[str, Any]:
        """Crea un episodio que documenta la evaluación"""
        
        # Construir contenido del episodio
        episode_content = f"""
# Evaluación del Framework de Testing - {datetime.now().isoformat()}

## Configuración Evaluada
- **Modelo**: {evaluation_result.model_config.get('name', 'Unknown')}
- **LLM**: {evaluation_result.model_config.get('llm_model', 'N/A')}
- **Embeddings**: {evaluation_result.model_config.get('embedding_model', 'N/A')} ({evaluation_result.embedding.dimensions} dimensiones)

## Resultados de Performance
- **Latencia**: {evaluation_result.performance.latency_ms:.2f}ms
- **Throughput**: {evaluation_result.performance.throughput_requests_per_sec:.2f} req/s
- **Eficiencia de tokens**: {evaluation_result.performance.token_efficiency:.2%}

## Métricas de Calidad del Grafo
- **Nodos**: {evaluation_result.graph_quality.node_count if evaluation_result.graph_quality else 'N/A'}
- **Edges**: {evaluation_result.graph_quality.edge_count if evaluation_result.graph_quality else 'N/A'}
- **Densidad**: {evaluation_result.graph_quality.graph_density if evaluation_result.graph_quality else 'N/A'}

## Métricas de Code Retrieval
- **CODE_RETRIEVAL_QUERY Precision**: {evaluation_result.code_retrieval.code_retrieval_query_precision if evaluation_result.code_retrieval else 'N/A'}
- **Task Type vs Baseline**: +{evaluation_result.code_retrieval.task_type_vs_baseline_improvement * 100:.0f}% mejora

## Test Cases Ejecutados
- **Total Suites**: {test_summary.get('total_suites', 0)}
- **Total Tests**: {test_summary.get('total_tests', 0)}
- **Categorías**: {', '.join(test_summary.get('categories', []))}

## Conclusión
Este episodio documenta la evaluación baseline del sistema con configuración OpenAI. 
Servirá como referencia para comparaciones futuras con Gemini embeddings (3072-dim) 
y el task type CODE_RETRIEVAL_QUERY.

## Metadata Técnica
```json
{json.dumps(evaluation_result.model_config, indent=2)}
```
"""
        
        # Crear el episodio
        try:
            result = await self.graphiti.add_episode(
                name="Framework Evaluation Baseline",
                episode_body=episode_content,
                source_description="Evaluation Framework Test",
                reference_time=datetime.now()
            )
            
            print("✅ Episodio de evaluación creado exitosamente")
            return {
                "success": True,
                "episode_id": result.episode_id if hasattr(result, 'episode_id') else "generated",
                "content_length": len(episode_content)
            }
            
        except Exception as e:
            print(f"❌ Error creando episodio: {e}")
            return {
                "success": False,
                "error": str(e)
            }

async def run_complete_evaluation_test():
    """Ejecuta test completo del framework de evaluación"""
    
    print("🚀 TEST COMPLETO DE EVALUACIÓN CON EPISODIO")
    print("=" * 70)
    
    # Paso 1: Configurar Graphiti con OpenAI (actual)
    print("\n📋 PASO 1: Configurando Graphiti con OpenAI...")
    try:
        # Usar la configuración simple como en los ejemplos
        uri = "bolt://localhost:7687"
        username = "neo4j"
        password = "pepo_graphiti_2025"
        
        graphiti = Graphiti(uri, username, password)
        await graphiti.build_indices_and_constraints()
        print("✅ Graphiti configurado correctamente")
    except Exception as e:
        print(f"❌ Error configurando Graphiti: {e}")
        return
    
    # Paso 2: Cargar test suites
    print("\n📋 PASO 2: Cargando test suites...")
    test_manager = TestSuiteManager()
    test_summary = test_manager.generate_test_summary()
    print(f"✅ {test_summary['total_tests']} tests cargados de {test_summary['total_suites']} suites")
    
    # Paso 3: Añadir contenido de prueba
    print("\n📋 PASO 3: Añadiendo contenido de prueba al grafo...")
    
    # Obtener muestras de código de los test cases
    code_retrieval_suite = test_manager.suites["code_retrieval"]
    
    for i, test_case in enumerate(code_retrieval_suite.test_cases[:3]):  # Primeros 3
        try:
            code_content = test_case.input_data.get("code", "")
            if code_content:
                print(f"  📝 Añadiendo: {test_case.name}")
                result = await graphiti.add_episode(
                    name=test_case.name,
                    episode_body=code_content,
                    source_description="Test code sample",
                    reference_time=datetime.now()
                )
                await asyncio.sleep(0.5)  # Pequeña pausa entre adiciones
        except Exception as e:
            print(f"  ❌ Error añadiendo {test_case.name}: {e}")
    
    # Paso 4: Configurar y ejecutar evaluación
    print("\n📋 PASO 4: Ejecutando evaluación completa...")
    
    # Configuración actual de OpenAI
    openai_config = {
        "name": "OpenAI_Current_Baseline",
        "llm_engine": "openai",
        "llm_model": "gpt-4o",
        "embedding_engine": "openai",
        "embedding_model": "text-embedding-3-small",
        "embedding_dimensions": 1536,
        "supports_task_types": False
    }
    
    # Crear framework de evaluación
    eval_framework = ExtendedEvaluationFramework(neo4j_driver=graphiti.driver)
    eval_framework.setup_complete_evaluators()
    
    # Ejecutar evaluación
    evaluation_result = await eval_framework.comprehensive_evaluation(openai_config, graphiti)
    
    # Paso 5: Búsquedas de prueba
    print("\n📋 PASO 5: Ejecutando búsquedas de prueba...")
    
    test_queries = [
        "algoritmo de ordenamiento eficiente",
        "quicksort implementation", 
        "binary search tree",
        "REST API client pattern"
    ]
    
    search_results = {}
    for query in test_queries:
        try:
            # Usar la búsqueda como en los ejemplos
            results = await graphiti.search(query=query, num_results=5)
            search_results[query] = {
                "count": len(results),
                "found": len(results) > 0
            }
            print(f"  🔍 '{query}': {len(results)} resultados")
        except Exception as e:
            print(f"  ❌ Error buscando '{query}': {e}")
            search_results[query] = {"count": 0, "found": False, "error": str(e)}
    
    # Paso 6: Crear episodio de evaluación
    print("\n📋 PASO 6: Creando episodio de evaluación...")
    
    episode_creator = EvaluationEpisodeCreator(graphiti)
    episode_result = await episode_creator.create_evaluation_episode(
        evaluation_result,
        test_summary
    )
    
    # Paso 7: Generar reporte final
    print("\n📊 REPORTE FINAL DE EVALUACIÓN")
    print("=" * 50)
    
    # Performance
    print(f"\n⚡ PERFORMANCE:")
    print(f"   Latencia: {evaluation_result.performance.latency_ms:.2f}ms")
    print(f"   Throughput: {evaluation_result.performance.throughput_requests_per_sec:.2f} req/s")
    
    # Embeddings
    print(f"\n🧮 EMBEDDINGS:")
    print(f"   Modelo: {openai_config['embedding_model']}")
    print(f"   Dimensiones: {evaluation_result.embedding.dimensions}")
    print(f"   Coherencia: {evaluation_result.embedding.embedding_coherence:.3f}")
    
    # Graph Quality
    if evaluation_result.graph_quality:
        print(f"\n🔗 CALIDAD DEL GRAFO:")
        print(f"   Nodos: {evaluation_result.graph_quality.node_count}")
        print(f"   Edges: {evaluation_result.graph_quality.edge_count}")
        print(f"   Densidad: {evaluation_result.graph_quality.graph_density:.3f}")
    
    # Code Retrieval
    if evaluation_result.code_retrieval:
        print(f"\n💻 CODE RETRIEVAL:")
        print(f"   Precisión (sin task types): {evaluation_result.code_retrieval.code_retrieval_query_precision:.3f}")
        print(f"   Preservación de contexto: {evaluation_result.code_retrieval.syntactic_context_preservation:.3f}")
    
    # Search Results
    print(f"\n🔍 RESULTADOS DE BÚSQUEDA:")
    for query, result in search_results.items():
        status = "✅" if result["found"] else "❌"
        print(f"   {status} '{query}': {result['count']} resultados")
    
    # Episode Status
    print(f"\n📝 EPISODIO DE EVALUACIÓN:")
    if episode_result["success"]:
        print(f"   ✅ Creado exitosamente (ID: {episode_result['episode_id']})")
    else:
        print(f"   ❌ Error: {episode_result.get('error', 'Unknown')}")
    
    # Overall Score
    overall_score = eval_framework.calculate_overall_score(evaluation_result)
    print(f"\n🏆 SCORE GENERAL: {overall_score:.3f}/1.000")
    
    # Recommendations
    recommendations = eval_framework.generate_recommendations(evaluation_result)
    if recommendations:
        print(f"\n💡 RECOMENDACIONES:")
        for rec in recommendations:
            print(f"   {rec}")
    
    # Exportar resultados
    print("\n📁 Exportando resultados...")
    eval_framework.export_results("evaluation_baseline_results.json")
    
    # Cleanup
    await graphiti.close()
    
    print("\n✅ TEST COMPLETO FINALIZADO")
    print("   Baseline establecido para comparación con Gemini")
    
    return {
        "evaluation_result": evaluation_result,
        "search_results": search_results,
        "episode_result": episode_result,
        "overall_score": overall_score
    }

# Función helper para test mock sin Graphiti real
async def run_mock_evaluation_test():
    """Versión mock del test para desarrollo"""
    
    print("🧪 TEST MOCK DE EVALUACIÓN (Sin Graphiti real)")
    print("=" * 50)
    
    # Mock de Graphiti
    class MockGraphiti:
        def __init__(self):
            self.memories = []
            
        async def add_memory(self, content):
            self.memories.append(content)
            await asyncio.sleep(0.1)
            return {"success": True}
            
        async def search_memory_nodes(self, query):
            # Simular búsqueda
            if "quicksort" in query.lower() or "ordenamiento" in query.lower():
                return [{"content": "quicksort implementation", "score": 0.9}]
            elif "binary" in query.lower() or "tree" in query.lower():
                return [{"content": "binary tree", "score": 0.85}]
            return []
            
        async def add_episode(self, name, episode_body, reference_time):
            return {"episode_id": "mock_episode_123", "success": True}
            
        async def close(self):
            pass
            
        @property
        def driver(self):
            return MockNeo4jDriver()
    
    class MockNeo4jDriver:
        async def execute_query(self, query):
            # Simular respuestas de Neo4j
            if "count(n)" in query:
                return type('obj', (object,), {'records': [{'nodes': 10, 'edges': 15}]})
            return type('obj', (object,), {'records': []})
    
    # Ejecutar con mock
    mock_graphiti = MockGraphiti()
    
    # Usar el framework real con mock
    test_manager = TestSuiteManager()
    eval_framework = ExtendedEvaluationFramework()
    eval_framework.setup_complete_evaluators()
    
    openai_config = {
        "name": "OpenAI_Mock_Test",
        "llm_engine": "openai",
        "llm_model": "gpt-4o",
        "embedding_engine": "openai",
        "embedding_model": "text-embedding-3-small",
        "embedding_dimensions": 1536,
        "supports_task_types": False
    }
    
    # Simular evaluación
    result = await eval_framework.comprehensive_evaluation(openai_config, mock_graphiti)
    
    print(f"\n✅ Mock Test Completado")
    print(f"   Score: {eval_framework.calculate_overall_score(result):.3f}")
    
    await mock_graphiti.close()

# Main
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--mock":
        # Ejecutar versión mock para testing
        asyncio.run(run_mock_evaluation_test())
    else:
        # Ejecutar versión real con Graphiti
        asyncio.run(run_complete_evaluation_test())