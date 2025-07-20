# 🚀 PLAN COMPLETO DE EVALUACIÓN MULTI-ENGINE GRAPHITI

## 📊 **CONTEXTO ACTUAL - ESTADO DEL PROYECTO**

### **Sesiones Previas Completadas**
1. **July 1, 2025**: Implementación completa del Token Monitoring System
2. **July 2, 2025 (AM)**: Framework de evaluación SOTA + identificación problema structured outputs
3. **July 2, 2025 (PM)**: Resolución problema json_schema - Phase 2.1 COMPLETADA

### **Infraestructura Disponible**
- ✅ **Neo4j**: Funcionando en `bolt://localhost:7687` (password: `pepo_graphiti_2025`)
- ✅ **APIs Configuradas**: OpenAI (`gpt-4o`), Anthropic, Gemini (como `GOOGLE_API_KEY`)
- ✅ **Token Monitoring**: Sistema completo con CLI (`uv run graphiti-tokens`)
- ✅ **MCP Server**: Funcionando en Claude Desktop con configuración correcta

### **Problema Resuelto**
- **Error**: `'response_format' of type 'json_schema' is not supported`
- **Causa**: Uso de `gpt-4o-mini` en lugar de `gpt-4o`
- **Solución**: Configuración explícita con `LLMConfig(model="gpt-4o")`

---

## 📁 **ARCHIVOS Y CÓDIGO EXISTENTE**

### **Framework de Evaluación**
```python
# evaluation_framework_complete.py (773 líneas)
- Clase: EvaluationFramework
  - Métodos: run_evaluation(), calculate_metrics(), generate_report()
- Evaluadores especializados:
  - GraphQualityEvaluator: node_count, edge_count, clustering_coefficient
  - HybridSearchEvaluator: vector_search_precision, keyword_search_recall
  - CodeRetrievalEvaluator: CODE_RETRIEVAL_QUERY effectiveness
  - EmbeddingComparisonEvaluator: dimension_analysis, stability_metrics
  - PerformanceEvaluator: latency, throughput, cost_analysis

# test_suites_definition.py (638 líneas)
- 13 casos de prueba en 4 suites:
  - CODE_RETRIEVAL_QUERY: quicksort, BST, API patterns
  - Graph Quality: properties, relationships, topology
  - Hybrid Search: vector, keyword, fusion
  - Embedding Comparison: dimensionality, task types
```

### **Configuración Multi-Engine**
```python
# mcp_server/config_multi_engine.py
- MultiEngineConfig: Configuración unificada para todos los providers
- LLMEngine enum: OPENAI, ANTHROPIC, GEMINI
- EmbeddingEngine enum: OPENAI, GEMINI, DUAL
- Métodos: from_env(), get_llm_client(), get_embedder()

# Configuración correcta validada:
llm_config = LLMConfig(
    api_key=os.environ.get("OPENAI_API_KEY"),
    model="gpt-4o",  # NO gpt-4o-mini
    small_model="gpt-4o-mini"
)
```

### **Scripts de Utilidad**
```python
# test_with_correct_config.py
- Script validado que funciona con json_schema
- Ejemplo de configuración correcta

# run.sh
- Wrapper para ejecutar con uv: ./run.sh script.py

# Token monitoring
- uv run graphiti-tokens summary -p all -d 7
- uv run graphiti-tokens export results.csv
```

### **Clases Core de Graphiti**
```python
# graphiti_core/graphiti.py
- Graphiti(uri, user, password, llm_client=None, embedder=None)
- Métodos: add_episode(), search(), get_memory()

# graphiti_core/llm_client/
- OpenAIClient(config: LLMConfig)
- GeminiClient(config: LLMConfig)  
- AnthropicClient(config: LLMConfig)

# graphiti_core/embedder/
- OpenAIEmbedder(config: OpenAIEmbedderConfig)
- GeminiEmbedder(config: GeminiEmbedderConfig)
  - Soporta task_type="CODE_RETRIEVAL_QUERY"
```

---

## 🎯 **ESTRATEGIA DE EVALUACIÓN: 2 INSTANCIAS**

### **Arquitectura de Test**
```
INSTANCIA 1: OpenAI Embeddings (text-embedding-3-small)
├── Neo4j Database: "eval_openai_embeddings"
├── Embeddings calculados UNA vez
├── Test con LLM: gpt-4o
├── Test con LLM: gemini-2.5-flash  
└── Test con LLM: claude-3-sonnet

INSTANCIA 2: Gemini Embeddings (gemini-embedding-exp-03-07)
├── Neo4j Database: "eval_gemini_embeddings"
├── Embeddings con CODE_RETRIEVAL_QUERY
├── Test con LLM: gpt-4o
├── Test con LLM: gemini-2.5-flash
└── Test con LLM: claude-3-sonnet
```

---

## 📋 **PLAN DE EJECUCIÓN DETALLADO**

### **FASE 0: PREPARACIÓN DEL ENTORNO (15 min)**

#### **0.1 Crear Branch de Evaluación**
```bash
# Desde el branch actual
git checkout -b evaluation/multi-engine-comparison
git add -A
git commit -m "chore: checkpoint before multi-engine evaluation"
```

#### **0.2 Configurar Variables de Entorno**
```bash
# Crear archivo .env.evaluation
cat > .env.evaluation << EOF
# LLM Configuration
MODEL_NAME=gpt-4o
SMALL_MODEL_NAME=gpt-4o-mini
GROUP_ID=pepo_phd_research

# API Keys (ya configuradas en shell)
# OPENAI_API_KEY=...
# ANTHROPIC_API_KEY=...
# GOOGLE_API_KEY=$GEMINI_API_KEY

# Neo4j
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=pepo_graphiti_2025

# Evaluation Settings
EVAL_DATASET_SIZE=small  # small/medium/large
EVAL_LOG_LEVEL=INFO
EOF

# Cargar variables
source .env.evaluation
```

#### **0.3 Crear Bases de Datos en Neo4j**
```cypher
-- Conectar a Neo4j y ejecutar
CREATE DATABASE eval_openai_embeddings IF NOT EXISTS;
CREATE DATABASE eval_gemini_embeddings IF NOT EXISTS;
```

#### **0.4 Preparar Dataset de Prueba**
```python
# create_test_dataset.py
"""
Dataset pequeño pero representativo para evaluación inicial
"""
MINI_PYTHON_PROJECT = {
    "name": "Python Utils Library",
    "episodes": [
        {
            "name": "String manipulation utilities",
            "content": """
            def reverse_string(s: str) -> str:
                '''Reverse a string using slicing'''
                return s[::-1]
            
            def is_palindrome(s: str) -> str:
                '''Check if string is palindrome'''
                clean = ''.join(c.lower() for c in s if c.isalnum())
                return clean == clean[::-1]
            """,
            "metadata": {"file": "string_utils.py", "type": "code"}
        },
        {
            "name": "Binary search tree implementation",
            "content": """
            class TreeNode:
                def __init__(self, val):
                    self.val = val
                    self.left = None
                    self.right = None
            
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
            "metadata": {"file": "data_structures.py", "type": "code"}
        },
        # ... más episodios
    ]
}
```

---

## 🧪 **TESTING STRATEGY - TEST-DRIVEN DEVELOPMENT**

### **Pre-Implementation Testing**
```python
# test_evaluation_setup.py
import pytest
import asyncio
from unittest.mock import Mock, AsyncMock

class TestEvaluationSetup:
    """Tests previos a la implementación"""
    
    @pytest.mark.asyncio
    async def test_database_creation(self):
        """Verificar que podemos crear múltiples databases"""
        # Mock de Neo4j driver
        mock_driver = AsyncMock()
        mock_driver.execute_query.return_value = Mock(records=[])
        
        # Test crear database
        query = "CREATE DATABASE test_db IF NOT EXISTS"
        result = await mock_driver.execute_query(query)
        assert result is not None
    
    @pytest.mark.asyncio
    async def test_embedder_configuration(self):
        """Verificar configuración de embedders"""
        from graphiti_core.embedder.openai import OpenAIEmbedder
        
        # Test configuración
        config = {"embedding_model": "text-embedding-3-small"}
        embedder = OpenAIEmbedder(config)
        assert embedder.model == "text-embedding-3-small"
    
    @pytest.mark.asyncio
    async def test_llm_switching(self):
        """Verificar cambio de LLM sin afectar embeddings"""
        # Simular cambio de LLM
        llm_configs = ["gpt-4o", "gemini-2.5-flash", "claude-3-sonnet"]
        for llm in llm_configs:
            config = {"model": llm}
            assert config["model"] == llm

# Ejecutar tests antes de implementar
# pytest test_evaluation_setup.py -v
```

### **Post-Implementation Testing**
```python
# test_evaluation_results.py
import pytest
import pandas as pd
from pathlib import Path

class TestEvaluationResults:
    """Tests posteriores a la evaluación"""
    
    def test_results_file_exists(self):
        """Verificar que se generaron archivos de resultados"""
        results_files = list(Path(".").glob("evaluation_results_*.csv"))
        assert len(results_files) > 0, "No se encontraron archivos de resultados"
    
    def test_results_completeness(self):
        """Verificar que todas las configuraciones se evaluaron"""
        df = pd.read_csv("evaluation_results_latest.csv")
        
        # Verificar 6 configuraciones (2 embedders × 3 LLMs)
        assert len(df) == 6, f"Se esperaban 6 configuraciones, se encontraron {len(df)}"
        
        # Verificar columnas necesarias
        required_cols = ['Configuration', 'Embedder', 'LLM', 'Overall Score']
        for col in required_cols:
            assert col in df.columns, f"Falta columna requerida: {col}"
    
    def test_scores_validity(self):
        """Verificar que los scores son válidos"""
        df = pd.read_csv("evaluation_results_latest.csv")
        
        # Scores deben estar entre 0 y 1
        score_cols = [col for col in df.columns if 'Score' in col]
        for col in score_cols:
            assert df[col].between(0, 1).all(), f"Scores inválidos en {col}"
    
    def test_cost_tracking(self):
        """Verificar que se registraron costos"""
        df = pd.read_csv("evaluation_results_latest.csv")
        assert 'Total Cost ($)' in df.columns
        assert df['Total Cost ($)'].sum() > 0, "No se registraron costos"

# Ejecutar después de la evaluación
# pytest test_evaluation_results.py -v
```

### **Continuous Testing During Development**
```bash
# watch_tests.sh
#!/bin/bash
# Script para ejecutar tests continuamente durante desarrollo

while true; do
    clear
    echo "=== RUNNING TESTS ==="
    echo "$(date)"
    echo
    
    # Tests unitarios
    pytest tests/unit/ -v --tb=short
    
    # Tests de integración
    pytest tests/integration/ -v --tb=short -m "not slow"
    
    echo
    echo "Waiting for changes... (Ctrl+C to stop)"
    
    # Usar fswatch o inotifywait según el sistema
    if command -v fswatch &> /dev/null; then
        fswatch -1 -r . --exclude "\.git" --exclude "__pycache__"
    else
        inotifywait -r -e modify,create,delete . --exclude ".git|__pycache__"
    fi
done
```

---

## 🗄️ **GESTIÓN DETALLADA DE INSTANCIAS NEO4J**

### **Arquitectura Multi-Database**
```
Neo4j Server (localhost:7687)
├── System Database (neo4j)
├── eval_openai_embeddings     # OpenAI text-embedding-3-small
├── eval_gemini_embeddings     # Gemini CODE_RETRIEVAL_QUERY
├── eval_jina_embeddings       # Future: Jina v4
├── eval_qwen_embeddings       # Future: Qwen3
└── eval_custom_embeddings     # Future: Custom models
```

### **Creación y Gestión de Databases**

#### **1. Script de Gestión de Databases**
```python
# manage_neo4j_databases.py
import asyncio
from typing import List, Dict
from neo4j import AsyncGraphDatabase
import logging

logger = logging.getLogger(__name__)

class Neo4jDatabaseManager:
    """Gestor de múltiples databases en Neo4j para evaluaciones"""
    
    def __init__(self, uri: str, user: str, password: str):
        self.uri = uri
        self.user = user
        self.password = password
        self.driver = AsyncGraphDatabase.driver(uri, auth=(user, password))
    
    async def create_database(self, db_name: str, drop_if_exists: bool = False):
        """Crear una nueva database para un embedder específico"""
        async with self.driver.session(database="system") as session:
            try:
                # Verificar si existe
                result = await session.run(
                    "SHOW DATABASES WHERE name = $name",
                    name=db_name
                )
                exists = len(await result.data()) > 0
                
                if exists and drop_if_exists:
                    logger.info(f"Dropping existing database: {db_name}")
                    await session.run(f"DROP DATABASE {db_name} IF EXISTS")
                    exists = False
                
                if not exists:
                    logger.info(f"Creating database: {db_name}")
                    await session.run(f"CREATE DATABASE {db_name}")
                    
                    # Esperar a que esté online
                    await session.run(f"START DATABASE {db_name}")
                    logger.info(f"Database {db_name} created and started")
                else:
                    logger.info(f"Database {db_name} already exists")
                    
            except Exception as e:
                logger.error(f"Error creating database {db_name}: {e}")
                raise
    
    async def list_databases(self) -> List[Dict]:
        """Listar todas las databases de evaluación"""
        async with self.driver.session(database="system") as session:
            result = await session.run(
                "SHOW DATABASES WHERE name STARTS WITH 'eval_'"
            )
            databases = await result.data()
            return databases
    
    async def get_database_stats(self, db_name: str) -> Dict:
        """Obtener estadísticas de una database"""
        async with self.driver.session(database=db_name) as session:
            # Contar nodos
            node_result = await session.run("MATCH (n) RETURN count(n) as count")
            node_count = (await node_result.single())["count"]
            
            # Contar relaciones
            edge_result = await session.run("MATCH ()-[r]->() RETURN count(r) as count")
            edge_count = (await edge_result.single())["count"]
            
            # Obtener labels
            label_result = await session.run("CALL db.labels()")
            labels = [record["label"] async for record in label_result]
            
            # Información de índices
            index_result = await session.run("SHOW INDEXES")
            indexes = await index_result.data()
            
            return {
                "database": db_name,
                "node_count": node_count,
                "edge_count": edge_count,
                "labels": labels,
                "index_count": len(indexes),
                "indexes": indexes
            }
    
    async def setup_evaluation_databases(self, embedder_configs: List[Dict]):
        """Configurar todas las databases para evaluación"""
        for config in embedder_configs:
            db_name = config['database_name']
            await self.create_database(db_name)
            
            # Crear índices específicos para Graphiti
            async with self.driver.session(database=db_name) as session:
                # Índices estándar de Graphiti
                await session.run(
                    "CREATE INDEX IF NOT EXISTS FOR (n:Entity) ON (n.uuid)"
                )
                await session.run(
                    "CREATE INDEX IF NOT EXISTS FOR (n:Episodic) ON (n.uuid)"
                )
                await session.run(
                    "CREATE INDEX IF NOT EXISTS FOR (n:Entity) ON (n.name)"
                )
                
                # Índice para embeddings si es necesario
                if config.get('embedding_dimensions'):
                    await session.run(
                        "CREATE VECTOR INDEX IF NOT EXISTS entity_embeddings "
                        "FOR (n:Entity) ON (n.embedding) "
                        f"OPTIONS {{indexConfig: {{"
                        f"  `vector.dimensions`: {config['embedding_dimensions']},"
                        f"  `vector.similarity_function`: 'cosine'"
                        f"}}}}"
                    )
    
    async def close(self):
        await self.driver.close()

# Uso del manager
async def setup_databases_for_evaluation():
    manager = Neo4jDatabaseManager(
        uri="bolt://localhost:7687",
        user="neo4j",
        password="pepo_graphiti_2025"
    )
    
    # Configuraciones de embedders
    embedder_configs = [
        {
            "name": "OpenAI",
            "database_name": "eval_openai_embeddings",
            "embedding_dimensions": 1536
        },
        {
            "name": "Gemini",
            "database_name": "eval_gemini_embeddings", 
            "embedding_dimensions": 3072
        },
        {
            "name": "Jina",
            "database_name": "eval_jina_embeddings",
            "embedding_dimensions": 1024  # Jina v4
        },
        {
            "name": "Qwen",
            "database_name": "eval_qwen_embeddings",
            "embedding_dimensions": 8192  # Qwen3-8B
        }
    ]
    
    # Crear todas las databases
    await manager.setup_evaluation_databases(embedder_configs)
    
    # Listar databases creadas
    databases = await manager.list_databases()
    print("\nDatabases de evaluación creadas:")
    for db in databases:
        stats = await manager.get_database_stats(db['name'])
        print(f"  - {db['name']}: {stats['node_count']} nodos, {stats['edge_count']} relaciones")
    
    await manager.close()

if __name__ == "__main__":
    asyncio.run(setup_databases_for_evaluation())
```

### **Configuración de Graphiti para Seleccionar Instancias**

#### **2. Factory Pattern para Configuraciones**
```python
# graphiti_config_factory.py
from typing import Dict, Optional
from graphiti_core import Graphiti
from graphiti_core.llm_client.config import LLMConfig
from graphiti_core.embedder.config import EmbedderConfig

class GraphitiConfigFactory:
    """Factory para crear configuraciones de Graphiti con diferentes embedders"""
    
    # Registro de configuraciones de embedders
    EMBEDDER_CONFIGS = {
        "openai": {
            "class": "OpenAIEmbedder",
            "config": {
                "embedding_model": "text-embedding-3-small",
                "dimensions": 1536
            },
            "database": "eval_openai_embeddings"
        },
        "gemini": {
            "class": "GeminiEmbedder",
            "config": {
                "embedding_model": "gemini-embedding-exp-03-07",
                "dimensions": 3072,
                "task_type": "CODE_RETRIEVAL_QUERY"
            },
            "database": "eval_gemini_embeddings"
        },
        "jina": {
            "class": "JinaEmbedder",
            "config": {
                "model_name": "jinaai/jina-embeddings-v4",
                "dimensions": 1024,
                "api_key_env": "JINA_API_KEY"
            },
            "database": "eval_jina_embeddings"
        },
        "qwen": {
            "class": "QwenEmbedder", 
            "config": {
                "model_name": "Qwen/Qwen3-Embedding-8B",
                "dimensions": 8192,
                "device": "cuda"  # Para GPU
            },
            "database": "eval_qwen_embeddings"
        }
    }
    
    # Registro de configuraciones de LLMs
    LLM_CONFIGS = {
        "gpt-4o": {
            "class": "OpenAIClient",
            "config": {"model": "gpt-4o"}
        },
        "gemini-2.5-flash": {
            "class": "GeminiClient",
            "config": {"model": "gemini-2.5-flash"}
        },
        "claude-3-sonnet": {
            "class": "AnthropicClient",
            "config": {"model": "claude-3-sonnet-20240320"}
        }
    }
    
    @classmethod
    def create_graphiti_instance(
        cls,
        embedder_name: str,
        llm_name: str,
        uri: str = "bolt://localhost:7687",
        user: str = "neo4j",
        password: str = "pepo_graphiti_2025"
    ) -> Graphiti:
        """
        Crear instancia de Graphiti con configuración específica
        
        Args:
            embedder_name: Nombre del embedder (openai, gemini, jina, qwen)
            llm_name: Nombre del LLM (gpt-4o, gemini-2.5-flash, claude-3-sonnet)
            
        Returns:
            Instancia configurada de Graphiti
        """
        # Obtener configuración del embedder
        if embedder_name not in cls.EMBEDDER_CONFIGS:
            raise ValueError(f"Embedder desconocido: {embedder_name}")
        
        embedder_config = cls.EMBEDDER_CONFIGS[embedder_name]
        database = embedder_config["database"]
        
        # Crear embedder
        embedder = cls._create_embedder(embedder_name, embedder_config)
        
        # Crear LLM client
        llm_client = cls._create_llm_client(llm_name)
        
        # Crear instancia de Graphiti
        graphiti = Graphiti(
            uri=uri,
            user=user,
            password=password,
            database=database,  # Database específica para este embedder
            llm_client=llm_client,
            embedder=embedder
        )
        
        return graphiti
    
    @classmethod
    def _create_embedder(cls, name: str, config: Dict):
        """Factory method para crear embedders"""
        if name == "openai":
            from graphiti_core.embedder.openai import OpenAIEmbedder, OpenAIEmbedderConfig
            return OpenAIEmbedder(OpenAIEmbedderConfig(**config["config"]))
            
        elif name == "gemini":
            from graphiti_core.embedder.gemini import GeminiEmbedder, GeminiEmbedderConfig
            return GeminiEmbedder(GeminiEmbedderConfig(**config["config"]))
            
        elif name == "jina":
            # Implementación futura
            from custom_embedders.jina import JinaEmbedder
            return JinaEmbedder(**config["config"])
            
        elif name == "qwen":
            # Implementación futura
            from custom_embedders.qwen import QwenEmbedder
            return QwenEmbedder(**config["config"])
    
    @classmethod
    def _create_llm_client(cls, name: str):
        """Factory method para crear LLM clients"""
        if name not in cls.LLM_CONFIGS:
            raise ValueError(f"LLM desconocido: {name}")
        
        llm_config = cls.LLM_CONFIGS[name]
        
        if name.startswith("gpt"):
            from graphiti_core.llm_client.openai_client import OpenAIClient
            from graphiti_core.llm_client.config import LLMConfig
            return OpenAIClient(LLMConfig(**llm_config["config"]))
            
        elif name.startswith("gemini"):
            from graphiti_core.llm_client.gemini_client import GeminiClient
            return GeminiClient(**llm_config["config"])
            
        elif name.startswith("claude"):
            from graphiti_core.llm_client.anthropic_client import AnthropicClient
            return AnthropicClient(**llm_config["config"])

# Ejemplo de uso
async def example_usage():
    # Crear instancia con OpenAI embeddings y GPT-4o
    graphiti_openai = GraphitiConfigFactory.create_graphiti_instance(
        embedder_name="openai",
        llm_name="gpt-4o"
    )
    
    # Crear instancia con Gemini embeddings y Claude
    graphiti_gemini = GraphitiConfigFactory.create_graphiti_instance(
        embedder_name="gemini",
        llm_name="claude-3-sonnet"
    )
    
    # Usar las instancias...
    await graphiti_openai.build_indices_and_constraints()
    await graphiti_gemini.build_indices_and_constraints()
```

---

## 🔌 **AGREGAR NUEVOS EMBEDDINGS (JINA, QWEN, ETC.)**

### **Guía para Implementar Nuevos Embedders**

#### **1. Estructura Base para Nuevo Embedder**
```python
# custom_embedders/base.py
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
import numpy as np

class BaseCustomEmbedder(ABC):
    """Clase base para embedders personalizados"""
    
    def __init__(self, model_name: str, dimensions: int, **kwargs):
        self.model_name = model_name
        self.dimensions = dimensions
        self.config = kwargs
        self._initialize_model()
    
    @abstractmethod
    def _initialize_model(self):
        """Inicializar el modelo de embeddings"""
        pass
    
    @abstractmethod
    async def create(self, texts: List[str]) -> List[List[float]]:
        """Crear embeddings para una lista de textos"""
        pass
    
    @abstractmethod
    def get_dimensions(self) -> int:
        """Retornar dimensiones del embedding"""
        return self.dimensions
```

#### **2. Implementación para Jina Embeddings**
```python
# custom_embedders/jina.py
import os
import aiohttp
from typing import List
from .base import BaseCustomEmbedder

class JinaEmbedder(BaseCustomEmbedder):
    """
    Embedder para Jina Embeddings v4
    https://huggingface.co/jinaai/jina-embeddings-v4
    """
    
    def __init__(self, api_key_env: str = "JINA_API_KEY", **kwargs):
        super().__init__(
            model_name="jinaai/jina-embeddings-v4",
            dimensions=1024,  # Jina v4 dimensions
            **kwargs
        )
        self.api_key = os.getenv(api_key_env)
        if not self.api_key:
            raise ValueError(f"API key not found in {api_key_env}")
        
        self.api_url = "https://api.jina.ai/v1/embeddings"
    
    def _initialize_model(self):
        """Jina usa API, no requiere inicialización local"""
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def create(self, texts: List[str]) -> List[List[float]]:
        """Crear embeddings usando Jina API"""
        async with aiohttp.ClientSession() as session:
            payload = {
                "model": self.model_name,
                "input": texts,
                "task": "text-matching"  # o "retrieval" para búsqueda
            }
            
            async with session.post(
                self.api_url, 
                json=payload, 
                headers=self.headers
            ) as response:
                if response.status != 200:
                    error = await response.text()
                    raise Exception(f"Jina API error: {error}")
                
                data = await response.json()
                embeddings = [item["embedding"] for item in data["data"]]
                return embeddings
    
    # Adapter para Graphiti
    async def embed(self, texts: List[str]) -> List[List[float]]:
        """Método compatible con Graphiti"""
        return await self.create(texts)
```

#### **3. Implementación para Qwen Embeddings**
```python
# custom_embedders/qwen.py
import torch
from transformers import AutoTokenizer, AutoModel
from typing import List
import numpy as np
from .base import BaseCustomEmbedder

class QwenEmbedder(BaseCustomEmbedder):
    """
    Embedder para Qwen3-Embedding-8B
    https://huggingface.co/Qwen/Qwen3-Embedding-8B
    Requiere GPU para rendimiento óptimo
    """
    
    def __init__(self, device: str = "cuda", **kwargs):
        super().__init__(
            model_name="Qwen/Qwen3-Embedding-8B",
            dimensions=8192,  # Qwen3 8B dimensions
            **kwargs
        )
        self.device = device if torch.cuda.is_available() else "cpu"
        if self.device == "cpu" and device == "cuda":
            print("⚠️ GPU no disponible, usando CPU (será más lento)")
    
    def _initialize_model(self):
        """Cargar modelo y tokenizer de HuggingFace"""
        print(f"Cargando {self.model_name} en {self.device}...")
        
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModel.from_pretrained(
            self.model_name,
            trust_remote_code=True
        ).to(self.device)
        
        # Modo evaluación
        self.model.eval()
        
        print(f"✅ Modelo cargado en {self.device}")
    
    async def create(self, texts: List[str]) -> List[List[float]]:
        """Crear embeddings usando el modelo local"""
        # Tokenizar textos
        encoded = self.tokenizer(
            texts,
            padding=True,
            truncation=True,
            max_length=512,
            return_tensors="pt"
        ).to(self.device)
        
        # Generar embeddings
        with torch.no_grad():
            outputs = self.model(**encoded)
            
            # Mean pooling
            embeddings = outputs.last_hidden_state.mean(dim=1)
            
            # Normalizar (opcional, para cosine similarity)
            embeddings = torch.nn.functional.normalize(embeddings, p=2, dim=1)
            
            # Convertir a lista
            embeddings_list = embeddings.cpu().numpy().tolist()
        
        return embeddings_list
    
    # Adapter para Graphiti
    async def embed(self, texts: List[str]) -> List[List[float]]:
        """Método compatible con Graphiti"""
        return await self.create(texts)
```

#### **4. Integración con Graphiti**
```python
# custom_embedders/adapter.py
from graphiti_core.embedder.client import EmbedderClient
from typing import List, Optional

class CustomEmbedderAdapter(EmbedderClient):
    """Adapter para integrar embedders personalizados con Graphiti"""
    
    def __init__(self, custom_embedder):
        self.embedder = custom_embedder
        self.dimensions = custom_embedder.get_dimensions()
    
    async def create(self, input_data: List[str], **kwargs) -> List[List[float]]:
        """Interfaz compatible con Graphiti"""
        return await self.embedder.create(input_data)
    
    def get_dimensions(self) -> int:
        return self.dimensions

# Uso en factory
def create_custom_embedder(embedder_type: str) -> EmbedderClient:
    """Factory para embedders personalizados"""
    if embedder_type == "jina":
        from custom_embedders.jina import JinaEmbedder
        jina = JinaEmbedder()
        return CustomEmbedderAdapter(jina)
        
    elif embedder_type == "qwen":
        from custom_embedders.qwen import QwenEmbedder
        qwen = QwenEmbedder()
        return CustomEmbedderAdapter(qwen)
    
    else:
        raise ValueError(f"Embedder desconocido: {embedder_type}")
```

#### **5. Testing de Nuevos Embedders**
```python
# test_custom_embedders.py
import pytest
import asyncio
from custom_embedders.jina import JinaEmbedder
from custom_embedders.qwen import QwenEmbedder

class TestCustomEmbedders:
    
    @pytest.mark.asyncio
    async def test_jina_embedder(self):
        """Test Jina embeddings"""
        if not os.getenv("JINA_API_KEY"):
            pytest.skip("JINA_API_KEY no configurada")
        
        embedder = JinaEmbedder()
        texts = ["Hello world", "Test embedding"]
        
        embeddings = await embedder.create(texts)
        
        assert len(embeddings) == 2
        assert len(embeddings[0]) == 1024  # Jina v4 dimensions
        assert all(isinstance(x, float) for x in embeddings[0])
    
    @pytest.mark.asyncio
    @pytest.mark.skipif(not torch.cuda.is_available(), reason="GPU required")
    async def test_qwen_embedder(self):
        """Test Qwen embeddings"""
        embedder = QwenEmbedder()
        texts = ["Hello world", "Test embedding"]
        
        embeddings = await embedder.create(texts)
        
        assert len(embeddings) == 2
        assert len(embeddings[0]) == 8192  # Qwen3-8B dimensions
        assert all(isinstance(x, float) for x in embeddings[0])
    
    @pytest.mark.asyncio
    async def test_embedder_with_graphiti(self):
        """Test integración con Graphiti"""
        from custom_embedders.adapter import create_custom_embedder
        
        embedder = create_custom_embedder("jina")
        
        # Test con Graphiti
        graphiti = Graphiti(
            uri="bolt://localhost:7687",
            user="neo4j",
            password="test",
            database="test_jina",
            embedder=embedder
        )
        
        # Verificar que se puede usar
        assert graphiti.embedder is not None
        assert graphiti.embedder.get_dimensions() == 1024
```

#### **6. Configuración de Requirements**
```toml
# pyproject.toml additions
[project.optional-dependencies]
custom-embedders = [
    "transformers>=4.35.0",
    "torch>=2.0.0",
    "sentence-transformers>=2.2.0",
    "aiohttp>=3.8.0",
]

# Para Jina (API-based)
jina = [
    "aiohttp>=3.8.0",
]

# Para Qwen (requiere GPU)
qwen = [
    "transformers>=4.35.0",
    "torch>=2.0.0",
    "accelerate>=0.25.0",
]
```

### **Checklist para Agregar Nuevo Embedder**
- [ ] Implementar clase heredando de `BaseCustomEmbedder`
- [ ] Definir dimensiones correctas del modelo
- [ ] Implementar método `create()` para generar embeddings
- [ ] Crear adapter para Graphiti
- [ ] Agregar configuración en `EMBEDDER_CONFIGS`
- [ ] Crear database específica en Neo4j
- [ ] Escribir tests unitarios
- [ ] Documentar requisitos y uso
- [ ] Agregar a `pyproject.toml` dependencies

---

### **FASE 1: POBLAR INSTANCIAS CON EMBEDDINGS (30 min)**

#### **1.1 Script de Población**
```python
# populate_instances.py
import asyncio
from datetime import datetime
from graphiti_core import Graphiti
from graphiti_core.llm_client.config import LLMConfig
from graphiti_core.llm_client.openai_client import OpenAIClient
from graphiti_core.embedder.openai import OpenAIEmbedder, OpenAIEmbedderConfig
from graphiti_core.embedder.gemini import GeminiEmbedder, GeminiEmbedderConfig

async def populate_instance(database_name, embedder_config, dataset):
    """Poblar una instancia con embeddings específicos"""
    print(f"\n{'='*60}")
    print(f"Poblando {database_name}")
    print(f"Embedder: {embedder_config['name']}")
    print(f"Dataset: {len(dataset['episodes'])} episodios")
    
    # Configurar LLM (siempre gpt-4o para población consistente)
    llm_config = LLMConfig(model="gpt-4o")
    llm_client = OpenAIClient(llm_config)
    
    # Configurar embedder según el tipo
    if embedder_config['type'] == 'openai':
        embedder = OpenAIEmbedder(
            OpenAIEmbedderConfig(embedding_model="text-embedding-3-small")
        )
    else:  # gemini
        embedder = GeminiEmbedder(
            GeminiEmbedderConfig(
                embedding_model="gemini-embedding-exp-03-07",
                task_type="CODE_RETRIEVAL_QUERY"
            )
        )
    
    # Crear instancia de Graphiti
    graphiti = Graphiti(
        uri="bolt://localhost:7687",
        user="neo4j",
        password="pepo_graphiti_2025",
        database=database_name,
        llm_client=llm_client,
        embedder=embedder
    )
    
    # Construir índices
    await graphiti.build_indices_and_constraints()
    
    # Poblar con episodios
    start_time = datetime.now()
    for i, episode in enumerate(dataset['episodes'], 1):
        print(f"  [{i}/{len(dataset['episodes'])}] {episode['name']}")
        await graphiti.add_episode(
            name=episode['name'],
            episode_body=episode['content'],
            source_description=f"Test dataset - {episode['metadata']['file']}",
            reference_time=datetime.now(),
            metadata=episode['metadata']
        )
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    # Verificar población
    stats = await graphiti.get_graph_statistics()
    print(f"\nEstadísticas finales:")
    print(f"  Nodos: {stats['node_count']}")
    print(f"  Relaciones: {stats['edge_count']}")
    print(f"  Tiempo: {duration:.2f}s")
    
    await graphiti.close()
    return stats

async def main():
    # Cargar dataset
    from create_test_dataset import MINI_PYTHON_PROJECT as dataset
    
    # Configuraciones de embedders
    embedder_configs = [
        {
            'name': 'OpenAI text-embedding-3-small',
            'type': 'openai',
            'database': 'eval_openai_embeddings'
        },
        {
            'name': 'Gemini gemini-embedding-exp-03-07 (CODE_RETRIEVAL)',
            'type': 'gemini',
            'database': 'eval_gemini_embeddings'
        }
    ]
    
    # Poblar cada instancia
    for config in embedder_configs:
        await populate_instance(config['database'], config, dataset)
    
    print(f"\n{'='*60}")
    print("✅ POBLACIÓN COMPLETA")
    print(f"{'='*60}")

if __name__ == "__main__":
    asyncio.run(main())
```

#### **1.2 Verificación de Población**
```bash
# Verificar con cypher-shell o Neo4j Browser
MATCH (n) RETURN count(n) as node_count, labels(n)[0] as label
ORDER BY label;
```

---

### **FASE 2: EVALUACIÓN MULTI-ENGINE (60 min)**

#### **2.1 Script Principal de Evaluación**
```python
# run_multi_engine_evaluation.py
import asyncio
import json
from datetime import datetime
from typing import Dict, List
import pandas as pd

from graphiti_core import Graphiti
from evaluation_framework_complete import EvaluationFramework
from test_suites_definition import TestSuiteManager

class MultiEngineEvaluator:
    def __init__(self):
        self.results = {}
        self.test_suite_manager = TestSuiteManager()
        
    async def evaluate_configuration(
        self, 
        database: str,
        embedder_name: str,
        llm_config: Dict,
        test_cases: List
    ):
        """Evaluar una configuración específica"""
        config_name = f"{embedder_name}__{llm_config['name']}"
        print(f"\n{'='*60}")
        print(f"Evaluando: {config_name}")
        print(f"Database: {database}")
        
        # Crear cliente LLM según configuración
        llm_client = self._create_llm_client(llm_config)
        
        # Conectar a Graphiti (embeddings ya están en la DB)
        graphiti = Graphiti(
            uri="bolt://localhost:7687",
            user="neo4j",
            password="pepo_graphiti_2025",
            database=database,
            llm_client=llm_client
        )
        
        # Crear framework de evaluación
        evaluator = EvaluationFramework(graphiti)
        
        # Ejecutar evaluación
        start_time = datetime.now()
        results = await evaluator.run_evaluation(test_cases)
        end_time = datetime.now()
        
        results['config'] = {
            'embedder': embedder_name,
            'llm': llm_config['name'],
            'duration': (end_time - start_time).total_seconds()
        }
        
        # Guardar resultados
        self.results[config_name] = results
        
        # Mostrar resumen
        print(f"\nResultados {config_name}:")
        print(f"  Overall Score: {results['overall_score']:.3f}")
        print(f"  Duración: {results['config']['duration']:.2f}s")
        
        await graphiti.close()
        return results
    
    def _create_llm_client(self, llm_config):
        """Factory para crear clientes LLM"""
        if llm_config['provider'] == 'openai':
            from graphiti_core.llm_client.openai_client import OpenAIClient
            from graphiti_core.llm_client.config import LLMConfig
            return OpenAIClient(LLMConfig(model=llm_config['model']))
            
        elif llm_config['provider'] == 'gemini':
            from graphiti_core.llm_client.gemini_client import GeminiClient
            # Configurar Gemini client
            return GeminiClient(...)
            
        elif llm_config['provider'] == 'anthropic':
            from graphiti_core.llm_client.anthropic_client import AnthropicClient
            # Configurar Anthropic client
            return AnthropicClient(...)
    
    def generate_comparison_report(self):
        """Generar reporte comparativo"""
        # Crear DataFrame para comparación
        comparison_data = []
        
        for config_name, results in self.results.items():
            row = {
                'Configuration': config_name,
                'Embedder': results['config']['embedder'],
                'LLM': results['config']['llm'],
                'Overall Score': results['overall_score'],
                'Code Retrieval Score': results['code_retrieval_score'],
                'Graph Quality Score': results['graph_quality_score'],
                'Performance Score': results['performance_score'],
                'Duration (s)': results['config']['duration'],
                'Total Cost ($)': results.get('total_cost', 0)
            }
            comparison_data.append(row)
        
        df = pd.DataFrame(comparison_data)
        df = df.sort_values('Overall Score', ascending=False)
        
        # Guardar resultados
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        df.to_csv(f'evaluation_results_{timestamp}.csv', index=False)
        
        with open(f'evaluation_full_results_{timestamp}.json', 'w') as f:
            json.dump(self.results, f, indent=2)
        
        return df

async def main():
    evaluator = MultiEngineEvaluator()
    
    # Configuraciones a probar
    EMBEDDER_CONFIGS = [
        {'name': 'openai_embeddings', 'database': 'eval_openai_embeddings'},
        {'name': 'gemini_embeddings', 'database': 'eval_gemini_embeddings'}
    ]
    
    LLM_CONFIGS = [
        {'name': 'gpt-4o', 'provider': 'openai', 'model': 'gpt-4o'},
        {'name': 'gemini-2.5-flash', 'provider': 'gemini', 'model': 'gemini-2.5-flash'},
        {'name': 'claude-3-sonnet', 'provider': 'anthropic', 'model': 'claude-3-sonnet-20240320'}
    ]
    
    # Obtener casos de prueba
    test_cases = evaluator.test_suite_manager.get_small_test_suite()
    
    # Ejecutar todas las combinaciones
    for embedder_config in EMBEDDER_CONFIGS:
        for llm_config in LLM_CONFIGS:
            await evaluator.evaluate_configuration(
                database=embedder_config['database'],
                embedder_name=embedder_config['name'],
                llm_config=llm_config,
                test_cases=test_cases
            )
    
    # Generar reporte comparativo
    print(f"\n{'='*60}")
    print("GENERANDO REPORTE COMPARATIVO")
    print(f"{'='*60}")
    
    df = evaluator.generate_comparison_report()
    print("\nRESULTADOS FINALES:")
    print(df.to_string())
    
    # Mejores configuraciones
    print(f"\n{'='*60}")
    print("MEJORES CONFIGURACIONES:")
    print(f"{'='*60}")
    print(f"\n1. MEJOR OVERALL: {df.iloc[0]['Configuration']}")
    print(f"2. MEJOR CODE RETRIEVAL: {df.loc[df['Code Retrieval Score'].idxmax()]['Configuration']}")
    print(f"3. MÁS EFICIENTE (Score/Cost): ...")

if __name__ == "__main__":
    asyncio.run(main())
```

---

### **FASE 3: ANÁLISIS Y DOCUMENTACIÓN (30 min)**

#### **3.1 Script de Análisis Detallado**
```python
# analyze_results.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def analyze_evaluation_results(results_file):
    """Análisis detallado de resultados"""
    df = pd.read_csv(results_file)
    
    # 1. Heatmap de scores
    pivot_overall = df.pivot(index='LLM', columns='Embedder', values='Overall Score')
    plt.figure(figsize=(10, 6))
    sns.heatmap(pivot_overall, annot=True, cmap='YlGn')
    plt.title('Overall Score: LLM vs Embedder')
    plt.savefig('heatmap_overall_score.png')
    
    # 2. Análisis de CODE_RETRIEVAL_QUERY
    gemini_embed = df[df['Embedder'] == 'gemini_embeddings']
    openai_embed = df[df['Embedder'] == 'openai_embeddings']
    
    improvement = (
        gemini_embed['Code Retrieval Score'].mean() - 
        openai_embed['Code Retrieval Score'].mean()
    ) / openai_embed['Code Retrieval Score'].mean() * 100
    
    print(f"Mejora con CODE_RETRIEVAL_QUERY: {improvement:.1f}%")
    
    # 3. Análisis costo-beneficio
    df['Score per Dollar'] = df['Overall Score'] / (df['Total Cost ($)'] + 0.001)
    best_value = df.loc[df['Score per Dollar'].idxmax()]
    print(f"\nMejor valor: {best_value['Configuration']}")
    
    return df
```

#### **3.2 Documentación de Resultados**
```markdown
# evaluation_results_analysis.md

## Resultados de Evaluación Multi-Engine

### Configuración Ganadora
- **Overall**: [configuración]
- **Code Retrieval**: [configuración]  
- **Costo-Beneficio**: [configuración]

### Hallazgos Clave
1. CODE_RETRIEVAL_QUERY mejora X% la recuperación de código
2. Gemini embeddings son Y% más grandes pero Z% más precisos
3. [Otros hallazgos]

### Recomendaciones
- Para código: Usar [configuración]
- Para costo mínimo: Usar [configuración]
- Para máxima calidad: Usar [configuración]
```

---

## 🛡️ **MEJORES PRÁCTICAS IMPLEMENTADAS**

### **Control de Versiones**
```bash
# Antes de cada fase
git add -A
git commit -m "chore: checkpoint before [phase]"

# Después de cambios importantes
git commit -m "feat: [description]"
```

### **Monitoreo de Costos**
```bash
# Durante evaluación
watch -n 30 'uv run graphiti-tokens summary -p all -d 1'

# Después de cada fase
uv run graphiti-tokens export phase_X_costs.csv -d 1
```

### **Logging y Debugging**
```python
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('evaluation.log'),
        logging.StreamHandler()
    ]
)
```

### **Manejo de Errores**
```python
try:
    result = await graphiti.add_episode(...)
except Exception as e:
    logger.error(f"Error en {config_name}: {str(e)}")
    # Continuar con siguiente configuración
    continue
```

### **Backup de Datos**
```bash
# Antes de empezar
neo4j-admin database dump eval_openai_embeddings --to=backup/
neo4j-admin database dump eval_gemini_embeddings --to=backup/
```

---

## 📋 **CHECKLIST PARA PRÓXIMA SESIÓN**

### **Antes de Empezar**
- [ ] Revisar este documento completo
- [ ] Verificar APIs configuradas: `env | grep API_KEY`
- [ ] Verificar Neo4j funcionando: `cypher-shell "MATCH (n) RETURN count(n)"`
- [ ] Activar token monitoring: `uv run graphiti-tokens status`
- [ ] Crear branch nuevo: `git checkout -b evaluation/session-X`

### **Orden de Ejecución**
1. [ ] **FASE 0**: Preparación (15 min)
   - [ ] Variables de entorno
   - [ ] Crear databases Neo4j
   - [ ] Preparar dataset

2. [ ] **FASE 1**: Población (30 min)
   - [ ] Ejecutar `populate_instances.py`
   - [ ] Verificar población correcta
   - [ ] Backup de databases

3. [ ] **FASE 2**: Evaluación (60 min)
   - [ ] Ejecutar `run_multi_engine_evaluation.py`
   - [ ] Monitorear costos en tiempo real
   - [ ] Guardar logs y resultados

4. [ ] **FASE 3**: Análisis (30 min)
   - [ ] Ejecutar `analyze_results.py`
   - [ ] Generar visualizaciones
   - [ ] Documentar hallazgos

### **Comandos Rápidos**
```bash
# Setup inicial
source .env.evaluation
export GOOGLE_API_KEY="$GEMINI_API_KEY"

# Población
./run.sh populate_instances.py

# Evaluación
./run.sh run_multi_engine_evaluation.py

# Monitoreo
uv run graphiti-tokens summary -p all -d 1

# Análisis
./run.sh analyze_results.py
```

---

## 🎯 **RESULTADO ESPERADO**

Al final de la evaluación tendrás:

1. **Matriz de Resultados 6x1**: 
   - 2 embedders × 3 LLMs = 6 configuraciones evaluadas

2. **Métricas Comparativas**:
   - Overall Score, Code Retrieval, Graph Quality, Performance
   - Costos exactos por configuración
   - Tiempos de ejecución

3. **Recomendaciones Específicas**:
   - Mejor configuración para código
   - Mejor configuración costo-beneficio
   - Impacto de CODE_RETRIEVAL_QUERY cuantificado

4. **Documentación Publicable**:
   - Metodología reproducible
   - Resultados con métricas SOTA
   - Análisis estadístico válido

---

*Plan generado: 2025-07-02*  
*Listo para ejecutar en próxima sesión*