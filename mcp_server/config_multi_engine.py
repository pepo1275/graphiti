# =====================================
# MULTI-ENGINE CONFIGURATION CLASSES
# =====================================

from enum import Enum
from typing import Literal, Union
from pydantic import BaseModel, Field
import os

class LLMEngine(str, Enum):
    """Available LLM engines."""
    OPENAI = "openai"
    ANTHROPIC = "anthropic" 
    GEMINI = "gemini"
    AZURE_OPENAI = "azure_openai"

class EmbeddingEngine(str, Enum):
    """Available embedding engines."""
    OPENAI = "openai"
    VERTEX_AI = "vertex_ai"
    GEMINI = "gemini"
    AZURE_OPENAI = "azure_openai"
    DUAL = "dual"  # Uses two engines for comparison

class DualEngineStrategy(str, Enum):
    """Strategies for dual-engine operation."""
    PRIMARY = "primary"          # Use primary, fallback on failure
    FALLBACK = "fallback"        # Same as primary but with detailed logging
    COMPARISON = "comparison"    # Use both engines and compare results  
    ROUND_ROBIN = "round_robin"  # Alternate between engines

class MultiEngineConfig(BaseModel):
    """Comprehensive configuration for multi-engine system."""
    
    # LLM Configuration
    llm_engine: LLMEngine = LLMEngine.GEMINI
    model_name: str = "gemini-2.5-flash"
    small_model_name: str = "gemini-2.5-flash"
    llm_temperature: float = 0.0
    
    # Embedding Configuration
    embedding_engine: EmbeddingEngine = EmbeddingEngine.DUAL
    embedder_model_name: str = "text-embedding-005"
    secondary_embedder_model_name: str = "gemini-embedding-exp-03-07"
    
    # Dual Engine Settings
    dual_engine_strategy: DualEngineStrategy = DualEngineStrategy.COMPARISON
    enable_task_type_optimization: bool = True
    
    # API Keys
    openai_api_key: str | None = None
    anthropic_api_key: str | None = None
    google_api_key: str | None = None
    
    # Google Cloud (Vertex AI)
    google_application_credentials: str | None = None
    google_cloud_project: str | None = None
    google_cloud_location: str = "us-central1"
    
    # Azure OpenAI
    azure_openai_endpoint: str | None = None
    azure_openai_api_version: str | None = None
    azure_openai_deployment_name: str | None = None
    azure_openai_use_managed_identity: bool = False
    
    # Performance Settings
    embedding_timeout_seconds: int = 30
    enable_embedding_caching: bool = True
    max_concurrent_embeddings: int = 5
    semaphore_limit: int = 10
    
    # General Settings
    group_id: str = "pepo_phd_research"
    log_level: str = "INFO"

    @classmethod
    def from_env(cls) -> 'MultiEngineConfig':
        """Create configuration from environment variables."""
        return cls(
            # LLM Configuration
            llm_engine=LLMEngine(os.environ.get('LLM_ENGINE', 'gemini')),
            model_name=os.environ.get('MODEL_NAME', 'gemini-2.5-flash'),
            small_model_name=os.environ.get('SMALL_MODEL_NAME', 'gemini-2.5-flash'),
            llm_temperature=float(os.environ.get('LLM_TEMPERATURE', '0.0')),
            
            # Embedding Configuration  
            embedding_engine=EmbeddingEngine(os.environ.get('EMBEDDING_ENGINE', 'dual')),
            embedder_model_name=os.environ.get('EMBEDDER_MODEL_NAME', 'text-embedding-005'),
            secondary_embedder_model_name=os.environ.get('SECONDARY_EMBEDDER_MODEL_NAME', 'gemini-embedding-exp-03-07'),
            
            # Dual Engine Settings
            dual_engine_strategy=DualEngineStrategy(os.environ.get('DUAL_ENGINE_STRATEGY', 'comparison')),
            enable_task_type_optimization=os.environ.get('ENABLE_TASK_TYPE_OPTIMIZATION', 'true').lower() == 'true',
            
            # API Keys
            openai_api_key=os.environ.get('OPENAI_API_KEY'),
            anthropic_api_key=os.environ.get('ANTHROPIC_API_KEY'),
            google_api_key=os.environ.get('GOOGLE_API_KEY'),
            
            # Google Cloud
            google_application_credentials=os.environ.get('GOOGLE_APPLICATION_CREDENTIALS'),
            google_cloud_project=os.environ.get('GOOGLE_CLOUD_PROJECT'),
            google_cloud_location=os.environ.get('GOOGLE_CLOUD_LOCATION', 'us-central1'),
            
            # Azure OpenAI
            azure_openai_endpoint=os.environ.get('AZURE_OPENAI_ENDPOINT'),
            azure_openai_api_version=os.environ.get('AZURE_OPENAI_API_VERSION'),
            azure_openai_deployment_name=os.environ.get('AZURE_OPENAI_DEPLOYMENT_NAME'),
            azure_openai_use_managed_identity=os.environ.get('AZURE_OPENAI_USE_MANAGED_IDENTITY', 'false').lower() == 'true',
            
            # Performance Settings
            embedding_timeout_seconds=int(os.environ.get('EMBEDDING_TIMEOUT_SECONDS', '30')),
            enable_embedding_caching=os.environ.get('ENABLE_EMBEDDING_CACHING', 'true').lower() == 'true',
            max_concurrent_embeddings=int(os.environ.get('MAX_CONCURRENT_EMBEDDINGS', '5')),
            semaphore_limit=int(os.environ.get('SEMAPHORE_LIMIT', '10')),
            
            # General Settings  
            group_id=os.environ.get('GROUP_ID', 'pepo_phd_research'),
            log_level=os.environ.get('LOG_LEVEL', 'INFO')
        )

# =====================================
# MODEL DEFINITIONS
# =====================================

AVAILABLE_MODELS = {
    LLMEngine.OPENAI: [
        "gpt-4o",
        "gpt-4o-mini", 
        "gpt-4-turbo",
        "gpt-3.5-turbo"
    ],
    LLMEngine.ANTHROPIC: [
        "claude-opus-4-20250514",
        "claude-sonnet-4-20250514",
        "claude-3-5-sonnet-20241022", 
        "claude-3-haiku-20240307"
    ],
    LLMEngine.GEMINI: [
        "gemini-2.5-pro",
        "gemini-2.5-flash",
        "gemini-2.0-flash",
        "gemini-1.5-pro",
        "gemini-1.5-flash"
    ],
    LLMEngine.AZURE_OPENAI: [
        # Deployment names configured in Azure
        "custom-deployment-name"
    ]
}

AVAILABLE_EMBEDDING_MODELS = {
    EmbeddingEngine.OPENAI: [
        "text-embedding-3-small",
        "text-embedding-3-large", 
        "text-embedding-ada-002"
    ],
    EmbeddingEngine.VERTEX_AI: [
        "text-embedding-005",
        "text-embedding-004"
    ],
    EmbeddingEngine.GEMINI: [
        "gemini-embedding-exp-03-07",
        "text-embedding-004"
    ],
    EmbeddingEngine.AZURE_OPENAI: [
        # Deployment names configured in Azure
        "custom-embedding-deployment"
    ]
}

def validate_model_compatibility(engine: LLMEngine, model: str) -> bool:
    """Validate if a model is compatible with the selected engine."""
    return model in AVAILABLE_MODELS.get(engine, [])

def validate_embedding_compatibility(engine: EmbeddingEngine, model: str) -> bool:
    """Validate if an embedding model is compatible with the selected engine."""
    return model in AVAILABLE_EMBEDDING_MODELS.get(engine, [])
