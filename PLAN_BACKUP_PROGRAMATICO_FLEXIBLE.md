# 📋 PLAN BACKUP PROGRAMÁTICO FLEXIBLE - GRAPHITI

## 🎯 OBJETIVO
Crear un sistema de backup programático flexible que permita:
- ✅ **Backup completo** de toda la base de datos
- ✅ **Backup selectivo** por filtros configurables  
- ✅ **Backup granular** de campos específicos
- ✅ **Validación automática** con tests integrados
- ✅ **Queries Cypher validadas** con MCP neo4j-data-modeling

---

## 📊 ANÁLISIS DEL ESQUEMA ACTUAL

### Tipos de Nodos Identificados (19 tipos)
```
CORE TYPES (Sistema Principal):
- Episodic (episodios principales con embeddings)
- Entity (entidades con name_embedding 1024/3072)

WORKFLOW TYPES (Flujo de procesos):
- Episode, LearningEpisode (episodios de aprendizaje)
- MethodologyNode, OperationalGuide, Step

DOMAIN TYPES (Dominio específico):
- Episodio, Problema, Solucion, Contexto, Paso, Leccion
- BuenaPractica, ComandoUtil, Instancia, ConfiguracionExitosa
- ResumenEjecutivo, ImpactoEpisodio

INFRASTRUCTURE TYPES (Infraestructura):
- Container, MCPServer, Plataforma, Herramienta
- Troubleshooting, Metricas, Consulta, Usuario

TEST TYPES:
- MigrationTest (temporal)
```

### Campos Críticos Detectados
- **Embeddings**: `name_embedding` (Entity) - CRÍTICO
- **UUID**: Presente en todos los tipos principales  
- **Timestamps**: `created_at`, `valid_at`, `last_updated`
- **Metadatos**: `group_id`, `name`, `description`

---

## 🏗️ ARQUITECTURA DEL SISTEMA FLEXIBLE

### Estructura de Directorios
```
graphiti_backup_system/
├── backup_engine/
│   ├── __init__.py
│   ├── core_backup.py          # Motor principal
│   ├── query_builder.py        # Constructor de queries
│   ├── filter_engine.py        # Sistema de filtros
│   ├── validator.py            # Validador con MCP
│   └── storage.py              # Almacenamiento
├── filters/
│   ├── __init__.py
│   ├── node_filters.py         # Filtros por tipo de nodo
│   ├── field_filters.py        # Filtros por campos
│   ├── relationship_filters.py # Filtros por relaciones
│   └── custom_filters.py       # Filtros personalizados
├── tests/
│   ├── __init__.py
│   ├── test_queries.py         # Tests de Cypher
│   ├── test_integrity.py       # Tests de integridad
│   ├── test_restore.py         # Tests de restauración
│   └── test_performance.py     # Tests de rendimiento
├── configs/
│   ├── backup_profiles.json    # Perfiles pre-configurados
│   ├── field_mappings.json     # Mapeos de campos
│   └── validation_rules.json   # Reglas de validación
├── docs/
│   ├── USER_GUIDE.md
│   ├── API_REFERENCE.md
│   └── EXAMPLES.md
└── scripts/
    ├── backup_full.py          # Backup completo
    ├── backup_selective.py     # Backup selectivo
    └── backup_custom.py        # Backup personalizado
```

---

## 🔧 COMPONENTES PRINCIPALES

### 1. Core Backup Engine
```python
class FlexibleBackupEngine:
    \"\"\"Motor principal de backup flexible\"\"\"
    
    def __init__(self, config: BackupConfig):
        self.config = config
        self.query_builder = QueryBuilder()
        self.filter_engine = FilterEngine()
        self.validator = MCPValidator()
        self.storage = StorageManager()
    
    def create_backup(self, filters: BackupFilters) -> BackupResult:
        \"\"\"Crear backup con filtros específicos\"\"\"
        
    def validate_queries(self, queries: List[str]) -> ValidationResult:
        \"\"\"Validar queries con MCP neo4j-data-modeling\"\"\"
        
    def test_backup_integrity(self, backup_path: str) -> IntegrityResult:
        \"\"\"Verificar integridad del backup\"\"\"
```

### 2. Sistema de Filtros Configurables
```python
@dataclass
class BackupFilters:
    # Filtros de nodos
    node_types: Optional[List[str]] = None          # ['Entity', 'Episodic']
    node_properties: Optional[Dict[str, Any]] = None # {'group_id': 'problem_solving'}
    
    # Filtros de campos  
    include_fields: Optional[List[str]] = None      # ['uuid', 'name', 'name_embedding']
    exclude_fields: Optional[List[str]] = None      # ['internal_metadata']
    
    # Filtros por embeddings
    embedding_dimensions: Optional[List[int]] = None # [1024, 3072]
    has_embeddings: Optional[bool] = None            # True/False
    
    # Filtros temporales
    created_after: Optional[datetime] = None
    created_before: Optional[datetime] = None
    
    # Filtros de relaciones
    include_relationships: bool = True
    relationship_types: Optional[List[str]] = None   # ['RELATES_TO', 'MENTIONS']
    
    # Filtros personalizados
    custom_cypher_where: Optional[str] = None        # "n.summary CONTAINS 'important'"
```

### 3. Perfiles Pre-configurados
```json
{
  "profiles": {
    "full_database": {
      "description": "Backup completo de toda la base de datos",
      "filters": {
        "node_types": null,
        "include_relationships": true,
        "storage_strategy": "hierarchical"
      }
    },
    "entities_with_embeddings": {
      "description": "Solo entidades con embeddings",
      "filters": {
        "node_types": ["Entity"],
        "has_embeddings": true,
        "include_fields": ["uuid", "name", "name_embedding", "summary"]
      }
    },
    "critical_1024_embeddings": {
      "description": "Entidades críticas con embeddings 1024",
      "filters": {
        "node_types": ["Entity"],
        "embedding_dimensions": [1024],
        "include_relationships": true
      }
    },
    "workflow_episodes": {
      "description": "Episodios y flujos de trabajo",
      "filters": {
        "node_types": ["Episode", "LearningEpisode", "Episodic"],
        "include_relationships": true
      }
    },
    "infrastructure_only": {
      "description": "Solo componentes de infraestructura",
      "filters": {
        "node_types": ["Container", "MCPServer", "Plataforma", "Herramienta"],
        "exclude_fields": ["internal_logs"]
      }
    }
  }
}
```

---

## 📝 QUERIES CYPHER VALIDADAS

### Query Base Para Nodos Con Filtros
```cypher
// Query Template - Validar con MCP neo4j-data-modeling
MATCH (n:{node_types})
WHERE {where_conditions}
WITH n, {field_selection}
RETURN {
    backup_metadata: {
        timestamp: datetime(),
        node_type: labels(n)[0],
        backup_profile: $profile_name,
        filter_applied: $filters_applied
    },
    node_data: {field_mapping},
    relationships: CASE 
        WHEN $include_relationships THEN [
            (n)-[r]->(m) | {
                type: type(r),
                properties: properties(r),
                target: {
                    uuid: m.uuid,
                    labels: labels(m),
                    name: coalesce(m.name, 'unnamed')
                }
            }
        ]
        ELSE []
    END
} as backup_record
```

### Queries Específicas Por Caso de Uso

#### 1. Backup de Entidades con Embeddings
```cypher
MATCH (n:Entity)
WHERE size(n.name_embedding) IN $embedding_dimensions
RETURN {
    core_data: {
        uuid: n.uuid,
        name: n.name,
        group_id: n.group_id,
        created_at: n.created_at,
        summary: n.summary
    },
    embeddings: {
        name_embedding: n.name_embedding,
        dimension: size(n.name_embedding)
    },
    metadata: {
        labels: labels(n),
        all_properties: keys(n)
    }
} as entity_backup
```

#### 2. Backup Completo Por Tipo
```cypher
CALL apoc.meta.nodeTypeProperties() YIELD nodeType, propertyName, propertyTypes
WITH nodeType, collect({name: propertyName, types: propertyTypes}) as props
WHERE nodeType IN $node_types
MATCH (n) WHERE any(label IN labels(n) WHERE label = nodeType)
RETURN {
    schema: {type: nodeType, properties: props},
    nodes: collect({
        uuid: coalesce(n.uuid, toString(id(n))),
        properties: properties(n)
    })
} as type_backup
```

#### 3. Backup de Relaciones Específicas
```cypher
MATCH (a)-[r:{relationship_types}]->(b)
WHERE any(label IN labels(a) WHERE label IN $source_types)
  AND any(label IN labels(b) WHERE label IN $target_types)
RETURN {
    relationship: {
        type: type(r),
        properties: properties(r)
    },
    source: {
        uuid: coalesce(a.uuid, toString(id(a))),
        labels: labels(a),
        name: coalesce(a.name, 'unnamed')
    },
    target: {
        uuid: coalesce(b.uuid, toString(id(b))),
        labels: labels(b), 
        name: coalesce(b.name, 'unnamed')
    }
} as relationship_backup
```

---

## 🧪 SISTEMA DE TESTS AUTOMATIZADOS

### Test Suite Estructura
```python
class BackupTestSuite:
    \"\"\"Suite completa de tests para backup flexible\"\"\"
    
    def test_query_validation_with_mcp(self):
        \"\"\"Test: Validar todas las queries con MCP neo4j-data-modeling\"\"\"
        
    def test_backup_profiles(self):
        \"\"\"Test: Verificar todos los perfiles de backup\"\"\"
        
    def test_filter_combinations(self):
        \"\"\"Test: Probar combinaciones de filtros\"\"\"
        
    def test_backup_integrity(self):
        \"\"\"Test: Verificar integridad de backups\"\"\"
        
    def test_restore_functionality(self):
        \"\"\"Test: Probar restauración de backups\"\"\"
        
    def test_performance_limits(self):
        \"\"\"Test: Verificar límites de rendimiento\"\"\"
        
    def test_edge_cases(self):
        \"\"\"Test: Casos extremos y errores\"\"\"
```

### Tests de Integridad Específicos
```python
def test_embedding_integrity(backup_file: str):
    \"\"\"Verificar integridad de embeddings respaldados\"\"\"
    # 1. Leer backup
    # 2. Validar dimensiones 
    # 3. Verificar rangos de valores
    # 4. Comparar con fuente original
    # 5. Test de restauración
    
def test_relationship_consistency(backup_file: str):
    \"\"\"Verificar consistencia de relaciones\"\"\"
    # 1. Validar que todos los UUIDs referenciados existen
    # 2. Verificar tipos de relaciones válidos
    # 3. Comprobar integridad referencial
```

---

## 📋 EJEMPLOS DE USO

### Ejemplo 1: Backup Completo
```python
from graphiti_backup_system import FlexibleBackupEngine, BackupFilters

# Configurar backup completo
filters = BackupFilters()  # Sin filtros = todo
engine = FlexibleBackupEngine(config_file="configs/production.json")

# Ejecutar backup
result = engine.create_backup(
    filters=filters,
    output_dir="/backups/full_20250818",
    profile="full_database"
)
```

### Ejemplo 2: Backup Solo Embeddings 1024
```python
# Backup específico de embeddings 1024 (como el que hicimos)
filters = BackupFilters(
    node_types=["Entity"],
    embedding_dimensions=[1024],
    include_fields=["uuid", "name", "name_embedding", "summary"],
    include_relationships=True
)

result = engine.create_backup(
    filters=filters,
    output_dir="/backups/embeddings_1024",
    profile="critical_1024_embeddings"
)
```

### Ejemplo 3: Backup Filtrado por Fechas
```python
from datetime import datetime, timedelta

# Backup de datos recientes
filters = BackupFilters(
    created_after=datetime.now() - timedelta(days=30),
    node_types=["Episode", "LearningEpisode"],
    custom_cypher_where="n.status = 'completed'"
)

result = engine.create_backup(filters=filters)
```

---

## 🚀 IMPLEMENTACIÓN PASO A PASO

### Fase 1: Core Engine (Semana 1)
- [ ] Estructura de directorios base
- [ ] Clase FlexibleBackupEngine
- [ ] Sistema de filtros básico
- [ ] Integración con MCP para validación
- [ ] Tests unitarios básicos

### Fase 2: Queries y Validación (Semana 2) 
- [ ] QueryBuilder con templates
- [ ] Validación automática con MCP neo4j-data-modeling
- [ ] Perfiles de backup pre-configurados
- [ ] Tests de queries específicas

### Fase 3: Storage y Restore (Semana 3)
- [ ] StorageManager flexible
- [ ] Sistema de compresión opcional
- [ ] Scripts de restauración automáticos
- [ ] Tests de integridad completos

### Fase 4: Interfaz y Documentación (Semana 4)
- [ ] CLI amigable
- [ ] Documentación completa
- [ ] Ejemplos de uso
- [ ] Tests de rendimiento

---

## ✅ CRITERIOS DE ACEPTACIÓN

### Funcionalidad
- ✅ Backup completo de base de datos en < 5 minutos
- ✅ Backup selectivo con cualquier combinación de filtros
- ✅ Validación automática de todas las queries Cypher
- ✅ Restauración verificada al 100%
- ✅ Tests automatizados con cobertura > 90%

### Calidad
- ✅ Queries validadas por MCP neo4j-data-modeling
- ✅ Sin pérdida de datos en el proceso
- ✅ Manejo robusto de errores
- ✅ Documentación completa
- ✅ Siguiendo metodología CLAUDE.md

---

## 🎯 PRÓXIMO CHECKPOINT

**SEGÚN CLAUDE.MD:** Plan detallado → STOP → Esperar aprobación

**PREGUNTA:** ¿Apruebas este plan para proceder con la implementación del sistema de backup programático flexible?

---

**AUTOR:** Claude Code  
**METODOLOGÍA:** CLAUDE.md v1.0  
**BASADO EN:** Experiencia exitosa con triple backup de embeddings 1024  
**TIMESTAMP:** 2025-08-18 20:00 UTC