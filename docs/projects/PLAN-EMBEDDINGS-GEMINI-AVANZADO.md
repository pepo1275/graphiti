# Plan: Embeddings Gemini Avanzado con Task Types y 3072D

**Estado**: Propuesta para revisión
**Autor**: Pepo + Claude
**Fecha**: 2026-01-31
**Contexto**: Fork está 40 commits detrás de upstream

---

## 0. Decisión Previa Crítica: ¿Sincronizar con Upstream Primero?

### Estado Actual del Fork

```
Tu fork (pepo1275/graphiti):  6c9824b (hace ~40 commits)
                              |
Upstream (getzep/graphiti):   c36723c (actual)
```

**Cambios relevantes en upstream que NO tienes:**
- Refactorización de prompts (#1191)
- Sagas para gestión de episodios (#1149)
- Adaptive chunking para inputs grandes (#1129)
- Graph Operations Interface (#1172)
- Edge extraction efficiency (#1140)
- Custom prompts (#1122)
- Triplet update (#1115)

### Opciones de Sincronización

| Opción | Descripción | Riesgo | Esfuerzo |
|--------|-------------|--------|----------|
| **A. Sync primero** | Merge upstream -> main, luego implementar embeddings | Bajo | 2-4h |
| **B. Implementar en fork actual** | Hacer cambios de embeddings ahora, merge después | Alto (conflictos) | Variable |
| **C. Feature branch desde upstream** | Crear branch desde upstream/main, implementar ahí | Bajo | 1h setup |

**Mi recomendación**: Opción C - Crear feature branch desde upstream actualizado.

```bash
# Opción C - Workflow recomendado
git checkout main
git merge upstream/main  # Sincronizar main
git checkout -b feature/gemini-embeddings-enhanced
# Implementar cambios
```

---

## 1. Resumen Ejecutivo

Este plan implementa soporte completo para las características avanzadas de Gemini Embeddings:

1. **Task Types** - Optimización semántica por caso de uso
2. **Dimensión 3072** - Máxima calidad de embeddings
3. **Normalización** - Fix del bug actual
4. **Reprocesamiento** - Migrar embeddings existentes a 3072D
5. **Campos duales** (opcional) - Para experimentación A/B

---

## 2. Características de Gemini Embedding API que NO usamos

### 2.1 Task Types Disponibles

| Task Type | Uso Óptimo | Usamos? |
|-----------|------------|---------|
| `RETRIEVAL_QUERY` | Queries de búsqueda | NO |
| `RETRIEVAL_DOCUMENT` | Documentos a indexar | NO |
| `CODE_RETRIEVAL_QUERY` | Búsqueda de código por NL | NO |
| `SEMANTIC_SIMILARITY` | Comparación de textos | NO |
| `CLASSIFICATION` | Clasificar textos | NO |
| `CLUSTERING` | Agrupar textos similares | NO |
| `QUESTION_ANSWERING` | Q&A | NO |
| `FACT_VERIFICATION` | Verificación de hechos | NO |

**Código actual (línea 105 de gemini.py):**
```python
config=types.EmbedContentConfig(output_dimensionality=self.config.embedding_dim)
# NO especifica task_type - usa default genérico
```

### 2.2 Beneficio de Task Types para Graphiti

```
GRAPHITI USE CASE             ->    OPTIMAL TASK TYPE
--------------------------------------------------------------
Búsqueda semántica de nodos   ->    RETRIEVAL_QUERY
Indexación de EntityNode.name ->    RETRIEVAL_DOCUMENT
Indexación de EntityEdge.fact ->    RETRIEVAL_DOCUMENT
Búsqueda de código/errores    ->    CODE_RETRIEVAL_QUERY
Deduplicación de entidades    ->    SEMANTIC_SIMILARITY
Clustering de comunidades     ->    CLUSTERING
```

### 2.3 Modelo Recomendado

**Actual**: `text-embedding-001` (línea 40)
**Recomendado**: `gemini-embedding-001` (nuevo, mejor calidad)

---

## 3. Análisis del Bug de Normalización

### 3.1 El Problema

```python
# Documentación de Google:
# "Embeddings with output_dimensionality < 3072 are NOT normalized.
# You must normalize them manually for accurate similarity calculations."

# Código actual - NO normaliza:
return result.embeddings[0].values  # Devuelve raw

# Impacto en similaridad coseno:
# cos_sim(a, b) = (a dot b) / (||a|| * ||b||)
# Si ||a|| != 1, el resultado es INCORRECTO
```

### 3.2 La Solución

```python
import numpy as np

def _normalize(embedding: list[float]) -> list[float]:
    """Normaliza vector a norma unitaria para similaridad coseno correcta."""
    arr = np.array(embedding)
    norm = np.linalg.norm(arr)
    return (arr / norm).tolist() if norm > 0 else embedding

# En create():
embedding = result.embeddings[0].values
if self.config.embedding_dim < 3072:
    embedding = self._normalize(embedding)
return embedding
```

### 3.3 Por qué 3072D no necesita normalización

Google pre-normaliza solo 3072D porque es la dimensión nativa del modelo. Las otras dimensiones son **truncaciones Matryoshka** que cambian la norma del vector.

---

## 4. Plan de Reprocesamiento de Embeddings

### 4.1 Qué significa "reprocesar"

```
Estado actual:
+------------------+
| EntityNode       |
| name_embedding:  |  <- 1024D (o lo que tengas)
| [0.1, 0.2, ...]  |    Sin normalizar
+------------------+

Estado objetivo:
+------------------+
| EntityNode       |
| name_embedding:  |  <- 3072D
| [0.05, 0.08,...] |    Normalizado (por API)
+------------------+
```

### 4.2 Script de Reprocesamiento

```python
#!/usr/bin/env python3
"""
Script para reprocesar embeddings existentes a 3072D con task_type apropiado.

IMPORTANTE: Este script:
1. Lee todos los nodos/edges de Neo4j
2. Regenera embeddings con nueva config
3. Actualiza en Neo4j

Uso:
    python reprocess_embeddings.py --dry-run  # Ver qué haría
    python reprocess_embeddings.py --execute  # Ejecutar
"""

import asyncio
from graphiti_core.embedder.gemini import GeminiEmbedder, GeminiEmbedderConfig
from neo4j import AsyncGraphDatabase

# Configuración nueva
NEW_CONFIG = GeminiEmbedderConfig(
    embedding_model="gemini-embedding-001",
    embedding_dim=3072,
    # task_type se especificará por tipo de embedding
)

async def reprocess_entity_nodes(driver, embedder, dry_run=True):
    """Reprocesa name_embedding de todos los EntityNode."""

    query_read = """
    MATCH (n:EntityNode)
    WHERE n.name IS NOT NULL
    RETURN n.uuid as uuid, n.name as name
    """

    query_update = """
    MATCH (n:EntityNode {uuid: $uuid})
    SET n.name_embedding = $embedding
    """

    async with driver.session() as session:
        result = await session.run(query_read)
        nodes = [record async for record in result]

        print(f"Found {len(nodes)} EntityNodes to reprocess")

        if dry_run:
            print("DRY RUN - No changes made")
            return

        for i, node in enumerate(nodes):
            # Generar nuevo embedding con RETRIEVAL_DOCUMENT
            embedding = await embedder.create(
                node["name"],
                task_type="RETRIEVAL_DOCUMENT"  # Óptimo para indexación
            )

            await session.run(query_update, {
                "uuid": node["uuid"],
                "embedding": embedding
            })

            if (i + 1) % 100 == 0:
                print(f"Processed {i + 1}/{len(nodes)} nodes")

        print(f"Completed reprocessing {len(nodes)} EntityNodes")

async def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", default=True)
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()

    dry_run = not args.execute

    # Conexión a Neo4j
    driver = AsyncGraphDatabase.driver(
        "bolt://localhost:7687",
        auth=("neo4j", "your_password")
    )

    embedder = GeminiEmbedder(NEW_CONFIG)

    try:
        await reprocess_entity_nodes(driver, embedder, dry_run)
    finally:
        await driver.close()

if __name__ == "__main__":
    asyncio.run(main())
```

### 4.3 Estimación de Costos de Reprocesamiento

| Métrica | Valor |
|---------|-------|
| Coste Gemini embedding | $0.00 (gratis) |
| Tiempo por embedding | ~100ms |
| 1000 nodos + 5000 edges | ~10 minutos |
| 10000 nodos + 50000 edges | ~100 minutos |

---

## 5. Implementación: Campos Duales (Experimental)

### 5.1 Por qué campos duales

Tu petición específica:
> "primero hacerlo duplicado y hacer pruebas para ver si merece la pena"

Esto permite:
1. Mantener embeddings actuales funcionando
2. Generar 3072D en paralelo
3. Comparar calidad de búsqueda
4. Migrar gradualmente

### 5.2 Cambios en Modelos

```python
# graphiti_core/nodes.py - EntityNode
class EntityNode(BaseModel):
    # Existente
    name_embedding: list[float] | None = Field(
        default=None,
        description='embedding of the name (current dimension)'
    )

    # NUEVO - Experimental
    name_embedding_3072: list[float] | None = Field(
        default=None,
        description='embedding of the name at 3072D with task_type optimization'
    )
    name_embedding_task_type: str | None = Field(
        default=None,
        description='task_type used for name_embedding_3072'
    )
```

### 5.3 Cambios en Embedder

```python
# graphiti_core/embedder/gemini.py

from enum import Enum

class GeminiTaskType(str, Enum):
    """Task types soportados por Gemini Embedding API."""
    RETRIEVAL_QUERY = "RETRIEVAL_QUERY"
    RETRIEVAL_DOCUMENT = "RETRIEVAL_DOCUMENT"
    CODE_RETRIEVAL_QUERY = "CODE_RETRIEVAL_QUERY"
    SEMANTIC_SIMILARITY = "SEMANTIC_SIMILARITY"
    CLASSIFICATION = "CLASSIFICATION"
    CLUSTERING = "CLUSTERING"
    QUESTION_ANSWERING = "QUESTION_ANSWERING"
    FACT_VERIFICATION = "FACT_VERIFICATION"


class GeminiEmbedderConfig(EmbedderConfig):
    embedding_model: str = Field(default="gemini-embedding-001")  # CAMBIO
    embedding_dim: int = Field(default=3072)  # CAMBIO a 3072
    task_type: GeminiTaskType | None = Field(default=None)  # NUEVO
    normalize: bool = Field(default=True)  # NUEVO
    api_key: str | None = None


class GeminiEmbedder(EmbedderClient):

    async def create(
        self,
        input_data: str | list[str],
        task_type: GeminiTaskType | str | None = None  # NUEVO parámetro
    ) -> list[float]:
        """
        Create embeddings with optional task_type optimization.

        Args:
            input_data: Text to embed
            task_type: Override config task_type for this call
        """
        effective_task_type = task_type or self.config.task_type

        config_params = {
            "output_dimensionality": self.config.embedding_dim
        }

        if effective_task_type:
            config_params["task_type"] = str(effective_task_type)

        result = await self.client.aio.models.embed_content(
            model=self.config.embedding_model,
            contents=[input_data],
            config=types.EmbedContentConfig(**config_params),
        )

        embedding = result.embeddings[0].values

        # NUEVO: Normalizar si es necesario
        if self.config.normalize and self.config.embedding_dim < 3072:
            embedding = self._normalize(embedding)

        return embedding

    def _normalize(self, embedding: list[float]) -> list[float]:
        """Normaliza a norma unitaria."""
        import numpy as np
        arr = np.array(embedding)
        norm = np.linalg.norm(arr)
        return (arr / norm).tolist() if norm > 0 else embedding
```

### 5.4 Patrón Query vs Document

```
BÚSQUEDA OPTIMIZADA CON TASK TYPES
----------------------------------

Usuario: "Como configuro Neo4j?"
                |
                v
Query embedding: RETRIEVAL_QUERY (optimizado para preguntas)
                |
                v
Compara contra:
- EntityNode.name_embedding_3072 (RETRIEVAL_DOCUMENT)
- EntityEdge.fact_embedding_3072 (RETRIEVAL_DOCUMENT)
                |
                v
Resultado: Nodos/edges más relevantes semánticamente
```

---

## 6. Plan de Ejecución por Fases

### Fase 0: Sincronización (RECOMENDADO PRIMERO)
**Duración**: 2-4 horas
**Objetivo**: Actualizar fork con upstream

```bash
# Paso 1: Backup
git checkout main
git branch backup-pre-sync

# Paso 2: Merge upstream
git fetch upstream
git merge upstream/main

# Paso 3: Resolver conflictos (si hay)
# Principalmente en mcp_server/config/ que borraron del upstream

# Paso 4: Verificar
make test  # Desde raíz
```

**Archivos que pueden tener conflictos:**
- `mcp_server/config/*` - Upstream eliminó tus configs personalizados
- `graphiti_core/nodes.py` - Cambios significativos
- `graphiti_core/edges.py` - Cambios significativos

### Fase 1: Fix Básico (Normalización + Modelo)
**Duración**: 2-4 horas
**Objetivo**: Corregir bugs sin cambiar arquitectura

**Cambios:**
1. `gemini.py`: Cambiar modelo default a `gemini-embedding-001`
2. `gemini.py`: Añadir normalización para dim < 3072
3. `client.py`: Cambiar EMBEDDING_DIM default a 3072

**Tests PRE:**
```python
# test_embedding_normalization_pre.py
def test_current_embeddings_not_normalized():
    """Verificar que embeddings actuales NO están normalizados."""
    # Genera embedding con dim=1024
    # Calcula norma
    # Assert norma != 1.0
```

**Tests POST:**
```python
def test_embeddings_normalized_after_fix():
    """Verificar que embeddings <3072D se normalizan."""
    # Genera embedding con dim=1024
    # Calcula norma
    # Assert abs(norma - 1.0) < 0.0001
```

### Fase 2: Task Types
**Duración**: 4-6 horas
**Objetivo**: Añadir soporte para task_type

**Cambios:**
1. `gemini.py`: Enum GeminiTaskType
2. `gemini.py`: Parámetro task_type en create()
3. Config YAML: Exponer task_type

### Fase 3: Campos Duales (Experimental)
**Duración**: 1-2 días
**Objetivo**: Permitir experimentación A/B

**Cambios:**
1. `nodes.py`: Campos `*_3072`
2. `edges.py`: Campos `*_3072`
3. `node_db_queries.py`: Persistencia
4. `edge_db_queries.py`: Persistencia
5. `search_utils.py`: Selector

### Fase 4: Reprocesamiento
**Duración**: Variable (depende de datos)
**Objetivo**: Migrar embeddings existentes

### Fase 5: Evaluación y Decisión
**Duración**: 1-2 días
**Objetivo**: Decidir si 3072D vale la pena

---

## 7. Archivos a Modificar (Resumen)

| Archivo | Fase | Cambio |
|---------|------|--------|
| `graphiti_core/embedder/gemini.py` | 1,2 | Normalización, task_type, modelo |
| `graphiti_core/embedder/client.py` | 1 | Default 3072D |
| `graphiti_core/nodes.py` | 3 | Campos *_3072 |
| `graphiti_core/edges.py` | 3 | Campos *_3072 |
| `graphiti_core/models/nodes/node_db_queries.py` | 3 | Persistencia |
| `graphiti_core/models/edges/edge_db_queries.py` | 3 | Persistencia |
| `graphiti_core/search/search_utils.py` | 3 | Selector |
| `scripts/reprocess_embeddings.py` | 4 | NUEVO |
| `scripts/evaluate_embeddings.py` | 5 | NUEVO |

---

## 8. Decisiones Pendientes para Ti

1. **Sincronizar con upstream primero?**
   - [ ] Sí, hacer merge antes de todo
   - [ ] No, implementar en fork actual

2. **Dimensión principal por defecto?**
   - [ ] Mantener 1024 (actual)
   - [ ] Cambiar a 1536 (balance)
   - [ ] Cambiar a 3072 (máxima calidad)

3. **Implementar campos duales?**
   - [ ] Sí, para experimentar A/B
   - [ ] No, ir directo a 3072D

4. **Qué task_type por defecto?**
   - [ ] Ninguno (comportamiento actual)
   - [ ] RETRIEVAL_DOCUMENT para indexación
   - [ ] Configurable por tipo de entidad

5. **Reprocesar embeddings existentes?**
   - [ ] Sí, todos a 3072D
   - [ ] No, solo nuevos
   - [ ] Gradual, ir migrando

---

## 9. Riesgos y Mitigaciones

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|------------|
| Conflictos en merge upstream | Alta | Medio | Backup antes, resolver manualmente |
| Incompatibilidad búsquedas mixtas | Media | Alto | Mantener campos actuales, migración gradual |
| Aumento almacenamiento Neo4j | Alta | Bajo | 3072D = 3x más, pero aceptable |
| API rate limits Gemini | Baja | Medio | Batch processing, delays |
| Regresión en búsquedas | Media | Alto | Tests A/B antes de migrar |

---

## 10. Próximos Pasos Inmediatos

Si decides proceder:

```bash
# 1. Crear branch de trabajo
git checkout main
git fetch upstream
git merge upstream/main  # Resolver conflictos
git checkout -b feature/gemini-embeddings-enhanced

# 2. Implementar Fase 1 (fix básico)
# Editar gemini.py

# 3. Tests
make test

# 4. PR interno (a tu main)
```

---

**Qué decisiones quieres tomar antes de proceder?**
