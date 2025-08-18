# 🔧 EMBEDDING REPAIR SYSTEM - GRAPHITI

## 📁 Estructura del Proyecto

```
scripts/embedding_repair/
├── embedding_repair_main.py    # Script principal todo-en-uno
├── backups/                    # Backups automáticos (timestamped)
├── logs/                      # Logs de ejecución 
├── configs/                   # Configuraciones específicas
└── docs/                      # Documentación y aprendizajes
    ├── README.md              # Este archivo
    ├── LEARNINGS.md           # Aprendizajes para módulo backup
    └── EXECUTION_LOG.md       # Log de ejecuciones
```

## 🎯 Propósito

**Urgencia**: Reparar embeddings con dimensión incorrecta (1024 → 3072) usando Gemini
**Futuro**: Base de conocimiento para módulo de backup programático en Graphiti

## 🚀 Uso Rápido

```bash
# Desde directorio raíz del proyecto
cd scripts/embedding_repair

# Modo simulación (recomendado primero)
python3 embedding_repair_main.py
# Elegir: 's' (simular)

# Ejecución real
python3 embedding_repair_main.py  
# Elegir: 'e' (ejecutar)
```

## 📊 Funcionalidades Implementadas

### ✅ Sistema de Backup
- **Backup de configuraciones**: `graphiti_core/embedder/client.py`, `claude_desktop_config.json`
- **Backup de estado Neo4j**: Snapshot completo de entidades y embeddings
- **Backup timestamped**: Cada ejecución genera directorio único
- **Verificación de integridad**: Conteos antes/después

### ✅ Análisis de Estado
- **Detección automática** de embeddings faltantes/incorrectos
- **Estadísticas por dimensión** de embeddings existentes
- **Análisis por grupos** afectados
- **Comparación pre/post regeneración**

### ✅ Regeneración Inteligente
- **API Gemini** con configuración optimizada (3072 dims)
- **Rate limiting** automático para evitar límites
- **Procesamiento en lotes** limitado y controlado
- **Manejo de errores** granular por entidad

### ✅ Sistema de Testing
- **Modo simulación** completo sin cambios reales
- **Validación previa** de conexiones y APIs
- **Tests de integridad** post-regeneración
- **Rollback automático** en caso de errores críticos

## 📝 Valor para Módulo de Backup

Este script sirve como **prototipo avanzado** para el futuro módulo de backup:

### 🔧 Patrones Implementados
- **Backup selectivo** por criterios (dimensión embedding)
- **Metadata enriquecida** con contexto de backup
- **Estructura de datos** para restore
- **Validación de integridad** automática

### 🏗️ Arquitectura Escalable
- **Configuración centralizada** fácil de adaptar
- **Separación de responsabilidades** (backup/análisis/regeneración)  
- **Logging estructurado** con estadísticas
- **Manejo de errores** robusto

### 💡 Aprendizajes Clave
- **Neo4j queries** optimizadas para backup selectivo
- **Integración con APIs externas** (Gemini) 
- **Gestión de dependencias** y configuraciones
- **UX de scripts** con modos interactivos

## 🔄 Roadmap de Integración

### Fase 1: Ejecutar Script (Ahora)
- [ ] Adaptar rutas del proyecto
- [ ] Ejecutar en modo simulación
- [ ] Verificar resultados
- [ ] Documentar aprendizajes

### Fase 2: Extraer Componentes Reutilizables
- [ ] Separar clase `BackupManager`  
- [ ] Extraer `EmbeddingAnalyzer`
- [ ] Crear `ConfigManager` genérico
- [ ] Modularizar sistema de reports

### Fase 3: Integrar en Graphiti Core
- [ ] Crear `graphiti_core.backup` package
- [ ] Integrar con sistema de configuración existente
- [ ] Añadir tests unitarios 
- [ ] Documentación API completa

## ⚠️ Notas Importantes

- **No ejecutar en producción** sin backup previo
- **Verificar API keys** antes de regenerar embeddings
- **Monitorear logs** durante ejecución real
- **Validar resultados** con queries de verificación

---

*Creado: 2025-08-18*  
*Propósito: Reparación urgente + Base para módulo backup*