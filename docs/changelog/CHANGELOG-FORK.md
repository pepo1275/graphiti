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
- [CONFIG] CLAUDE.md con instrucciones para Claude Code
- [CONFIG] Configuración de memoria para Claude Desktop en `mcp_server/config/`

### Changed (CI/CD - Fase -1)
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

### Planned (Pendiente de implementación)
- [FORK] Soporte para task_type en GeminiEmbedder
- [FORK] Normalización automática de embeddings < 3072D
- [FORK] Campos duales de embeddings para experimentación A/B
- [FORK] Scripts de reprocesamiento de embeddings

### Upstream Pending
- Sincronización pendiente con upstream (40 commits atrás)
- Último commit local: 6c9824b
- Último commit upstream: c36723c

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

| Fecha | Commit Upstream | Commit Fork | Conflictos |
|-------|-----------------|-------------|------------|
| 2025-12-09 | 6dc7b88 | 6c9824b | Ninguno (fork inicial) |
| Pendiente | c36723c | - | Por determinar |

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
- [Upstream Graphiti](https://github.com/getzep/graphiti)
