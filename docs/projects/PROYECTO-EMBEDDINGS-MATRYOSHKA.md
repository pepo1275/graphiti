# Proyecto: Embeddings Matryoshka en Graphiti

**Estado**: Propuesta
**Autor**: Pepo + Claude
**Fecha**: 2026-01-31
**Prioridad**: Media-Alta (mejora de calidad de búsqueda)

---

## 1. Resumen Ejecutivo

Este proyecto propone implementar soporte para embeddings Matryoshka en Graphiti, permitiendo:
1. Experimentar con diferentes dimensiones (768, 1536, 3072)
2. Comparar calidad de búsqueda entre dimensiones
3. Optimizar almacenamiento vs precisión según caso de uso
4. Corregir el bug actual de normalización

---

## 2. Contexto: ¿Qué es Matryoshka Representation Learning?

### 2.1 Concepto

Matryoshka Representation Learning (MRL) es una técnica de entrenamiento de embeddings donde:

```
Embedding 3072-dim: [d₁, d₂, d₃, ..., d₃₀₇₂]
                     ↓
Contiene embeddings válidos anidados:
├── [d₁...d₂₅₆]   → embedding 256-dim válido
├── [d₁...d₇₆₈]   → embedding 768-dim válido
├── [d₁...d₁₅₃₆]  → embedding 1536-dim válido
└── [d₁...d₃₀₇₂]  → embedding 3072-dim completo
```

**Analogía**: Como las muñecas rusas Matryoshka, cada embedding contiene versiones más pequeñas de sí mismo.

### 2.2 Cómo Funciona el Entrenamiento

Durante el entrenamiento, el modelo optimiza múltiples funciones de pérdida simultáneamente:

```python
# Pseudocódigo del entrenamiento MRL
total_loss = 0
for dim in [256, 768, 1536, 3072]:
    truncated_embedding = full_embedding[:dim]
    loss = contrastive_loss(truncated_embedding, labels)
    total_loss += weight[dim] * loss
```

Esto fuerza al modelo a **frontload** (cargar al frente) la información más importante.

### 2.3 Visualización de Distribución de Información

```
Dimensiones:  0    256    768    1536    3072
              |-----|------|-------|-------|

Densidad de información semántica:
              ████████████████████████████████  ← Máxima (3072)
              ██████████████████████████        ← Alta (1536)
              ████████████████████              ← Buena (768)
              ████████████                      ← Básica (256)

Nota: No es lineal - las primeras dimensiones contienen
      proporcionalmente más información que las últimas.
```

### 2.4 Utilidades Prácticas

| Caso de Uso | Dimensión | Justificación |
|-------------|-----------|---------------|
| **Búsqueda en cascada** | 256 → 3072 | Filtrado rápido, luego ranking preciso |
| **Almacenamiento limitado** | 768 | ~75% reducción vs 3072, calidad aceptable |
| **Máxima precisión** | 3072 | Casos críticos, búsqueda semántica fina |
| **Dispositivos móviles** | 256-768 | Restricciones de memoria/latencia |
| **Experimentos A/B** | Múltiples | Comparar trade-offs en producción |

### 2.5 Proveedores con Soporte Matryoshka

| Proveedor | Modelo | Dimensiones Soportadas | Normalización |
|-----------|--------|------------------------|---------------|
| **Google Gemini** | gemini-embedding-001 | 768, 1536, 3072 | Solo 3072 pre-normalizado |
| **OpenAI** | text-embedding-3-small/large | 256-3072 | Pre-normalizado |
| **Voyage** | voyage-3-large | 256-1024 | Pre-normalizado |
| **Nomic** | nomic-embed-text-v1.5 | 64-768 | Requiere normalización |

---

## 3. Estado Actual en Graphiti

### 3.1 Campos de Embedding Existentes

```python
# graphiti_core/nodes.py - EntityNode (línea 436)
name_embedding: list[float] | None = Field(
    default=None,
    description='embedding of the name'
)

# graphiti_core/edges.py - EntityEdge (línea 224)
fact_embedding: list[float] | None = Field(
    default=None,
    description='embedding of the fact'
)

# graphiti_core/nodes.py - CommunityNode (línea 592)
name_embedding: list[float] | None = Field(
    default=None,
    description='embedding of the summary'
)
```

### 3.2 Configuración de Dimensión

```python
# graphiti_core/embedder/client.py (línea 23)
EMBEDDING_DIM = int(os.getenv('EMBEDDING_DIM', 1024))  # Default 1024

class EmbedderConfig(BaseModel):
    embedding_dim: int = Field(default=EMBEDDING_DIM, frozen=True)
```

### 3.3 Uso en Gemini Embedder

```python
# graphiti_core/embedder/gemini.py (línea ~105)
result = await asyncio.to_thread(
    genai.embed_content,
    model=self.model,
    content=text,
    config=types.EmbedContentConfig(
        output_dimensionality=self.config.embedding_dim  # Usa la config
    ),
)
```

### 3.4 BUG IDENTIFICADO: Falta de Normalización

**Problema crítico**: Graphiti no normaliza embeddings después de truncar.

```python
# Código actual (gemini.py) - NO normaliza
embedding = result.embedding  # ← Devuelve sin normalizar si dim < 3072

# Impacto: Similaridad coseno incorrecta
# cos_sim(a, b) = (a · b) / (||a|| * ||b||)
# Si ||a|| ≠ 1 y ||b|| ≠ 1, el resultado está sesgado
```

**Evidencia de Google**:
> "Embeddings with output_dimensionality < 3072 are NOT normalized.
> You must normalize them manually for accurate similarity calculations."

---

## 4. Opciones de Implementación

### 4.1 Opción A: Fix Mínimo (Normalización)

**Objetivo**: Corregir el bug de normalización sin cambiar arquitectura.

**Cambios**:
```python
# graphiti_core/embedder/gemini.py
import numpy as np

async def create(self, input_data: str | list[str]) -> list[float]:
    # ... código existente ...
    embedding = result.embedding

    # NUEVO: Normalizar si dimensión < 3072
    if self.config.embedding_dim < 3072:
        embedding = self._normalize(embedding)

    return embedding

def _normalize(self, embedding: list[float]) -> list[float]:
    arr = np.array(embedding)
    norm = np.linalg.norm(arr)
    return (arr / norm).tolist() if norm > 0 else embedding
```

**Archivos a modificar**: 1
- `graphiti_core/embedder/gemini.py`

**Esfuerzo**: 1-2 horas
**Riesgo**: Bajo
**Valor**: Alto (corrige bug crítico)

---

### 4.2 Opción B: Embeddings Duales (Campos Paralelos)

**Objetivo**: Permitir almacenar dos dimensiones simultáneamente para experimentos A/B.

**Cambios en modelos**:
```python
# graphiti_core/nodes.py - EntityNode
name_embedding: list[float] | None = Field(...)      # Dimensión principal
name_embedding_hd: list[float] | None = Field(...)   # Dimensión alta (3072)

# graphiti_core/edges.py - EntityEdge
fact_embedding: list[float] | None = Field(...)
fact_embedding_hd: list[float] | None = Field(...)
```

**Nuevo método de generación**:
```python
# graphiti_core/nodes.py
async def generate_dual_embeddings(
    self,
    embedder_primary: EmbedderClient,
    embedder_hd: EmbedderClient
):
    text = self.name
    self.name_embedding = await embedder_primary.create(input_data=[text])
    self.name_embedding_hd = await embedder_hd.create(input_data=[text])
```

**Archivos a modificar**: 6
- `graphiti_core/embedder/client.py` - Config dual
- `graphiti_core/nodes.py` - Campos + métodos
- `graphiti_core/edges.py` - Campos + métodos
- `graphiti_core/models/nodes/node_db_queries.py` - Persistencia
- `graphiti_core/models/edges/edge_db_queries.py` - Persistencia
- `graphiti_core/search/search_utils.py` - Selector de embedding

**Esfuerzo**: 2-3 días
**Riesgo**: Medio
**Valor**: Alto (permite experimentos sin migración)

---

### 4.3 Opción C: Búsqueda en Cascada (Cascade Search)

**Objetivo**: Optimizar búsqueda usando embeddings pequeños para filtrar, grandes para ranking.

**Arquitectura**:
```
Query: "¿Cuáles son los errores de RPVEA?"
         ↓
    [Embedding 768-dim]
         ↓
    Búsqueda en 100K nodos
    (rápida, ~10ms)
         ↓
    Top 1000 candidatos
         ↓
    [Re-embedding 3072-dim]
         ↓
    Re-ranking preciso
    (más lento, ~50ms)
         ↓
    Top 10 resultados finales
```

**Implementación**:
```python
# graphiti_core/search/cascade_search.py (NUEVO)
class CascadeSearcher:
    def __init__(
        self,
        embedder_coarse: EmbedderClient,  # 768-dim
        embedder_fine: EmbedderClient,    # 3072-dim
        coarse_k: int = 1000,
        fine_k: int = 10
    ):
        self.embedder_coarse = embedder_coarse
        self.embedder_fine = embedder_fine
        self.coarse_k = coarse_k
        self.fine_k = fine_k

    async def search(self, query: str, nodes: list[EntityNode]) -> list[EntityNode]:
        # Fase 1: Filtrado rápido
        query_emb_coarse = await self.embedder_coarse.create([query])
        candidates = self._coarse_filter(query_emb_coarse, nodes, self.coarse_k)

        # Fase 2: Re-ranking preciso
        query_emb_fine = await self.embedder_fine.create([query])
        results = self._fine_rank(query_emb_fine, candidates, self.fine_k)

        return results
```

**Archivos a modificar**: 4
- `graphiti_core/search/cascade_search.py` - NUEVO
- `graphiti_core/search/__init__.py` - Export
- `graphiti_core/graphiti.py` - Integración
- `graphiti_core/embedder/client.py` - Config multi-dim

**Esfuerzo**: 1 semana
**Riesgo**: Medio-Alto
**Valor**: Muy Alto (mejora rendimiento en grafos grandes)

---

### 4.4 Opción D: Configuración por Tipo de Entidad

**Objetivo**: Diferentes dimensiones según el tipo de entidad.

**Caso de uso**:
- `Error`, `Solution`: 3072-dim (precisión crítica)
- `Procedure`: 1536-dim (balance)
- `Preference`: 768-dim (menos crítico)

**Configuración**:
```yaml
# config.yaml
embeddings:
  default_dim: 1536
  entity_overrides:
    Error: 3072
    Solution: 3072
    Procedure: 1536
    Preference: 768
```

**Esfuerzo**: 3-4 días
**Riesgo**: Medio
**Valor**: Alto (optimización de almacenamiento)

---

## 5. Plan de Implementación Recomendado

### Fase 1: Fix Crítico (Sprint 1)
**Duración**: 1-2 días

1. Implementar Opción A (normalización)
2. Añadir tests de normalización
3. Documentar comportamiento

**Entregables**:
- PR con fix de normalización
- Test: `test_gemini_normalization.py`

### Fase 2: Experimento de Calidad (Sprint 2)
**Duración**: 3-4 días

1. Crear script de evaluación standalone
2. Generar dataset de prueba
3. Comparar precisión 768 vs 1536 vs 3072
4. Documentar resultados

**Entregables**:
- `scripts/evaluate_embedding_quality.py`
- `docs/EMBEDDING-QUALITY-REPORT.md`

### Fase 3: Embeddings Duales (Sprint 3)
**Duración**: 1 semana

1. Implementar Opción B
2. Migración de datos existentes
3. Flag de búsqueda `use_hd=True/False`
4. Tests de integración

**Entregables**:
- Campos `*_hd` en modelos
- Script de migración
- Documentación de uso

### Fase 4: Búsqueda en Cascada (Sprint 4) - Opcional
**Duración**: 1-2 semanas

1. Implementar Opción C
2. Benchmarks de rendimiento
3. Configuración de umbrales

**Entregables**:
- `CascadeSearcher` funcional
- Benchmark report

---

## 6. Métricas de Éxito

| Métrica | Baseline | Objetivo Fase 1 | Objetivo Fase 3 |
|---------|----------|-----------------|-----------------|
| Normalización correcta | ❌ | ✅ | ✅ |
| Recall@10 (benchmark interno) | TBD | +5% | +10% |
| Almacenamiento por nodo | 1536*4 bytes | - | Configurable |
| Latencia búsqueda (1K nodos) | ~50ms | - | <30ms (cascada) |

---

## 7. Riesgos y Mitigaciones

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|------------|
| Incompatibilidad con datos existentes | Media | Alto | Script de migración + backup |
| Degradación de rendimiento | Baja | Medio | Benchmarks en cada fase |
| Aumento significativo de almacenamiento | Alta | Medio | Campos HD opcionales |
| Complejidad de mantenimiento | Media | Medio | Documentación exhaustiva |

---

## 8. Decisiones Pendientes

1. **¿Cuál es la dimensión principal por defecto?**
   - [ ] 1024 (actual)
   - [ ] 1536 (balance)
   - [ ] 3072 (máxima calidad)

2. **¿Migrar datos existentes o solo nuevos?**
   - [ ] Regenerar todos los embeddings
   - [ ] Solo aplicar a nuevos datos

3. **¿Implementar cascada o embeddings duales primero?**
   - [ ] Duales (más simple, permite experimentos)
   - [ ] Cascada (más valor para grafos grandes)

---

## 9. Referencias

- [Matryoshka Representation Learning (Paper)](https://arxiv.org/abs/2205.13147)
- [Google Gemini Embedding Documentation](https://ai.google.dev/gemini-api/docs/embeddings)
- [OpenAI Embeddings with Matryoshka](https://platform.openai.com/docs/guides/embeddings)
- [Graphiti Source Code](https://github.com/getzep/graphiti)

---

## 10. Apéndice: Script de Evaluación Rápida

```python
#!/usr/bin/env python3
"""
Script para evaluar calidad de embeddings Matryoshka.
Compara similaridad coseno entre diferentes dimensiones.

Uso:
    python evaluate_matryoshka.py --dims 768,1536,3072
"""

import asyncio
import numpy as np
from graphiti_core.embedder.gemini import GeminiEmbedder, GeminiEmbedderConfig

# Pares de textos para evaluar (similar, no similar)
TEST_PAIRS = [
    # Pares similares (esperamos alta similaridad)
    ("Error de conexión a Neo4j", "Fallo al conectar con la base de datos Neo4j"),
    ("Configurar API key de OpenAI", "Establecer credenciales de OpenAI"),

    # Pares no similares (esperamos baja similaridad)
    ("Error de conexión a Neo4j", "Receta de paella valenciana"),
    ("Configurar API key de OpenAI", "Historia del Imperio Romano"),
]

def normalize(embedding: list[float]) -> np.ndarray:
    arr = np.array(embedding)
    norm = np.linalg.norm(arr)
    return arr / norm if norm > 0 else arr

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b))

async def evaluate_dimension(dim: int) -> dict:
    config = GeminiEmbedderConfig(embedding_dim=dim)
    embedder = GeminiEmbedder(config)

    results = {"dimension": dim, "similarities": []}

    for text1, text2 in TEST_PAIRS:
        emb1 = normalize(await embedder.create([text1]))
        emb2 = normalize(await embedder.create([text2]))
        sim = cosine_similarity(emb1, emb2)
        results["similarities"].append({
            "text1": text1[:30] + "...",
            "text2": text2[:30] + "...",
            "similarity": round(sim, 4)
        })

    return results

async def main():
    dimensions = [768, 1536, 3072]

    print("=" * 60)
    print("EVALUACIÓN DE EMBEDDINGS MATRYOSHKA")
    print("=" * 60)

    for dim in dimensions:
        results = await evaluate_dimension(dim)
        print(f"\n### Dimensión: {dim}")
        for item in results["similarities"]:
            print(f"  {item['text1']} <-> {item['text2']}")
            print(f"    Similaridad: {item['similarity']}")

if __name__ == "__main__":
    asyncio.run(main())
```

---

**Próximo paso recomendado**: Implementar Fase 1 (fix de normalización) y ejecutar script de evaluación para tener baseline de calidad.
