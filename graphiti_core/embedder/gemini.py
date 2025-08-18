"""
Copyright 2024, Zep Software, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from collections.abc import Iterable

from google import genai  # type: ignore
from google.genai import types  # type: ignore
from pydantic import Field

from .client import EmbedderClient, EmbedderConfig

DEFAULT_EMBEDDING_MODEL = 'embedding-001'


def detect_content_type(content: str) -> str:
    """
    Detectar si el contenido es código o texto regular para optimizar task_type
    
    Args:
        content: Texto a analizar
        
    Returns:
        "CODE_RETRIEVAL_QUERY" para contenido de código
        "RETRIEVAL_QUERY" para texto regular
    """
    if not content or not isinstance(content, str):
        return "RETRIEVAL_QUERY"
    
    # Indicadores de código Python
    python_indicators = [
        'def ', 'class ', 'import ', 'from ', 'return ',
        'if ', 'for ', 'while ', 'try:', 'except:', 'with ',
        '    ', '\t'  # Indentación típica de Python
    ]
    
    # Indicadores de código Cypher
    cypher_indicators = [
        'MATCH ', 'WHERE ', 'RETURN ', 'CREATE ', 'WITH ',
        'ORDER BY', 'LIMIT ', 'DISTINCT ', 'UNION ',
        '()-[', ']->(', '<-[', ']-', 'CALL '
    ]
    
    # Indicadores de otros lenguajes
    other_code_indicators = [
        'function ', 'const ', 'var ', 'let ', '=>',
        'SELECT ', 'FROM ', 'INSERT ', 'UPDATE ', 'DELETE ',
        '#include', 'public class', 'private ', 'protected '
    ]
    
    content_upper = content.upper()
    
    # Contar indicadores
    python_score = sum(1 for indicator in python_indicators if indicator in content)
    cypher_score = sum(1 for indicator in cypher_indicators if indicator in content_upper)
    other_score = sum(1 for indicator in other_code_indicators if indicator in content_upper)
    
    total_code_score = python_score + cypher_score + other_score
    
    # Si tiene 2 o más indicadores de código, clasificar como código
    if total_code_score >= 2:
        return "CODE_RETRIEVAL_QUERY"
    
    # Verificar patrones específicos que son claramente código
    code_patterns = [
        '```',  # Bloques de código markdown
        '{', '}',  # Llaves de programación
        'def ', 'function(',  # Definiciones de función
        'SELECT', 'MATCH',  # Queries de base de datos
    ]
    
    pattern_score = sum(1 for pattern in code_patterns if pattern in content_upper)
    if pattern_score >= 1:
        return "CODE_RETRIEVAL_QUERY"
    
    return "RETRIEVAL_QUERY"


class GeminiEmbedderConfig(EmbedderConfig):
    embedding_model: str = Field(default=DEFAULT_EMBEDDING_MODEL)
    api_key: str | None = None
    task_type: str | None = Field(
        default=None, 
        description="Task type for embeddings (e.g., 'CODE_RETRIEVAL_QUERY', 'RETRIEVAL_QUERY')"
    )


class GeminiEmbedder(EmbedderClient):
    """
    Google Gemini Embedder Client
    """

    def __init__(self, config: GeminiEmbedderConfig | None = None):
        if config is None:
            config = GeminiEmbedderConfig()
        self.config = config

        # Configure the Gemini API
        self.client = genai.Client(
            api_key=config.api_key,
        )

    async def create(
        self, input_data: str | list[str] | Iterable[int] | Iterable[Iterable[int]]
    ) -> list[float]:
        """
        Create embeddings for the given input data using Google's Gemini embedding model.
        Automatically detects content type and applies appropriate task_type optimization.

        Args:
            input_data: The input data to create embeddings for. Can be a string, list of strings,
                       or an iterable of integers or iterables of integers.

        Returns:
            A list of floats representing the embedding vector.
        """
        # Determinar task_type
        task_type = self.config.task_type
        if not task_type and isinstance(input_data, str):
            # Detección automática solo para strings
            task_type = detect_content_type(input_data)
        
        # Preparar configuración con task_type si está disponible
        embed_config = types.EmbedContentConfig(
            output_dimensionality=self.config.embedding_dim
        )
        
        if task_type:
            embed_config.task_type = task_type
        
        # Generate embeddings
        result = await self.client.aio.models.embed_content(
            model=self.config.embedding_model or DEFAULT_EMBEDDING_MODEL,
            contents=[input_data],  # type: ignore[arg-type]  # mypy fails on broad union type
            config=embed_config,
        )

        if not result.embeddings or len(result.embeddings) == 0 or not result.embeddings[0].values:
            raise ValueError('No embeddings returned from Gemini API in create()')

        return result.embeddings[0].values

    async def create_batch(self, input_data_list: list[str]) -> list[list[float]]:
        """Create embeddings for a batch of text inputs with task_type optimization."""
        
        # Para batch, usar task_type configurado o detectar del primer elemento
        task_type = self.config.task_type
        if not task_type and input_data_list:
            # Detectar del primer elemento como representativo
            task_type = detect_content_type(input_data_list[0])
        
        # Preparar configuración
        embed_config = types.EmbedContentConfig(
            output_dimensionality=self.config.embedding_dim
        )
        
        if task_type:
            embed_config.task_type = task_type
        
        # Generate embeddings
        result = await self.client.aio.models.embed_content(
            model=self.config.embedding_model or DEFAULT_EMBEDDING_MODEL,
            contents=input_data_list,  # type: ignore[arg-type]  # mypy fails on broad union type
            config=embed_config,
        )

        if not result.embeddings or len(result.embeddings) == 0:
            raise Exception('No embeddings returned')

        embeddings = []
        for embedding in result.embeddings:
            if not embedding.values:
                raise ValueError('Empty embedding values returned')
            embeddings.append(embedding.values)
        return embeddings
