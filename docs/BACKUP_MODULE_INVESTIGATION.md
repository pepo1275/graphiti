# 📊 INVESTIGACIÓN MÓDULO DE BACKUP - GRAPHITI
## Fecha: 2025-01-23

---

## 🎯 OBJETIVO
Implementar un módulo de backup programático para evitar el consumo excesivo de tokens al ejecutar operaciones de backup desde Claude Desktop.

---

## 📋 CONTEXTO DEL PROBLEMA

### Situación Actual
- Las operaciones de backup desde Claude Desktop consumen tokens excesivos
- El plan de backup existente (`/Users/pepo/Downloads/graphiti_backup_plan_2025.md`) tiene 371 líneas
- Incluye queries Cypher complejas para backup de:
  - 10 entidades con embeddings de dimensión 1024
  - Relaciones especializadas
  - Esquema ontológico con APOC

### Entidades Afectadas (10)
1. `graphiti-mcp-server`
2. `neo4j-docker-graphiti`
3. `claude_desktop_config.json`
4. `Graphiti`
5. `Desktop Commander`
6. `pepo`
7. `Gemini`
8. `RETRIEVAL_DOCUMENT`
9. `CODE_RETRIEVAL_QUERY`
10. `embedding-001`

---

## 🔍 HALLAZGOS DE LA INVESTIGACIÓN

### 1. NO existe funcionalidad de backup/restore en Graphiti actualmente

**Archivos revisados:**
- ✅ `graphiti_core/utils/maintenance/graph_data_operations.py`
  - Contiene: `clear_data()` y `retrieve_episodes()`
  - NO contiene: funciones de backup/restore

- ✅ `graphiti_core/driver/`
  - Neo4j y FalkorDB drivers con `execute_query()`
  - Se puede reutilizar para ejecutar queries de backup

- ✅ `graphiti_core/telemetry/`
  - Tiene `export_to_csv()` para tokens
  - NO tiene export de datos del grafo

### 2. Componentes reutilizables encontrados

```python
# Driver Neo4j disponible
from graphiti_core.driver.neo4j_driver import Neo4jDriver

# Puede ejecutar queries Cypher directamente
driver = Neo4jDriver(...)
result = await driver.execute_query(cypher_query, params)
```

### 3. Estructura propuesta del módulo

```
graphiti_core/
└── utils/
    └── backup/
        ├── __init__.py
        ├── backup_manager.py      # Core backup logic
        ├── restore_manager.py     # Restore functionality
        ├── schemas.py            # Pydantic models for backup data
        ├── validators.py         # Validation logic
        └── tests/
            ├── test_backup.py
            └── test_restore.py
```

---

## 📝 PLAN DE BACKUP EXISTENTE (RESUMEN)

### Queries principales del plan original:

1. **Backup Schema con APOC**
```cypher
CALL db.labels() YIELD label
WITH collect(label) as all_labels
CALL db.relationshipTypes() YIELD relationshipType  
WITH all_labels, collect(relationshipType) as all_rels
RETURN {
  node_types: all_labels,
  relationship_types: all_rels,
  apoc_version: apoc.version()
} as schema_backup
```

2. **Backup Entidades 1024**
```cypher
MATCH (n:Entity)
WHERE size(n.name_embedding) = 1024
RETURN {
  core_data: {
    uuid: n.uuid,
    name: n.name,
    group_id: n.group_id,
    entity_type: n.entity_type,
    created_at: n.created_at,
    updated_at: n.updated_at
  },
  embeddings: {
    name_embedding: n.name_embedding,
    embedding_dimension: size(n.name_embedding)
  }
} as entity_backup
```

3. **Backup Relaciones**
```cypher
MATCH (n:Entity)-[r]-(m)
WHERE size(n.name_embedding) = 1024
RETURN {
  source_entity: n,
  relationship: type(r) + properties(r),
  target_node: m
} as relationship_backup
```

---

## 🏗️ DISEÑO PROPUESTO DEL MÓDULO

### BackupManager Class
```python
class BackupManager:
    def __init__(self, driver: Neo4jDriver):
        self.driver = driver
        
    async def create_backup(
        self,
        output_dir: Path,
        filter_criteria: Dict = None
    ) -> BackupResult:
        """Create full or filtered backup."""
        
    async def backup_schema(self) -> Dict:
        """Backup graph schema."""
        
    async def backup_entities(
        self,
        filter: Dict = None
    ) -> List[Entity]:
        """Backup entities with optional filter."""
        
    async def backup_relationships(
        self,
        entity_uuids: List[str] = None
    ) -> List[Relationship]:
        """Backup relationships."""
```

### RestoreManager Class
```python
class RestoreManager:
    def __init__(self, driver: Neo4jDriver):
        self.driver = driver
        
    async def restore_from_backup(
        self,
        backup_path: Path,
        strategy: RestoreStrategy = RestoreStrategy.MERGE
    ) -> RestoreResult:
        """Restore from backup file."""
        
    async def validate_backup(
        self,
        backup_path: Path
    ) -> ValidationResult:
        """Validate backup integrity."""
```

---

## 🎯 VENTAJAS DEL MÓDULO PROGRAMÁTICO

1. **Eficiencia**: Ejecuta directamente sin overhead de Claude
2. **Reusabilidad**: Código reutilizable para diferentes escenarios
3. **Testing**: Tests automatizados garantizan confiabilidad
4. **Integración**: Se integra con el sistema existente de Graphiti
5. **CLI**: Puede exponerse como comando CLI
6. **API**: Puede exponerse vía MCP server

---

## 📊 ESTIMACIÓN DE ESFUERZO

| Componente | Tiempo Estimado | Complejidad |
|------------|----------------|-------------|
| BackupManager | 4h | Media |
| RestoreManager | 4h | Media |
| Schemas/Models | 2h | Baja |
| Tests | 4h | Media |
| Integración | 2h | Baja |
| **Total** | **16h** | **Media** |

---

## 🚀 PRÓXIMOS PASOS RECOMENDADOS

1. **Aprobar el diseño del módulo**
2. **Crear feature branch**: `feature/backup-module`
3. **Implementar incrementalmente**:
   - Primero: BackupManager básico
   - Segundo: Schemas y validación
   - Tercero: RestoreManager
   - Cuarto: Tests completos
4. **Integrar con MCP server**
5. **Documentar uso y API**

---

## 📝 NOTAS ADICIONALES

- El módulo debe mantener compatibilidad con embeddings de diferentes dimensiones
- Considerar compresión para backups grandes
- Implementar versionado de backups
- Añadir logs detallados para debugging
- Considerar backup incremental en el futuro
- **IMPORTANTE**: El módulo debe soportar tanto backups completos como selectivos

---

*Documento generado durante investigación inicial*
*Autor: Claude Code + Usuario*
*Estado: Investigación completada, esperando decisión de implementación*