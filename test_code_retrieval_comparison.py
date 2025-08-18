"""
Prueba comparativa CODE_RETRIEVAL_QUERY vs Estándar
Genera reporte documentado para validación por terceros
"""

import asyncio
import os
import json
from datetime import datetime, timezone
from typing import List, Dict, Any
from graphiti_core import Graphiti
from graphiti_core.nodes import EpisodeType
from graphiti_core.llm_client.gemini_client import GeminiClient
from graphiti_core.llm_client.config import LLMConfig
from graphiti_core.embedder.gemini import GeminiEmbedder, GeminiEmbedderConfig

class CodeRetrievalEvaluator:
    """Evaluador comparativo CODE_RETRIEVAL_QUERY vs embeddings estándar"""
    
    def __init__(self):
        self.results = {
            "test_metadata": {
                "timestamp": datetime.now().isoformat(),
                "test_version": "1.0",
                "description": "Comparative evaluation of CODE_RETRIEVAL_QUERY vs standard embeddings",
                "instances": {
                    "with_code_retrieval": "bolt://localhost:7693 (graphiti-neo4j-gemini)",
                    "standard": "bolt://localhost:7687 (graphiti-neo4j)"
                }
            },
            "configuration": {},
            "test_cases": [],
            "results": {
                "with_code_retrieval": [],
                "standard": [],
                "comparison": {}
            }
        }
    
    async def setup_instances(self) -> tuple[Graphiti, Graphiti]:
        """Configurar ambas instancias para comparación"""
        
        google_api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        if not google_api_key:
            raise ValueError("GOOGLE_API_KEY requerida")
        
        print("🔧 Configurando instancias...")
        
        # LLM común para ambas instancias
        llm_config = LLMConfig(
            api_key=google_api_key,
            model="gemini-2.5-pro",
            small_model="gemini-2.5-flash",
            temperature=0.0
        )
        llm_client = GeminiClient(config=llm_config)
        
        # Guardar configuración
        self.results["configuration"] = {
            "llm_model": "gemini-2.5-pro",
            "small_model": "gemini-2.5-flash",
            "embedding_model": "gemini-embedding-001",
            "embedding_dimensions": 3072,
            "temperature": 0.0
        }
        
        # Instancia CON CODE_RETRIEVAL_QUERY
        embedder_with_code = GeminiEmbedder(config=GeminiEmbedderConfig(
            api_key=google_api_key,
            embedding_model="gemini-embedding-001",
            embedding_dim=3072,
            task_type="CODE_RETRIEVAL_QUERY"
        ))
        
        graphiti_with_code = Graphiti(
            uri="bolt://localhost:7693",  # graphiti-neo4j-gemini
            user="neo4j",
            password="pepo_graphiti_2025",
            llm_client=llm_client,
            embedder=embedder_with_code
        )
        
        # Instancia SIN CODE_RETRIEVAL_QUERY
        embedder_standard = GeminiEmbedder(config=GeminiEmbedderConfig(
            api_key=google_api_key,
            embedding_model="gemini-embedding-001",
            embedding_dim=3072,
            task_type=None  # Sin optimización
        ))
        
        graphiti_standard = Graphiti(
            uri="bolt://localhost:7687",  # graphiti-neo4j
            user="neo4j",
            password="pepo_graphiti_2025",
            llm_client=llm_client,
            embedder=embedder_standard
        )
        
        print("   ✅ Instancia CON CODE_RETRIEVAL_QUERY: puerto 7693")
        print("   ✅ Instancia SIN CODE_RETRIEVAL_QUERY: puerto 7687")
        
        return graphiti_with_code, graphiti_standard
    
    def create_test_cases(self) -> List[Dict[str, Any]]:
        """Crear casos de prueba específicos para CODE_RETRIEVAL_QUERY"""
        
        test_cases = [
            {
                "id": "python_algorithm",
                "name": "Algoritmo Quicksort Python",
                "content": """
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)

# Implementación recursiva del algoritmo quicksort
# Complejidad promedio: O(n log n)
""",
                "search_queries": [
                    "quicksort algorithm python",
                    "recursive sorting function",
                    "divide and conquer sorting"
                ],
                "expected_benefit": "HIGH - Código Python con patrones algorítmicos"
            },
            {
                "id": "cypher_query",
                "name": "Query Cypher Neo4j",
                "content": """
MATCH (p:Person)-[:WORKS_AT]->(c:Company)
WHERE p.age > 30 AND c.industry = 'Technology'
WITH p, c, p.salary as salary
ORDER BY salary DESC
RETURN p.name, c.name, salary
LIMIT 10
""",
                "search_queries": [
                    "find employees in technology companies",
                    "cypher query person company relationship",
                    "graph database query employees"
                ],
                "expected_benefit": "HIGH - Query Cypher específica"
            },
            {
                "id": "data_structure",
                "name": "Estructura de Datos - Binary Tree",
                "content": """
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class BinaryTree:
    def __init__(self):
        self.root = None
    
    def insert(self, val):
        if not self.root:
            self.root = TreeNode(val)
        else:
            self._insert_recursive(self.root, val)
    
    def _insert_recursive(self, node, val):
        if val < node.val:
            if not node.left:
                node.left = TreeNode(val)
            else:
                self._insert_recursive(node.left, val)
        else:
            if not node.right:
                node.right = TreeNode(val)
            else:
                self._insert_recursive(node.right, val)
""",
                "search_queries": [
                    "binary tree data structure",
                    "tree insertion algorithm",
                    "recursive tree operations"
                ],
                "expected_benefit": "HIGH - Estructura de datos con código"
            },
            {
                "id": "regular_text",
                "name": "Texto Regular - Descripción ML",
                "content": """
Machine learning is a subset of artificial intelligence that focuses on the development of algorithms and statistical models that enable computer systems to improve their performance on a specific task through experience. Unlike traditional programming where explicit instructions are provided, machine learning systems learn patterns from data and make predictions or decisions without being explicitly programmed for every scenario.
""",
                "search_queries": [
                    "machine learning artificial intelligence",
                    "algorithms statistical models",
                    "computer systems learning patterns"
                ],
                "expected_benefit": "LOW - Texto regular sin código"
            }
        ]
        
        self.results["test_cases"] = test_cases
        return test_cases
    
    async def run_comparison(self):
        """Ejecutar comparación completa"""
        
        print("🚀 INICIANDO EVALUACIÓN COMPARATIVA CODE_RETRIEVAL_QUERY")
        print("=" * 70)
        
        try:
            # Setup
            graphiti_with_code, graphiti_standard = await self.setup_instances()
            
            # Construir índices
            print("\n📊 Construyendo índices...")
            await graphiti_with_code.build_indices_and_constraints()
            await graphiti_standard.build_indices_and_constraints()
            print("   ✅ Índices construidos en ambas instancias")
            
            # Crear casos de prueba
            test_cases = self.create_test_cases()
            print(f"\n📝 Casos de prueba creados: {len(test_cases)}")
            
            # Escribir episodios en ambas instancias
            print("\n✍️ Escribiendo episodios...")
            for i, case in enumerate(test_cases, 1):
                print(f"   [{i}/{len(test_cases)}] {case['name']}")
                
                # Escribir CON CODE_RETRIEVAL_QUERY
                await graphiti_with_code.add_episode(
                    name=f"code_{case['id']}",
                    episode_body=case['content'],
                    reference_time=datetime.now(timezone.utc),
                    source=EpisodeType.text,
                    source_description=f"Test CODE_RETRIEVAL_QUERY - {case['name']}",
                    group_id="eval_code_retrieval"
                )
                
                # Escribir SIN CODE_RETRIEVAL_QUERY
                await graphiti_standard.add_episode(
                    name=f"standard_{case['id']}",
                    episode_body=case['content'],
                    reference_time=datetime.now(timezone.utc),
                    source=EpisodeType.text,
                    source_description=f"Test standard embeddings - {case['name']}",
                    group_id="eval_standard"
                )
            
            print("   ✅ Todos los episodios escritos")
            
            # Ejecutar búsquedas comparativas
            print("\n🔍 Ejecutando búsquedas comparativas...")
            
            for case in test_cases:
                print(f"\n📋 Caso: {case['name']}")
                
                case_results = {
                    "case_id": case['id'],
                    "case_name": case['name'],
                    "expected_benefit": case['expected_benefit'],
                    "queries": []
                }
                
                for query in case['search_queries']:
                    print(f"   🔍 '{query}'")
                    
                    query_result = {
                        "query": query,
                        "with_code_retrieval": {"count": 0, "relevant_found": False, "top_result": None},
                        "standard": {"count": 0, "relevant_found": False, "top_result": None}
                    }
                    
                    # Buscar CON CODE_RETRIEVAL_QUERY
                    try:
                        results_code = await graphiti_with_code.search(query, limit=5)
                        query_result["with_code_retrieval"]["count"] = len(results_code)
                        
                        if results_code:
                            top_result = results_code[0]
                            query_result["with_code_retrieval"]["top_result"] = {
                                "name": top_result.name,
                                "snippet": top_result.episode_body[:100] + "..."
                            }
                            
                            # Verificar si encontró el episodio relevante
                            if case['id'] in top_result.name:
                                query_result["with_code_retrieval"]["relevant_found"] = True
                                print(f"      ✅ CON CODE_RETRIEVAL: {len(results_code)} resultados (relevante encontrado)")
                            else:
                                print(f"      ⚠️ CON CODE_RETRIEVAL: {len(results_code)} resultados (relevante NO en top)")
                        else:
                            print(f"      ❌ CON CODE_RETRIEVAL: 0 resultados")
                            
                    except Exception as e:
                        print(f"      ❌ Error CON CODE_RETRIEVAL: {str(e)[:50]}")
                        query_result["with_code_retrieval"]["error"] = str(e)
                    
                    # Buscar SIN CODE_RETRIEVAL_QUERY
                    try:
                        results_standard = await graphiti_standard.search(query, limit=5)
                        query_result["standard"]["count"] = len(results_standard)
                        
                        if results_standard:
                            top_result = results_standard[0]
                            query_result["standard"]["top_result"] = {
                                "name": top_result.name,
                                "snippet": top_result.episode_body[:100] + "..."
                            }
                            
                            # Verificar si encontró el episodio relevante
                            if case['id'] in top_result.name:
                                query_result["standard"]["relevant_found"] = True
                                print(f"      ✅ SIN CODE_RETRIEVAL: {len(results_standard)} resultados (relevante encontrado)")
                            else:
                                print(f"      ⚠️ SIN CODE_RETRIEVAL: {len(results_standard)} resultados (relevante NO en top)")
                        else:
                            print(f"      ❌ SIN CODE_RETRIEVAL: 0 resultados")
                            
                    except Exception as e:
                        print(f"      ❌ Error SIN CODE_RETRIEVAL: {str(e)[:50]}")
                        query_result["standard"]["error"] = str(e)
                    
                    case_results["queries"].append(query_result)
                
                self.results["results"]["with_code_retrieval"].append(case_results)
            
            # Generar análisis comparativo
            await self.generate_comparison_analysis()
            
            # Cleanup
            await graphiti_with_code.close()
            await graphiti_standard.close()
            
            # Guardar reporte
            self.save_report()
            
            print("\n🎉 EVALUACIÓN COMPLETADA")
            return True
            
        except Exception as e:
            print(f"\n❌ ERROR EN EVALUACIÓN: {e}")
            return False
    
    async def generate_comparison_analysis(self):
        """Generar análisis estadístico de la comparación"""
        
        print("\n📊 Generando análisis comparativo...")
        
        total_queries = 0
        code_retrieval_better = 0
        standard_better = 0
        tied = 0
        
        code_retrieval_relevant_found = 0
        standard_relevant_found = 0
        
        for case_result in self.results["results"]["with_code_retrieval"]:
            for query_result in case_result["queries"]:
                total_queries += 1
                
                code_count = query_result["with_code_retrieval"]["count"]
                standard_count = query_result["standard"]["count"]
                
                code_relevant = query_result["with_code_retrieval"]["relevant_found"]
                standard_relevant = query_result["standard"]["relevant_found"]
                
                if code_relevant:
                    code_retrieval_relevant_found += 1
                if standard_relevant:
                    standard_relevant_found += 1
                
                if code_count > standard_count:
                    code_retrieval_better += 1
                elif standard_count > code_count:
                    standard_better += 1
                else:
                    tied += 1
        
        # Calcular métricas
        code_precision = (code_retrieval_relevant_found / total_queries * 100) if total_queries > 0 else 0
        standard_precision = (standard_relevant_found / total_queries * 100) if total_queries > 0 else 0
        
        improvement = code_precision - standard_precision
        
        self.results["results"]["comparison"] = {
            "total_queries": total_queries,
            "metrics": {
                "code_retrieval_precision": round(code_precision, 2),
                "standard_precision": round(standard_precision, 2),
                "improvement_percentage": round(improvement, 2)
            },
            "performance": {
                "code_retrieval_better": code_retrieval_better,
                "standard_better": standard_better,
                "tied": tied
            },
            "conclusion": self.generate_conclusion(improvement, code_retrieval_better, standard_better)
        }
        
        print(f"   📈 CODE_RETRIEVAL_QUERY precision: {code_precision:.1f}%")
        print(f"   📈 Standard precision: {standard_precision:.1f}%")
        print(f"   📊 Improvement: {improvement:+.1f}%")
    
    def generate_conclusion(self, improvement: float, code_better: int, standard_better: int) -> str:
        """Generar conclusión basada en resultados"""
        
        if improvement > 10:
            return "CODE_RETRIEVAL_QUERY shows significant improvement (>10%) in code search tasks"
        elif improvement > 0:
            return "CODE_RETRIEVAL_QUERY shows modest improvement in code search tasks"
        elif improvement < -10:
            return "Standard embeddings perform significantly better than CODE_RETRIEVAL_QUERY"
        else:
            return "No significant difference between CODE_RETRIEVAL_QUERY and standard embeddings"
    
    def save_report(self):
        """Guardar reporte detallado para validación por terceros"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Reporte JSON detallado
        json_filename = f"code_retrieval_evaluation_{timestamp}.json"
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        # Reporte markdown legible
        md_filename = f"code_retrieval_report_{timestamp}.md"
        with open(md_filename, 'w', encoding='utf-8') as f:
            f.write(self.generate_markdown_report())
        
        print(f"\n📄 Reportes generados:")
        print(f"   • JSON detallado: {json_filename}")
        print(f"   • Reporte legible: {md_filename}")
        
        return json_filename, md_filename
    
    def generate_markdown_report(self) -> str:
        """Generar reporte en formato Markdown"""
        
        comparison = self.results["results"]["comparison"]
        config = self.results["configuration"]
        metadata = self.results["test_metadata"]
        
        report = f"""# Evaluación CODE_RETRIEVAL_QUERY vs Embeddings Estándar

## Metadatos de la Prueba
- **Fecha**: {metadata['timestamp']}
- **Versión**: {metadata['test_version']}
- **Descripción**: {metadata['description']}

## Configuración
- **LLM Principal**: {config['llm_model']}
- **LLM Secundario**: {config['small_model']}
- **Modelo Embeddings**: {config['embedding_model']}
- **Dimensiones**: {config['embedding_dimensions']}
- **Temperatura**: {config['temperature']}

## Instancias Utilizadas
- **CON CODE_RETRIEVAL_QUERY**: {metadata['instances']['with_code_retrieval']}
- **SIN CODE_RETRIEVAL_QUERY**: {metadata['instances']['standard']}

## Resultados

### Métricas Generales
- **Total Consultas**: {comparison['total_queries']}
- **Precisión CODE_RETRIEVAL_QUERY**: {comparison['metrics']['code_retrieval_precision']}%
- **Precisión Estándar**: {comparison['metrics']['standard_precision']}%
- **Mejora**: {comparison['metrics']['improvement_percentage']:+.1f}%

### Rendimiento por Consulta
- **CODE_RETRIEVAL_QUERY mejor**: {comparison['performance']['code_retrieval_better']} consultas
- **Estándar mejor**: {comparison['performance']['standard_better']} consultas
- **Empate**: {comparison['performance']['tied']} consultas

## Conclusión
{comparison['conclusion']}

## Casos de Prueba Detallados
"""
        
        for i, case in enumerate(self.results["test_cases"], 1):
            report += f"""
### {i}. {case['name']}
- **Beneficio Esperado**: {case['expected_benefit']}
- **Consultas de Prueba**: {len(case['search_queries'])}
  {chr(10).join(f"  - {q}" for q in case['search_queries'])}
"""
        
        report += f"""
---
*Reporte generado automáticamente el {metadata['timestamp']}*
*Validable por terceros mediante el archivo JSON correspondiente*
"""
        
        return report

async def main():
    """Función principal"""
    
    evaluator = CodeRetrievalEvaluator()
    success = await evaluator.run_comparison()
    
    if success:
        print("\n🎯 EVALUACIÓN EXITOSA")
        print("📋 Reportes generados para validación por terceros")
        return True
    else:
        print("\n❌ EVALUACIÓN FALLIDA")
        return False

if __name__ == "__main__":
    result = asyncio.run(main())
    exit(0 if result else 1)