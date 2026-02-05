# Plan Maestro: Mejoras de Graphiti Fork

**Estado**: En ejecución (Fase -1 y 0 completadas)
**Autor**: Pepo + Claude
**Fecha**: 2026-01-31 (actualizado 2026-02-05)
**Versión**: 1.1

---

## 1. Visión General

### 1.1 Objetivo

Mantener un fork de Graphiti que:
1. **Sea compatible con upstream** - Poder hacer merge de mejoras de getzep/graphiti
2. **Incluya mejoras propias** - Embeddings avanzados, configuraciones personalizadas
3. **Esté documentado** - Trazabilidad completa de cambios y decisiones
4. **Sea desplegable** - En múltiples entornos (local, AuraDB, Docker)

### 1.2 Estado Actual (actualizado 2026-02-05)

```
getzep/graphiti (upstream)     pepo1275/graphiti (fork)
         |                              |
    affca93 (actual)              ac21101 (main, sincronizado)
         |                              |
         |                     +-- Fase -1: CI/CD adaptado ✅
         |                     +-- Fase 0: Sync upstream ✅
         |                     +-- Configs personalizadas
         |                     +-- CLAUDE.md + docs/projects/
         |                     +-- Entity Types personalizados
         |
    ⚠️ upstream/chore/gemini-improvements (no mergeado)
         |     → Refactor mayor (188 archivos, -24K líneas)
         |     → Ver sección 7.2 para impacto
```

### 1.3 Principio de Diseño

```
+------------------------------------------------------------------+
|  REGLA DE ORO: Cambios Aditivos, No Destructivos                 |
+------------------------------------------------------------------+
|                                                                  |
|  SI un cambio modifica comportamiento existente:                 |
|     -> Hacerlo configurable con flag/env var                     |
|     -> Default = comportamiento upstream                         |
|     -> Documentar en CHANGELOG-FORK.md                           |
|                                                                  |
|  SI un cambio añade funcionalidad nueva:                         |
|     -> Añadir en módulo separado si es posible                   |
|     -> No romper imports existentes                              |
|     -> Documentar en CHANGELOG-FORK.md                           |
|                                                                  |
+------------------------------------------------------------------+
```

---

## 2. Arquitectura del Fork

### 2.1 Estructura de Branches

```
main (sincronizado con upstream)
  |
  +-- feature/embeddings-enhanced     <- Mejoras de embeddings
  |
  +-- feature/custom-configs          <- Configuraciones personalizadas
  |
  +-- release/pepo-v1.0               <- Release estable del fork
```

### 2.2 Estrategia de Sincronización

```bash
# Workflow de sincronización mensual (o cuando haya releases importantes)

# 1. Actualizar main desde upstream
git checkout main
git fetch upstream
git merge upstream/main --no-edit
git push origin main

# 2. Rebase de feature branches
git checkout feature/embeddings-enhanced
git rebase main
# Resolver conflictos si los hay

# 3. Crear release tag
git checkout main
git merge feature/embeddings-enhanced
git tag -a pepo-v1.x -m "Release con mejoras de embeddings"
```

### 2.3 Archivos que NUNCA deben conflictuar con upstream

| Archivo/Directorio | Razón |
|--------------------|-------|
| `CLAUDE.md` | Solo existe en fork |
| `.claude/` | Solo existe en fork |
| `docs/projects/` | Solo existe en fork |
| `docs/deployment/` | Solo existe en fork |
| `docs/decisions/` | Solo existe en fork |
| `docs/changelog/` | Solo existe en fork |
| `checkpoints/` | Solo existe en fork |
| `mcp_server/config/config-*.yaml` | Configs personalizadas |
| `.github/workflows-upstream-disabled/` | Workflows desactivados |
| `scripts/pepo-*.py` | Scripts personalizados |

### 2.4 Problemas de CI/CD (CRÍTICO - Resolver ANTES de sync)

**Documento detallado**: [PROBLEMAS-CI-CD-FORK.md](./PROBLEMAS-CI-CD-FORK.md)

Los workflows de upstream usan infraestructura privada de Zep:

| Problema | Impacto | Solución |
|----------|---------|----------|
| `depot-ubuntu-*` runners | Jobs fallarán | Cambiar a `ubuntu-22.04` |
| `DANIEL_PAT` secret | CLA no funciona | Desactivar cla.yml |
| `ANTHROPIC_API_KEY` | Reviews no funcionan | Desactivar claude*.yml |
| `DOCKERHUB_*` secrets | Releases fallan | Desactivar release*.yml |

**Acción requerida ANTES de Fase 0:**
```bash
# 1. Modificar runners en workflows esenciales
sed -i '' 's/depot-ubuntu-22.04/ubuntu-22.04/g' .github/workflows/*.yml
sed -i '' 's/depot-ubuntu-24.04-small/ubuntu-24.04/g' .github/workflows/*.yml

# 2. Mover workflows innecesarios
mkdir -p .github/workflows-upstream-disabled
mv .github/workflows/cla.yml .github/workflows-upstream-disabled/
mv .github/workflows/claude*.yml .github/workflows-upstream-disabled/
mv .github/workflows/release*.yml .github/workflows-upstream-disabled/
```

### 2.5 Archivos que PUEDEN conflictuar (requieren cuidado)

| Archivo | Estrategia | Fase |
|---------|------------|------|
| `graphiti_core/embedder/gemini.py` | Cambios aditivos marcados `# [FORK]` | 1 |
| `graphiti_core/embedder/client.py` | **NO TOCAR** — override solo en GeminiEmbedderConfig | — |
| `graphiti_core/nodes.py` | Campos opcionales con `default=None` | 2 |
| `graphiti_core/edges.py` | Campos opcionales con `default=None` | 2 |
| `graphiti_core/search/search_utils.py` | Función helper aditiva para selector | 2 |
| `tests/embedder/test_gemini_fork.py` | **Archivo NUEVO** — tests propios separados | 1 |

---

## 3. Roadmap de Mejoras

### 3.1 Diagrama de Dependencias (actualizado 2026-02-05)

```
+------------------+
|  FASE -1         |  ✅ COMPLETADA
|  Preparar CI/CD  |
+--------+---------+
         |
         v
+------------------+
|  FASE 0          |  ✅ COMPLETADA
|  Sync Upstream   |
+--------+---------+
         |
         v
+-------------------------------+
|  FASE 1                       |  ← SIGUIENTE
|  Embeddings Gemini Avanzados  |
|  (Normalización + Modelo +    |
|   Task Types)                 |
|  Archivo único: gemini.py     |
+--------+----------------------+
         |
         v
+-------------------------------+
|  FASE 2                       |
|  Campos Duales                |
|  (name_embedding_enhanced +   |
|   fact_embedding_enhanced)    |
|  Índices Neo4j 3072D          |
+--------+----------------------+
         |
         v
+-------------------------------+
|  FASE 3                       |
|  Reprocesamiento              |
|  (Scripts standalone, $0)     |
+--------+----------------------+
         |
         v
+-------------------------------+
|  FASE 4                       |
|  Evaluación y Decisión        |
|  (1024 vs 3072, task_types)   |
+--------+----------------------+
         |
         v
+-------------------------------+
|  FASE 5                       |
|  Release pepo-v1.0            |
+-------------------------------+
```

**Cambio vs plan original**: Fases 1+2 originales (normalización + task types) se fusionaron
en una sola porque tocan el mismo archivo (`gemini.py`) y son ~35 líneas cohesivas.
Esto reduce de 7 fases a 6 (realmente 5 pendientes) y minimiza superficie de conflicto.

### 3.2 Detalle de Fases

#### FASE -1: Preparar CI/CD ✅ COMPLETADA (2026-02-05)
- Commit: `983f848`
- Runners cambiados a ubuntu-22.04
- 7 workflows desactivados a `.github/workflows-upstream-disabled/`
- Tests: F-1-T1 a F-1-T8 PASS

#### FASE 0: Sincronización con Upstream ✅ COMPLETADA (2026-02-05)
- Merge commit: `9e6b2a0` (upstream affca93 → fork main)
- Formatting fix: `ac21101`
- 0 conflictos (git rename tracking funcionó perfectamente)
- Push a origin vía SSH (fix de OAuth workflow scope)
- Tests: 249 passed, Pyright 0 errores (mejorado de 28)

---

#### FASE 1: Embeddings Gemini Avanzados (Normalización + Modelo + Task Types)
**Documento**: [PLAN-EMBEDDINGS-GEMINI-AVANZADO.md](./PLAN-EMBEDDINGS-GEMINI-AVANZADO.md)
**Duración estimada**: 4-6 horas
**Prerequisito para**: Fase 2

**¿Por qué se fusionaron las antiguas Fases 1 y 2?**
Normalización, cambio de modelo y task types tocan el mismo archivo (`gemini.py`).
Separarlas creaba 2 commits/PRs innecesarios y duplicaba riesgo de conflicto.

**Archivos modificados:**

| Archivo | Cambio | Líneas |
|---------|--------|--------|
| `graphiti_core/embedder/gemini.py` | Normalización, modelo, GeminiTaskType enum, task_type en create()/create_batch() | ~35 |
| `tests/embedder/test_gemini_fork.py` | **NUEVO** — Tests de normalización, task_types, modelo | ~100 |

**Archivos que NO se tocan:**

| Archivo | Por qué no |
|---------|-----------|
| `graphiti_core/embedder/client.py` | `EMBEDDING_DIM=1024` es global para todos los embedders. Override solo en `GeminiEmbedderConfig` |
| `graphiti_core/helpers.py` | Ya tiene `normalize_l2()` que reutilizamos — no hace falta tocar |
| `graphiti_core/nodes.py` | Campos duales son Fase 2, no mezclar |
| `graphiti_core/edges.py` | Igual |

**Cambios concretos en `gemini.py`:**

```python
# 1.1 — Modelo default (1 línea)
DEFAULT_EMBEDDING_MODEL = 'gemini-embedding-001'  # [FORK] Upgraded from text-embedding-001

# 1.2 — Enum de task types (~15 líneas)
class GeminiTaskType(str, Enum):  # [FORK]
    RETRIEVAL_QUERY = 'RETRIEVAL_QUERY'
    RETRIEVAL_DOCUMENT = 'RETRIEVAL_DOCUMENT'
    CODE_RETRIEVAL_QUERY = 'CODE_RETRIEVAL_QUERY'
    SEMANTIC_SIMILARITY = 'SEMANTIC_SIMILARITY'
    CLASSIFICATION = 'CLASSIFICATION'
    CLUSTERING = 'CLUSTERING'
    QUESTION_ANSWERING = 'QUESTION_ANSWERING'
    FACT_VERIFICATION = 'FACT_VERIFICATION'

# 1.3 — Config con override de dimensión y task_type (~3 líneas)
class GeminiEmbedderConfig(EmbedderConfig):
    embedding_model: str = Field(default=DEFAULT_EMBEDDING_MODEL)
    embedding_dim: int = Field(default=3072)  # [FORK] Override Gemini to 3072D
    api_key: str | None = None
    task_type: GeminiTaskType | None = Field(default=None)  # [FORK]

# 1.4 — Normalización y task_type en create() (~10 líneas)
async def create(self, input_data, task_type=None) -> list[float]:
    effective_task_type = task_type or self.config.task_type
    config_params = {'output_dimensionality': self.config.embedding_dim}
    if effective_task_type:
        config_params['task_type'] = str(effective_task_type)
    result = await self.client.aio.models.embed_content(
        model=..., contents=[input_data],
        config=types.EmbedContentConfig(**config_params),
    )
    embedding = result.embeddings[0].values
    # [FORK] Normalize for dim < 3072 (Google only pre-normalizes 3072D)
    if self.config.embedding_dim < 3072:
        from graphiti_core.helpers import normalize_l2
        embedding = normalize_l2(embedding).tolist()
    return embedding
```

**Compatibilidad upstream:**
- Todos los cambios marcados con `# [FORK]`
- `task_type=None` por defecto → comportamiento upstream intacto
- Normalización solo aplica cuando `dim < 3072` → 3072D se comporta igual que antes
- Si upstream mergea `gemini-improvements`: conflicto solo en este archivo, resolución ~5 min
- Validación de modelo con task_type: warning si el modelo no soporta task_types

---

#### FASE 2: Campos Duales (Experimental)
**Documento**: [PLAN-EMBEDDINGS-GEMINI-AVANZADO.md](./PLAN-EMBEDDINGS-GEMINI-AVANZADO.md) - Sección 5
**Duración estimada**: 1-2 días
**Prerequisito para**: Fase 3

**Objetivo**: Permitir experimentación A/B manteniendo embeddings actuales funcionando.
"Primero hacerlo duplicado y hacer pruebas para ver si merece la pena" — Pepo.

**Archivos modificados:**

| Archivo | Cambio |
|---------|--------|
| `graphiti_core/nodes.py` | Campo `name_embedding_enhanced: list[float] \| None = Field(default=None)` |
| `graphiti_core/edges.py` | Campo `fact_embedding_enhanced: list[float] \| None = Field(default=None)` |
| `graphiti_core/search/search_utils.py` | Función selector `# [FORK]`: usar enhanced si existe, fallback a standard |
| Script Neo4j o `graph_queries.py` | Índice vector separado: `CREATE VECTOR INDEX ... OPTIONS {vector.dimensions: 3072}` |

**Cómo funciona la generación dual:**
```python
# En EntityNode.generate_name_embedding():
# 1. Genera embedding standard (comportamiento upstream intacto)
self.name_embedding = await embedder.create(input_data=[text])
# 2. Si embedder es Gemini con config enhanced, genera 3072D también
if hasattr(embedder, 'config') and hasattr(embedder.config, 'task_type'):
    self.name_embedding_enhanced = await embedder.create(
        input_data=[text],
        task_type='RETRIEVAL_DOCUMENT'
    )
```

**Compatibilidad upstream:**
- Campos con `default=None` → Neo4j ignora si no se usan
- Upstream no tiene campos `*_enhanced` → no puede conflictear
- Si upstream elimina `GraphOperationsInterface` (gemini-improvements): irrelevante,
  nuestros campos son propiedades Pydantic, no métodos de interfaz

**Riesgo con upstream/chore/gemini-improvements:**
- `nodes.py` y `edges.py` cambian mucho en esa rama (eliminan métodos de interfaz)
- Pero nuestros cambios son **adiciones al modelo** (campos), no a los métodos
- Git merge: upstream reorganiza métodos + nosotros añadimos campos = sin conflicto real

---

#### FASE 3: Reprocesamiento de Embeddings
**Duración estimada**: Variable (depende de volumen de datos)
**Prerequisito para**: Fase 4

**Objetivo**: Regenerar embeddings existentes a 3072D con task_type en los campos `*_enhanced`.

**Scripts a crear (todos son archivos nuevos, 0 conflicto):**
```
scripts/
  +-- pepo-reprocess-embeddings.py    # Lee nodos/edges de Neo4j, regenera a 3072D
  +-- pepo-backup-neo4j.py            # Dump de embeddings antes de migrar
```

**Características:**
- `--dry-run` para previsualizar sin ejecutar
- Coste: $0 (Gemini embeddings API es gratuita)
- Velocidad: ~100ms/embedding → 1000 nodos en ~10 min
- Escribe SOLO en `*_enhanced`, no toca embeddings originales
- Standalone: conecta directamente a Neo4j, no depende de MCP server

---

#### FASE 4: Evaluación y Decisión
**Duración estimada**: 1-2 días

**Objetivo**: Comparar calidad `name_embedding` (1024D) vs `name_embedding_enhanced` (3072D + task_type).

**Scripts a crear:**
```
scripts/
  +-- pepo-evaluate-embeddings.py     # Comparar calidad de búsqueda
  +-- pepo-benchmark-search.py        # Benchmark de latencia y precisión
```

**Métricas:**
- Recall@10 en búsquedas semánticas
- Precisión en deduplicación (SEMANTIC_SIMILARITY)
- Calidad de búsqueda de código (CODE_RETRIEVAL_QUERY vs genérico)
- Almacenamiento Neo4j (3072D = ~3x más espacio)
- Latencia de generación y búsqueda

**Decisión resultante:**
| Resultado | Acción |
|-----------|--------|
| 3072D mejora significativamente | Migrar `name_embedding` a 3072D, eliminar `*_enhanced` |
| No mejora | Quedarse con 1024D, usar task_types solo donde aporte |
| Mejora solo para ciertos tipos | Config per entity type (idea Matryoshka) |

---

#### FASE 5: Release pepo-v1.0
**Duración estimada**: 2-4 horas

**Tareas:**
- [ ] Merge todas las feature branches a main
- [ ] Actualizar CHANGELOG-FORK.md
- [ ] Crear tag `pepo-v1.0`
- [ ] Documentar en README diferencias con upstream

---

## 4. Sistema de Documentación y Trazabilidad

### 4.1 Estructura de Documentación

```
docs/
  +-- projects/
  |     +-- PLAN-MAESTRO-MEJORAS-GRAPHITI.md    # Este documento
  |     +-- PLAN-EMBEDDINGS-GEMINI-AVANZADO.md  # Plan específico
  |     +-- PROYECTO-EMBEDDINGS-MATRYOSHKA.md   # Explicación técnica
  |
  +-- deployment/
  |     +-- GUIA-AURADB-FREE.md
  |     +-- GUIA-DOCKER-LOCAL.md
  |     +-- SCRIPT-SYNC.md
  |     +-- SYNC-ARCHITECTURE.md
  |
  +-- decisions/                                 # NUEVO
  |     +-- ADR-001-embedding-dimension.md
  |     +-- ADR-002-task-types.md
  |     +-- ADR-003-dual-fields.md
  |
  +-- changelog/                                 # NUEVO
        +-- CHANGELOG-FORK.md
        +-- CHANGELOG-UPSTREAM-SYNC.md
```

### 4.2 Formato de Architecture Decision Records (ADR)

```markdown
# ADR-XXX: Título de la Decisión

## Estado
Propuesto | Aceptado | Deprecado | Reemplazado por ADR-YYY

## Contexto
Descripción del problema o necesidad que requiere una decisión.

## Decisión
La decisión tomada y su justificación.

## Consecuencias
- Positivas: ...
- Negativas: ...
- Riesgos: ...

## Alternativas Consideradas
1. Alternativa A: ...
2. Alternativa B: ...

## Referencias
- Links a documentos, issues, PRs relacionados
```

### 4.3 CHANGELOG-FORK.md (Template)

```markdown
# Changelog del Fork (pepo1275/graphiti)

Este archivo documenta los cambios específicos de este fork respecto a upstream.

## [Unreleased]

### Added
- [FORK] Campos `name_embedding_enhanced` en EntityNode
- [FORK] Soporte para task_type en GeminiEmbedder
- [FORK] Scripts de reprocesamiento en scripts/pepo-*

### Changed
- [FORK] Default embedding_dim cambiado a 3072 (configurable)
- [FORK] Normalización automática para embeddings < 3072D

### Fixed
- [FORK] Bug de normalización en embeddings Gemini < 3072D

### Upstream Syncs
- 2026-01-31: Sincronizado con upstream c36723c (40 commits)

## [pepo-v1.0] - 2026-XX-XX

### Added
- Versión inicial del fork con mejoras de embeddings
```

### 4.4 Convenciones de Commits

```
# Prefijos para commits del fork
[FORK] feat: Add enhanced embedding fields
[FORK] fix: Normalize embeddings < 3072D
[FORK] docs: Add ADR for embedding dimension
[FORK] scripts: Add reprocessing script

# Prefijos para syncs con upstream
[SYNC] Merge upstream/main (c36723c)
[SYNC] Resolve conflicts in nodes.py
```

---

## 5. Checklist de Compatibilidad

### 5.1 Antes de cada cambio

- [ ] El cambio es aditivo (no modifica comportamiento existente)?
- [ ] Si modifica comportamiento, hay flag para desactivar?
- [ ] El default mantiene comportamiento upstream?
- [ ] Los tests existentes siguen pasando?
- [ ] Está documentado en CHANGELOG-FORK.md?
- [ ] Si es decisión arquitectónica, hay ADR?

### 5.2 Antes de sync con upstream

- [ ] Backup del estado actual creado?
- [ ] Feature branches rebased sobre main?
- [ ] Lista de archivos que pueden conflictuar revisada?
- [ ] Plan de resolución de conflictos definido?

### 5.3 Antes de release

- [ ] Todos los tests pasan?
- [ ] CHANGELOG-FORK.md actualizado?
- [ ] README documenta diferencias con upstream?
- [ ] Tag creado con formato pepo-vX.Y?

---

## 6. Próximos Pasos Inmediatos

### 6.1 Orden de Ejecución Recomendado

```
1. [HOY] Crear estructura de documentación
   - docs/decisions/
   - docs/changelog/CHANGELOG-FORK.md

2. [HOY] Crear ADR-001 para decisión de embeddings

3. [SIGUIENTE] FASE 0: Sync con upstream
   - Resolver conflictos
   - Verificar tests

4. [DESPUÉS] FASE 1: Fix normalización
   - Implementar con flag configurable
   - Tests

5. [CONTINUAR] Fases 2-6 según plan
```

### 6.2 Comandos para Empezar

```bash
# 1. Crear estructura de documentación
mkdir -p docs/decisions docs/changelog

# 2. Crear CHANGELOG-FORK.md
touch docs/changelog/CHANGELOG-FORK.md

# 3. Backup antes de sync
git checkout main
git branch backup-pre-sync-$(date +%Y%m%d)

# 4. Iniciar sync
git fetch upstream
git merge upstream/main
# Resolver conflictos...
```

---

## 7. Matriz de Riesgos del Plan Completo

### 7.1 Riesgos Generales

| Riesgo | Prob. | Impacto | Mitigación |
|--------|-------|---------|------------|
| Conflictos complejos en sync | Alta | Medio | Backup + feature branches |
| Regresión en búsquedas | Media | Alto | Tests A/B, rollback plan |
| Upstream cambia embedder | Baja | Alto | Flags configurables, ADRs |
| Pérdida de trazabilidad | Media | Medio | CHANGELOG obligatorio |
| Incompatibilidad futura | Media | Alto | Principio de cambios aditivos |

### 7.2 ⚠️ RIESGO CRÍTICO: upstream/chore/gemini-improvements

**Rama upstream no mergeada** que contiene un refactor mayor de Graphiti (188 archivos, -24,000 líneas neto).
**Detección automática**: `scripts/check-upstream-impact.sh`
**Documentación detallada**: [CHANGELOG-FORK.md — Upstream Watch Flags](../changelog/CHANGELOG-FORK.md)

#### Impactos clasificados por severidad

| Impacto | Severidad | Qué pasa | Acción requerida |
|---------|-----------|----------|-----------------|
| **MCP Server reescrito** | 🔴 Alta | `mcp_server/src/` eliminado, nuevo flat file | Adaptar docker-compose, migrar config YAML→ENV |
| **Embedder factory sin Gemini** | 🔴 Alta | `create_client()` solo soporta OpenAI/Azure | Añadir path Gemini con detección de GOOGLE_API_KEY |
| **Entity Types hardcoded** | 🟡 Media | Solo 3 tipos (Requirement/Preference/Procedure) | Crear loader extensible para nuestros 19 tipos |
| **Tool renombrada** | 🟡 Media | `search_nodes` → `search_memory_nodes` | Actualizar CLAUDE.md y prompts |
| **Interfaces eliminadas** | 🟡 Media | GraphOperationsInterface + SearchInterface gone | Nuestros campos duales no dependen de ellas |
| **Gemini embedder simplificado** | 🟢 Baja | Constructor reducido, batch simplificado | Nuestros cambios son aditivos, conflicto solo en gemini.py |
| **Content chunking eliminado** | 🟢 Baja | `content_chunking.py` removido | No afecta nuestro plan de embeddings |

#### Principio de mitigación

> **"Un solo archivo de conflicto"**: Si upstream mergea gemini-improvements,
> el ÚNICO archivo donde tendremos conflicto real en Fase 1 es `gemini.py`.
> Todo lo demás son archivos nuevos nuestros o campos con `default=None`.
> La adaptación del MCP server es trabajo separado (4-8h).

#### Señales de que upstream está por mergear

1. PR abierto desde `chore/gemini-improvements` a `main`
2. Actividad reciente en la rama (últimos 7 días)
3. Bump de versión en `pyproject.toml` a nueva major
4. Changelog de upstream menciona "v2" o "breaking changes"

---

## 8. Referencias

### Documentos Relacionados
- [PLAN-EMBEDDINGS-GEMINI-AVANZADO.md](./PLAN-EMBEDDINGS-GEMINI-AVANZADO.md)
- [PROYECTO-EMBEDDINGS-MATRYOSHKA.md](./PROYECTO-EMBEDDINGS-MATRYOSHKA.md)
- [GUIA-DOCKER-LOCAL.md](../deployment/GUIA-DOCKER-LOCAL.md)
- [GUIA-AURADB-FREE.md](../deployment/GUIA-AURADB-FREE.md)

### Links Externos
- [Upstream Graphiti](https://github.com/getzep/graphiti)
- [Gemini Embedding API](https://ai.google.dev/gemini-api/docs/embeddings)
- [ADR Template](https://adr.github.io/)

---

**Siguiente paso**: Crear estructura de documentación y ADR-001 para la decisión de embeddings.
