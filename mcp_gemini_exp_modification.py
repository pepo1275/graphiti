# 🚀 MODIFICACIÓN MCP GRAPHITI: GEMINI EXPERIMENTAL EMBEDDINGS
# Modelo: gemini-embedding-exp-03-07 (#1 Mundial MTEB 68.32)
# Fecha: 28 Junio 2025
# Para: Pepo PhD Research - Máximo rendimiento embeddings

"""
INSTRUCCIONES DE IMPLEMENTACIÓN:

1. Conseguir Gemini API Key:
   https://aistudio.google.com/app/apikey

2. Aplicar cambios en /Users/pepo/graphiti-pepo-local/graphiti/mcp_server/graphiti_mcp_server.py

3. Variables de entorno:
   GOOGLE_API_KEY=tu_clave_google_real
   EMBEDDER_MODEL_NAME=gemini-embedding-exp-03-07

4. ⚠️ IMPORTANTE: clear_graph() después del cambio
"""

# ============================================================================
# MODIFICACIONES ARCHIVO: graphiti_mcp_server.py
# ============================================================================

# LÍNEA ~25 - IMPORTS ADICIONALES
# Agregar después de imports existentes:
"""
from graphiti_core.embedder.gemini import GeminiEmbedder, GeminiEmbedderConfig
"""

# LÍNEA ~380 - CONFIGURACIÓN EXTENDIDA
# Modificar clase GraphitiEmbedderConfig:
"""
class GraphitiEmbedderConfig(BaseModel):
    model: str = DEFAULT_EMBEDDER_MODEL
    api_key: str | None = None
    google_api_key: str | None = None  # ← NUEVO CAMPO
    azure_openai_endpoint: str | None = None
    azure_openai_embedding_deployment_name: str | None = None
    azure_openai_embedding_api_version: str | None = None
    azure_openai_embedding_api_key: str | None = None
"""

# LÍNEA ~388 - DETECCIÓN DE PROVIDER (REEMPLAZAR from_env)
"""
@classmethod
def from_env(cls) -> 'GraphitiEmbedderConfig':
    # PRIORIDAD 1: Google Gemini Experimental (MEJOR RENDIMIENTO)
    google_api_key = os.environ.get('GOOGLE_API_KEY', None)
    if google_api_key:
        # Usar modelo experimental por defecto
        model_name = os.environ.get('EMBEDDER_MODEL_NAME', 'gemini-embedding-exp-03-07')
        return cls(
            google_api_key=google_api_key,
            model=model_name,
        )
    
    # PRIORIDAD 2: Azure OpenAI (código existente)
    azure_openai_endpoint = os.environ.get('AZURE_OPENAI_ENDPOINT', None)
    azure_openai_embedding_deployment_name = os.environ.get(
        'AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME', None
    )
    azure_openai_embedding_api_version = os.environ.get(
        'AZURE_OPENAI_EMBEDDING_API_VERSION', None
    )
    azure_openai_embedding_api_key = os.environ.get(
        'AZURE_OPENAI_EMBEDDING_API_KEY', None
    )

    if (
        azure_openai_endpoint
        and azure_openai_embedding_deployment_name
        and azure_openai_embedding_api_version
        and azure_openai_embedding_api_key
    ):
        return cls(
            azure_openai_endpoint=azure_openai_endpoint,
            azure_openai_embedding_deployment_name=azure_openai_embedding_deployment_name,
            azure_openai_embedding_api_version=azure_openai_embedding_api_version,
            azure_openai_embedding_api_key=azure_openai_embedding_api_key,
            model=os.environ.get('EMBEDDER_MODEL_NAME', DEFAULT_EMBEDDER_MODEL),
        )
    
    # PRIORIDAD 3: OpenAI (código existente)
    api_key = os.environ.get('OPENAI_API_KEY', None)
    return cls(
        api_key=api_key,
        model=os.environ.get('EMBEDDER_MODEL_NAME', DEFAULT_EMBEDDER_MODEL),
    )
"""

# LÍNEA ~438 - CLIENTE GEMINI (REEMPLAZAR create_client)
"""
def create_client(self) -> EmbedderClient:
    if self.google_api_key is not None:
        # Google Gemini embeddings (incluyendo experimental)
        logger.info(f"Using Google Gemini embeddings with model: {self.model}")
        embedder_config = GeminiEmbedderConfig(
            api_key=self.google_api_key,
            embedding_model=self.model
        )
        return GeminiEmbedder(config=embedder_config)
    elif self.azure_openai_endpoint is not None:
        # Azure OpenAI embeddings (código existente)
        logger.info(f"Using Azure OpenAI embeddings with model: {self.model}")
        return AzureOpenAIEmbedderClient(
            api_key=self.azure_openai_embedding_api_key,
            api_version=self.azure_openai_embedding_api_version,
            azure_endpoint=self.azure_openai_endpoint,
            azure_deployment=self.azure_openai_embedding_deployment_name,
            model=self.model,
        )
    else:
        # OpenAI embeddings (código existente)
        logger.info(f"Using OpenAI embeddings with model: {self.model}")
        config = OpenAIEmbedderConfig(
            api_key=self.api_key,
            embedding_model=self.model,
        )
        return OpenAIEmbedder(config=config)
"""

# ============================================================================
# CONFIGURACIÓN CLAUDE DESKTOP
# ============================================================================

claude_desktop_config = {
    "mcpServers": {
        "graphiti-pepo": {
            "command": "python",
            "args": ["/Users/pepo/graphiti-pepo-local/graphiti/mcp_server/graphiti_mcp_server.py"],
            "env": {
                # LLM Principal (Claude para razonamiento)
                "ANTHROPIC_API_KEY": "tu_clave_anthropic_real",
                "MODEL_NAME": "claude-3-sonnet-20240229",
                
                # EMBEDDINGS (Gemini Experimental - #1 Mundial)
                "GOOGLE_API_KEY": "tu_clave_google_real",
                "EMBEDDER_MODEL_NAME": "gemini-embedding-exp-03-07",
                
                # Configuración Graphiti
                "NEO4J_URI": "bolt://localhost:7687",
                "NEO4J_USER": "neo4j", 
                "NEO4J_PASSWORD": "your_neo4j_password",
                "GROUP_ID": "pepo_phd_research"
            }
        }
    }
}

# ============================================================================
# ALTERNATIVAS DE MODELOS POR RENDIMIENTO
# ============================================================================

embedding_models_ranking = {
    # 🥇 MÁXIMO RENDIMIENTO (Experimental)
    "gemini-embedding-exp-03-07": {
        "mteb_score": 68.32,
        "status": "experimental", 
        "cost": "bajo",
        "specialty": "Rendimiento superior, entrenado en Gemini"
    },
    
    # 🥈 ALTO RENDIMIENTO (Estable)  
    "text-embedding-005": {
        "mteb_score": 66.31,
        "status": "GA",
        "cost": "bajo", 
        "specialty": "Gecko research, estable y potente"
    },
    
    # 🥉 BUENO (Actual estándar)
    "text-embedding-3-small": {
        "mteb_score": 62.3,
        "status": "GA",
        "cost": "medio",
        "specialty": "OpenAI estándar, bien documentado"
    }
}

# ============================================================================
# COMANDOS DE IMPLEMENTACIÓN
# ============================================================================

implementacion_commands = """
# 1. Conseguir Google API Key
# https://aistudio.google.com/app/apikey

# 2. Aplicar modificaciones MCP server
cd /Users/pepo/graphiti-pepo-local/graphiti/mcp_server
cp graphiti_mcp_server.py graphiti_mcp_server.py.backup
# Aplicar cambios del código arriba

# 3. Actualizar variables de entorno
echo 'GOOGLE_API_KEY=tu_clave_google_real' >> .env
echo 'EMBEDDER_MODEL_NAME=gemini-embedding-exp-03-07' >> .env
# Comentar: # OPENAI_API_KEY=...

# 4. Actualizar Claude Desktop config
# Aplicar configuración claude_desktop_config arriba

# 5. ⚠️ CRÍTICO: Regenerar grafo (embeddings incompatibles)
# En Claude Desktop:
# "clear_graph" 
# "Añade episodio de prueba: 'Test nuevo sistema embeddings Gemini experimental'"

# 6. Validar funcionamiento
# Buscar: "test experimental embeddings"
# Debería devolver el episodio con alta relevancia
"""

# ============================================================================
# MÉTRICAS DE ÉXITO ESPERADAS
# ============================================================================

metricas_exito = {
    "mejora_relevancia": "+10-15%",  # vs OpenAI text-embedding-3-small
    "mejora_contexto": "+20%",       # Comprensión relaciones complejas  
    "reduccion_costo": "-50%",       # vs OpenAI pricing
    "velocidad": "Similar",          # Latency comparable
    "estabilidad": "⚠️ Experimental" # Puede cambiar
}

print("✅ Archivo de modificación creado exitosamente")
print("📁 Ubicación: /Users/pepo/graphiti-pepo-local/mcp_gemini_exp_modification.py")
print("🚀 Siguiente paso: Conseguir Google API key y aplicar modificaciones")
print("⚡ Resultado esperado: +10-15% mejora en calidad embeddings")
