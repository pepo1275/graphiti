# Modificaciones necesarias para agregar Gemini embeddings al MCP server

# 1. Agregar imports (línea ~25 en graphiti_mcp_server.py)
from graphiti_core.embedder.gemini import GeminiEmbedder, GeminiEmbedderConfig

# 2. Agregar campo a GraphitiEmbedderConfig (línea ~380)
class GraphitiEmbedderConfig(BaseModel):
    model: str = DEFAULT_EMBEDDER_MODEL
    api_key: str | None = None
    google_api_key: str | None = None  # ← NUEVO
    azure_openai_endpoint: str | None = None
    # ... resto igual

# 3. Modificar from_env() para detectar Google (línea ~388)
@classmethod
def from_env(cls) -> 'GraphitiEmbedderConfig':
    # Detectar Google API key
    google_api_key = os.environ.get('GOOGLE_API_KEY', None)
    
    if google_api_key:
        # Usar Gemini embeddings
        model = os.environ.get('EMBEDDER_MODEL_NAME', 'embedding-001')
        return cls(
            google_api_key=google_api_key,
            model=model,
        )
    
    # Resto de lógica existente...

# 4. Modificar create_client() para soportar Gemini (línea ~438)
def create_client(self) -> EmbedderClient:
    if self.google_api_key is not None:
        # Google Gemini setup
        embedder_config = GeminiEmbedderConfig(
            api_key=self.google_api_key,
            embedding_model=self.model
        )
        return GeminiEmbedder(config=embedder_config)
    
    # Resto de lógica existente (Azure, OpenAI)...

# 5. Variables de entorno necesarias
"""
# .env file
GOOGLE_API_KEY=tu_clave_google_aqui
EMBEDDER_MODEL_NAME=embedding-001
"""

# 6. Claude Desktop config
"""
"env": {
  "ANTHROPIC_API_KEY": "sk-ant-...",
  "GOOGLE_API_KEY": "tu_clave_google",
  "EMBEDDER_MODEL_NAME": "embedding-001",
  // ... resto igual
}
"""
