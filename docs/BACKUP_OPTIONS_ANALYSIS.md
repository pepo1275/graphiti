# 📊 ANÁLISIS DE OPCIONES PARA BACKUP/RESTORE - GRAPHITI
## Fecha: 2025-01-23

---

## 🔍 INVESTIGACIÓN REALIZADA

### 1. Repositorios Analizados

#### **Graphiti Original (getzep/graphiti)**
- **URL**: https://github.com/getzep/graphiti
- **Hallazgos**:
  - ✅ Añadido soporte para Gemini y Ollama
  - ✅ Integración con Azure OpenAI
  - ❌ NO tiene funcionalidad de backup/restore
  - 📝 Enfoque en actualizaciones incrementales en tiempo real
  - 📝 558 commits, último: August 8, 2024

#### **Neo4j LLM Graph Builder**
- **URL**: https://github.com/neo4j-labs/llm-graph-builder
- **Hallazgos**:
  - 🔍 Extracción de conocimiento con esquemas personalizables
  - 🔍 Procesamiento por chunks con embeddings
  - ❌ NO tiene backup/restore específico
  - 💡 Depende completamente del backup nativo de Neo4j
  - 📝 Soporta múltiples fuentes: PDFs, docs, YouTube, Wikipedia

#### **Neo4j Nativo (Documentación oficial)**
- **URL**: https://neo4j.com/docs/operations-manual/current/backup-restore/
- **Hallazgos**:
  - ✅ `neo4j-admin` para backup completo de base de datos
  - ✅ Backup online (sin interrumpir operaciones)
  - ❌ NO soporta backup selectivo de nodos/relaciones
  - ❌ NO permite backup vía Cypher
  - 📝 Es backup a nivel de base de datos completa

---

## 💡 OPCIONES IDENTIFICADAS

### **OPCIÓN A: Export/Import Selectivo (RECOMENDADA)** ⭐

**Descripción**: Módulo ligero para exportar/importar subgrafos específicos

```python
class GraphitiExporter:
    """Exporta subgrafos específicos a JSON/CSV"""
    
    async def export_entities(
        self,
        group_id: str = None,
        embedding_size: int = None,
        entity_type: str = None
    ) -> Dict:
        """Exporta entidades con filtros flexibles"""
        
    async def export_subgraph(
        self,
        entity_uuids: List[str],
        depth: int = 1
    ) -> Dict:
        """Exporta subgrafo alrededor de entidades específicas"""
        
    async def export_by_time_range(
        self,
        start_date: datetime,
        end_date: datetime
    ) -> Dict:
        """Exporta datos en rango temporal"""

class GraphitiImporter:
    """Importa datos preservando integridad"""
    
    async def import_entities(
        self,
        data: Dict,
        merge_strategy: str = "skip"  # skip|override|merge
    ) -> ImportResult:
        """Importa con estrategia configurable"""
        
    async def validate_import_data(
        self,
        data: Dict
    ) -> ValidationResult:
        """Valida datos antes de importar"""
```

**Ventajas**:
- ✅ Resuelve el caso específico de las 10 entidades con embeddings 1024
- ✅ Simple y enfocado
- ✅ No duplica funcionalidad de Neo4j
- ✅ Útil para migración entre ambientes
- ✅ Fácil de testear y mantener

**Desventajas**:
- ❌ No es backup completo del sistema
- ❌ Requiere implementación custom

---

### **OPCIÓN B: Wrapper de neo4j-admin**

**Descripción**: Interfaz Python para comandos nativos de Neo4j

```python
class Neo4jBackupWrapper:
    def backup_full(self, output_path: Path) -> BackupResult:
        """Wrapper para neo4j-admin database backup"""
        result = subprocess.run([
            "neo4j-admin", "database", "backup",
            "neo4j", "--to-path", str(output_path)
        ])
        return BackupResult(success=result.returncode == 0)
        
    def restore_full(self, backup_path: Path) -> RestoreResult:
        """Wrapper para neo4j-admin database restore"""
        # Similar implementation
```

**Ventajas**:
- ✅ Usa herramientas probadas de Neo4j
- ✅ Backup completo garantizado
- ✅ Mínima implementación

**Desventajas**:
- ❌ No permite backup selectivo
- ❌ Requiere acceso a neo4j-admin
- ❌ No resuelve el problema de tokens

---

### **OPCIÓN C: No implementar nada**

**Descripción**: Usar herramientas existentes directamente

**Proceso**:
1. Para backup completo: `neo4j-admin database backup`
2. Para export selectivo: Queries Cypher manuales
3. Documentar el proceso para el equipo

**Ventajas**:
- ✅ Cero desarrollo
- ✅ Usa herramientas estándar
- ✅ Sin mantenimiento adicional

**Desventajas**:
- ❌ Proceso manual propenso a errores
- ❌ Consume tokens si se hace desde Claude
- ❌ Sin automatización

---

### **OPCIÓN D: Solución Híbrida**

**Descripción**: Combinar export selectivo + documentación de neo4j-admin

```python
# Para casos específicos
exporter = GraphitiExporter(driver)
await exporter.export_entities(embedding_size=1024)

# Para backup completo (documentado)
"""
BACKUP COMPLETO:
neo4j-admin database backup neo4j --to-path=/backups/$(date +%Y%m%d)
"""
```

---

## 📊 MATRIZ DE DECISIÓN

| Criterio | Opción A | Opción B | Opción C | Opción D |
|----------|----------|----------|----------|----------|
| **Resuelve problema tokens** | ✅ | ✅ | ❌ | ✅ |
| **Backup selectivo** | ✅ | ❌ | Parcial | ✅ |
| **Backup completo** | ❌ | ✅ | ✅ | ✅ |
| **Esfuerzo desarrollo** | Medio | Bajo | Nulo | Bajo |
| **Mantenibilidad** | Media | Baja | Nula | Baja |
| **Automatización** | ✅ | ✅ | ❌ | ✅ |
| **Testeable** | ✅ | Parcial | ❌ | ✅ |

---

## 🎯 RECOMENDACIÓN FINAL

### **Implementar OPCIÓN A (Export/Import Selectivo) como MVP**

**Razones**:
1. **Resuelve el problema inmediato**: Exportar 10 entidades sin consumir tokens
2. **Simple y enfocado**: No intenta reemplazar neo4j-admin
3. **Valor agregado real**: Casos de uso que neo4j-admin no cubre
4. **Extensible**: Se puede expandir según necesidades

### **Plan de implementación sugerido**:

#### Fase 1: MVP (2-4 horas)
```python
# Solo lo esencial
- export_entities(filter)
- import_entities(data)
- Formato JSON simple
```

#### Fase 2: Mejoras (si se necesitan)
```python
# Añadir según demanda
- export_subgraph()
- Validación de datos
- Múltiples formatos
```

#### Fase 3: Integración (opcional)
```python
# Si tiene valor
- CLI commands
- MCP server endpoints
- GitHub Actions
```

---

## 📝 CASOS DE USO ESPECÍFICOS

### 1. **Problema Original: 10 entidades con embeddings 1024**
```python
exporter = GraphitiExporter(driver)
data = await exporter.export_entities(
    embedding_size=1024,
    group_id="problem_solving"
)
# Guardar a archivo
with open("backup_entities_1024.json", "w") as f:
    json.dump(data, f)
```

### 2. **Migración entre ambientes**
```python
# En desarrollo
data = await exporter.export_entities(group_id="test_group")

# En producción
await importer.import_entities(data, merge_strategy="skip")
```

### 3. **Backup antes de operación peligrosa**
```python
# Backup selectivo
critical_entities = ["uuid1", "uuid2", "uuid3"]
backup = await exporter.export_subgraph(critical_entities, depth=2)

# Hacer operación peligrosa...

# Si falla, restaurar
await importer.import_entities(backup, merge_strategy="override")
```

---

## 🔄 ESTADO PARA CONTINUACIÓN

- **Documentos creados**: 
  - `BACKUP_MODULE_INVESTIGATION.md` - Diseño completo del módulo
  - `BACKUP_OPTIONS_ANALYSIS.md` - Este documento
  - Plan original en: `/Users/pepo/Downloads/graphiti_backup_plan_2025.md`

- **Decisión pendiente**: ¿Implementar Opción A (MVP) o no hacer nada?
- **Tiempo estimado**: 2-4 horas para MVP funcional
- **Próximo paso**: Crear feature branch si se aprueba

---

*Documento de análisis para retomar después de reinicio*
*Autor: Claude Code + Usuario*
*Fecha: 2025-01-23*