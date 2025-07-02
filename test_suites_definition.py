#!/usr/bin/env python3
"""
TEST SUITES DEFINITION - Definición de casos de prueba específicos
Tests preparados ANTES de ejecutar el framework de evaluación
"""

from typing import List, Dict, Any
from dataclasses import dataclass

# ===== TEST CASE DEFINITIONS =====

@dataclass
class TestCase:
    """Caso de prueba base"""
    id: str
    name: str
    description: str
    input_data: Any
    expected_output: Any
    success_criteria: Dict[str, Any]
    category: str

@dataclass
class CodeRetrievalTestCase(TestCase):
    """Caso de prueba específico para CODE_RETRIEVAL_QUERY"""
    query_type: str  # "natural_language", "technical_term", "functional_description"
    code_language: str
    complexity_level: str  # "simple", "intermediate", "complex"
    expected_task_type: str  # "CODE_RETRIEVAL_QUERY", "RETRIEVAL_DOCUMENT"

# ===== CODE RETRIEVAL TEST SUITE =====

class CodeRetrievalTestSuite:
    """Suite de tests para CODE_RETRIEVAL_QUERY task type"""
    
    def __init__(self):
        self.test_cases = self._define_code_retrieval_tests()
        self.ground_truth = self._define_ground_truth()
    
    def _define_code_retrieval_tests(self) -> List[CodeRetrievalTestCase]:
        """Define casos de prueba específicos para CODE_RETRIEVAL_QUERY"""
        
        return [
            # Test 1: Algoritmo de ordenamiento
            CodeRetrievalTestCase(
                id="cr_001",
                name="Quicksort Algorithm Retrieval", 
                description="Recuperar implementación de quicksort mediante query natural",
                input_data={
                    "code": '''
def quicksort(arr):
    """
    Implementación eficiente del algoritmo quicksort
    Complejidad: O(n log n) promedio, O(n²) peor caso
    """
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return quicksort(left) + middle + quicksort(right)

# Ejemplo de uso
test_array = [64, 34, 25, 12, 22, 11, 90]
sorted_array = quicksort(test_array)
print(f"Array ordenado: {sorted_array}")
                    ''',
                    "natural_query": "algoritmo para ordenar un array de manera eficiente divide y vencerás",
                    "technical_query": "quicksort implementation with pivot partitioning",
                    "functional_query": "sort array efficiently with recursive approach"
                },
                expected_output={
                    "should_retrieve": True,
                    "relevance_score": 0.9,
                    "context_preservation": 0.85
                },
                success_criteria={
                    "retrieval_precision": 0.8,
                    "semantic_relevance": 0.85,
                    "code_completeness": 0.9
                },
                category="algorithms",
                query_type="natural_language",
                code_language="python",
                complexity_level="intermediate",
                expected_task_type="CODE_RETRIEVAL_QUERY"
            ),
            
            # Test 2: Estructura de datos
            CodeRetrievalTestCase(
                id="cr_002",
                name="Binary Search Tree Implementation",
                description="Recuperar implementación de BST con operaciones básicas",
                input_data={
                    "code": '''
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class BinarySearchTree:
    def __init__(self):
        self.root = None
    
    def insert(self, val):
        """Inserta un valor en el BST"""
        if not self.root:
            self.root = TreeNode(val)
        else:
            self._insert_recursive(self.root, val)
    
    def _insert_recursive(self, node, val):
        if val < node.val:
            if node.left is None:
                node.left = TreeNode(val)
            else:
                self._insert_recursive(node.left, val)
        else:
            if node.right is None:
                node.right = TreeNode(val)
            else:
                self._insert_recursive(node.right, val)
    
    def search(self, val):
        """Busca un valor en el BST"""
        return self._search_recursive(self.root, val)
    
    def _search_recursive(self, node, val):
        if not node or node.val == val:
            return node
        if val < node.val:
            return self._search_recursive(node.left, val)
        return self._search_recursive(node.right, val)
                    ''',
                    "natural_query": "estructura de datos para búsqueda rápida con orden",
                    "technical_query": "binary search tree with insert and search operations",
                    "functional_query": "tree data structure for efficient searching and insertion"
                },
                expected_output={
                    "should_retrieve": True,
                    "relevance_score": 0.88,
                    "context_preservation": 0.90
                },
                success_criteria={
                    "retrieval_precision": 0.85,
                    "semantic_relevance": 0.88,
                    "code_completeness": 0.95
                },
                category="data_structures",
                query_type="technical_term",
                code_language="python",
                complexity_level="complex",
                expected_task_type="CODE_RETRIEVAL_QUERY"
            ),
            
            # Test 3: API Pattern
            CodeRetrievalTestCase(
                id="cr_003",
                name="REST API Client Pattern",
                description="Recuperar patrón de cliente REST con manejo de errores",
                input_data={
                    "code": '''
import requests
import json
from typing import Dict, Any, Optional

class APIClient:
    """Cliente REST con manejo robusto de errores y retry"""
    
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        })
    
    def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """GET request con manejo de errores"""
        try:
            response = self.session.get(
                f"{self.base_url}/{endpoint.lstrip('/')}", 
                params=params,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise APIException(f"GET request failed: {e}")
    
    def post(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """POST request con validación"""
        try:
            response = self.session.post(
                f"{self.base_url}/{endpoint.lstrip('/')}", 
                json=data,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise APIException(f"POST request failed: {e}")

class APIException(Exception):
    """Excepción personalizada para errores de API"""
    pass
                    ''',
                    "natural_query": "cliente HTTP para consumir APIs REST con manejo de errores",
                    "technical_query": "REST API client with error handling and authentication",
                    "functional_query": "HTTP client for API requests with timeout and retry"
                },
                expected_output={
                    "should_retrieve": True,
                    "relevance_score": 0.85,
                    "context_preservation": 0.88
                },
                success_criteria={
                    "retrieval_precision": 0.80,
                    "semantic_relevance": 0.85,
                    "code_completeness": 0.90
                },
                category="api_patterns",
                query_type="functional_description",
                code_language="python",
                complexity_level="intermediate",
                expected_task_type="CODE_RETRIEVAL_QUERY"
            ),
            
            # Test 4: Caso Edge - Query ambigua
            CodeRetrievalTestCase(
                id="cr_004",
                name="Ambiguous Query Handling",
                description="Manejo de query ambigua que podría referirse a múltiples conceptos",
                input_data={
                    "code": '''
def binary_search(arr, target):
    """Búsqueda binaria en array ordenado"""
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
                    ''',
                    "ambiguous_query": "search",  # Podría ser binary search, linear search, etc.
                    "specific_query": "binary search in sorted array",
                    "context_query": "efficient search algorithm for sorted data"
                },
                expected_output={
                    "should_retrieve": True,
                    "relevance_score": 0.70,  # Menor por ambigüedad
                    "context_preservation": 0.80
                },
                success_criteria={
                    "retrieval_precision": 0.70,
                    "semantic_relevance": 0.75,
                    "disambiguation_quality": 0.65
                },
                category="edge_cases",
                query_type="ambiguous",
                code_language="python",
                complexity_level="simple",
                expected_task_type="CODE_RETRIEVAL_QUERY"
            )
        ]
    
    def _define_ground_truth(self) -> Dict[str, Any]:
        """Define ground truth para evaluación"""
        return {
            "cr_001": {
                "relevant_docs": [0],  # El documento 0 es relevante
                "relevance_scores": [0.9],
                "expected_rank": 1
            },
            "cr_002": {
                "relevant_docs": [1],
                "relevance_scores": [0.88], 
                "expected_rank": 1
            },
            "cr_003": {
                "relevant_docs": [2],
                "relevance_scores": [0.85],
                "expected_rank": 1
            },
            "cr_004": {
                "relevant_docs": [3],
                "relevance_scores": [0.70],
                "expected_rank": 1
            }
        }

# ===== GRAPH QUALITY TEST SUITE =====

class GraphQualityTestSuite:
    """Suite de tests para calidad del knowledge graph"""
    
    def __init__(self):
        self.test_cases = self._define_graph_quality_tests()
    
    def _define_graph_quality_tests(self) -> List[TestCase]:
        """Define casos de prueba para calidad del grafo"""
        
        return [
            TestCase(
                id="gq_001",
                name="Node Property Completeness",
                description="Verificar completitud de propiedades en nodos",
                input_data={
                    "expected_properties": ["content", "timestamp", "embedding", "type"],
                    "minimum_completeness": 0.8
                },
                expected_output={
                    "completeness_ratio": 0.85
                },
                success_criteria={
                    "min_completeness": 0.8,
                    "properties_coverage": 0.9
                },
                category="node_quality"
            ),
            
            TestCase(
                id="gq_002", 
                name="Relationship Semantic Coherence",
                description="Verificar coherencia semántica de relaciones",
                input_data={
                    "relationship_types": ["CONTAINS", "RELATES_TO", "FOLLOWS", "IMPLEMENTS"],
                    "semantic_threshold": 0.7
                },
                expected_output={
                    "coherence_score": 0.8
                },
                success_criteria={
                    "min_coherence": 0.7,
                    "relationship_validity": 0.85
                },
                category="relationship_quality"
            ),
            
            TestCase(
                id="gq_003",
                name="Graph Connectivity Analysis",
                description="Análizar conectividad y estructura del grafo",
                input_data={
                    "min_connected_components": 1,
                    "expected_avg_degree": 2.5
                },
                expected_output={
                    "connected_components": 1,
                    "average_degree": 2.8
                },
                success_criteria={
                    "connectivity": 0.9,
                    "structural_coherence": 0.8
                },
                category="topology"
            )
        ]

# ===== HYBRID SEARCH TEST SUITE =====

class HybridSearchTestSuite:
    """Suite de tests para búsqueda híbrida"""
    
    def __init__(self):
        self.test_cases = self._define_hybrid_search_tests()
    
    def _define_hybrid_search_tests(self) -> List[TestCase]:
        """Define casos de prueba para búsqueda híbrida"""
        
        return [
            TestCase(
                id="hs_001",
                name="Vector Search Precision",
                description="Evaluar precisión de búsqueda vectorial",
                input_data={
                    "test_queries": [
                        "sorting algorithm implementation",
                        "data structure for fast retrieval", 
                        "API client with error handling"
                    ],
                    "embedding_model": "test_model"
                },
                expected_output={
                    "precision_at_1": 0.8,
                    "precision_at_3": 0.7
                },
                success_criteria={
                    "min_precision_1": 0.7,
                    "min_precision_3": 0.6
                },
                category="vector_search"
            ),
            
            TestCase(
                id="hs_002",
                name="Keyword Search Effectiveness",
                description="Evaluar efectividad de búsqueda por keywords",
                input_data={
                    "keyword_queries": [
                        "quicksort python",
                        "binary tree insert",
                        "REST API client"
                    ],
                    "bm25_enabled": True
                },
                expected_output={
                    "keyword_precision": 0.75,
                    "keyword_recall": 0.70
                },
                success_criteria={
                    "min_keyword_precision": 0.7,
                    "min_keyword_recall": 0.65
                },
                category="keyword_search"
            ),
            
            TestCase(
                id="hs_003",
                name="Hybrid Fusion Quality",
                description="Evaluar calidad de fusión de métodos híbridos",
                input_data={
                    "fusion_weights": {"vector": 0.5, "keyword": 0.3, "graph": 0.2},
                    "test_queries": ["comprehensive search test"]
                },
                expected_output={
                    "fusion_effectiveness": 0.85,
                    "method_contribution_balance": 0.8
                },
                success_criteria={
                    "min_fusion_effectiveness": 0.8,
                    "balanced_contribution": 0.75
                },
                category="hybrid_fusion"
            )
        ]

# ===== EMBEDDING COMPARISON TEST SUITE =====

class EmbeddingComparisonTestSuite:
    """Suite de tests para comparar embeddings OpenAI vs Gemini"""
    
    def __init__(self):
        self.test_cases = self._define_embedding_comparison_tests()
    
    def _define_embedding_comparison_tests(self) -> List[TestCase]:
        """Define casos de prueba para comparación de embeddings"""
        
        return [
            TestCase(
                id="ec_001",
                name="Dimensionality Impact Analysis",
                description="Analizar impacto de dimensionalidad 1536 vs 3072",
                input_data={
                    "openai_dimensions": 1536,
                    "gemini_dimensions": 3072,
                    "test_texts": [
                        "def quicksort(arr): # sorting algorithm",
                        "class BinaryTree: # data structure",
                        "import requests # API client"
                    ]
                },
                expected_output={
                    "dimensional_efficiency_openai": 0.8,
                    "dimensional_efficiency_gemini": 0.85,
                    "information_density_ratio": 1.2
                },
                success_criteria={
                    "gemini_efficiency_gain": 0.05,
                    "information_preservation": 0.9
                },
                category="dimensionality"
            ),
            
            TestCase(
                id="ec_002", 
                name="CODE_RETRIEVAL_QUERY Task Type Effectiveness",
                description="Evaluar efectividad específica del task type CODE_RETRIEVAL_QUERY",
                input_data={
                    "task_types": ["CODE_RETRIEVAL_QUERY", "RETRIEVAL_DOCUMENT", "CLUSTERING"],
                    "code_samples": [
                        "algorithm implementation",
                        "data structure definition", 
                        "API usage pattern"
                    ]
                },
                expected_output={
                    "code_retrieval_query_precision": 0.90,
                    "baseline_precision": 0.75,
                    "improvement_ratio": 1.2
                },
                success_criteria={
                    "min_cquery_precision": 0.85,
                    "min_improvement": 0.15
                },
                category="task_type_effectiveness"
            ),
            
            TestCase(
                id="ec_003",
                name="Semantic Stability Comparison", 
                description="Comparar estabilidad semántica entre modelos",
                input_data={
                    "similarity_pairs": [
                        ("def sort(arr):", "sorting algorithm implementation"),
                        ("class Tree:", "tree data structure"),
                        ("api_client.get()", "HTTP GET request")
                    ],
                    "stability_threshold": 0.8
                },
                expected_output={
                    "openai_stability": 0.82,
                    "gemini_stability": 0.87,
                    "cross_model_consistency": 0.75
                },
                success_criteria={
                    "min_stability": 0.8,
                    "consistency_threshold": 0.7
                },
                category="semantic_stability"
            )
        ]

# ===== TEST SUITE MANAGER =====

class TestSuiteManager:
    """Gestor centralizado de todas las suites de test"""
    
    def __init__(self):
        self.suites = {
            "code_retrieval": CodeRetrievalTestSuite(),
            "graph_quality": GraphQualityTestSuite(), 
            "hybrid_search": HybridSearchTestSuite(),
            "embedding_comparison": EmbeddingComparisonTestSuite()
        }
    
    def get_all_test_cases(self) -> Dict[str, List[TestCase]]:
        """Obtiene todos los casos de prueba organizados por suite"""
        return {name: suite.test_cases for name, suite in self.suites.items()}
    
    def get_test_case_by_id(self, test_id: str) -> TestCase:
        """Obtiene un caso de prueba específico por ID"""
        for suite in self.suites.values():
            for test_case in suite.test_cases:
                if test_case.id == test_id:
                    return test_case
        raise ValueError(f"Test case {test_id} not found")
    
    def get_tests_by_category(self, category: str) -> List[TestCase]:
        """Obtiene tests por categoría"""
        tests = []
        for suite in self.suites.values():
            tests.extend([tc for tc in suite.test_cases if tc.category == category])
        return tests
    
    def generate_test_summary(self) -> Dict[str, Any]:
        """Genera resumen de todos los tests disponibles"""
        summary = {
            "total_suites": len(self.suites),
            "total_tests": sum(len(suite.test_cases) for suite in self.suites.values()),
            "suites_breakdown": {},
            "categories": set()
        }
        
        for name, suite in self.suites.items():
            summary["suites_breakdown"][name] = {
                "test_count": len(suite.test_cases),
                "test_ids": [tc.id for tc in suite.test_cases]
            }
            summary["categories"].update(tc.category for tc in suite.test_cases)
        
        summary["categories"] = list(summary["categories"])
        return summary

# ===== VALIDATION FUNCTIONS =====

def validate_test_suite_definitions():
    """Valida que todas las definiciones de test sean correctas"""
    
    manager = TestSuiteManager()
    summary = manager.generate_test_summary()
    
    print("🧪 VALIDACIÓN DE TEST SUITES")
    print("=" * 50)
    print(f"✅ Total Suites: {summary['total_suites']}")
    print(f"✅ Total Tests: {summary['total_tests']}")
    print(f"✅ Categorías: {len(summary['categories'])}")
    
    print("\n📊 BREAKDOWN POR SUITE:")
    for suite_name, details in summary["suites_breakdown"].items():
        print(f"  🔸 {suite_name}: {details['test_count']} tests")
        for test_id in details["test_ids"]:
            print(f"    - {test_id}")
    
    print(f"\n🏷️  CATEGORÍAS DISPONIBLES:")
    for category in summary["categories"]:
        tests_in_category = manager.get_tests_by_category(category)
        print(f"  🔹 {category}: {len(tests_in_category)} tests")
    
    return True

def prepare_test_data_for_framework():
    """Prepara datos de test para usar con el framework de evaluación"""
    
    manager = TestSuiteManager()
    
    # Extraer test data estructurado
    code_retrieval_suite = manager.suites["code_retrieval"]
    
    # Formatear para framework
    framework_test_data = {
        "code_retrieval_queries": [],
        "ground_truth": {},
        "code_samples": [],
        "expected_results": {}
    }
    
    for test_case in code_retrieval_suite.test_cases:
        if isinstance(test_case, CodeRetrievalTestCase):
            # Queries para testing
            framework_test_data["code_retrieval_queries"].append({
                "id": test_case.id,
                "natural_query": test_case.input_data.get("natural_query"),
                "technical_query": test_case.input_data.get("technical_query"),
                "expected_task_type": test_case.expected_task_type,
                "complexity": test_case.complexity_level
            })
            
            # Código para almacenar
            framework_test_data["code_samples"].append({
                "id": test_case.id,
                "code": test_case.input_data.get("code"),
                "language": test_case.code_language,
                "category": test_case.category
            })
            
            # Resultados esperados
            framework_test_data["expected_results"][test_case.id] = test_case.expected_output
    
    return framework_test_data

# ===== DEMO =====

if __name__ == "__main__":
    print("🚀 DEMO: Test Suites Definition")
    print("=" * 60)
    
    # Validar definiciones
    validate_test_suite_definitions()
    
    # Preparar datos para framework
    test_data = prepare_test_data_for_framework()
    print(f"\n📋 DATOS PREPARADOS PARA FRAMEWORK:")
    print(f"   Queries de prueba: {len(test_data['code_retrieval_queries'])}")
    print(f"   Muestras de código: {len(test_data['code_samples'])}")
    print(f"   Resultados esperados: {len(test_data['expected_results'])}")
    
    print("\n✅ Test suites preparados y validados!")
    print("   Listos para usar con evaluation_framework_complete.py")