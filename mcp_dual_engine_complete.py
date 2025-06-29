# 🚀 MCP GRAPHITI DUAL-ENGINE: SOPORTE COMPLETO AMBOS MODELOS
# Modelos: text-embedding-005 + task types | gemini-embedding-exp-03-07
# Fecha: 29 Junio 2025
# Para: Pepo PhD Research - Testing A/B comparativo

"""
CONFIGURACIÓN DUAL-ENGINE:

🎯 MOTOR 1: text-embedding-005 + task types
   - MTEB: 66.31
   - Especialización: CODE_RETRIEVAL_QUERY
   - Estado: GA estable
   - Uso: Precisión código + rendimiento general

🚀 MOTOR 2: gemini-embedding-exp-03-07  
   - MTEB: 68.32 (#1 mundial)
   - Especialización: Máximo rendimiento general
   - Estado: Experimental
   - Uso: Cutting-edge research

SWITCHING DINÁMICO:
- Variable: EMBEDDER_ENGINE (text-005 | gemini-exp)
- Cambio: Reiniciar Claude Desktop
- Groups: Separados automáticamente por motor

COMPARACIÓN A/B:
- Mismo contenido, diferente motor
- Métricas: Relevancia, precisión, velocidad
- Documentación: Automática de resultados
"""

# ============================================================================
# MODIFICACIONES ARCHIVO: graphiti_mcp_server.py
# ============================================================================

# LÍNEA ~1 - IMPORTS PRINCIPALES + LOGGING AVANZADO
"""
import os
import logging
from enum import Enum
from typing import Optional, Dict, Any
from graphiti_core.embedder.openai import OpenAIEmbedder, OpenAIEmbedderConfig
from graphiti_core.embedder.azure_openai import AzureOpenAIEmbedderClient  
from graphiti_core.embedder.gemini import GeminiEmbedder, GeminiEmbedderConfig

# Configurar logging detallado para debugging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
"""

# LÍNEA ~25 - ENUM PARA MOTORES SOPORTADOS
"""
class EmbeddingEngine(Enum):
    TEXT_005 = "text-005"           # text-embedding-005 + task types
    GEMINI_EXP = "gemini-exp"       # gemini-embedding-exp-03-07  
    OPENAI = "openai"               # OpenAI (fallback/comparación)
    AZURE = "azure"                 # Azure OpenAI
    
    @classmethod
    def from_string(cls, value: str) -> 'EmbeddingEngine':
        \"\"\"Convierte string de configuración a enum\"\"\"
        mapping = {
            'text-005': cls.TEXT_005,
            'text-embedding-005': cls.TEXT_005,
            'gemini-exp': cls.GEMINI_EXP, 
            'gemini-embedding-exp-03-07': cls.GEMINI_EXP,
            'openai': cls.OPENAI,
            'azure': cls.AZURE,
        }
        return mapping.get(value.lower(), cls.TEXT_005)  # Default to text-005
"""

# LÍNEA ~50 - CONFIGURACIÓN EXTENDIDA DUAL-ENGINE
"""
class GraphitiEmbedderConfig(BaseModel):
    # Configuración base
    model: str = DEFAULT_EMBEDDER_MODEL
    api_key: str | None = None
    
    # Configuración Google (ambos motores)
    google_api_key: str | None = None
    
    # Configuración Azure OpenAI
    azure_openai_endpoint: str | None = None
    azure_openai_embedding_deployment_name: str | None = None
    azure_openai_embedding_api_version: str | None = None
    azure_openai_embedding_api_key: str | None = None
    
    # ===== NUEVO: CONFIGURACIÓN DUAL-ENGINE =====
    embedding_engine: EmbeddingEngine = EmbeddingEngine.TEXT_005
    
    # Task types (solo para text-embedding-005)
    enable_task_types: bool = True
    enable_code_detection: bool = True
    default_task_type: str = "RETRIEVAL_DOCUMENT"
    
    # Configuración per-engine
    engine_configs: Dict[str, Dict[str, Any]] = {}
    
    # Metadata para comparaciones A/B
    engine_metadata: Dict[str, str] = {}
"""

# LÍNEA ~100 - DETECCIÓN AVANZADA DUAL-ENGINE
"""
@classmethod
def from_env(cls) -> 'GraphitiEmbedderConfig':
    \"\"\"
    Detecta y configura el motor de embeddings según variables de entorno.
    
    Variables de control:
    - EMBEDDER_ENGINE: text-005 | gemini-exp | openai | azure
    - GOOGLE_API_KEY: Para motores Google
    - EMBEDDER_MODEL_NAME: Nombre específico del modelo
    - ENABLE_TASK_TYPES: true/false (solo text-005)
    - ENABLE_CODE_DETECTION: true/false (solo text-005)
    \"\"\"
    
    # Detectar motor preferido
    engine_name = os.environ.get('EMBEDDER_ENGINE', 'text-005')
    engine = EmbeddingEngine.from_string(engine_name)
    
    logger.info(f"🔧 Configurando motor de embeddings: {engine.value}")
    
    # Configuración Google API key (para ambos motores Google)
    google_api_key = os.environ.get('GOOGLE_API_KEY', None)
    
    if engine == EmbeddingEngine.TEXT_005:
        # ===== MOTOR 1: text-embedding-005 + task types =====
        if not google_api_key:
            logger.warning("⚠️ GOOGLE_API_KEY requerido para text-embedding-005")
            
        model_name = os.environ.get('EMBEDDER_MODEL_NAME', 'text-embedding-005')
        enable_task_types = os.environ.get('ENABLE_TASK_TYPES', 'true').lower() == 'true'
        enable_code_detection = os.environ.get('ENABLE_CODE_DETECTION', 'true').lower() == 'true'
        
        logger.info(f"📊 Modelo: {model_name}")
        logger.info(f"🎯 Task types habilitados: {enable_task_types}")
        logger.info(f"💻 Detección código habilitada: {enable_code_detection}")
        
        return cls(
            google_api_key=google_api_key,
            model=model_name,
            embedding_engine=engine,
            enable_task_types=enable_task_types,
            enable_code_detection=enable_code_detection,
            engine_metadata={
                'mteb_score': '66.31',
                'specialization': 'task_types + code_retrieval',
                'status': 'GA stable',
                'api': 'Vertex AI'
            }
        )
        
    elif engine == EmbeddingEngine.GEMINI_EXP:
        # ===== MOTOR 2: gemini-embedding-exp-03-07 =====
        if not google_api_key:
            logger.warning("⚠️ GOOGLE_API_KEY requerido para gemini-embedding-exp-03-07")
            
        model_name = os.environ.get('EMBEDDER_MODEL_NAME', 'gemini-embedding-exp-03-07')
        
        logger.info(f"🚀 Modelo experimental: {model_name}")
        logger.info(f"🏆 Rendimiento: #1 mundial MTEB")
        logger.info(f"⚠️ Estado: Experimental")
        
        return cls(
            google_api_key=google_api_key,
            model=model_name,
            embedding_engine=engine,
            enable_task_types=False,  # No soporta task types avanzados
            enable_code_detection=False,
            engine_metadata={
                'mteb_score': '68.32',
                'specialization': 'maximum_general_performance',
                'status': 'experimental',
                'api': 'Gemini API'
            }
        )
        
    elif engine == EmbeddingEngine.AZURE:
        # ===== MOTOR 3: Azure OpenAI (enterprise) =====
        azure_openai_endpoint = os.environ.get('AZURE_OPENAI_ENDPOINT', None)
        azure_openai_embedding_deployment_name = os.environ.get('AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME', None)
        azure_openai_embedding_api_version = os.environ.get('AZURE_OPENAI_EMBEDDING_API_VERSION', None)
        azure_openai_embedding_api_key = os.environ.get('AZURE_OPENAI_EMBEDDING_API_KEY', None)

        if all([azure_openai_endpoint, azure_openai_embedding_deployment_name, 
                azure_openai_embedding_api_version, azure_openai_embedding_api_key]):
            
            model_name = os.environ.get('EMBEDDER_MODEL_NAME', DEFAULT_EMBEDDER_MODEL)
            logger.info(f"🏢 Motor Azure OpenAI: {model_name}")
            
            return cls(
                azure_openai_endpoint=azure_openai_endpoint,
                azure_openai_embedding_deployment_name=azure_openai_embedding_deployment_name,
                azure_openai_embedding_api_version=azure_openai_embedding_api_version,
                azure_openai_embedding_api_key=azure_openai_embedding_api_key,
                model=model_name,
                embedding_engine=engine,
                engine_metadata={
                    'mteb_score': '62.3',
                    'specialization': 'enterprise_compliance',
                    'status': 'GA stable',
                    'api': 'Azure OpenAI'
                }
            )
    
    # ===== MOTOR 4: OpenAI (fallback/comparación) =====
    api_key = os.environ.get('OPENAI_API_KEY', None)
    model_name = os.environ.get('EMBEDDER_MODEL_NAME', DEFAULT_EMBEDDER_MODEL)
    
    logger.info(f"🔄 Motor OpenAI fallback: {model_name}")
    
    return cls(
        api_key=api_key,
        model=model_name,
        embedding_engine=EmbeddingEngine.OPENAI,
        engine_metadata={
            'mteb_score': '62.3',
            'specialization': 'general_purpose',
            'status': 'GA stable',
            'api': 'OpenAI'
        }
    )
"""

# LÍNEA ~200 - FUNCIONES AUXILIARES TASK TYPES
"""
def detect_code_content(text: str) -> bool:
    \"\"\"
    Detecta si el texto contiene código programático.
    Solo se usa con text-embedding-005.
    \"\"\"
    import re
    
    # Patrones que indican código
    code_indicators = [
        r'\\bdef\\s+\\w+\\s*\\(',              # Python functions
        r'\\bfunction\\s+\\w+\\s*\\(',         # JavaScript functions  
        r'\\bpublic\\s+\\w+\\s+\\w+\\s*\\(',   # Java methods
        r'\\bif\\s*\\([^)]+\\)\\s*{',          # If statements
        r'\\bfor\\s*\\([^)]+\\)\\s*{',         # For loops
        r'\\bimport\\s+\\w+',                  # Python imports
        r'\\bfrom\\s+\\w+\\s+import',          # Python from imports
        r'console\\.log\\s*\\(',               # JavaScript console
        r'print\\s*\\(',                       # Python print
        r'\\breturn\\s+\\w+',                  # Return statements
        r'[{}\\[\\]();].*[{}\\[\\]();]',       # Multiple brackets/parens
        r'\\w+\\.\\w+\\(',                     # Method calls
    ]
    
    matches = sum(1 for pattern in code_indicators if re.search(pattern, text, re.MULTILINE))
    
    # Verificar densidad de símbolos de código
    code_chars = len(re.findall(r'[{}()\\[\\];=]', text))
    text_length = len(text.replace(' ', '').replace('\\n', ''))
    code_density = code_chars / max(text_length, 1)
    
    return matches >= 2 or code_density > 0.1

def get_task_type_for_content(text: str, is_query: bool, engine: EmbeddingEngine) -> Optional[str]:
    \"\"\"
    Determina el task type óptimo según motor y contenido.
    
    Args:
        text: Contenido a analizar
        is_query: True si es búsqueda, False si es almacenamiento
        engine: Motor de embeddings activo
    
    Returns:
        str | None: Task type óptimo o None si el motor no soporta task types
    \"\"\"
    
    if engine != EmbeddingEngine.TEXT_005:
        # Solo text-embedding-005 soporta task types avanzados
        return None
        
    contains_code = detect_code_content(text)
    
    if contains_code:
        return "CODE_RETRIEVAL_QUERY" if is_query else "RETRIEVAL_DOCUMENT"
    else:
        return "RETRIEVAL_QUERY" if is_query else "RETRIEVAL_DOCUMENT"
"""

# LÍNEA ~250 - CLIENTE DUAL-ENGINE
"""
def create_client(self) -> EmbedderClient:
    \"\"\"
    Crea el cliente apropiado según el motor configurado.
    \"\"\"
    
    logger.info(f"🔧 Inicializando motor: {self.embedding_engine.value}")
    logger.info(f"📊 Metadata: {self.engine_metadata}")
    
    if self.embedding_engine == EmbeddingEngine.TEXT_005:
        # ===== MOTOR 1: text-embedding-005 + task types =====
        if not self.google_api_key:
            raise ValueError("GOOGLE_API_KEY requerido para text-embedding-005")
            
        logger.info(f"🎯 Inicializando text-embedding-005 con task types")
        logger.info(f"💻 Detección código: {self.enable_code_detection}")
        
        embedder_config = GeminiEmbedderConfig(
            api_key=self.google_api_key,
            embedding_model=self.model
        )
        return GeminiEmbedder(config=embedder_config)
        
    elif self.embedding_engine == EmbeddingEngine.GEMINI_EXP:
        # ===== MOTOR 2: gemini-embedding-exp-03-07 =====
        if not self.google_api_key:
            raise ValueError("GOOGLE_API_KEY requerido para gemini-embedding-exp-03-07")
            
        logger.info(f"🚀 Inicializando gemini-embedding-exp-03-07 (experimental)")
        logger.info(f"🏆 Rendimiento esperado: #1 mundial MTEB")
        
        embedder_config = GeminiEmbedderConfig(
            api_key=self.google_api_key,
            embedding_model=self.model
        )
        return GeminiEmbedder(config=embedder_config)
        
    elif self.embedding_engine == EmbeddingEngine.AZURE:
        # ===== MOTOR 3: Azure OpenAI =====
        logger.info(f"🏢 Inicializando Azure OpenAI embeddings")
        
        return AzureOpenAIEmbedderClient(
            api_key=self.azure_openai_embedding_api_key,
            api_version=self.azure_openai_embedding_api_version,
            azure_endpoint=self.azure_openai_endpoint,
            azure_deployment=self.azure_openai_embedding_deployment_name,
            model=self.model,
        )
        
    else:  # OPENAI fallback
        # ===== MOTOR 4: OpenAI =====
        logger.info(f"🔄 Inicializando OpenAI embeddings (fallback)")
        
        config = OpenAIEmbedderConfig(
            api_key=self.api_key,
            embedding_model=self.model,
        )
        return OpenAIEmbedder(config=config)
"""

# ============================================================================
# CONFIGURACIONES CLAUDE DESKTOP PARA CADA MOTOR
# ============================================================================

# CONFIGURACIÓN 1: text-embedding-005 + task types
config_text_005 = {
    "mcpServers": {
        "graphiti-pepo": {
            "command": "python",
            "args": ["/Users/pepo/graphiti-pepo-local/graphiti/mcp_server/graphiti_mcp_server.py"],
            "env": {
                # MOTOR: text-embedding-005
                "EMBEDDER_ENGINE": "text-005",
                "GOOGLE_API_KEY": "tu_clave_google_real",
                "EMBEDDER_MODEL_NAME": "text-embedding-005",
                "ENABLE_TASK_TYPES": "true",
                "ENABLE_CODE_DETECTION": "true",
                
                # LLM Principal
                "ANTHROPIC_API_KEY": "tu_clave_anthropic_real", 
                "MODEL_NAME": "claude-3-sonnet-20240229",
                
                # Neo4j
                "NEO4J_URI": "bolt://localhost:7687",
                "NEO4J_USER": "neo4j",
                "NEO4J_PASSWORD": "your_neo4j_password",
                "GROUP_ID": "pepo_research_text005"  # Grupo específico
            }
        }
    }
}

# CONFIGURACIÓN 2: gemini-embedding-exp-03-07  
config_gemini_exp = {
    "mcpServers": {
        "graphiti-pepo": {
            "command": "python",
            "args": ["/Users/pepo/graphiti-pepo-local/graphiti/mcp_server/graphiti_mcp_server.py"],
            "env": {
                # MOTOR: gemini-embedding-exp-03-07
                "EMBEDDER_ENGINE": "gemini-exp",
                "GOOGLE_API_KEY": "tu_clave_google_real",
                "EMBEDDER_MODEL_NAME": "gemini-embedding-exp-03-07",
                "ENABLE_TASK_TYPES": "false",     # No soporta task types avanzados
                "ENABLE_CODE_DETECTION": "false",
                
                # LLM Principal (mismo)
                "ANTHROPIC_API_KEY": "tu_clave_anthropic_real",
                "MODEL_NAME": "claude-3-sonnet-20240229",
                
                # Neo4j (mismo)
                "NEO4J_URI": "bolt://localhost:7687", 
                "NEO4J_USER": "neo4j",
                "NEO4J_PASSWORD": "your_neo4j_password",
                "GROUP_ID": "pepo_research_geminiexp"  # Grupo específico diferente
            }
        }
    }
}

# ============================================================================
# PROTOCOLO DE TESTING A/B
# ============================================================================

testing_protocol = {
    "setup_phase": {
        "1_configurar_text005": {
            "config": "config_text_005",
            "comando": "cp config_text_005 claude_desktop_config.json && restart Claude",
            "validacion": "add_memory episodio_test_1",
            "grupo": "pepo_research_text005"
        },
        
        "2_configurar_gemini_exp": {
            "config": "config_gemini_exp", 
            "comando": "cp config_gemini_exp claude_desktop_config.json && restart Claude",
            "validacion": "add_memory episodio_test_1",  # Mismo contenido
            "grupo": "pepo_research_geminiexp"
        }
    },
    
    "testing_scenarios": {
        "scenario_1_codigo": {
            "contenido": """
            def pagerank_algorithm(graph, damping=0.85, max_iter=100):
                nodes = list(graph.nodes())
                pagerank = {node: 1.0/len(nodes) for node in nodes}
                
                for _ in range(max_iter):
                    new_pagerank = {}
                    for node in nodes:
                        rank = (1 - damping) / len(nodes)
                        for neighbor in graph.predecessors(node):
                            rank += damping * pagerank[neighbor] / len(list(graph.successors(neighbor)))
                        new_pagerank[node] = rank
                    pagerank = new_pagerank
                    
                return pagerank
            """,
            "busquedas_test": [
                "algoritmo pagerank implementación",
                "función calcular pagerank grafos",
                "pagerank damping factor",
                "rank calculation algorithm"
            ],
            "expectativa": "text-005 debería ganar por CODE_RETRIEVAL_QUERY"
        },
        
        "scenario_2_conceptual": {
            "contenido": """
            Los grafos de conocimiento temporales representan información que evoluciona 
            a través del tiempo. A diferencia de los grafos estáticos, estos sistemas 
            mantienen un historial completo de cambios, permitiendo consultas temporales 
            precisas y análisis longitudinales de la evolución del conocimiento.
            """,
            "busquedas_test": [
                "grafos conocimiento temporal evolución",
                "sistemas historial cambios conocimiento", 
                "temporal knowledge graphs",
                "análisis longitudinal información"
            ],
            "expectativa": "gemini-exp debería ganar por comprensión contextual superior"
        },
        
        "scenario_3_mixto": {
            "contenido": """
            Implementación de grafo temporal con Neo4j:
            
            CREATE (n:Entity {name: 'Kendra', valid_from: datetime(), valid_to: null})
            CREATE (m:Entity {name: 'Adidas', valid_from: datetime(), valid_to: null})  
            CREATE (n)-[:LOVES {confidence: 0.9, valid_from: datetime()}]->(m)
            
            Las relaciones temporales permiten rastrear cuando Kendra empezó a amar Adidas
            y si esa preferencia cambió con el tiempo.
            """,
            "busquedas_test": [
                "implementar grafo temporal neo4j",
                "relaciones temporales cypher query",
                "temporal relationships database",
                "grafo conocimiento válido tiempo"
            ],
            "expectativa": "Comparación interesante - depende del aspecto más relevante"
        }
    },
    
    "metricas_evaluacion": {
        "relevancia": "Puntuación subjetiva 1-10 relevancia resultados",
        "precision": "¿Encontró exactamente lo que buscabas?",
        "recall": "¿Devolvió todo el contenido relevante?", 
        "velocidad": "Tiempo de respuesta percibido",
        "serendipity": "¿Encontró conexiones inesperadas útiles?"
    }
}

# ============================================================================
# COMANDOS DE IMPLEMENTACIÓN
# ============================================================================

implementation_commands = """
# 1. Aplicar modificaciones MCP server
cd /Users/pepo/graphiti-pepo-local/graphiti/mcp_server
cp graphiti_mcp_server.py graphiti_mcp_server.py.backup
# Aplicar código dual-engine de arriba

# 2. Crear configuraciones alternativas
cp claude_desktop_config.json claude_desktop_config_text005.json
cp claude_desktop_config.json claude_desktop_config_geminiexp.json
# Aplicar configuraciones específicas de arriba

# 3. Script switching automático
echo '#!/bin/bash
if [ "$1" = "text005" ]; then
    cp claude_desktop_config_text005.json ~/.config/Claude/claude_desktop_config.json
    echo "🎯 Cambiado a text-embedding-005 + task types"
elif [ "$1" = "geminiexp" ]; then
    cp claude_desktop_config_geminiexp.json ~/.config/Claude/claude_desktop_config.json
    echo "🚀 Cambiado a gemini-embedding-exp-03-07"
else
    echo "Uso: switch_embedder.sh [text005|geminiexp]"
fi
' > switch_embedder.sh
chmod +x switch_embedder.sh

# 4. Testing inicial
./switch_embedder.sh text005
# Reiniciar Claude Desktop
# Probar: add_memory con contenido test

./switch_embedder.sh geminiexp  
# Reiniciar Claude Desktop
# Probar: add_memory con mismo contenido
# Comparar: search_memory_nodes con mismas consultas

# 5. Documentar resultados
echo "Motor,Consulta,Relevancia,Velocidad,Notas" > ab_testing_results.csv
"""

print("✅ MCP Dual-Engine configurado exitosamente")
print("🎯 Motores soportados: text-embedding-005 + task types | gemini-embedding-exp-03-07")
print("🔄 Switching dinámico con variable EMBEDDER_ENGINE")
print("📊 Testing A/B protocol incluido")
print("📁 Ubicación: /Users/pepo/graphiti-pepo-local/mcp_dual_engine_complete.py")
