"""
Prueba rápida y enfocada: CODE_RETRIEVAL_QUERY vs Estándar
Con reporte documentado para terceros
"""

import asyncio
import os
import json
from datetime import datetime, timezone
from graphiti_core import Graphiti
from graphiti_core.nodes import EpisodeType
from graphiti_core.llm_client.gemini_client import GeminiClient
from graphiti_core.llm_client.config import LLMConfig
from graphiti_core.embedder.gemini import GeminiEmbedder, GeminiEmbedderConfig

async def run_fast_comparison():
    """Prueba rápida con 1 caso de cada tipo"""
    
    print("⚡ PRUEBA RÁPIDA: CODE_RETRIEVAL_QUERY vs Estándar")
    print("=" * 55)
    
    # Configurar API
    google_api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not google_api_key:
        print("❌ GOOGLE_API_KEY requerida")
        return None
    
    print(f"✅ API configurada: {google_api_key[:8]}...")
    
    # Preparar reporte
    report = {
        "test_info": {
            "timestamp": datetime.now().isoformat(),
            "test_type": "Fast CODE_RETRIEVAL_QUERY Comparison",
            "version": "1.0"
        },
        "configuration": {
            "llm": "gemini-2.5-pro",
            "embedding_model": "gemini-embedding-001",
            "dimensions": 3072,
            "instances": {
                "code_retrieval": "bolt://localhost:7693 (graphiti-neo4j-gemini)",
                "standard": "bolt://localhost:7687 (graphiti-neo4j)"
            }
        },
        "results": []
    }
    
    try:
        print("\n🔧 Configurando instancias...")
        
        # LLM común
        llm_config = LLMConfig(
            api_key=google_api_key,
            model="gemini-2.5-pro",
            small_model="gemini-2.5-flash",
            temperature=0.0
        )
        llm_client = GeminiClient(config=llm_config)
        
        # Instancia CON CODE_RETRIEVAL_QUERY
        embedder_with_code = GeminiEmbedder(config=GeminiEmbedderConfig(
            api_key=google_api_key,
            embedding_model="gemini-embedding-001",
            embedding_dim=3072,
            task_type="CODE_RETRIEVAL_QUERY"
        ))
        
        graphiti_code = Graphiti(
            uri="bolt://localhost:7693",
            user="neo4j",
            password="pepo_graphiti_2025",
            llm_client=llm_client,
            embedder=embedder_with_code
        )
        
        # Instancia SIN CODE_RETRIEVAL_QUERY
        embedder_standard = GeminiEmbedder(config=GeminiEmbedderConfig(
            api_key=google_api_key,
            embedding_model="gemini-embedding-001",
            embedding_dim=3072,
            task_type=None
        ))
        
        graphiti_standard = Graphiti(
            uri="bolt://localhost:7687",
            user="neo4j", 
            password="pepo_graphiti_2025",
            llm_client=llm_client,
            embedder=embedder_standard
        )
        
        print("   ✅ Instancias configuradas")
        
        # Casos de prueba simples
        test_cases = [
            {
                "id": "python_code",
                "name": "Código Python - Fibonacci",
                "content": "def fibonacci(n):\\n    if n <= 1:\\n        return n\\n    return fibonacci(n-1) + fibonacci(n-2)",
                "query": "fibonacci recursive function",
                "type": "code"
            },
            {
                "id": "regular_text", 
                "name": "Texto Regular - IA",
                "content": "Artificial intelligence is transforming how we process information and make decisions in the modern world.",
                "query": "artificial intelligence information processing",
                "type": "text"
            }
        ]
        
        print(f"\n📝 Casos de prueba: {len(test_cases)}")
        
        # Procesar cada caso
        for i, case in enumerate(test_cases, 1):
            print(f"\n[{i}/{len(test_cases)}] {case['name']}")
            
            case_result = {
                "case_id": case['id'],
                "case_name": case['name'],
                "case_type": case['type'],
                "query": case['query'],
                "results": {}
            }
            
            # Escribir en instancia CON CODE_RETRIEVAL_QUERY
            try:
                print("   📝 Escribiendo CON CODE_RETRIEVAL_QUERY...")
                await graphiti_code.add_episode(
                    name=f"code_{case['id']}",
                    episode_body=case['content'],
                    reference_time=datetime.now(timezone.utc),
                    source=EpisodeType.text,
                    source_description=f"Test with CODE_RETRIEVAL_QUERY",
                    group_id="test_code_retrieval"
                )
                print("     ✅ Escrito exitosamente")
                
                # Buscar
                print("   🔍 Buscando CON CODE_RETRIEVAL_QUERY...")
                results_code = await graphiti_code.search(case['query'], num_results=3)
                
                case_result["results"]["with_code_retrieval"] = {
                    "success": True,
                    "count": len(results_code),
                    "found_relevant": any(case['id'] in r.name for r in results_code),
                    "top_result": results_code[0].name if results_code else None
                }
                
                print(f"     ✅ {len(results_code)} resultados encontrados")
                
            except Exception as e:
                print(f"     ❌ Error: {str(e)[:50]}")
                case_result["results"]["with_code_retrieval"] = {
                    "success": False,
                    "error": str(e)
                }
            
            # Escribir en instancia SIN CODE_RETRIEVAL_QUERY
            try:
                print("   📝 Escribiendo SIN CODE_RETRIEVAL_QUERY...")
                await graphiti_standard.add_episode(
                    name=f"standard_{case['id']}",
                    episode_body=case['content'],
                    reference_time=datetime.now(timezone.utc),
                    source=EpisodeType.text,
                    source_description=f"Test without CODE_RETRIEVAL_QUERY",
                    group_id="test_standard"
                )
                print("     ✅ Escrito exitosamente")
                
                # Buscar
                print("   🔍 Buscando SIN CODE_RETRIEVAL_QUERY...")
                results_standard = await graphiti_standard.search(case['query'], num_results=3)
                
                case_result["results"]["standard"] = {
                    "success": True,
                    "count": len(results_standard),
                    "found_relevant": any(case['id'] in r.name for r in results_standard),
                    "top_result": results_standard[0].name if results_standard else None
                }
                
                print(f"     ✅ {len(results_standard)} resultados encontrados")
                
            except Exception as e:
                print(f"     ❌ Error: {str(e)[:50]}")
                case_result["results"]["standard"] = {
                    "success": False,
                    "error": str(e)
                }
            
            # Comparar resultados
            if (case_result["results"].get("with_code_retrieval", {}).get("success") and 
                case_result["results"].get("standard", {}).get("success")):
                
                code_count = case_result["results"]["with_code_retrieval"]["count"]
                standard_count = case_result["results"]["standard"]["count"]
                
                if code_count > standard_count:
                    winner = "CODE_RETRIEVAL_QUERY"
                elif standard_count > code_count:
                    winner = "STANDARD"
                else:
                    winner = "TIE"
                
                case_result["comparison"] = {
                    "winner": winner,
                    "code_count": code_count,
                    "standard_count": standard_count,
                    "difference": code_count - standard_count
                }
                
                print(f"   🏆 Ganador: {winner} ({code_count} vs {standard_count})")
            else:
                case_result["comparison"] = {"winner": "INCONCLUSIVE", "reason": "One or both tests failed"}
                print("   ⚠️ Comparación inconclusiva")
            
            report["results"].append(case_result)
        
        # Cleanup
        await graphiti_code.close()
        await graphiti_standard.close()
        
        # Generar resumen
        total_cases = len(test_cases)
        code_wins = sum(1 for r in report["results"] if r.get("comparison", {}).get("winner") == "CODE_RETRIEVAL_QUERY")
        standard_wins = sum(1 for r in report["results"] if r.get("comparison", {}).get("winner") == "STANDARD")
        ties = sum(1 for r in report["results"] if r.get("comparison", {}).get("winner") == "TIE")
        
        report["summary"] = {
            "total_cases": total_cases,
            "code_retrieval_wins": code_wins,
            "standard_wins": standard_wins,
            "ties": ties,
            "conclusion": generate_conclusion(code_wins, standard_wins, total_cases)
        }
        
        print(f"\n📊 RESUMEN FINAL:")
        print(f"   • Total casos: {total_cases}")
        print(f"   • CODE_RETRIEVAL_QUERY gana: {code_wins}")
        print(f"   • Estándar gana: {standard_wins}")
        print(f"   • Empates: {ties}")
        print(f"   • Conclusión: {report['summary']['conclusion']}")
        
        return report
        
    except Exception as e:
        print(f"\n❌ ERROR GENERAL: {e}")
        report["error"] = str(e)
        return report

def generate_conclusion(code_wins: int, standard_wins: int, total: int) -> str:
    """Generar conclusión basada en resultados"""
    if code_wins > standard_wins:
        percentage = (code_wins / total) * 100
        return f"CODE_RETRIEVAL_QUERY superior en {percentage:.0f}% de casos"
    elif standard_wins > code_wins:
        percentage = (standard_wins / total) * 100
        return f"Embeddings estándar superiores en {percentage:.0f}% de casos"
    else:
        return "Rendimiento equivalente entre ambos métodos"

def save_report(report: dict) -> tuple[str, str]:
    """Guardar reporte en JSON y Markdown"""
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Archivo JSON
    json_file = f"code_retrieval_test_{timestamp}.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    # Archivo Markdown
    md_file = f"code_retrieval_report_{timestamp}.md"
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(generate_markdown_report(report))
    
    return json_file, md_file

def generate_markdown_report(report: dict) -> str:
    """Generar reporte en Markdown para terceros"""
    
    summary = report.get("summary", {})
    config = report.get("configuration", {})
    
    md = f"""# Evaluación CODE_RETRIEVAL_QUERY vs Embeddings Estándar

## Información de la Prueba
- **Fecha**: {report['test_info']['timestamp']}
- **Tipo**: {report['test_info']['test_type']}
- **Versión**: {report['test_info']['version']}

## Configuración Técnica
- **LLM**: {config.get('llm', 'N/A')}
- **Modelo Embeddings**: {config.get('embedding_model', 'N/A')}
- **Dimensiones**: {config.get('dimensions', 'N/A')}

### Instancias Neo4j
- **CON CODE_RETRIEVAL_QUERY**: {config.get('instances', {}).get('code_retrieval', 'N/A')}
- **SIN CODE_RETRIEVAL_QUERY**: {config.get('instances', {}).get('standard', 'N/A')}

## Resultados

### Resumen Ejecutivo
- **Total casos evaluados**: {summary.get('total_cases', 0)}
- **CODE_RETRIEVAL_QUERY gana**: {summary.get('code_retrieval_wins', 0)} casos
- **Embeddings estándar gana**: {summary.get('standard_wins', 0)} casos
- **Empates**: {summary.get('ties', 0)} casos

**Conclusión**: {summary.get('conclusion', 'No disponible')}

## Casos de Prueba Detallados

"""
    
    for i, result in enumerate(report.get("results", []), 1):
        md += f"""### {i}. {result['case_name']}
- **Tipo**: {result['case_type']}
- **Consulta**: "{result['query']}"

**Resultados**:
"""
        
        if "with_code_retrieval" in result["results"]:
            code_res = result["results"]["with_code_retrieval"]
            if code_res.get("success"):
                md += f"- CON CODE_RETRIEVAL_QUERY: {code_res['count']} resultados\n"
            else:
                md += f"- CON CODE_RETRIEVAL_QUERY: Error - {code_res.get('error', 'N/A')}\n"
        
        if "standard" in result["results"]:
            std_res = result["results"]["standard"]
            if std_res.get("success"):
                md += f"- SIN CODE_RETRIEVAL_QUERY: {std_res['count']} resultados\n"
            else:
                md += f"- SIN CODE_RETRIEVAL_QUERY: Error - {std_res.get('error', 'N/A')}\n"
        
        if "comparison" in result:
            comp = result["comparison"]
            md += f"- **Ganador**: {comp.get('winner', 'N/A')}\n"
        
        md += "\n"
    
    md += f"""
---
**Nota**: Este reporte fue generado automáticamente y puede ser validado por terceros 
mediante el archivo JSON correspondiente que contiene todos los datos técnicos.

*Generado el {report['test_info']['timestamp']}*
"""
    
    return md

async def main():
    """Función principal"""
    print("🚀 Iniciando evaluación rápida CODE_RETRIEVAL_QUERY...")
    
    report = await run_fast_comparison()
    
    if report and not report.get("error"):
        print("\n💾 Guardando reportes...")
        json_file, md_file = save_report(report)
        
        print(f"\n📄 REPORTES GENERADOS:")
        print(f"   • Datos técnicos: {json_file}")
        print(f"   • Reporte legible: {md_file}")
        print(f"\n✅ EVALUACIÓN COMPLETADA EXITOSAMENTE")
        print(f"📋 Los reportes pueden ser validados por terceros")
        
        return True
    else:
        print(f"\n❌ EVALUACIÓN FALLÓ")
        if report and report.get("error"):
            print(f"Error: {report['error']}")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)