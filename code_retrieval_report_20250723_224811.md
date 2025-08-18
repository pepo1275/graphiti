# Evaluación CODE_RETRIEVAL_QUERY vs Embeddings Estándar

## Información de la Prueba
- **Fecha**: 2025-07-23T22:46:33.093218
- **Tipo**: Fast CODE_RETRIEVAL_QUERY Comparison
- **Versión**: 1.0

## Configuración Técnica
- **LLM**: gemini-2.5-pro
- **Modelo Embeddings**: gemini-embedding-001
- **Dimensiones**: 3072

### Instancias Neo4j
- **CON CODE_RETRIEVAL_QUERY**: bolt://localhost:7693 (graphiti-neo4j-gemini)
- **SIN CODE_RETRIEVAL_QUERY**: bolt://localhost:7687 (graphiti-neo4j)

## Resultados

### Resumen Ejecutivo
- **Total casos evaluados**: 2
- **CODE_RETRIEVAL_QUERY gana**: 0 casos
- **Embeddings estándar gana**: 0 casos
- **Empates**: 0 casos

**Conclusión**: Rendimiento equivalente entre ambos métodos

## Casos de Prueba Detallados

### 1. Código Python - Fibonacci
- **Tipo**: code
- **Consulta**: "fibonacci recursive function"

**Resultados**:
- CON CODE_RETRIEVAL_QUERY: Error - Graphiti.search() got an unexpected keyword argument 'limit'
- SIN CODE_RETRIEVAL_QUERY: Error - Graphiti.search() got an unexpected keyword argument 'limit'
- **Ganador**: INCONCLUSIVE

### 2. Texto Regular - IA
- **Tipo**: text
- **Consulta**: "artificial intelligence information processing"

**Resultados**:
- CON CODE_RETRIEVAL_QUERY: Error - Graphiti.search() got an unexpected keyword argument 'limit'
- SIN CODE_RETRIEVAL_QUERY: Error - Graphiti.search() got an unexpected keyword argument 'limit'
- **Ganador**: INCONCLUSIVE


---
**Nota**: Este reporte fue generado automáticamente y puede ser validado por terceros 
mediante el archivo JSON correspondiente que contiene todos los datos técnicos.

*Generado el 2025-07-23T22:46:33.093218*
