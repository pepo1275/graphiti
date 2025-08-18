# Workflow MCP Testing - CODE_RETRIEVAL_QUERY vs Standard Embeddings

**Fecha**: 2025-07-23  
**Propósito**: Documentación sistemática para comparación cuantitativa  
**Alcance**: Proceso reproducible para evaluaciones futuras y agentes automatizados

---

## 📋 OVERVIEW DEL PROCESO

### Objetivo Principal
Comparar la efectividad de CODE_RETRIEVAL_QUERY (Gemini) vs embeddings estándar (OpenAI) en búsqueda semántica de código Python y Cypher.

### Instancias de Prueba
- **Gemini Instance** (Puerto 7693): CODE_RETRIEVAL_QUERY habilitado
- **OpenAI Instance** (Puerto 7694): Embeddings estándar text-embedding-3-large
- **Dimensiones**: 3072 (balanceadas para comparación justa)

---

## 🔄 FASE 1: PREPARACIÓN Y VERIFICACIÓN

### 1.1 Verificación de Conectividad MCP
```bash
# Verificar servidores MCP disponibles
claude mcp list

# Resultado esperado:
# ✓ neo4j-docker-graphiti-gemini
# ✓ neo4j-docker-graphiti-openai
# ✓ neo4j-data-modeling
```

### 1.2 Verificación de Esquemas
**Herramienta MCP**: `get_neo4j_schema`

**Comando para Gemini**:
```python
mcp__neo4j-docker-graphiti-gemini__graphiti_gemini-get_neo4j_schema()
```

**Comando para OpenAI**:
```python
mcp__neo4j-docker-graphiti-openai__graphiti_openai-get_neo4j_schema()
```

**Validación Esperada**:
- Ambas instancias deben tener labels: `Entity`, `Episodic`
- Propiedades consistentes entre instancias
- ⚠️ **Diferencia**: Gemini tiene `Entity.RELATES_TO`, OpenAI no

### 1.3 Limpieza de Datos Previos (Opcional)
**Solo si es necesario limpiar datos de pruebas anteriores**

```cypher
// Verificar datos existentes de pruebas
MATCH (e:Episodic)
WHERE e.source = "mcp_comparative_test"
RETURN count(*) as existing_test_records;

// Si >0, ejecutar limpieza:
MATCH (e:Episodic)
WHERE e.source = "mcp_comparative_test"
DELETE e;
```

---

## 🔄 FASE 2: INSERCIÓN DE DATOS DE PRUEBA

### 2.1 Casos de Prueba Definidos

| Caso | Tipo | Contenido | Beneficio Esperado |
|------|------|-----------|-------------------|
| Python Fibonacci | Código | Función recursiva Python | **HIGH** |
| Cypher Query | Código | Query Neo4j complejo | **HIGH** |
| Texto IA | Texto | Descripción tecnológica | **LOW** |

### 2.2 Proceso de Inserción

**Para cada caso de prueba**:
1. Ejecutar query INSERT en instancia Gemini
2. Ejecutar query INSERT en instancia OpenAI  
3. Verificar inserción exitosa
4. Continuar con siguiente caso

**Template de Comando MCP**:
```python
mcp__neo4j-docker-graphiti-gemini__graphiti_gemini-write_neo4j_cypher(
    query="CREATE (e:Episodic { content: $content, group_id: $group_id, ... })",
    params={"content": "...", "group_id": "test_gemini_python_fibonacci", ...}
)
```

### 2.3 Verificación de Inserción
**Después de cada inserción**:

```cypher
MATCH (e:Episodic)
WHERE e.group_id STARTS WITH "test_gemini" OR e.group_id STARTS WITH "test_openai"
RETURN e.group_id, e.name, e.created_at
ORDER BY e.created_at DESC;
```

**Resultado Esperado**: 6 registros total (3 Gemini + 3 OpenAI)

---

## 🔄 FASE 3: EJECUCIÓN DE BÚSQUEDAS COMPARATIVAS

### 3.1 Metodología de Búsqueda

**Para cada caso de prueba (3 casos)**:
- Ejecutar 3 búsquedas diferentes por caso
- Total: 9 búsquedas × 2 instancias = **18 búsquedas totales**

### 3.2 Búsquedas por Caso

#### Caso 1: Python Fibonacci
1. `"fibonacci recursive function python"`
2. `"calculate fibonacci sequence"`  
3. `"recursive algorithm fibonacci"`

#### Caso 2: Cypher Query
1. `"cypher query person company relationship"`
2. `"find employees in technology companies"`
3. `"graph database query workers"`

#### Caso 3: Texto Regular IA
1. `"artificial intelligence machine learning"`
2. `"cognitive processes algorithms"`
3. `"pattern identification datasets"`

### 3.3 Template de Ejecución

**Para cada búsqueda**:
```python
# Búsqueda en Gemini
result_gemini = mcp__neo4j-docker-graphiti-gemini__graphiti_gemini-read_neo4j_cypher(
    query="MATCH (e:Episodic) WHERE e.group_id = $group_id AND (condiciones_busqueda) RETURN e.content, e.source_description",
    params={"group_id": "test_gemini_python_fibonacci"}
)

# Búsqueda en OpenAI
result_openai = mcp__neo4j-docker-graphiti-openai__graphiti_openai-read_neo4j_cypher(
    query="MATCH (e:Episodic) WHERE e.group_id = $group_id AND (condiciones_busqueda) RETURN e.content, e.source_description",
    params={"group_id": "test_openai_python_fibonacci"}
)
```

---

## 🔄 FASE 4: RECOLECCIÓN Y ANÁLISIS DE RESULTADOS

### 4.1 Métricas a Recolectar

**Por cada búsqueda**:
- **Número de resultados encontrados**
- **Relevancia del contenido** (¿contiene lo buscado?)
- **Tiempo de respuesta** (si disponible)
- **Precisión semántica** (evaluación cualitativa)

### 4.2 Estructura de Resultados

```json
{
  "timestamp": "2025-07-23T...",
  "test_case": "python_fibonacci",
  "search_query": "fibonacci recursive function python",
  "results": {
    "gemini": {
      "instance": "CODE_RETRIEVAL_QUERY",
      "results_count": 1,
      "found_content": true,
      "relevance_score": "HIGH",
      "response_time_ms": null
    },
    "openai": {
      "instance": "STANDARD_EMBEDDINGS", 
      "results_count": 1,
      "found_content": true,
      "relevance_score": "MEDIUM",
      "response_time_ms": null
    }
  }
}
```

### 4.3 Criterios de Evaluación

#### Relevancia Alta (HIGH)
- Resultado contiene exactamente el contenido buscado
- Términos de búsqueda coinciden semánticamente
- Contexto apropiado preservado

#### Relevancia Media (MEDIUM)
- Resultado relacionado pero no exacto
- Algunos términos coinciden
- Contexto parcialmente relevante

#### Relevancia Baja (LOW)
- Resultado no relacionado con búsqueda
- Coincidencia accidental de términos
- Sin contexto semántico

---

## 🔄 FASE 5: GENERACIÓN DE REPORTE FINAL

### 5.1 Análisis Cuantitativo

**Métricas Clave**:
- **Casos de código** (Python + Cypher): ¿Gemini > OpenAI?
- **Casos de texto**: ¿Diferencia significativa?
- **Mejora porcentual** en precisión semántica
- **Tasa de éxito** (búsquedas exitosas / total)

### 5.2 Criterios de Éxito

#### ✅ Éxito Mínimo
- CODE_RETRIEVAL_QUERY ≥ +10% mejor en casos de código
- Sin degradación >5% en casos de texto regular
- Al menos 6/9 búsquedas de código exitosas

#### 🎯 Éxito Óptimo  
- CODE_RETRIEVAL_QUERY ≥ +20% mejor en casos de código
- Mejora o neutralidad en casos de texto
- 8/9 búsquedas de código exitosas

### 5.3 Formato de Reporte

```markdown
# Reporte Final - CODE_RETRIEVAL_QUERY vs Standard Embeddings

## Resumen Ejecutivo
- **Resultado**: [RECOMMEND / NOT_RECOMMEND] CODE_RETRIEVAL_QUERY
- **Mejora en código**: +X% vs embeddings estándar
- **Impacto en texto**: +/-Y% vs embeddings estándar

## Métricas Detalladas
[Tabla comparativa con todos los resultados]

## Recomendación
[Análisis técnico y recomendación para producción]
```

---

## 🔄 FASE 6: LIMPIEZA Y DOCUMENTACIÓN

### 6.1 Limpieza de Datos de Prueba
```cypher
// Ejecutar al final para limpiar datos de prueba
MATCH (e:Episodic)
WHERE e.source = "mcp_comparative_test"
DELETE e;
```

### 6.2 Archivos Generados
- ✅ `mcp_schema_analysis_20250723.md`
- ✅ `mcp_standardized_queries_20250723.cypher`  
- ✅ `mcp_testing_workflow_20250723.md` (este archivo)
- 🔄 `mcp_comparative_results_20250723.json` (pendiente)
- 🔄 `mcp_final_report_20250723.md` (pendiente)

---

## 🤖 AUTOMATIZACIÓN FUTURA

### Consideraciones para Agentes
1. **Validación de prerrequisitos**: Verificar conectividad MCP antes de iniciar
2. **Manejo de errores**: Reintentos automáticos en fallos de conexión
3. **Paralelización**: Ejecutar búsquedas en paralelo cuando sea posible
4. **Validación de resultados**: Verificar estructura de respuestas MCP
5. **Rollback automático**: Limpieza en caso de fallos parciales

### Hooks y Triggers
- **Pre-ejecución**: Verificar instancias Neo4j activas
- **Post-inserción**: Validar datos insertados correctamente  
- **Post-búsqueda**: Verificar formato de resultados
- **Post-análisis**: Generar reporte automático

---

## 📝 NOTAS PARA DESARROLLADORES

### Limitaciones Identificadas
1. **Búsquedas semánticas**: Las queries actuales usan `CONTAINS`, no búsqueda vectorial
2. **Índices vectoriales**: No confirmado si están disponibles en las instancias
3. **Tiempo de respuesta**: No medido en esta versión del workflow
4. **Escalabilidad**: Diseñado para casos de prueba pequeños (3 casos)

### Mejoras Futuras
1. **Búsqueda vectorial real**: Implementar queries con embeddings
2. **Casos de prueba ampliados**: Agregar más tipos de código
3. **Métricas avanzadas**: Medir tiempo de respuesta y throughput
4. **Evaluación automática**: Scoring automatizado de relevancia

---

**Última actualización**: 2025-07-23  
**Próximo paso**: Ejecutar workflow completo con herramientas MCP  
**Archivos relacionados**: 
- `CODE_RETRIEVAL_QUERY_STATUS_COMPLETE.md`
- `mcp_test_plan_20250723_231748.json`
- `mcp_execution_guide_20250723_231748.md`