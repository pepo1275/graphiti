# 🚀 ESTRATEGIA DE MIGRACIÓN LIMPIA: GRAPHITI-PRODUCTION

## 📋 PATRÓN OBSERVADO EN LLM-GRAPH-BUILDER

### Estructura exitosa anterior:
```
/Users/pepo/Dev/llm-graph-builder/              # Repo principal (para experimentar)
├── .git/                                       # Git del repo original/upstream
├── ...archivos del proyecto...
└── llm-graph-builder-production/               # Subdirectorio LIMPIO
    ├── .git/                                   # Git propio conectado a tu fork
    ├── ...archivos organizados y limpios...
    └── estructura de producción
```

### Configuración git en producción:
- `origin`: `git@github.com:pepo1275/llm-graph-builder.git` (tu fork)
- `upstream`: `https://github.com/neo4j-labs/llm-graph-builder.git` (repo original)

---

## 🎯 ESTRATEGIA PARA GRAPHITI

### PASO 1: Crear estructura similar
```
/Users/pepo/Dev/graphiti/                       # Nuevo directorio principal
├── graphiti-research/                          # Para experimentar (repo actual)
└── graphiti-production/                        # Repo LIMPIO conectado a tu fork
```

### PASO 2: Configuración git objetivo
```bash
# En graphiti-production/
git remote add origin git@github.com:pepo1275/graphiti.git
git remote add upstream https://github.com/getzep/graphiti.git
```

---

## 📊 INVENTARIO DE CAMBIOS ACTUALES

### CATEGORÍA A: Metodología (MIGRAR PRIMERO) ✅
```
CLAUDE.md                                       # → graphiti-production/
docs/DEVELOPMENT_METHODOLOGY.md                 # → graphiti-production/docs/
docs/CHECKPOINTS.md                            # → graphiti-production/docs/
docs/INDEX.md                                  # → graphiti-production/docs/
.claude/check_methodology.py                   # → graphiti-production/.claude/
.claude/pre-commit-validator.sh               # → graphiti-production/.claude/
```

### CATEGORÍA B: Investigación Backup (MIGRAR SEGUNDO) 📚
```
docs/BACKUP_MODULE_INVESTIGATION.md            # → graphiti-production/docs/
docs/BACKUP_OPTIONS_ANALYSIS.md               # → graphiti-production/docs/
/Users/pepo/Downloads/graphiti_backup_plan_2025.md  # → docs/backup/
```

### CATEGORÍA C: Cambios en Core (REVISAR Y MIGRAR) ⚠️
```
graphiti_core/embedder/gemini.py              # +100 líneas sin documentar
```
**Acción**: Revisar línea por línea, documentar, crear tests

### CATEGORÍA D: Tests de Retrieval (ORGANIZAR) 🧪
```
test_code_retrieval_comparison.py
test_code_retrieval_fast.py
test_code_retrieval_mcp.py
test_code_retrieval_query_implementation.py
test_code_retrieval_real.py
test_code_retrieval_simple.py
```
**Acción**: Crear `tests/evaluation/` directory

### CATEGORÍA E: Reportes (ARCHIVAR) 📋
```
CODE_RETRIEVAL_QUERY_STATUS_COMPLETE.md
code_retrieval_report_20250723_*.md
code_retrieval_test_20250723_*.json
mcp_*.md
mcp_*.cypher  
mcp_*.json
```
**Acción**: Crear `archive/evaluations/` directory

---

## 🚀 PLAN DE MIGRACIÓN PASO A PASO

### FASE 1: Preparación (15 minutos)
1. **Crear estructura base**:
   ```bash
   mkdir -p /Users/pepo/Dev/graphiti
   cd /Users/pepo/Dev/graphiti
   
   # Mover repo actual a subdirectorio research
   mv /Users/pepo/graphiti-pepo-local ./graphiti-research
   ```

2. **Crear repo producción limpio**:
   ```bash
   cd /Users/pepo/Dev/graphiti
   git clone https://github.com/getzep/graphiti.git graphiti-production
   cd graphiti-production
   
   # Configurar remotes
   git remote rename origin upstream  
   git remote add origin git@github.com:pepo1275/graphiti.git
   
   # Crear branch de trabajo
   git checkout -b feature/development-methodology
   ```

### FASE 2: Migración Metodología (30 minutos)
```bash
# Copiar archivos de metodología
cp ../graphiti-research/CLAUDE.md ./
mkdir -p docs
cp ../graphiti-research/docs/DEVELOPMENT_METHODOLOGY.md ./docs/
cp ../graphiti-research/docs/CHECKPOINTS.md ./docs/
cp ../graphiti-research/docs/INDEX.md ./docs/

mkdir -p .claude
cp ../graphiti-research/.claude/check_methodology.py ./.claude/
cp ../graphiti-research/.claude/pre-commit-validator.sh ./.claude/

# Actualizar .gitignore
cat ../graphiti-research/.gitignore >> .gitignore
```

**Commit**: `feat: implement development methodology and Claude Code automation`

### FASE 3: Migración Investigación Backup (20 minutos)
```bash
git checkout -b feature/backup-module-investigation

# Crear estructura organizada
mkdir -p docs/backup
cp ../graphiti-research/docs/BACKUP_MODULE_INVESTIGATION.md ./docs/backup/
cp ../graphiti-research/docs/BACKUP_OPTIONS_ANALYSIS.md ./docs/backup/
cp /Users/pepo/Downloads/graphiti_backup_plan_2025.md ./docs/backup/original_plan.md
```

**Commit**: `docs: add backup module investigation and analysis`

### FASE 4: Revisión Cambios Core (60 minutos)
```bash
git checkout -b feature/gemini-embedder-review

# Copiar cambios pero NO commitear aún
cp ../graphiti-research/graphiti_core/embedder/gemini.py ./graphiti_core/embedder/

# REVISAR línea por línea
# DOCUMENTAR cambios  
# CREAR tests
# SOLO ENTONCES commitear
```

### FASE 5: Organización Tests (30 minutos)
```bash
git checkout -b evaluation/retrieval-tests

# Crear estructura organizada
mkdir -p tests/evaluation/retrieval
cp ../graphiti-research/test_code_retrieval_*.py ./tests/evaluation/retrieval/

# Crear README explicativo
```

### FASE 6: Archivo de Reportes (15 minutos)
```bash
git checkout -b archive/evaluation-reports

mkdir -p archive/evaluations/2025-07-23
cp ../graphiti-research/code_retrieval_report_*.md ./archive/evaluations/2025-07-23/
cp ../graphiti-research/code_retrieval_test_*.json ./archive/evaluations/2025-07-23/
cp ../graphiti-research/mcp_*.* ./archive/evaluations/2025-07-23/
```

---

## 🔄 FLUJO DE TRABAJO CONTINUO

### Para nuevos desarrollos:
1. **Experimentar** en `graphiti-research/` (repo actual)
2. **Refinar** cambios con metodología activa
3. **Migrar** cambios probados a `graphiti-production/`
4. **Commitear** en branches específicas
5. **PR** a tu fork desde graphiti-production

### Ventajas de este enfoque:
- ✅ Historia git limpia en producción
- ✅ Separación clara: experiment vs production
- ✅ Fácil sincronización con upstream
- ✅ No se pierde trabajo de investigación
- ✅ Proceso reproducible

---

## 📋 CHECKLIST DE MIGRACIÓN

### Preparación:
- [ ] Crear `/Users/pepo/Dev/graphiti/`
- [ ] Mover repo actual a `graphiti-research/`
- [ ] Clonar repo limpio como `graphiti-production/`
- [ ] Configurar remotes correctamente

### Migración por categorías:
- [ ] Metodología → `feature/development-methodology`
- [ ] Backup investigation → `feature/backup-module-investigation`  
- [ ] Core changes → `feature/gemini-embedder-review` (CON REVISIÓN)
- [ ] Tests → `evaluation/retrieval-tests`
- [ ] Reportes → `archive/evaluation-reports`

### Verificación:
- [ ] Cada branch tiene un propósito claro
- [ ] Commits son atómicos y documentados
- [ ] Tests pasan donde aplique
- [ ] Metodología se aplica automáticamente

---

## 🎯 RESULTADO ESPERADO

```
/Users/pepo/Dev/graphiti/
├── graphiti-research/              # Para experimentar libremente
│   └── (repo actual con todo el trabajo)
└── graphiti-production/            # Para desarrollo limpio y organizado  
    ├── .git → tu fork
    ├── CLAUDE.md
    ├── docs/
    │   ├── DEVELOPMENT_METHODOLOGY.md
    │   └── backup/
    ├── .claude/
    ├── tests/evaluation/
    ├── archive/evaluations/
    └── graphiti_core/ (con cambios revisados)
```

**Estado final**: Repo de producción limpio, organizado, con metodología activa y listo para PRs profesionales a tu fork.