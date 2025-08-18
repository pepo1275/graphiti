# Guía de Ejecución MCP - CODE_RETRIEVAL_QUERY Test

## 1. Verificar Estado de Instancias

**Herramienta:** `get_status`
- Verificar conectividad con graphiti-neo4j-gemini 
- Verificar conectividad con graphiti-neo4j-openai

## 2. Limpiar Datos Previos (Opcional)

**Herramienta:** `clear_graph` 
- Limpiar instancia Gemini si necesario
- Limpiar instancia OpenAI si necesario

## 3. Ejecutar Casos de Prueba

### Caso 1: Código Python - Fibonacci

**Paso 1 - Agregar a Gemini (CODE_RETRIEVAL_QUERY):**
```
add_memory(
    content="
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# Fun...",
    group_id="test_gemini_python_fibonacci",
    source_description="Test CODE_RETRIEVAL_QUERY - Código Python - Fibonacci"
)
```

**Paso 2 - Agregar a OpenAI (Standard):**  
```
add_memory(
    content="
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# Fun...",
    group_id="test_openai_python_fibonacci",
    source_description="Test Standard Embeddings - Código Python - Fibonacci"
)
```

**Paso 3 - Búsquedas Comparativas:**

- Gemini: `search_memory_nodes(query="fibonacci recursive function python", group_ids=["test_gemini_python_fibonacci"], max_results=3)`
- OpenAI: `search_memory_nodes(query="fibonacci recursive function python", group_ids=["test_openai_python_fibonacci"], max_results=3)`

- Gemini: `search_memory_nodes(query="calculate fibonacci sequence", group_ids=["test_gemini_python_fibonacci"], max_results=3)`
- OpenAI: `search_memory_nodes(query="calculate fibonacci sequence", group_ids=["test_openai_python_fibonacci"], max_results=3)`

- Gemini: `search_memory_nodes(query="recursive algorithm fibonacci", group_ids=["test_gemini_python_fibonacci"], max_results=3)`
- OpenAI: `search_memory_nodes(query="recursive algorithm fibonacci", group_ids=["test_openai_python_fibonacci"], max_results=3)`
### Caso 2: Query Cypher - Personas y Empresas

**Paso 1 - Agregar a Gemini (CODE_RETRIEVAL_QUERY):**
```
add_memory(
    content="
MATCH (p:Person)-[:WORKS_AT]->(c:Company)
WHERE p.age > 30 AND c.industry = 'Technology'
RETURN p.n...",
    group_id="test_gemini_cypher_query",
    source_description="Test CODE_RETRIEVAL_QUERY - Query Cypher - Personas y Empresas"
)
```

**Paso 2 - Agregar a OpenAI (Standard):**  
```
add_memory(
    content="
MATCH (p:Person)-[:WORKS_AT]->(c:Company)
WHERE p.age > 30 AND c.industry = 'Technology'
RETURN p.n...",
    group_id="test_openai_cypher_query",
    source_description="Test Standard Embeddings - Query Cypher - Personas y Empresas"
)
```

**Paso 3 - Búsquedas Comparativas:**

- Gemini: `search_memory_nodes(query="cypher query person company relationship", group_ids=["test_gemini_cypher_query"], max_results=3)`
- OpenAI: `search_memory_nodes(query="cypher query person company relationship", group_ids=["test_openai_cypher_query"], max_results=3)`

- Gemini: `search_memory_nodes(query="find employees in technology companies", group_ids=["test_gemini_cypher_query"], max_results=3)`
- OpenAI: `search_memory_nodes(query="find employees in technology companies", group_ids=["test_openai_cypher_query"], max_results=3)`

- Gemini: `search_memory_nodes(query="graph database query workers", group_ids=["test_gemini_cypher_query"], max_results=3)`
- OpenAI: `search_memory_nodes(query="graph database query workers", group_ids=["test_openai_cypher_query"], max_results=3)`
### Caso 3: Texto Regular - Descripción IA

**Paso 1 - Agregar a Gemini (CODE_RETRIEVAL_QUERY):**
```
add_memory(
    content="
Artificial intelligence represents a transformative technology that enables machines to 
simulate h...",
    group_id="test_gemini_regular_text",
    source_description="Test CODE_RETRIEVAL_QUERY - Texto Regular - Descripción IA"
)
```

**Paso 2 - Agregar a OpenAI (Standard):**  
```
add_memory(
    content="
Artificial intelligence represents a transformative technology that enables machines to 
simulate h...",
    group_id="test_openai_regular_text",
    source_description="Test Standard Embeddings - Texto Regular - Descripción IA"
)
```

**Paso 3 - Búsquedas Comparativas:**

- Gemini: `search_memory_nodes(query="artificial intelligence machine learning", group_ids=["test_gemini_regular_text"], max_results=3)`
- OpenAI: `search_memory_nodes(query="artificial intelligence machine learning", group_ids=["test_openai_regular_text"], max_results=3)`

- Gemini: `search_memory_nodes(query="cognitive processes algorithms", group_ids=["test_gemini_regular_text"], max_results=3)`
- OpenAI: `search_memory_nodes(query="cognitive processes algorithms", group_ids=["test_openai_regular_text"], max_results=3)`

- Gemini: `search_memory_nodes(query="pattern identification datasets", group_ids=["test_gemini_regular_text"], max_results=3)`
- OpenAI: `search_memory_nodes(query="pattern identification datasets", group_ids=["test_openai_regular_text"], max_results=3)`

## 4. Analizar Resultados

Para cada búsqueda, comparar:
- Número de resultados encontrados
- Relevancia de los resultados (si contienen el contenido buscado)
- Precisión semántica

## 5. Documentar Conclusiones

- CODE_RETRIEVAL_QUERY vs Standard para casos de código
- Diferencias en casos de texto regular
- Recomendación final

---
*Generado el 2025-07-23T23:17:48.317558*
