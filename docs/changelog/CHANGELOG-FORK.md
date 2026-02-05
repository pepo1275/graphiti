# Changelog del Fork (pepo1275/graphiti)

Este archivo documenta los cambios específicos de este fork respecto a [upstream getzep/graphiti](https://github.com/getzep/graphiti).

## Convenciones

- **[FORK]**: Cambios específicos del fork
- **[SYNC]**: Sincronizaciones con upstream
- **[CONFIG]**: Cambios de configuración
- **[DOCS]**: Documentación

---

## [Unreleased]

### Added
- [DOCS] Sistema de documentación de proyectos en `docs/projects/`
- [DOCS] Guías de deployment en `docs/deployment/`
- [DOCS] Architecture Decision Records en `docs/decisions/`
- [DOCS] Análisis de problemas CI/CD en `docs/projects/PROBLEMAS-CI-CD-FORK.md`
- [DOCS] Tests POST con criterios de aceptación en `docs/projects/TESTS-POST-CRITERIOS-ACEPTACION.md`
- [CONFIG] CLAUDE.md con instrucciones para Claude Code
- [CONFIG] Configuración de memoria para Claude Desktop en `mcp_server/config/`
- [FORK] Script de detección de cambios upstream: `scripts/check-upstream-impact.sh`

### Changed (CI/CD - Fase -1) — Commit 983f848
- [FORK] `unit_tests.yml`: Runner cambiado de `depot-ubuntu-22.04` a `ubuntu-22.04`
- [FORK] `lint.yml`: Runner cambiado de `depot-ubuntu-22.04` a `ubuntu-22.04`
- [FORK] `typecheck.yml`: Runner cambiado de `depot-ubuntu-22.04` a `ubuntu-22.04`
- [FORK] Workflows desactivados movidos a `.github/workflows-upstream-disabled/`:
  - `cla.yml` (requiere DANIEL_PAT - token personal de Zep)
  - `claude-code-review.yml` (requiere ANTHROPIC_API_KEY de Zep)
  - `claude-code-review-manual.yml` (requiere ANTHROPIC_API_KEY de Zep)
  - `claude.yml` (requiere ANTHROPIC_API_KEY de Zep)
  - `release-mcp-server.yml` (requiere DOCKERHUB secrets de Zep)
  - `release-server-container.yml` (requiere DOCKERHUB secrets de Zep)
  - `release-graphiti-core.yml` (publica a PyPI bajo namespace de Zep)

### Changed (Sync Upstream - Fase 0) — Commit 9e6b2a0
- [SYNC] Merge upstream/main (affca93) — 53 archivos, 0 conflictos
- [SYNC] Git rename tracking aplicó cambios upstream a workflows renombrados automáticamente
- [FORK] Remote origin cambiado de HTTPS a SSH (OAuth scope fix)
- [FORK] Ruff formatting aplicado a 4 archivos upstream post-merge (ac21101)

### Planned (Pendiente de implementación)
- [FORK] Soporte para task_type en GeminiEmbedder (Fase 1-2)
- [FORK] Normalización automática de embeddings < 3072D (Fase 1)
- [FORK] Cambio modelo default a gemini-embedding-001 (Fase 1)
- [FORK] Campos duales de embeddings para experimentación A/B (Fase 3)
- [FORK] Scripts de reprocesamiento de embeddings (Fase 4)

### Upstream Synced
- Sincronizado con upstream el 2026-02-05
- Commit upstream: affca93
- Commit merge: 9e6b2a0

---

## ⚠️ UPSTREAM WATCH FLAGS

Ramas de upstream que, al ser mergeadas a main, impactarán nuestro fork.
Ejecutar `scripts/check-upstream-impact.sh` para verificar automáticamente.

### FLAG: UPSTREAM-MCP-REFACTOR (upstream/chore/gemini-improvements)

**Estado**: 🔴 ACTIVO — No mergeado a upstream/main
**Última verificación**: 2026-02-05
**Rama**: `upstream/chore/gemini-improvements` (188 archivos, -24,000 líneas neto)

**¿Qué es?** Un refactor mayor de Graphiti. No solo mejoras de Gemini — es probablemente la próxima versión major.

**Impactos en nuestro fork:**

#### 1. MCP Server — Reescritura total
- `mcp_server/src/` → eliminado completamente
- Nuevo archivo flat: `mcp_server/graphiti_mcp_server.py` (1251 líneas)
- `config/*.yaml` eliminados → configuración por ENV vars + CLI args
- Docker simplificado: 1 Dockerfile, 1 docker-compose.yml
- **Acción**: Adaptar `docker-compose-claude-memory.yml` al nuevo layout
- **Acción**: Migrar config YAML a ENV vars o crear wrapper

#### 2. MCP Tools — Renombradas y nuevas
| Tool actual | Tool nueva | ¿Breaking? |
|-------------|-----------|------------|
| `search_nodes` | `search_memory_nodes` | ⚠️ SÍ |
| `add_memory` | `add_memory` | ✅ No |
| `search_memory_facts` | `search_memory_facts` | ✅ No |
| — | `get_entity_edge` | Nueva |
| — | `get_episodes` | Nueva |
| — | `get_status` | Nueva (resource) |
- **Acción**: Actualizar CLAUDE.md y cualquier prompt que use `search_nodes`

#### 3. Embedder Factory — Sin soporte Gemini
- `GraphitiEmbedderConfig.create_client()` solo genera `OpenAIEmbedder` o `AzureOpenAIEmbedderClient`
- **No hay path para GeminiEmbedder**
- **Acción**: Añadir factory path para Gemini con detección de `GOOGLE_API_KEY`

#### 4. Entity Types — Hardcoded a 3
- Nuevo server tiene solo: `Requirement`, `Preference`, `Procedure`
- Nuestro config tiene 19 entity types personalizados
- **Acción**: Crear mecanismo de extensión o mantener nuestro loader

#### 5. Core Architecture — Eliminaciones masivas
- `GraphOperationsInterface` eliminada (acabamos de integrar)
- `SearchInterface` eliminada
- Neptune driver eliminado
- Kuzu driver eliminado
- OpenTelemetry eliminado
- `content_chunking.py` eliminado (acabamos de traer)
- **Impacto**: Nuestros cambios aditivos en nodes/edges deben adaptarse a la nueva arquitectura simplificada
- **Positivo**: Menos código = menos superficie de conflicto

#### 6. Gemini Embedder — Simplificado
- Constructor reducido (sin batch_size, sin client param)
- Modelo default cambiado a `embedding-001`
- Batch processing simplificado (sin fallback individual)
- **Nuestros cambios (task_type, normalización) siguen siendo compatibles** — conflicto limitado a `gemini.py`

**Estimación de adaptación**: 4-8 horas cuando se active

---

## [pepo-v0.1] - 2025-12-09

### Added
- [FORK] Fork inicial desde getzep/graphiti
- [CONFIG] Configuración personalizada para memoria de Claude
- [CONFIG] Entity Types personalizados (19 tipos)
- [DOCS] CLAUDE.md inicial
- [DOCS] Checkpoints de desarrollo

### Configuration
- Embedder: Gemini (gemini-embedding-001)
- LLM: Gemini
- Reranker: OpenAI (workaround por incompatibilidad)
- Neo4j: Puerto 7476 (local)

---

## Historial de Sincronizaciones con Upstream

| Fecha | Commit Upstream | Commit Fork | Conflictos | Notas |
|-------|-----------------|-------------|------------|-------|
| 2025-12-09 | 6dc7b88 | 6c9824b | Ninguno | Fork inicial |
| 2026-02-05 | affca93 | 9e6b2a0 | 0 (auto-merge) | 53 archivos, rename tracking OK |

---

## Notas de Compatibilidad

### Archivos que difieren de upstream
- `CLAUDE.md` - Solo existe en fork
- `.claude/` - Solo existe en fork
- `docs/projects/` - Solo existe en fork
- `docs/deployment/` - Solo existe en fork
- `docs/decisions/` - Solo existe en fork
- `docs/changelog/` - Solo existe en fork
- `checkpoints/` - Solo existe en fork
- `mcp_server/config/config-claude-memory.yaml` - Config personalizada
- `.github/workflows-upstream-disabled/` - Workflows desactivados
- `.github/workflows/unit_tests.yml` - Runner modificado
- `.github/workflows/lint.yml` - Runner modificado
- `.github/workflows/typecheck.yml` - Runner modificado

### Variables de entorno del fork
```bash
# Próximas (no implementadas aún)
GRAPHITI_NORMALIZE_EMBEDDINGS=true  # Normalizar embeddings < 3072D
GRAPHITI_EMBEDDING_DIM=3072         # Dimensión de embeddings
GRAPHITI_TASK_TYPE=RETRIEVAL_DOCUMENT  # Task type de Gemini
```

---

## Referencias

- [Plan Maestro de Mejoras](../projects/PLAN-MAESTRO-MEJORAS-GRAPHITI.md)
- [Plan de Embeddings Avanzado](../projects/PLAN-EMBEDDINGS-GEMINI-AVANZADO.md)
- [Tests POST y Criterios de Aceptación](../projects/TESTS-POST-CRITERIOS-ACEPTACION.md)
- [Upstream Graphiti](https://github.com/getzep/graphiti)
- Script de detección: `scripts/check-upstream-impact.sh`
