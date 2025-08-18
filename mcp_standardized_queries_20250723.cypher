-- =====================================================
-- MCP STANDARDIZED QUERIES - CODE_RETRIEVAL_QUERY TEST
-- =====================================================
-- Fecha: 2025-07-23
-- Propósito: Queries estandarizadas para comparación
-- Instancias: Gemini (CODE_RETRIEVAL_QUERY) vs OpenAI (Standard)
-- =====================================================

-- =====================================================
-- 1. QUERIES DE INSERCIÓN DE DATOS DE PRUEBA
-- =====================================================

-- -----------------------------------------------------
-- 1.1 Caso Python - Fibonacci (Gemini Instance)
-- -----------------------------------------------------
CREATE (e:Episodic {
    content: "\ndef fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)\n\n# Función recursiva para calcular secuencia de Fibonacci\n# Ejemplo: fibonacci(10) = 55\n",
    group_id: "test_gemini_python_fibonacci",
    source_description: "Test CODE_RETRIEVAL_QUERY - Código Python - Fibonacci",
    created_at: datetime(),
    uuid: randomUUID(),
    name: "fibonacci_test_gemini",
    source: "mcp_comparative_test",
    valid_at: datetime()
});

-- -----------------------------------------------------
-- 1.2 Caso Python - Fibonacci (OpenAI Instance)
-- -----------------------------------------------------
CREATE (e:Episodic {
    content: "\ndef fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)\n\n# Función recursiva para calcular secuencia de Fibonacci\n# Ejemplo: fibonacci(10) = 55\n",
    group_id: "test_openai_python_fibonacci",
    source_description: "Test Standard Embeddings - Código Python - Fibonacci",
    created_at: datetime(),
    uuid: randomUUID(),
    name: "fibonacci_test_openai",
    source: "mcp_comparative_test",
    valid_at: datetime()
});

-- -----------------------------------------------------
-- 1.3 Caso Cypher - Query Personas y Empresas (Gemini)
-- -----------------------------------------------------
CREATE (e:Episodic {
    content: "\nMATCH (p:Person)-[:WORKS_AT]->(c:Company)\nWHERE p.age > 30 AND c.industry = 'Technology'\nRETURN p.name, c.name, p.salary\nORDER BY p.salary DESC\nLIMIT 10\n",
    group_id: "test_gemini_cypher_query",
    source_description: "Test CODE_RETRIEVAL_QUERY - Query Cypher - Personas y Empresas",
    created_at: datetime(),
    uuid: randomUUID(),
    name: "cypher_test_gemini",
    source: "mcp_comparative_test",
    valid_at: datetime()
});

-- -----------------------------------------------------
-- 1.4 Caso Cypher - Query Personas y Empresas (OpenAI)
-- -----------------------------------------------------
CREATE (e:Episodic {
    content: "\nMATCH (p:Person)-[:WORKS_AT]->(c:Company)\nWHERE p.age > 30 AND c.industry = 'Technology'\nRETURN p.name, c.name, p.salary\nORDER BY p.salary DESC\nLIMIT 10\n",
    group_id: "test_openai_cypher_query",
    source_description: "Test Standard Embeddings - Query Cypher - Personas y Empresas",
    created_at: datetime(),
    uuid: randomUUID(),
    name: "cypher_test_openai",
    source: "mcp_comparative_test",
    valid_at: datetime()
});

-- -----------------------------------------------------
-- 1.5 Caso Texto Regular - Descripción IA (Gemini)
-- -----------------------------------------------------
CREATE (e:Episodic {
    content: "\nArtificial intelligence represents a transformative technology that enables machines to \nsimulate human cognitive processes. Machine learning algorithms can identify patterns \nin large datasets and make predictions or decisions without explicit programming.\n",
    group_id: "test_gemini_regular_text",
    source_description: "Test CODE_RETRIEVAL_QUERY - Texto Regular - Descripción IA",
    created_at: datetime(),
    uuid: randomUUID(),
    name: "text_test_gemini",
    source: "mcp_comparative_test",
    valid_at: datetime()
});

-- -----------------------------------------------------
-- 1.6 Caso Texto Regular - Descripción IA (OpenAI)
-- -----------------------------------------------------
CREATE (e:Episodic {
    content: "\nArtificial intelligence represents a transformative technology that enables machines to \nsimulate human cognitive processes. Machine learning algorithms can identify patterns \nin large datasets and make predictions or decisions without explicit programming.\n",
    group_id: "test_openai_regular_text",
    source_description: "Test Standard Embeddings - Texto Regular - Descripción IA",
    created_at: datetime(),
    uuid: randomUUID(),
    name: "text_test_openai",
    source: "mcp_comparative_test",
    valid_at: datetime()
});

-- =====================================================
-- 2. QUERIES DE BÚSQUEDA COMPARATIVA
-- =====================================================

-- -----------------------------------------------------
-- 2.1 Verificación de Datos Insertados
-- -----------------------------------------------------

-- Verificar datos Gemini
MATCH (e:Episodic)
WHERE e.group_id STARTS WITH "test_gemini"
RETURN e.group_id, e.name, e.source_description, e.created_at
ORDER BY e.created_at DESC;

-- Verificar datos OpenAI
MATCH (e:Episodic)
WHERE e.group_id STARTS WITH "test_openai"
RETURN e.group_id, e.name, e.source_description, e.created_at
ORDER BY e.created_at DESC;

-- -----------------------------------------------------
-- 2.2 Búsquedas Caso Python - Fibonacci
-- -----------------------------------------------------

-- Búsqueda 1: "fibonacci recursive function python"
-- Gemini
MATCH (e:Episodic)
WHERE e.group_id = "test_gemini_python_fibonacci"
  AND (e.content CONTAINS "fibonacci" OR e.content CONTAINS "recursive")
RETURN e.content, e.source_description, e.created_at, 
       "GEMINI_FIBONACCI_SEARCH_1" as test_case;

-- OpenAI
MATCH (e:Episodic)
WHERE e.group_id = "test_openai_python_fibonacci"
  AND (e.content CONTAINS "fibonacci" OR e.content CONTAINS "recursive")
RETURN e.content, e.source_description, e.created_at,
       "OPENAI_FIBONACCI_SEARCH_1" as test_case;

-- Búsqueda 2: "calculate fibonacci sequence"
-- Gemini
MATCH (e:Episodic)
WHERE e.group_id = "test_gemini_python_fibonacci"
  AND (e.content CONTAINS "fibonacci" OR e.content CONTAINS "sequence")
RETURN e.content, e.source_description, e.created_at,
       "GEMINI_FIBONACCI_SEARCH_2" as test_case;

-- OpenAI
MATCH (e:Episodic)
WHERE e.group_id = "test_openai_python_fibonacci"
  AND (e.content CONTAINS "fibonacci" OR e.content CONTAINS "sequence")
RETURN e.content, e.source_description, e.created_at,
       "OPENAI_FIBONACCI_SEARCH_2" as test_case;

-- Búsqueda 3: "recursive algorithm fibonacci"
-- Gemini
MATCH (e:Episodic)
WHERE e.group_id = "test_gemini_python_fibonacci"
  AND (e.content CONTAINS "recursive" OR e.content CONTAINS "algorithm")
RETURN e.content, e.source_description, e.created_at,
       "GEMINI_FIBONACCI_SEARCH_3" as test_case;

-- OpenAI
MATCH (e:Episodic)
WHERE e.group_id = "test_openai_python_fibonacci"
  AND (e.content CONTAINS "recursive" OR e.content CONTAINS "algorithm")
RETURN e.content, e.source_description, e.created_at,
       "OPENAI_FIBONACCI_SEARCH_3" as test_case;

-- -----------------------------------------------------
-- 2.3 Búsquedas Caso Cypher - Personas y Empresas
-- -----------------------------------------------------

-- Búsqueda 1: "cypher query person company relationship"
-- Gemini
MATCH (e:Episodic)
WHERE e.group_id = "test_gemini_cypher_query"
  AND (e.content CONTAINS "Person" OR e.content CONTAINS "Company" OR e.content CONTAINS "WORKS_AT")
RETURN e.content, e.source_description, e.created_at,
       "GEMINI_CYPHER_SEARCH_1" as test_case;

-- OpenAI
MATCH (e:Episodic)
WHERE e.group_id = "test_openai_cypher_query"
  AND (e.content CONTAINS "Person" OR e.content CONTAINS "Company" OR e.content CONTAINS "WORKS_AT")
RETURN e.content, e.source_description, e.created_at,
       "OPENAI_CYPHER_SEARCH_1" as test_case;

-- Búsqueda 2: "find employees in technology companies"
-- Gemini
MATCH (e:Episodic)
WHERE e.group_id = "test_gemini_cypher_query"
  AND (e.content CONTAINS "Technology" OR e.content CONTAINS "industry" OR e.content CONTAINS "salary")
RETURN e.content, e.source_description, e.created_at,
       "GEMINI_CYPHER_SEARCH_2" as test_case;

-- OpenAI
MATCH (e:Episodic)
WHERE e.group_id = "test_openai_cypher_query"
  AND (e.content CONTAINS "Technology" OR e.content CONTAINS "industry" OR e.content CONTAINS "salary")
RETURN e.content, e.source_description, e.created_at,
       "OPENAI_CYPHER_SEARCH_2" as test_case;

-- Búsqueda 3: "graph database query workers"
-- Gemini
MATCH (e:Episodic)
WHERE e.group_id = "test_gemini_cypher_query"
  AND (e.content CONTAINS "MATCH" OR e.content CONTAINS "WHERE" OR e.content CONTAINS "RETURN")
RETURN e.content, e.source_description, e.created_at,
       "GEMINI_CYPHER_SEARCH_3" as test_case;

-- OpenAI
MATCH (e:Episodic)
WHERE e.group_id = "test_openai_cypher_query"
  AND (e.content CONTAINS "MATCH" OR e.content CONTAINS "WHERE" OR e.content CONTAINS "RETURN")
RETURN e.content, e.source_description, e.created_at,
       "OPENAI_CYPHER_SEARCH_3" as test_case;

-- -----------------------------------------------------
-- 2.4 Búsquedas Caso Texto Regular - IA
-- -----------------------------------------------------

-- Búsqueda 1: "artificial intelligence machine learning"
-- Gemini
MATCH (e:Episodic)
WHERE e.group_id = "test_gemini_regular_text"
  AND (e.content CONTAINS "artificial" OR e.content CONTAINS "intelligence" OR e.content CONTAINS "machine")
RETURN e.content, e.source_description, e.created_at,
       "GEMINI_TEXT_SEARCH_1" as test_case;

-- OpenAI
MATCH (e:Episodic)
WHERE e.group_id = "test_openai_regular_text"
  AND (e.content CONTAINS "artificial" OR e.content CONTAINS "intelligence" OR e.content CONTAINS "machine")
RETURN e.content, e.source_description, e.created_at,
       "OPENAI_TEXT_SEARCH_1" as test_case;

-- Búsqueda 2: "cognitive processes algorithms"
-- Gemini
MATCH (e:Episodic)
WHERE e.group_id = "test_gemini_regular_text"
  AND (e.content CONTAINS "cognitive" OR e.content CONTAINS "processes" OR e.content CONTAINS "algorithms")
RETURN e.content, e.source_description, e.created_at,
       "GEMINI_TEXT_SEARCH_2" as test_case;

-- OpenAI
MATCH (e:Episodic)
WHERE e.group_id = "test_openai_regular_text"
  AND (e.content CONTAINS "cognitive" OR e.content CONTAINS "processes" OR e.content CONTAINS "algorithms")
RETURN e.content, e.source_description, e.created_at,
       "OPENAI_TEXT_SEARCH_2" as test_case;

-- Búsqueda 3: "pattern identification datasets"
-- Gemini
MATCH (e:Episodic)
WHERE e.group_id = "test_gemini_regular_text"
  AND (e.content CONTAINS "patterns" OR e.content CONTAINS "datasets" OR e.content CONTAINS "predictions")
RETURN e.content, e.source_description, e.created_at,
       "GEMINI_TEXT_SEARCH_3" as test_case;

-- OpenAI
MATCH (e:Episodic)
WHERE e.group_id = "test_openai_regular_text"
  AND (e.content CONTAINS "patterns" OR e.content CONTAINS "datasets" OR e.content CONTAINS "predictions")
RETURN e.content, e.source_description, e.created_at,
       "OPENAI_TEXT_SEARCH_3" as test_case;

-- =====================================================
-- 3. QUERIES DE ANÁLISIS Y LIMPIEZA
-- =====================================================

-- -----------------------------------------------------
-- 3.1 Conteo de Resultados por Instancia
-- -----------------------------------------------------

-- Conteo Gemini
MATCH (e:Episodic)
WHERE e.group_id STARTS WITH "test_gemini"
RETURN e.group_id, count(*) as total_records
ORDER BY e.group_id;

-- Conteo OpenAI
MATCH (e:Episodic)
WHERE e.group_id STARTS WITH "test_openai"
RETURN e.group_id, count(*) as total_records
ORDER BY e.group_id;

-- -----------------------------------------------------
-- 3.2 Análisis de Resultados de Búsqueda
-- -----------------------------------------------------

-- Query para evaluar relevancia de búsquedas
MATCH (e:Episodic)
WHERE e.source = "mcp_comparative_test"
RETURN 
    CASE 
        WHEN e.group_id CONTAINS "gemini" THEN "GEMINI"
        WHEN e.group_id CONTAINS "openai" THEN "OPENAI"
        ELSE "OTHER"
    END as embedding_type,
    CASE
        WHEN e.group_id CONTAINS "python" THEN "PYTHON_CODE"
        WHEN e.group_id CONTAINS "cypher" THEN "CYPHER_CODE"
        WHEN e.group_id CONTAINS "regular" THEN "REGULAR_TEXT"
        ELSE "OTHER"
    END as content_type,
    count(*) as records_count,
    e.created_at
ORDER BY embedding_type, content_type;

-- -----------------------------------------------------
-- 3.3 Limpieza de Datos de Prueba (cuando sea necesario)
-- -----------------------------------------------------

-- ADVERTENCIA: Solo ejecutar cuando se quiera limpiar todos los datos de prueba
-- MATCH (e:Episodic)
-- WHERE e.source = "mcp_comparative_test"
-- DELETE e;

-- Limpieza selectiva por instancia
-- MATCH (e:Episodic)
-- WHERE e.group_id STARTS WITH "test_gemini"
-- DELETE e;

-- MATCH (e:Episodic)
-- WHERE e.group_id STARTS WITH "test_openai"
-- DELETE e;

-- =====================================================
-- 4. QUERIES DE VALIDACIÓN
-- =====================================================

-- -----------------------------------------------------
-- 4.1 Verificar Integridad de Datos
-- -----------------------------------------------------

-- Verificar que todos los casos de prueba estén presentes
MATCH (e:Episodic)
WHERE e.source = "mcp_comparative_test"
RETURN 
    e.group_id,
    e.name,
    length(e.content) as content_length,
    e.created_at
ORDER BY e.group_id;

-- Verificar unicidad de UUIDs
MATCH (e:Episodic)
WHERE e.source = "mcp_comparative_test"
WITH e.uuid as uuid, count(*) as count_uuid
WHERE count_uuid > 1
RETURN uuid, count_uuid;

-- =====================================================
-- FIN DEL ARCHIVO
-- =====================================================
-- Próximo archivo: mcp_testing_workflow_20250723.md