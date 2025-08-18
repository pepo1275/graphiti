# 🛑 CHECKPOINTS DE APROBACIÓN OBLIGATORIOS

## 📋 RESUMEN EJECUTIVO
Este documento define los puntos de parada OBLIGATORIOS donde se requiere aprobación explícita del usuario antes de continuar.

---

## 🔴 CHECKPOINTS CRÍTICOS (PARADA OBLIGATORIA)

### ✋ CHECKPOINT 0: SETUP INICIAL
**Cuándo**: Antes de crear branches o configurar entorno
**Validar**:
- [ ] Branch actual correcta
- [ ] Estado git limpio
- [ ] Herramientas instaladas
- [ ] Backup de configuraciones existentes

**Comando de verificación**:
```bash
git status && git branch --show-current
```

**Pregunta al usuario**: 
> "¿Apruebas el setup inicial y la creación de la branch feature/[nombre]?"

---

### ✋ CHECKPOINT 1: ANÁLISIS COMPLETADO
**Cuándo**: Después de analizar código existente
**Validar**:
- [ ] Arquitectura documentada
- [ ] Dependencias identificadas
- [ ] Riesgos evaluados
- [ ] Impacto estimado

**Entregables**:
- Documento de análisis
- Lista de riesgos
- Dependencias afectadas

**Pregunta al usuario**:
> "He completado el análisis. ¿Apruebas los hallazgos y procedo con el plan?"

---

### ✋ CHECKPOINT 2: PLAN DETALLADO
**Cuándo**: Antes de diseño técnico
**Validar**:
- [ ] Objetivos claros
- [ ] Alcance definido
- [ ] Timeline realista
- [ ] Criterios de aceptación

**Entregables**:
- Plan de implementación
- Criterios de aceptación
- Estimación de tiempo

**Pregunta al usuario**:
> "El plan está listo. ¿Apruebas el alcance y timeline propuestos?"

---

### ✋ CHECKPOINT 3: DISEÑO TÉCNICO
**Cuándo**: Antes de implementación
**Validar**:
- [ ] Arquitectura diseñada
- [ ] Interfaces definidas
- [ ] Tests planificados
- [ ] CI/CD configurado

**Entregables**:
- Diseño de arquitectura
- Especificación de interfaces
- Plan de testing

**Pregunta al usuario**:
> "Diseño técnico completo. ¿Apruebas la arquitectura propuesta?"

---

### ✋ CHECKPOINT 4: BACKUP REALIZADO
**Cuándo**: Antes de cambios en código
**Validar**:
- [ ] Safety commit creado
- [ ] Tag de backup
- [ ] Configuraciones respaldadas
- [ ] Datos críticos seguros

**Comando de verificación**:
```bash
git tag -l "backup-*" | tail -1
```

**Pregunta al usuario**:
> "Backup completo (tag: [nombre]). ¿Procedo con la implementación?"

---

### ✋ CHECKPOINT 5: DESARROLLO COMPLETADO
**Cuándo**: Antes de crear PR
**Validar**:
- [ ] Todos los tests pasan
- [ ] Coverage >80%
- [ ] Sin errores de linting
- [ ] Documentación actualizada

**Comando de verificación**:
```bash
pytest && ruff check . && mypy graphiti_core/
```

**Pregunta al usuario**:
> "Desarrollo completo, tests pasando. ¿Creo el Pull Request?"

---

### ✋ CHECKPOINT 6: PR LISTO PARA REVIEW
**Cuándo**: PR creado pero antes de solicitar review
**Validar**:
- [ ] Self-review completado
- [ ] CI/CD verde
- [ ] Documentación incluida
- [ ] CHANGELOG actualizado

**Pregunta al usuario**:
> "PR #[número] listo. ¿Solicito review formal?"

---

### ✋ CHECKPOINT 7: PRE-MERGE
**Cuándo**: Después de aprobaciones, antes de merge
**Validar**:
- [ ] 2+ aprobaciones
- [ ] Sin conflictos
- [ ] Tests finales pasando
- [ ] Version bump si necesario

**Pregunta al usuario**:
> "PR aprobado y listo. ¿Procedo con el merge?"

---

## 🟡 CHECKPOINTS DE INFORMACIÓN (SIN PARADA)

Estos puntos requieren informar pero NO detener:

### 📢 INFO 1: Tests ejecutándose
```markdown
"Ejecutando suite de tests... [X/Y completados]"
```

### 📢 INFO 2: Commit realizado
```markdown
"Commit realizado: [hash] - [mensaje]"
```

### 📢 INFO 3: Push completado
```markdown
"Push exitoso a origin/[branch]"
```

---

## 🔄 PROTOCOLO DE ROLLBACK

Si el usuario NO aprueba en cualquier checkpoint:

### 1. Preguntar razón
```markdown
"Entendido. ¿Qué aspecto necesita revisión?"
```

### 2. Si requiere rollback
```bash
# Volver al último punto seguro
git reset --hard [last-safe-commit]
git clean -fd
```

### 3. Documentar el rechazo
```markdown
## Checkpoint [X] - No aprobado
- Fecha: [timestamp]
- Razón: [feedback del usuario]
- Acción: [rollback/modificar/cancelar]
```

---

## 📊 TRACKING DE CHECKPOINTS

### Formato de registro (.claude/checkpoint_log.json)
```json
{
  "session_id": "2025-01-23-001",
  "checkpoints": [
    {
      "id": 0,
      "name": "setup_inicial",
      "timestamp": "2025-01-23T10:00:00Z",
      "status": "approved",
      "approver": "user",
      "notes": "Branch feature/backup-module creada"
    }
  ]
}
```

---

## 🚨 REGLAS DE ORO

1. **NUNCA** saltarse un checkpoint crítico
2. **SIEMPRE** esperar confirmación explícita
3. **DOCUMENTAR** cada aprobación/rechazo
4. **ROLLBACK** inmediato si hay dudas
5. **COMUNICAR** claramente el estado actual

---

## 📝 PLANTILLA DE SOLICITUD

```markdown
## 🛑 CHECKPOINT [N]: [NOMBRE]

### Estado actual:
- [Descripción del trabajo completado]

### Validaciones:
✅ [Validación 1]
✅ [Validación 2]
✅ [Validación 3]

### Próximos pasos si apruebas:
- [Siguiente acción]

### Archivos modificados:
- [Lista de archivos]

### Riesgos identificados:
- [Riesgo si existe]

**¿Apruebas continuar? (SI/NO/REVISAR)**
```

---

*Este documento es parte integral de la metodología de desarrollo.*
*Versión: 1.0.0 - Fecha: 2025-01-23*