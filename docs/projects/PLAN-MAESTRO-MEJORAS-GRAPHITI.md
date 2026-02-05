# Plan Maestro: Mejoras de Graphiti Fork

**Estado**: Propuesta para revisión
**Autor**: Pepo + Claude
**Fecha**: 2026-01-31
**Versión**: 1.0

---

## 1. Visión General

### 1.1 Objetivo

Mantener un fork de Graphiti que:
1. **Sea compatible con upstream** - Poder hacer merge de mejoras de getzep/graphiti
2. **Incluya mejoras propias** - Embeddings avanzados, configuraciones personalizadas
3. **Esté documentado** - Trazabilidad completa de cambios y decisiones
4. **Sea desplegable** - En múltiples entornos (local, AuraDB, Docker)

### 1.2 Estado Actual

```
getzep/graphiti (upstream)     pepo1275/graphiti (fork)
         |                              |
    c36723c (actual)              6c9824b (40 commits atrás)
         |                              |
         |                     +-- Configs personalizadas
         |                     +-- CLAUDE.md
         |                     +-- Docs de deployment
         |                     +-- Entity Types personalizados
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

| Archivo | Estrategia |
|---------|------------|
| `graphiti_core/embedder/gemini.py` | Cambios aditivos con flags |
| `graphiti_core/embedder/client.py` | Mantener compatibilidad |
| `graphiti_core/nodes.py` | Campos opcionales nuevos |
| `graphiti_core/edges.py` | Campos opcionales nuevos |
| `pyproject.toml` | Solo añadir deps si necesario |

---

## 3. Roadmap de Mejoras

### 3.1 Diagrama de Dependencias

```
+------------------+
|  FASE -1         |
|  Preparar CI/CD  |  <-- NUEVO: Resolver problemas de workflows
+--------+---------+
         |
         v
+------------------+
|  FASE 0          |
|  Sync Upstream   |
+--------+---------+
         |
         v
+------------------+     +------------------+
|  FASE 1          |     |  FASE 2          |
|  Fix Embeddings  +---->+  Task Types      |
|  (Normalización) |     |  (Gemini API)    |
+--------+---------+     +--------+---------+
         |                        |
         v                        v
+------------------+     +------------------+
|  FASE 3          |     |  FASE 4          |
|  Campos Duales   +---->+  Reprocesar      |
|  (Experimental)  |     |  Embeddings      |
+--------+---------+     +--------+---------+
         |                        |
         +------------+-----------+
                      |
                      v
              +------------------+
              |  FASE 5          |
              |  Evaluación      |
              |  y Decisión      |
              +------------------+
                      |
                      v
              +------------------+
              |  FASE 6          |
              |  Release         |
              |  pepo-v1.0       |
              +------------------+
```

### 3.2 Detalle de Fases

#### FASE 0: Sincronización con Upstream
**Documento**: N/A (proceso técnico)
**Duración estimada**: 2-4 horas
**Prerequisito para**: Todas las demás fases

**Tareas:**
- [ ] Backup del estado actual
- [ ] Merge upstream/main -> main
- [ ] Resolver conflictos en mcp_server/config/
- [ ] Verificar que tests pasan
- [ ] Documentar cambios importantes de upstream

**Criterio de aceptación:**
- `make test` pasa
- Configs personalizadas preservadas
- CHANGELOG-FORK.md actualizado

---

#### FASE 1: Fix Embeddings (Normalización)
**Documento**: [PLAN-EMBEDDINGS-GEMINI-AVANZADO.md](./PLAN-EMBEDDINGS-GEMINI-AVANZADO.md) - Sección 3
**Duración estimada**: 2-4 horas
**Prerequisito para**: Fase 2, 3

**Cambios en código:**
```python
# graphiti_core/embedder/gemini.py
# Añadir normalización condicional

NORMALIZE_EMBEDDINGS = os.getenv('GRAPHITI_NORMALIZE_EMBEDDINGS', 'true').lower() == 'true'

def _normalize(self, embedding: list[float]) -> list[float]:
    import numpy as np
    arr = np.array(embedding)
    norm = np.linalg.norm(arr)
    return (arr / norm).tolist() if norm > 0 else embedding

# En create():
if NORMALIZE_EMBEDDINGS and self.config.embedding_dim < 3072:
    embedding = self._normalize(embedding)
```

**Compatibilidad upstream:**
- Flag `GRAPHITI_NORMALIZE_EMBEDDINGS=true` (default)
- Si upstream añade normalización, desactivar con `false`

---

#### FASE 2: Task Types de Gemini
**Documento**: [PLAN-EMBEDDINGS-GEMINI-AVANZADO.md](./PLAN-EMBEDDINGS-GEMINI-AVANZADO.md) - Sección 2
**Duración estimada**: 4-6 horas
**Prerequisito para**: Fase 3

**Cambios en código:**
```python
# graphiti_core/embedder/gemini.py

class GeminiTaskType(str, Enum):
    RETRIEVAL_QUERY = "RETRIEVAL_QUERY"
    RETRIEVAL_DOCUMENT = "RETRIEVAL_DOCUMENT"
    CODE_RETRIEVAL_QUERY = "CODE_RETRIEVAL_QUERY"
    # ... resto

class GeminiEmbedderConfig(EmbedderConfig):
    # Campos existentes...
    task_type: str | None = Field(default=None)  # NUEVO, opcional
```

**Compatibilidad upstream:**
- `task_type=None` por defecto (comportamiento upstream)
- Solo se usa si se configura explícitamente

---

#### FASE 3: Campos Duales (Experimental)
**Documento**: [PLAN-EMBEDDINGS-GEMINI-AVANZADO.md](./PLAN-EMBEDDINGS-GEMINI-AVANZADO.md) - Sección 5
**Duración estimada**: 1-2 días
**Prerequisito para**: Fase 4

**Cambios en código:**
```python
# graphiti_core/nodes.py

class EntityNode(BaseModel):
    # Campos existentes (upstream)
    name_embedding: list[float] | None = Field(...)

    # Campos nuevos (fork) - OPCIONALES
    name_embedding_enhanced: list[float] | None = Field(
        default=None,
        description='[FORK] Enhanced embedding at 3072D with task_type'
    )
    name_embedding_config: dict | None = Field(
        default=None,
        description='[FORK] Config used for enhanced embedding'
    )
```

**Compatibilidad upstream:**
- Campos marcados con `[FORK]` en descripción
- Default `None` - no afecta comportamiento existente
- Neo4j ignora propiedades no usadas

---

#### FASE 4: Reprocesamiento de Embeddings
**Documento**: [PLAN-EMBEDDINGS-GEMINI-AVANZADO.md](./PLAN-EMBEDDINGS-GEMINI-AVANZADO.md) - Sección 4
**Duración estimada**: Variable (depende de datos)
**Prerequisito para**: Fase 5

**Scripts a crear:**
```
scripts/
  +-- pepo-reprocess-embeddings.py    # Regenerar embeddings
  +-- pepo-backup-neo4j.py            # Backup antes de migrar
  +-- pepo-validate-embeddings.py     # Validar integridad
```

**Compatibilidad upstream:**
- Scripts en directorio separado con prefijo `pepo-`
- No modifican comportamiento de graphiti_core

---

#### FASE 5: Evaluación y Decisión
**Documento**: [PLAN-EMBEDDINGS-GEMINI-AVANZADO.md](./PLAN-EMBEDDINGS-GEMINI-AVANZADO.md) - Sección 5
**Duración estimada**: 1-2 días

**Scripts a crear:**
```
scripts/
  +-- pepo-evaluate-embeddings.py     # Comparar calidad
  +-- pepo-benchmark-search.py        # Benchmark de búsqueda
```

**Métricas a evaluar:**
- Recall@10 en búsquedas
- Precisión en deduplicación
- Tiempo de generación
- Almacenamiento

---

#### FASE 6: Release pepo-v1.0
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

| Riesgo | Prob. | Impacto | Mitigación |
|--------|-------|---------|------------|
| Conflictos complejos en sync | Alta | Medio | Backup + feature branches |
| Regresión en búsquedas | Media | Alto | Tests A/B, rollback plan |
| Upstream cambia embedder | Baja | Alto | Flags configurables, ADRs |
| Pérdida de trazabilidad | Media | Medio | CHANGELOG obligatorio |
| Incompatibilidad futura | Media | Alto | Principio de cambios aditivos |

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
