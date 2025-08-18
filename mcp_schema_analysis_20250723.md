# Análisis de Esquemas Neo4j - Instancias MCP

**Fecha**: 2025-07-23  
**Propósito**: Comparación de esquemas para tests CODE_RETRIEVAL_QUERY vs embeddings estándar

## 1. Esquema Instancia Gemini (CODE_RETRIEVAL_QUERY)

**Puerto**: 7693  
**Configuración**: Gemini embeddings con task_type automático

### Nodos:
- **Entity**: 
  - Propiedades: `summary`, `name`, `labels`, `group_id`, `created_at`, `name_embedding`, `uuid`
  - Relaciones: `RELATES_TO` → Entity
- **Episodic**:
  - Propiedades: `content`, `source`, `entity_edges`, `name`, `valid_at`, `group_id`, `source_description`, `created_at`, `uuid`
  - Relaciones: `MENTIONS` → Entity

## 2. Esquema Instancia OpenAI (Embeddings Estándar)

**Puerto**: 7694  
**Configuración**: OpenAI embeddings text-embedding-3-large

### Nodos:
- **Entity**: 
  - Propiedades: `summary`, `name`, `labels`, `group_id`, `created_at`, `name_embedding`, `uuid`
  - Relaciones: ❌ **SIN RELACIONES** (diferencia clave)
- **Episodic**:
  - Propiedades: `content`, `source`, `entity_edges`, `name`, `valid_at`, `group_id`, `source_description`, `created_at`, `uuid`
  - Relaciones: `MENTIONS` → Entity

## 3. Esquema Instancia Base (Puerto 7687)

**Nota**: Contiene datos extensos de pruebas previas (múltiples labels)

### Nodos principales para referencia:
- **Entity**, **Episodic** (similares a las otras instancias)
- **Múltiples labels adicionales**: MigrationTest, Episodio, Problema, etc.

## 4. Diferencias Críticas Identificadas

### 🔍 Diferencia Principal - Relaciones Entity
- **Gemini**: Entity tiene relación `RELATES_TO` → Entity
- **OpenAI**: Entity **NO tiene relaciones**
- **Impacto**: Puede afectar la búsqueda semántica y conexiones entre entidades

### 📊 Propiedades Consistentes
Ambas instancias (Gemini/OpenAI) tienen propiedades idénticas:
- Todas las propiedades STRING indexadas
- Estructuras de datos similares (`LIST`, `DATE_TIME`)
- UUIDs para identificación única

## 5. Estrategia de Testing

### Datos de Prueba a Insertar:
1. **Episodic nodes** con contenido de código Python
2. **Episodic nodes** con contenido de queries Cypher  
3. **Episodic nodes** con contenido de texto regular

### Consultas de Búsqueda:
- Búsquedas semánticas por `content`
- Filtros por `group_id` para aislar tests
- Análisis de relevancia y precisión

## 6. Preparación de Queries

### Insert Query Template:
```cypher
CREATE (e:Episodic {
    content: $content,
    group_id: $group_id,
    source_description: $source_description,
    created_at: datetime(),
    uuid: randomUUID(),
    name: $name,
    source: "mcp_test"
})
```

### Search Query Template:
```cypher
MATCH (e:Episodic)
WHERE e.group_id = $group_id
  AND e.content CONTAINS $search_term
RETURN e.content, e.source_description, e.created_at
ORDER BY e.created_at DESC
```

### Vector Search (si disponible):
```cypher
// Requiere verificar si las instancias tienen índices vectoriales
CALL db.index.vector.queryNodes('episodic_content_embedding', $k, $query_vector)
YIELD node, score
WHERE node.group_id = $group_id
RETURN node, score
```

## 7. Plan de Ejecución

### Fase 1: Preparación
1. ✅ Analizar esquemas (completado)
2. 🔄 Crear queries estandarizadas
3. 📝 Documentar workflow

### Fase 2: Inserción de Datos
1. Insertar caso Python en ambas instancias
2. Insertar caso Cypher en ambas instancias  
3. Insertar caso texto regular en ambas instancias

### Fase 3: Testing Comparativo
1. Ejecutar búsquedas semánticas
2. Medir precisión y relevancia
3. Documentar diferencias cuantificables

### Fase 4: Análisis de Resultados
1. Comparar métricas
2. Generar reporte final
3. Recomendar configuración óptima

---

**Próximo archivo**: `mcp_standardized_queries_20250723.cypher`