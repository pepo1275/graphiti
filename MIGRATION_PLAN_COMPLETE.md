# 🚀 PLAN COMPLETO DE MIGRACIÓN - OPCIÓN A (SEGURA)

## 📋 CONTEXTO Y DECISIÓN

### Problema identificado:
- Repo actual tiene Docker + MCP + Neo4j corriendo desde `/Users/pepo/graphiti-pepo-local/`
- Mover el directorio rompería configuraciones críticas
- Necesitamos migración limpia sin interrumpir servicios

### Solución adoptada:
**OPCIÓN A**: Crear repo limpio en paralelo, mantener setup actual intacto

---

## 🛡️ ANÁLISIS DE RIESGOS EVITADOS

### ❌ Lo que NO haremos (para evitar problemas):
- ❌ NO mover `/Users/pepo/graphiti-pepo-local/`
- ❌ NO tocar Docker compose activo 
- ❌ NO interrumpir MCP servers
- ❌ NO afectar configuración Claude Desktop existente

### ✅ Lo que SÍ haremos (seguro):
- ✅ Crear nuevo repo en ubicación independiente
- ✅ Migrar cambios por copia, no por movimiento
- ✅ Mantener ambos repos hasta verificar funcionamiento
- ✅ Proceso reversible en cualquier momento

---

## 📅 CRONOGRAMA DE EJECUCIÓN

### **MOMENTO DE REINICIO CLAUDE CODE**: 
🔄 **DESPUÉS DE FASE 1** (crear estructura base)

**¿Por qué ese momento?**
- CLAUDE.md estará en el nuevo repo
- Metodología se cargará automáticamente
- Checkpoints funcionarán desde el primer momento
- Mejor experiencia de desarrollo

---

## 🚀 FASES DETALLADAS

### **FASE 1: Estructura Base (5 minutos)**
**Objetivo**: Crear repo limpio listo para metodología

```bash
# 1. Crear directorio para producción
mkdir -p /Users/pepo/Dev/graphiti-production
cd /Users/pepo/Dev/graphiti-production

# 2. Clonar repo upstream limpio
git clone https://github.com/getzep/graphiti.git .

# 3. Configurar remotes para fork
git remote rename origin upstream
git remote add origin git@github.com:pepo1275/graphiti.git

# 4. Verificar configuración
git remote -v
# upstream  https://github.com/getzep/graphiti.git (fetch)
# upstream  https://github.com/getzep/graphiti.git (push)  
# origin    git@github.com:pepo1275/graphiti.git (fetch)
# origin    git@github.com:pepo1275/graphiti.git (push)

# 5. Verificar branch actual
git branch
# * main
```

**✅ Checkpoint FASE 1**: Repo limpio creado, remotes configurados

**🔄 REINICIAR CLAUDE CODE AQUÍ**
- Cambiar directorio de trabajo a: `/Users/pepo/Dev/graphiti-production`
- CLAUDE.md se cargará automáticamente cuando se migre

---

### **FASE 2: Migración Metodología (30 minutos)**
**Objetivo**: Migrar sistema completo de metodología

```bash
# 1. Crear branch para metodología
git checkout -b feature/development-methodology

# 2. Copiar CLAUDE.md (¡CRÍTICO!)
cp /Users/pepo/graphiti-pepo-local/CLAUDE.md ./

# 3. Copiar documentación metodología
mkdir -p docs
cp /Users/pepo/graphiti-pepo-local/docs/DEVELOPMENT_METHODOLOGY.md ./docs/
cp /Users/pepo/graphiti-pepo-local/docs/CHECKPOINTS.md ./docs/
cp /Users/pepo/graphiti-pepo-local/docs/INDEX.md ./docs/

# 4. Copiar scripts validación
mkdir -p .claude
cp /Users/pepo/graphiti-pepo-local/.claude/check_methodology.py ./.claude/
cp /Users/pepo/graphiti-pepo-local/.claude/pre-commit-validator.sh ./.claude/

# 5. Actualizar .gitignore
cat >> .gitignore << 'EOF'

# Claude Code methodology tracking
.claude/methodology_status.json
.claude/checkpoint_log.json
.claude/temp/
.claude/*.log
EOF

# 6. Commit completo
git add .
git commit -m "feat: implement development methodology and Claude Code automation

- Add CLAUDE.md for automatic instruction loading by Claude Code
- Create comprehensive development methodology (7 phases)
- Add validation scripts and checkpoint system
- Setup .claude/ directory with methodology validators
- Update .gitignore for .claude/ temporary files

This commit establishes a professional development workflow that will be
automatically applied by Claude Code in future sessions. The methodology
includes mandatory checkpoints, validation scripts, and clear documentation
structure.

No functional changes to the codebase are included in this commit."

# 7. Push primera branch
git push -u origin feature/development-methodology
```

**✅ Checkpoint FASE 2**: Metodología migrada, CLAUDE.md activo, checkpoints funcionando

---

### **FASE 3: Investigación Backup (20 minutos)**
**Objetivo**: Migrar documentación completa de backup

```bash
# 1. Branch desde main
git checkout main
git checkout -b feature/backup-investigation

# 2. Crear estructura organizada
mkdir -p docs/backup

# 3. Copiar investigación backup
cp /Users/pepo/graphiti-pepo-local/docs/BACKUP_MODULE_INVESTIGATION.md ./docs/backup/
cp /Users/pepo/graphiti-pepo-local/docs/BACKUP_OPTIONS_ANALYSIS.md ./docs/backup/
cp /Users/pepo/graphiti-pepo-local/docs/TECHNICAL_DECISION_20250123.md ./docs/backup/

# 4. Copiar plan original
cp /Users/pepo/Downloads/graphiti_backup_plan_2025.md ./docs/backup/original_plan.md

# 5. Crear índice backup
cat > docs/backup/README.md << 'EOF'
# Backup Module Investigation

## Overview
Complete investigation and analysis for implementing backup/restore functionality in Graphiti.

## Files
- `BACKUP_MODULE_INVESTIGATION.md`: Detailed module design and architecture
- `BACKUP_OPTIONS_ANALYSIS.md`: Analysis of 4 implementation options with recommendation
- `TECHNICAL_DECISION_20250123.md`: Technical decision record for selective commits
- `original_plan.md`: Original 371-line backup plan that consumed too many tokens

## Status
Investigation complete. Ready for implementation when prioritized.

## Recommendation
Implement Option A: Export/Import Selectivo as MVP (2-4 hours estimated).
EOF

# 6. Commit investigación
git add docs/backup/
git commit -m "docs: add backup module investigation and analysis

- Complete investigation of backup/restore options for Graphiti
- Analysis of 4 different approaches with pros/cons
- Technical recommendation: Export/Import Selectivo as MVP
- Original backup plan preserved for reference
- Architecture design ready for implementation

This addresses the original problem of backup operations consuming
too many tokens when executed from Claude Desktop."

# 7. Push branch
git push -u origin feature/backup-investigation
```

**✅ Checkpoint FASE 3**: Documentación backup migrada y organizada

---

### **FASE 4: Revisión Cambios Core (60 minutos - CRÍTICA)**
**Objetivo**: Revisar y migrar cambios en graphiti_core con documentación

```bash
# 1. Nueva branch
git checkout main
git checkout -b feature/gemini-embedder-review

# 2. ANTES de copiar - analizar cambios
cd /Users/pepo/graphiti-pepo-local
git diff HEAD~10 graphiti_core/embedder/gemini.py > /tmp/gemini_changes.patch
git log --oneline -10 graphiti_core/embedder/gemini.py

# 3. Copiar archivo modificado
cd /Users/pepo/Dev/graphiti-production
cp /Users/pepo/graphiti-pepo-local/graphiti_core/embedder/gemini.py ./graphiti_core/embedder/

# 4. CREAR DOCUMENTACIÓN de cambios
cat > docs/GEMINI_EMBEDDER_CHANGES.md << 'EOF'
# Gemini Embedder Changes Review

## Change Summary
[TO BE COMPLETED AFTER REVIEW]
- Added ~100 lines to graphiti_core/embedder/gemini.py
- Changes made during embeddings comparison evaluation

## Review Checklist
- [ ] Document purpose of each new function
- [ ] Verify performance implications
- [ ] Add unit tests for new functionality
- [ ] Check compatibility with existing code
- [ ] Update API documentation if needed

## Changes Detail
[TO BE COMPLETED AFTER LINE-BY-LINE REVIEW]

## Test Requirements
[TO BE ADDED AFTER UNDERSTANDING CHANGES]
EOF

# 5. ⚠️ NO COMMITEAR AÚN - Primero revisar
echo "⚠️ REVIEW REQUIRED: Check gemini.py changes before committing"
echo "   1. Open gemini.py and review each change"
echo "   2. Document purpose in GEMINI_EMBEDDER_CHANGES.md"
echo "   3. Add tests for new functionality"
echo "   4. Only then commit"
```

**⚠️ STOP - REVISIÓN MANUAL REQUERIDA**
- Esta fase requiere revisión línea por línea
- No proceder automáticamente
- Solo commitear después de documentar y testear

---

### **FASE 5: Tests Evaluación (30 minutos)**
**Objetivo**: Organizar tests de evaluación con documentación

```bash
# 1. Nueva branch
git checkout main
git checkout -b evaluation/retrieval-tests

# 2. Crear estructura tests
mkdir -p tests/evaluation/retrieval

# 3. Copiar tests
cp /Users/pepo/graphiti-pepo-local/test_code_retrieval_*.py ./tests/evaluation/retrieval/

# 4. Crear documentación tests
cat > tests/evaluation/retrieval/README.md << 'EOF'
# Retrieval Evaluation Test Suite

## Purpose
Comprehensive tests for evaluating different code retrieval methods and performance optimization.

## Test Files
- `test_code_retrieval_comparison.py`: Compare different retrieval strategies
- `test_code_retrieval_fast.py`: Performance benchmarks
- `test_code_retrieval_mcp.py`: MCP integration tests  
- `test_code_retrieval_query_implementation.py`: Query implementation tests
- `test_code_retrieval_real.py`: Tests with real data
- `test_code_retrieval_simple.py`: Basic functionality tests

## Status
- Tests copied from evaluation branch
- Need integration with main test suite
- Documentation pending review

## Next Steps
1. Review each test file purpose
2. Ensure all tests pass independently
3. Document expected results
4. Integrate with CI/CD pipeline
5. Add performance benchmarks

## Usage
```bash
# Run individual test
python tests/evaluation/retrieval/test_code_retrieval_simple.py

# Run full suite (after integration)
pytest tests/evaluation/retrieval/
```
EOF

# 5. Crear configuración tests
cat > tests/evaluation/conftest.py << 'EOF'
"""
Configuration for evaluation tests.
"""
import pytest
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Common fixtures for evaluation tests
@pytest.fixture
def evaluation_config():
    """Common configuration for evaluation tests."""
    return {
        "performance_baseline_ms": 300,
        "metrics_collection": True,
        "test_data_path": "tests/evaluation/data/"
    }
EOF

# 6. Commit tests
git add tests/
git commit -m "test: add retrieval evaluation test suite

- Comprehensive tests for code retrieval evaluation
- Performance benchmarks and method comparisons  
- MCP integration testing capabilities
- Documentation and configuration for test suite

Tests migrated from evaluation branch and organized for
integration with main test suite. Review and integration pending."

# 7. Push branch
git push -u origin evaluation/retrieval-tests
```

**✅ Checkpoint FASE 5**: Tests migrados y documentados

---

### **FASE 6: Archivo Reportes (15 minutos)**
**Objetivo**: Archivar reportes históricos de evaluación

```bash
# 1. Nueva branch
git checkout main
git checkout -b archive/evaluation-reports-2025-07-23

# 2. Crear estructura archivo
mkdir -p archive/evaluations/2025-07-23

# 3. Copiar reportes
cp /Users/pepo/graphiti-pepo-local/CODE_RETRIEVAL_QUERY_STATUS_COMPLETE.md ./archive/evaluations/2025-07-23/
cp /Users/pepo/graphiti-pepo-local/code_retrieval_report_20250723_*.md ./archive/evaluations/2025-07-23/
cp /Users/pepo/graphiti-pepo-local/code_retrieval_test_20250723_*.json ./archive/evaluations/2025-07-23/
cp /Users/pepo/graphiti-pepo-local/mcp_*.md ./archive/evaluations/2025-07-23/
cp /Users/pepo/graphiti-pepo-local/mcp_*.cypher ./archive/evaluations/2025-07-23/
cp /Users/pepo/graphiti-pepo-local/mcp_*.json ./archive/evaluations/2025-07-23/

# 4. Crear índice archivo
cat > archive/evaluations/2025-07-23/README.md << 'EOF'
# Evaluation Reports - July 23, 2025

## Context
Historical evaluation reports from code retrieval and MCP testing performed on July 23, 2025.
These reports were generated during the embeddings comparison evaluation phase.

## Contents

### Code Retrieval Reports
- `code_retrieval_report_20250723_224811.md`: Performance evaluation report
- `code_retrieval_report_20250723_225429.md`: Comparative analysis report
- `CODE_RETRIEVAL_QUERY_STATUS_COMPLETE.md`: Query status completion report

### Test Data
- `code_retrieval_test_20250723_224811.json`: Test execution data
- `code_retrieval_test_20250723_225429.json`: Comparative test data

### MCP Analysis
- `mcp_execution_guide_20250723_231748.md`: MCP execution guide
- `mcp_schema_analysis_20250723.md`: Schema analysis
- `mcp_standardized_queries_20250723.cypher`: Standardized Cypher queries
- `mcp_test_plan_20250723_231748.json`: Test plan configuration
- `mcp_testing_workflow_20250723.md`: Testing workflow documentation

## Status
- **Type**: Historical data
- **Impact**: No effect on current development
- **Purpose**: Reference and documentation
- **Retention**: Permanent archive

## Related Work
- Phase 1 embeddings comparison evaluation
- OpenAI vs Gemini embedding analysis
- MCP server integration testing
EOF

# 5. Commit archivo
git add archive/
git commit -m "archive: preserve evaluation reports from July 23, 2025

- Complete code retrieval evaluation reports and analysis
- MCP schema analysis and testing documentation
- Test data and execution results from embeddings comparison
- Historical data preserved for reference and future analysis

No impact on current development. Archive maintained for
documentation and lessons learned purposes."

# 6. Push archivo
git push -u origin archive/evaluation-reports-2025-07-23
```

**✅ Checkpoint FASE 6**: Reportes archivados correctamente

---

## 📊 ESTADO FINAL POST-MIGRACIÓN

### **Estructura resultante**:
```
/Users/pepo/graphiti-pepo-local/          # ← INTACTO (Docker+MCP funcionando)
├── docker-compose.yml (running)
├── neo4j container (active)
├── mcp_server/ (active)
└── (todo el trabajo actual intacto)

/Users/pepo/Dev/graphiti-production/       # ← NUEVO REPO LIMPIO
├── .git → origin: tu fork, upstream: getzep/graphiti
├── main (limpio desde upstream)
├── feature/development-methodology ✅
│   ├── CLAUDE.md (activo)
│   ├── docs/DEVELOPMENT_METHODOLOGY.md
│   └── .claude/ (scripts validación)
├── feature/backup-investigation ✅
│   └── docs/backup/ (investigación completa)
├── feature/gemini-embedder-review ⚠️
│   └── (requiere revisión manual)
├── evaluation/retrieval-tests ✅
│   └── tests/evaluation/retrieval/
└── archive/evaluation-reports-2025-07-23 ✅
    └── archive/evaluations/2025-07-23/
```

---

## 🔄 FLUJO DE TRABAJO POST-MIGRACIÓN

### **Para desarrollo diario**:
1. **Usar**: `/Users/pepo/Dev/graphiti-production/`
2. **CLAUDE.md**: Se carga automáticamente
3. **Metodología**: Activa con checkpoints
4. **PRs**: Desde branches → tu fork → upstream

### **Para datos/experimentos**:
1. **Neo4j**: Sigue en `/Users/pepo/graphiti-pepo-local/`
2. **Docker**: No cambiar hasta migrar datos
3. **MCP**: Puede configurarse para ambos repos

### **Para colaboración**:
1. **Fork actualizado**: Con estructura profesional
2. **Historia limpia**: Commits organizados por objetivo
3. **Documentación**: Completa y organizada

---

## 🎯 VENTAJAS CONSEGUIDAS

### ✅ **Seguridad**:
- Zero riesgo de romper configuraciones existentes
- Ambos repos funcionando independientemente
- Proceso completamente reversible

### ✅ **Profesionalización**:
- Historia git limpia y organizada
- Commits atómicos por objetivo
- Documentación completa de decisiones

### ✅ **Productividad**:
- CLAUDE.md aplicándose automáticamente
- Metodología con checkpoints activa
- Estructura lista para colaboración

### ✅ **Flexibilidad**:
- Puedes usar ambos repos según necesidad
- Migración gradual de servicios cuando convenga
- Mantener datos en repo actual hasta decidir

---

## 🚦 MOMENTO CRÍTICO DE REINICIO

### **REINICIAR DESPUÉS DE FASE 1**:
1. **Ejecutar FASE 1** (crear estructura)
2. **Cambiar directorio de trabajo** a `/Users/pepo/Dev/graphiti-production`
3. **REINICIAR CLAUDE CODE**
4. **Verificar carga de metodología**
5. **Continuar con FASE 2-6**

### **¿Por qué reiniciar ahí?**
- CLAUDE.md estará disponible después de FASE 2
- Mejor experiencia desde el primer momento
- Metodología se activará automáticamente
- Checkpoints funcionarán correctamente

---

**Este documento se copiará también al nuevo repo como referencia histórica del proceso de migración.**