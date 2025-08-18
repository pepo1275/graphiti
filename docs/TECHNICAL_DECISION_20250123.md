# 📋 DECISIÓN TÉCNICA: ESTRATEGIA DE COMMITS
## Fecha: 2025-01-23
## Estado: PENDIENTE DE APROBACIÓN

---

## 🎯 CONTEXTO

### Situación actual
Tenemos cambios mezclados en el repositorio que incluyen:
1. **Metodología de desarrollo** (nuevo, limpio, documentado)
2. **Tests de code retrieval** (sin contexto claro, ~6 archivos)
3. **Modificaciones en gemini.py** (+100 líneas sin documentación)
4. **Reportes y archivos JSON** (evaluaciones previas)

### Problema identificado
- Mezcla de objetivos en una sola branch
- Falta de trazabilidad y documentación
- Riesgo de crear deuda técnica
- Dificultad para revertir cambios específicos

---

## 🔍 ANÁLISIS TÉCNICO

### Archivos por categoría

#### CATEGORÍA A: Metodología (LISTO PARA COMMIT) ✅
```
CLAUDE.md                           # Nuevo - Instrucciones automáticas
docs/DEVELOPMENT_METHODOLOGY.md      # Nuevo - Proceso completo
docs/CHECKPOINTS.md                 # Nuevo - Puntos de control
docs/INDEX.md                        # Nuevo - Índice documentación
docs/BACKUP_MODULE_INVESTIGATION.md  # Nuevo - Investigación backup
docs/BACKUP_OPTIONS_ANALYSIS.md      # Nuevo - Análisis opciones
.claude/check_methodology.py         # Nuevo - Validador
.claude/pre-commit-validator.sh      # Nuevo - Pre-commit hook
.gitignore                          # Modificado - Añadido .claude/
```

#### CATEGORÍA B: Tests de Retrieval (REQUIERE REVISIÓN) ⚠️
```
test_code_retrieval_comparison.py
test_code_retrieval_fast.py
test_code_retrieval_mcp.py
test_code_retrieval_query_implementation.py
test_code_retrieval_real.py
test_code_retrieval_simple.py
```

#### CATEGORÍA C: Modificaciones Core (REQUIERE REVIEW) ⚠️
```
graphiti_core/embedder/gemini.py    # +100 líneas, sin tests
```

#### CATEGORÍA D: Reportes y Datos (EVALUAR SI COMMITEAR) 📊
```
CODE_RETRIEVAL_QUERY_STATUS_COMPLETE.md
code_retrieval_report_20250723_*.md
code_retrieval_test_20250723_*.json
mcp_*.md
mcp_*.cypher
mcp_*.json
```

---

## 📊 DECISIÓN TOMADA

### **ESTRATEGIA: COMMIT SELECTIVO + STASH**

#### Fase 1: Commit de Metodología (INMEDIATO)
Solo commitear archivos de Categoría A que son:
- Independientes de la funcionalidad
- Completamente documentados
- Sin riesgo de breaking changes
- Establecen base para trabajo futuro

#### Fase 2: Stash de trabajo en progreso
Guardar temporalmente Categorías B, C y D para:
- Revisión con metodología activa
- Documentación apropiada
- Testing adecuado
- Commits separados por objetivo

---

## 💻 COMANDOS A EJECUTAR

### PASO 1: Verificar estado actual
```bash
git status
git diff --stat
```

### PASO 2: Añadir archivos de metodología selectivamente
```bash
# Añadir archivos de metodología
git add CLAUDE.md
git add docs/DEVELOPMENT_METHODOLOGY.md
git add docs/CHECKPOINTS.md
git add docs/INDEX.md
git add docs/BACKUP_MODULE_INVESTIGATION.md
git add docs/BACKUP_OPTIONS_ANALYSIS.md
git add docs/TECHNICAL_DECISION_20250123.md
git add .claude/check_methodology.py
git add .claude/pre-commit-validator.sh
git add .gitignore

# Verificar que solo estos archivos están staged
git status
```

### PASO 3: Crear commit descriptivo
```bash
git commit -m "feat: implement development methodology and Claude Code automation

- Add CLAUDE.md for automatic instruction loading by Claude Code
- Create comprehensive development methodology (7 phases)
- Add validation scripts and checkpoint system
- Setup .claude/ directory with methodology validators
- Document backup module investigation and options
- Update .gitignore for .claude/ temporary files

This commit establishes a professional development workflow that will be
automatically applied by Claude Code in future sessions. The methodology
includes mandatory checkpoints, validation scripts, and clear documentation
structure.

No functional changes to the codebase are included in this commit."
```

### PASO 4: Push a remote
```bash
git push origin evaluation/embeddings-comparison
```

### PASO 5: Stash trabajo restante
```bash
# Guardar todo lo demás con descripción clara
git stash push -m "WIP: retrieval tests + gemini changes + reports - needs review"

# Verificar stash creado
git stash list
```

---

## 📋 SEGUIMIENTO POST-COMMIT

### Trabajo pendiente en stash:

1. **Tests de Retrieval**
   - Crear branch: `evaluation/retrieval-tests`
   - Documentar propósito y resultados esperados
   - Añadir a suite de tests oficial

2. **Cambios en Gemini**
   - Crear branch: `feature/gemini-enhancements`
   - Review de 100+ líneas añadidas
   - Añadir tests unitarios
   - Documentar cambios

3. **Reportes y Datos**
   - Evaluar si van al repo o a docs externos
   - Considerar .gitignore para archivos temporales

---

## ✅ CHECKLIST DE APROBACIÓN

### Antes de ejecutar, confirmar:
- [ ] Entiendo que solo se commitea la metodología
- [ ] Acepto que el resto queda en stash para revisión
- [ ] Comprendo que esto establece el proceso para futuros desarrollos
- [ ] Estoy de acuerdo con el mensaje de commit
- [ ] Entiendo que Claude Code aplicará CLAUDE.md automáticamente

### Riesgos mitigados:
- ✅ No se mezclan objetivos diferentes
- ✅ Historia de git queda limpia
- ✅ Fácil de revertir si es necesario
- ✅ No se pierde ningún trabajo (stash)
- ✅ Establece base sólida para continuar

---

## 🚦 ESTADO DE APROBACIÓN

**Estado actual**: ⏸️ **ESPERANDO APROBACIÓN**

**Para aprobar, el usuario debe confirmar**:
> "Apruebo el commit selectivo de metodología según lo documentado"

**Para rechazar o modificar**:
> "Necesito cambiar [especificar qué]"

---

## 📝 NOTAS ADICIONALES

- Este documento sirve como registro de decisión arquitectónica (ADR)
- La decisión está basada en mejores prácticas de ingeniería de software
- Prioriza la claridad y mantenibilidad sobre la velocidad
- Establece precedente para futuros desarrollos

---

*Documento preparado por: Claude Code (actuando como Tech Lead)*
*Revisado por: Pendiente*
*Decisión: Pendiente*