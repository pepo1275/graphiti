# 📚 ÍNDICE DE DOCUMENTACIÓN - PROYECTO GRAPHITI
## Última actualización: 2025-01-23

---

## 🏗️ METODOLOGÍA Y PROCESO

### 📋 Documentos principales
1. **[CLAUDE.md](../CLAUDE.md)** ⭐
   - Instrucciones obligatorias para Claude Code
   - Checkpoints críticos
   - Reglas inquebrantables
   - **LEER SIEMPRE al inicio de cada sesión**

2. **[DEVELOPMENT_METHODOLOGY.md](DEVELOPMENT_METHODOLOGY.md)**
   - Metodología completa de desarrollo
   - 7 fases del pipeline
   - Git workflow y CI/CD
   - Templates y comandos

3. **[CHECKPOINTS.md](CHECKPOINTS.md)**
   - Puntos de parada obligatorios
   - Plantillas de aprobación
   - Protocolo de rollback

---

## 🔧 MÓDULO DE BACKUP (En investigación)

### 📊 Documentos de análisis
1. **[BACKUP_MODULE_INVESTIGATION.md](BACKUP_MODULE_INVESTIGATION.md)**
   - Diseño completo del módulo propuesto
   - Arquitectura BackupManager/RestoreManager
   - Estimación de esfuerzo: 16h
   - Estado: Esperando decisión

2. **[BACKUP_OPTIONS_ANALYSIS.md](BACKUP_OPTIONS_ANALYSIS.md)**
   - Análisis de 4 opciones
   - Comparación con Neo4j nativo
   - Recomendación: Opción A (Export/Import Selectivo)
   - MVP estimado: 2-4h

### 📝 Recursos externos
- **Plan original**: `/Users/pepo/Downloads/graphiti_backup_plan_2025.md`
  - 371 líneas con queries Cypher
  - 10 entidades con embeddings 1024
  - Incluye scripts de restauración

---

## 🚀 CONFIGURACIÓN DEL PROYECTO

### Claude Code
- **[claude_code/CLAUDE_CODE_COMPLETE.md](claude_code/CLAUDE_CODE_COMPLETE.md)**
  - Configuración actual del proyecto
  - Estado de branches
  - Mejores prácticas obligatorias

### Scripts y herramientas
- **[.claude/check_methodology.py](../.claude/check_methodology.py)**
  - Validador de cumplimiento
  - Ejecutar antes de commits

- **[.claude/pre-commit-validator.sh](../.claude/pre-commit-validator.sh)**
  - Validación automática pre-commit
  - Verifica branch, tests, calidad

---

## 📊 ESTADO ACTUAL DEL PROYECTO

### Branch actual
- **evaluation/embeddings-comparison**
- Trabajando en: Metodología y módulo de backup

### Archivos modificados (no commiteados)
- ✅ CLAUDE.md (creado)
- ✅ docs/DEVELOPMENT_METHODOLOGY.md (movido)
- ✅ docs/CHECKPOINTS.md (creado)
- ✅ docs/BACKUP_MODULE_INVESTIGATION.md (creado)
- ✅ docs/BACKUP_OPTIONS_ANALYSIS.md (creado)
- ✅ docs/INDEX.md (este archivo)
- ✅ .claude/* (scripts de validación)
- ✅ .gitignore (actualizado)

### Decisiones pendientes
1. ¿Hacer commit de la metodología implementada?
2. ¿Implementar módulo de backup Opción A (MVP)?
3. ¿Reiniciar sesión con metodología activa?

---

## 🔄 PARA RETOMAR EL TRABAJO

### Si reinicias la sesión:
1. Claude Code leerá automáticamente `CLAUDE.md`
2. Revisar este INDEX.md para contexto
3. Consultar documentos específicos según necesidad

### Comandos útiles:
```bash
# Ver estado actual
git status
git branch --show-current

# Validar metodología
python3 .claude/check_methodology.py

# Si decides hacer commit
git add -A
git commit -m "feat: implement development methodology and Claude Code automation"
git push origin evaluation/embeddings-comparison
```

### Próximos pasos sugeridos:
1. **Commit de metodología** (recomendado)
2. **Decidir sobre módulo backup**:
   - Opción A: Implementar MVP (2-4h)
   - Opción C: No hacer nada, usar neo4j-admin
3. **Continuar con evaluación de embeddings**

---

## 📝 NOTAS IMPORTANTES

### Sobre la metodología
- Ya está configurada para aplicarse automáticamente
- Claude Code la seguirá sin recordatorios
- Los checkpoints son obligatorios

### Sobre el módulo de backup
- Investigación completa documentada
- Recomendación: Export/Import selectivo
- Resuelve problema de tokens
- No duplica funcionalidad de Neo4j

### Sobre el estado git
- Cambios importantes no commiteados
- Considerar hacer safety commit
- Branch correcta para trabajo

---

*Este índice es el punto de entrada para toda la documentación del proyecto*
*Actualizar cuando se añadan nuevos documentos importantes*