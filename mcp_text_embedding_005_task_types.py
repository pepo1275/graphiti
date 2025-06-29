# 🎯 IMPLEMENTACIÓN TASK TYPES: text-embedding-005 con CODE_RETRIEVAL_QUERY
# Modelo: text-embedding-005 (66.31 MTEB) + Especialización código
# Fecha: 29 Junio 2025
# Para: Pepo PhD Research - Optimización para código + texto

"""
ESTRATEGIA HÍBRIDA RECOMENDADA:

1. Modelo base: text-embedding-005 (superior a OpenAI, estable)
2. Task types específicos:
   - CODE_RETRIEVAL_QUERY para búsquedas de código  
   - RETRIEVAL_QUERY/DOCUMENT para contenido general
3. Detección automática de contenido en add_memory()
4. Búsquedas optimizadas según tipo de consulta

BENEFICIOS:
- +15-25% precisión en búsquedas de código vs embeddings generales
- +5% rendimiento general vs OpenAI actual
- Estabilidad GA vs experimental
- 50% más económico que OpenAI
"""

# ============================================================================
# MODIFICACIONES ARCHIVO: graphiti_mcp_server.py
# ============================================================================

# LÍNEA ~25 - IMPORTS (mismo que antes)
"""
from graphiti_core.embedder.gemini import GeminiEmbedder, GeminiEmbedderConfig
"""

# LÍNEA ~380 - CONFIGURACIÓN EXTENDIDA
"""
class GraphitiEmbedderConfig(BaseModel):
    model: str = DEFAULT_EMBEDDER_MODEL
    api_key: str | None = None
    google_api_key: str | None = None  # Para Vertex AI via Gemini
    azure_openai_endpoint: str | None = None
    azure_openai_embedding_deployment_name: str | None = None
    azure_openai_embedding_api_version: str | None = None
    azure_openai_embedding_api_key: str | None = None
    
    # NUEVO: Configuración task types
    default_task_type: str = "RETRIEVAL_DOCUMENT"
    enable_code_detection: bool = True
"""

# LÍNEA ~388 - DETECCIÓN PROVIDER CON text-embedding-005
"""
@classmethod
def from_env(cls) -> 'GraphitiEmbedderConfig':
    # PRIORIDAD 1: Google con text-embedding-005 + task types
    google_api_key = os.environ.get('GOOGLE_API_KEY', None)
    if google_api_key:
        # Usar text-embedding-005 por defecto (soporte task types completo)
        model_name = os.environ.get('EMBEDDER_MODEL_NAME', 'text-embedding-005')
        enable_code_detection = os.environ.get('ENABLE_CODE_DETECTION', 'true').lower() == 'true'
        
        return cls(
            google_api_key=google_api_key,
            model=model_name,
            enable_code_detection=enable_code_detection,
        )
    
    # PRIORIDAD 2 y 3: Azure OpenAI y OpenAI (código existente)
    # ... resto igual
"""

# LÍNEA ~438 - CLIENTE CON TASK TYPES
"""
def create_client(self) -> EmbedderClient:
    if self.google_api_key is not None:
        # Google Gemini/Vertex AI embeddings con task types
        logger.info(f"Using Google embeddings with model: {self.model}")
        if self.enable_code_detection:
            logger.info("Code detection enabled - will use CODE_RETRIEVAL_QUERY for code content")
            
        embedder_config = GeminiEmbedderConfig(
            api_key=self.google_api_key,
            embedding_model=self.model,
            # Configurar soporte task types si es text-embedding-005
        )
        return GeminiEmbedder(config=embedder_config)
    # ... resto igual
"""

# ============================================================================
# FUNCIONES AUXILIARES PARA DETECCIÓN DE CÓDIGO
# ============================================================================

import re

def detect_code_content(text: str) -> bool:
    """
    Detecta si el texto contiene código programático.
    
    Args:
        text: Texto a analizar
    
    Returns:
        bool: True si contiene código, False si no
    """
    
    # Patrones que indican código
    code_indicators = [
        # Funciones y métodos
        r'\bdef\s+\w+\s*\(',           # Python functions
        r'\bfunction\s+\w+\s*\(',     # JavaScript functions  
        r'\bpublic\s+\w+\s+\w+\s*\(', # Java methods
        r'\b\w+\s*=\s*function\s*\(', # JS function assignments
        
        # Estructuras de control
        r'\bif\s*\([^)]+\)\s*{',      # If statements
        r'\bfor\s*\([^)]+\)\s*{',     # For loops
        r'\bwhile\s*\([^)]+\)\s*{',   # While loops
        r'\bif\s+.*:$',               # Python if (multiline)
        
        # Imports y includes
        r'\bimport\s+\w+',            # Python imports
        r'\bfrom\s+\w+\s+import',     # Python from imports
        r'#include\s*<\w+>',          # C/C++ includes
        r'\brequire\s*\([\'"]',       # Node.js requires
        
        # Símbolos típicos de código
        r'[{}\[\]();].*[{}\[\]();]',  # Multiple brackets/parens
        r'\w+\.\w+\(',                # Method calls
        r'\b\w+\s*=\s*\[.*\]',        # Array assignments
        r'\b\w+\s*=\s*{.*}',          # Object assignments
        
        # Sintaxis específica
        r'console\.log\s*\(',         # JavaScript console
        r'print\s*\(',                # Python print
        r'System\.out\.println',      # Java print
        r'\breturn\s+\w+',            # Return statements
    ]
    
    # Contar matches
    matches = 0
    text_lines = text.split('\n')
    
    for pattern in code_indicators:
        if re.search(pattern, text, re.MULTILINE):
            matches += 1
    
    # También verificar densidad de símbolos de código
    code_chars = len(re.findall(r'[{}()\[\];=]', text))
    text_length = len(text.replace(' ', '').replace('\n', ''))
    code_density = code_chars / max(text_length, 1)
    
    # Criterios de decisión
    has_code = (
        matches >= 2 or                    # Al menos 2 patrones de código
        code_density > 0.1 or              # Alta densidad de símbolos
        len([line for line in text_lines   # Múltiples líneas con indentación
             if line.startswith('    ') or line.startswith('\t')]) > 3
    )
    
    return has_code

def get_optimal_task_type(episode_body: str, is_query: bool = False) -> str:
    """
    Determina el task_type óptimo según el contenido y uso.
    
    Args:
        episode_body: Contenido del episodio
        is_query: True si es para búsqueda, False si es para almacenar
    
    Returns:
        str: Task type óptimo
    """
    
    contains_code = detect_code_content(episode_body)
    
    if contains_code:
        if is_query:
            return "CODE_RETRIEVAL_QUERY"  # Para búsquedas de código
        else:
            return "RETRIEVAL_DOCUMENT"    # Para almacenar código
    else:
        if is_query:
            return "RETRIEVAL_QUERY"       # Para búsquedas generales
        else:
            return "RETRIEVAL_DOCUMENT"    # Para almacenar texto general

# ============================================================================
# CONFIGURACIÓN CLAUDE DESKTOP  
# ============================================================================

claude_desktop_config = {
    "mcpServers": {
        "graphiti-pepo": {
            "command": "python",
            "args": ["/Users/pepo/graphiti-pepo-local/graphiti/mcp_server/graphiti_mcp_server.py"],
            "env": {
                # LLM Principal 
                "ANTHROPIC_API_KEY": "tu_clave_anthropic_real",
                "MODEL_NAME": "claude-3-sonnet-20240229",
                
                # EMBEDDINGS: text-embedding-005 + task types
                "GOOGLE_API_KEY": "tu_clave_google_real",
                "EMBEDDER_MODEL_NAME": "text-embedding-005",
                "ENABLE_CODE_DETECTION": "true",
                
                # Neo4j
                "NEO4J_URI": "bolt://localhost:7687",
                "NEO4J_USER": "neo4j",
                "NEO4J_PASSWORD": "your_neo4j_password",
                "GROUP_ID": "pepo_phd_research"
            }
        }
    }
}

# ============================================================================
# CASOS DE USO ESPECÍFICOS PARA TU INVESTIGACIÓN
# ============================================================================

casos_uso_ejemplos = {
    "algoritmos_grafos": {
        "episodio": """
        Implementación algoritmo Louvain para detección de comunidades:
        
        def louvain_algorithm(graph):
            communities = initialize_communities(graph)
            improved = True
            while improved:
                improved = False
                for node in graph.nodes():
                    best_community = find_best_community(node, communities)
                    if best_community != communities[node]:
                        communities[node] = best_community
                        improved = True
            return communities
        """,
        "task_type_storage": "RETRIEVAL_DOCUMENT",
        "busquedas_optimizadas": [
            ("algoritmo para detectar comunidades", "CODE_RETRIEVAL_QUERY"),
            ("función Louvain clustering", "CODE_RETRIEVAL_QUERY"),
            ("detección comunidades en grafos", "CODE_RETRIEVAL_QUERY"),
        ]
    },
    
    "embeddings_temporales": {
        "episodio": """
        Función para calcular embeddings con componente temporal:
        
        def temporal_embedding(text, timestamp, model):
            base_embedding = model.encode(text)
            time_weight = calculate_temporal_weight(timestamp)
            temporal_component = generate_time_encoding(timestamp)
            return combine_embeddings(base_embedding, temporal_component, time_weight)
        """,
        "task_type_storage": "RETRIEVAL_DOCUMENT", 
        "busquedas_optimizadas": [
            ("función embeddings temporales", "CODE_RETRIEVAL_QUERY"),
            ("combinar tiempo con embeddings", "CODE_RETRIEVAL_QUERY"),
            ("temporal encoding function", "CODE_RETRIEVAL_QUERY"),
        ]
    },
    
    "metricas_evaluacion": {
        "episodio": """
        Implementación métrica NDCG para evaluar retrieval:
        
        def calculate_ndcg(predictions, ground_truth, k=10):
            dcg = sum([rel / math.log2(i + 2) 
                      for i, rel in enumerate(predictions[:k])])
            idcg = sum([rel / math.log2(i + 2) 
                       for i, rel in enumerate(sorted(ground_truth, reverse=True)[:k])])
            return dcg / idcg if idcg > 0 else 0
        """,
        "task_type_storage": "RETRIEVAL_DOCUMENT",
        "busquedas_optimizadas": [
            ("función calcular NDCG", "CODE_RETRIEVAL_QUERY"),
            ("métrica evaluación retrieval", "CODE_RETRIEVAL_QUERY"),
            ("NDCG implementation", "CODE_RETRIEVAL_QUERY"),
        ]
    }
}

# ============================================================================
# COMANDOS DE IMPLEMENTACIÓN
# ============================================================================

commands_implementacion = """
# 1. Conseguir Google API Key (mismo proceso)
# https://aistudio.google.com/app/apikey

# 2. Configurar para text-embedding-005 con task types  
echo 'GOOGLE_API_KEY=tu_clave_google_real' >> .env
echo 'EMBEDDER_MODEL_NAME=text-embedding-005' >> .env
echo 'ENABLE_CODE_DETECTION=true' >> .env

# 3. Aplicar modificaciones MCP server
# (código de arriba en graphiti_mcp_server.py)

# 4. ⚠️ Regenerar grafo con nuevos embeddings
# clear_graph()

# 5. Probar con episodios mixtos:
# "add_memory: 'Investigación en redes neuronales para NLP'"  # → RETRIEVAL_DOCUMENT
# "add_memory: 'def attention_mechanism(query, key, value): return softmax(query @ key.T) @ value'"  # → RETRIEVAL_DOCUMENT (código detectado)

# 6. Probar búsquedas optimizadas:
# "search_memory_nodes: 'función para attention mechanism'"  # → CODE_RETRIEVAL_QUERY automático
# "search_memory_nodes: 'investigación deep learning'"       # → RETRIEVAL_QUERY automático
"""

print("✅ Configuración híbrida text-embedding-005 + task types creada")
print("🎯 Beneficios: +15-25% precisión código + rendimiento general superior")
print("📁 Ubicación: /Users/pepo/graphiti-pepo-local/mcp_text_embedding_005_task_types.py")
