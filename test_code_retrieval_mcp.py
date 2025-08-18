"""
Prueba CODE_RETRIEVAL_QUERY usando herramientas MCP
Utiliza las instancias graphiti-neo4j-openai y graphiti-neo4j-gemini vía MCP
"""

import json
from datetime import datetime

def test_code_retrieval_with_mcp():
    """
    Prueba comparativa usando herramientas MCP disponibles
    """
    
    print("🚀 PRUEBA CODE_RETRIEVAL_QUERY VIA MCP")
    print("=" * 50)
    
    # Preparar reporte
    report = {
        "test_info": {
            "timestamp": datetime.now().isoformat(),
            "method": "MCP Tools",
            "description": "CODE_RETRIEVAL_QUERY comparison using MCP services"
        },
        "test_cases": [],
        "results": {"mcp_tests": [], "summary": {}}
    }
    
    # Casos de prueba
    test_cases = [
        {
            "id": "python_fibonacci",
            "name": "Código Python - Fibonacci",
            "type": "code",
            "content": """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# Función recursiva para calcular secuencia de Fibonacci
# Ejemplo: fibonacci(10) = 55
""",
            "search_queries": [
                "fibonacci recursive function python",
                "calculate fibonacci sequence",
                "recursive algorithm fibonacci"
            ]
        },
        {
            "id": "cypher_query",
            "name": "Query Cypher - Personas y Empresas", 
            "type": "code",
            "content": """
MATCH (p:Person)-[:WORKS_AT]->(c:Company)
WHERE p.age > 30 AND c.industry = 'Technology'
RETURN p.name, c.name, p.salary
ORDER BY p.salary DESC
LIMIT 10
""",
            "search_queries": [
                "cypher query person company relationship",
                "find employees in technology companies",
                "graph database query workers"
            ]
        },
        {
            "id": "regular_text",
            "name": "Texto Regular - Descripción IA",
            "type": "text", 
            "content": """
Artificial intelligence represents a transformative technology that enables machines to 
simulate human cognitive processes. Machine learning algorithms can identify patterns 
in large datasets and make predictions or decisions without explicit programming.
""",
            "search_queries": [
                "artificial intelligence machine learning",
                "cognitive processes algorithms",
                "pattern identification datasets"
            ]
        }
    ]
    
    report["test_cases"] = test_cases
    
    print(f"📝 Casos de prueba preparados: {len(test_cases)}")
    print("\n🔧 USANDO HERRAMIENTAS MCP DISPONIBLES:")
    print("   • add_memory - Para agregar episodios")
    print("   • search_memory_nodes - Para búsqueda de entidades")
    print("   • search_memory_facts - Para búsqueda de relaciones")
    print("   • get_status - Para verificar conectividad")
    
    # Simular uso de MCP (ya que necesito que Claude Code ejecute las herramientas)
    print(f"\n📋 PLAN DE EJECUCIÓN MCP:")
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n[{i}/{len(test_cases)}] {case['name']}")
        
        # Plan para instancia Gemini (CON CODE_RETRIEVAL_QUERY)
        print(f"   🟢 GEMINI INSTANCE (CODE_RETRIEVAL_QUERY):")
        print(f"      1. add_memory(group_id='test_gemini_code', content='{case['name']}', description='Code with CODE_RETRIEVAL_QUERY')")
        
        for query in case['search_queries']:
            print(f"      2. search_memory_nodes(query='{query}', group_ids=['test_gemini_code'], max_results=3)")
        
        # Plan para instancia OpenAI (SIN CODE_RETRIEVAL_QUERY específico)
        print(f"   🔵 OPENAI INSTANCE (STANDARD):")
        print(f"      1. add_memory(group_id='test_openai_standard', content='{case['name']}', description='Standard embeddings')")
        
        for query in case['search_queries']:
            print(f"      2. search_memory_nodes(query='{query}', group_ids=['test_openai_standard'], max_results=3)")
        
        # Preparar estructura de resultados
        case_result = {
            "case_id": case['id'],
            "case_name": case['name'],
            "case_type": case['type'],
            "queries": case['search_queries'],
            "mcp_operations": {
                "gemini_add": f"add_memory(group_id='test_gemini_code', content='{case['name']}', ...)",
                "openai_add": f"add_memory(group_id='test_openai_standard', content='{case['name']}', ...)",
                "search_operations": len(case['search_queries']) * 2  # Para ambas instancias
            },
            "expected_benefit": "HIGH" if case['type'] == "code" else "LOW"
        }
        
        report["results"]["mcp_tests"].append(case_result)
    
    # Generar resumen
    total_cases = len(test_cases)
    code_cases = sum(1 for case in test_cases if case['type'] == 'code')
    text_cases = total_cases - code_cases
    total_operations = sum(len(case['search_queries']) for case in test_cases) * 2 + total_cases * 2
    
    report["results"]["summary"] = {
        "total_test_cases": total_cases,
        "code_cases": code_cases,
        "text_cases": text_cases,
        "total_mcp_operations": total_operations,
        "instances_to_compare": ["graphiti-neo4j-gemini", "graphiti-neo4j-openai"],
        "status": "READY_FOR_EXECUTION"
    }
    
    print(f"\n📊 RESUMEN DEL PLAN:")
    print(f"   • Total casos de prueba: {total_cases}")
    print(f"   • Casos de código (beneficio esperado): {code_cases}")
    print(f"   • Casos de texto regular: {text_cases}")
    print(f"   • Total operaciones MCP: {total_operations}")
    print(f"   • Instancias a comparar: graphiti-neo4j-gemini vs graphiti-neo4j-openai")
    
    # Guardar plan de ejecución
    plan_file = f"mcp_test_plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(plan_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Plan guardado en: {plan_file}")
    print(f"\n🎯 LISTO PARA EJECUTAR CON MCP TOOLS")
    print(f"📋 Claude Code puede ahora usar las herramientas MCP para ejecutar esta comparación")
    
    return report, plan_file

def generate_mcp_execution_guide(report):
    """Generar guía para ejecutar con herramientas MCP"""
    
    guide = f"""# Guía de Ejecución MCP - CODE_RETRIEVAL_QUERY Test

## 1. Verificar Estado de Instancias

**Herramienta:** `get_status`
- Verificar conectividad con graphiti-neo4j-gemini 
- Verificar conectividad con graphiti-neo4j-openai

## 2. Limpiar Datos Previos (Opcional)

**Herramienta:** `clear_graph` 
- Limpiar instancia Gemini si necesario
- Limpiar instancia OpenAI si necesario

## 3. Ejecutar Casos de Prueba

"""
    
    for i, case in enumerate(report["test_cases"], 1):
        guide += f"""### Caso {i}: {case['name']}

**Paso 1 - Agregar a Gemini (CODE_RETRIEVAL_QUERY):**
```
add_memory(
    content="{case['content'][:100]}...",
    group_id="test_gemini_{case['id']}",
    source_description="Test CODE_RETRIEVAL_QUERY - {case['name']}"
)
```

**Paso 2 - Agregar a OpenAI (Standard):**  
```
add_memory(
    content="{case['content'][:100]}...",
    group_id="test_openai_{case['id']}",
    source_description="Test Standard Embeddings - {case['name']}"
)
```

**Paso 3 - Búsquedas Comparativas:**
"""
        
        for query in case['search_queries']:
            guide += f"""
- Gemini: `search_memory_nodes(query="{query}", group_ids=["test_gemini_{case['id']}"], max_results=3)`
- OpenAI: `search_memory_nodes(query="{query}", group_ids=["test_openai_{case['id']}"], max_results=3)`
"""
    
    guide += f"""
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
*Generado el {report['test_info']['timestamp']}*
"""
    
    guide_file = f"mcp_execution_guide_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(guide_file, 'w', encoding='utf-8') as f:
        f.write(guide) 
    
    return guide_file

if __name__ == "__main__":
    print("🚀 Preparando prueba CODE_RETRIEVAL_QUERY con MCP...")
    
    report, plan_file = test_code_retrieval_with_mcp()
    guide_file = generate_mcp_execution_guide(report)
    
    print(f"\n📄 ARCHIVOS GENERADOS:")
    print(f"   • Plan de ejecución: {plan_file}")
    print(f"   • Guía de ejecución: {guide_file}")
    
    print(f"\n✅ PREPARACIÓN COMPLETADA")
    print(f"🎯 Claude Code puede ejecutar la comparación usando herramientas MCP")