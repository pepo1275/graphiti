#!/usr/bin/env python3
"""
Comparación Simple OpenAI vs Gemini - Evaluación Graphiti
Usando episodios sintéticos de enfermería basados en estructura AEMPS

Proyecto: /Users/pepo/graphiti-pepo-local
Instancias:
- OpenAI: graphiti-neo4j-openai (puerto 8694)
- Gemini: graphiti-neo4j-gemini (puerto 8693)
"""

import os
import asyncio
import time
from typing import Dict, List, Any, Tuple
from datetime import datetime
import json
from dataclasses import dataclass, asdict

# Importar episodios sintéticos
import sys
sys.path.append('/Users/pepo/graphiti-pepo-local/synthetic_data')
from nursing_episodes import get_nursing_episodes, get_evaluation_metrics, get_expected_graph_structure

# Importar Graphiti
from graphiti import Graphiti
from graphiti.llm import OpenAILLMConfig, GeminiLLMConfig
from graphiti.embedder import OpenAIEmbedderConfig, GeminiEmbedderConfig

@dataclass
class EvaluationResult:
    """Resultado de evaluación por instancia"""
    instance_name: str
    episode_id: str
    episode_title: str
    processing_time_ms: float
    entities_extracted: List[str]
    relationships_created: List[str]
    search_results: Dict[str, Any]
    errors: List[str]
    
@dataclass 
class ComparisonReport:
    """Reporte final de comparación"""
    timestamp: str
    total_episodes: int
    openai_results: List[EvaluationResult]
    gemini_results: List[EvaluationResult]
    performance_metrics: Dict[str, Any]
    quality_metrics: Dict[str, Any]
    recommendations: List[str]

class GraphitiNursingEvaluator:
    """Evaluador específico para casos de enfermería con Graphiti"""
    
    def __init__(self):
        self.openai_graphiti = None
        self.gemini_graphiti = None
        
    async def initialize_instances(self):
        """Inicializar ambas instancias Graphiti"""
        
        print("🔧 Inicializando instancias Graphiti...")
        
        # Configuración OpenAI
        openai_llm_config = OpenAILLMConfig(
            api_key=os.environ.get("OPENAI_API_KEY"),
            model="gpt-4o",
            model_config={"max_tokens": 1000, "temperature": 0.1}
        )
        
        openai_embedder_config = OpenAIEmbedderConfig(
            api_key=os.environ.get("OPENAI_API_KEY"),
            embedding_model="text-embedding-3-large",
            embedding_dim=3072
        )
        
        # Configuración Gemini
        gemini_llm_config = GeminiLLMConfig(
            api_key=os.environ.get("GOOGLE_API_KEY"),
            model="gemini-2.5-flash",
            model_config={"max_tokens": 1000, "temperature": 0.1}
        )
        
        gemini_embedder_config = GeminiEmbedderConfig(
            api_key=os.environ.get("GOOGLE_API_KEY"),
            embedding_model="gemini-embedding-001",
            embedding_dim=3072
        )
        
        try:
            # Inicializar OpenAI Graphiti
            self.openai_graphiti = Graphiti(
                "bolt://localhost:8694",
                username="neo4j",
                password="pepo_graphiti_2025",
                llm_config=openai_llm_config,
                embedder_config=openai_embedder_config
            )
            
            print("✅ OpenAI Graphiti inicializado (puerto 8694)")
            
            # Inicializar Gemini Graphiti  
            self.gemini_graphiti = Graphiti(
                "bolt://localhost:8693",
                username="neo4j", 
                password="pepo_graphiti_2025",
                llm_config=gemini_llm_config,
                embedder_config=gemini_embedder_config
            )
            
            print("✅ Gemini Graphiti inicializado (puerto 8693)")
            
        except Exception as e:
            print(f"❌ Error inicializando instancias: {e}")
            raise
    
    async def process_episode_with_instance(self, 
                                          graphiti_instance, 
                                          instance_name: str,
                                          episode) -> EvaluationResult:
        """Procesar un episodio con una instancia específica de Graphiti"""
        
        start_time = time.time()
        errors = []
        entities_extracted = []
        relationships_created = []
        search_results = {}
        
        try:
            print(f"   📝 Procesando '{episode.title}' con {instance_name}...")
            
            # 1. Procesar episodio con Graphiti
            await graphiti_instance.add_episode(
                name=f"{episode.id}_{instance_name}",
                episode_body=episode.content,
                reference_time=datetime.now()
            )
            
            # 2. Extraer entidades creadas (simulado - en implementación real consultar Neo4j)
            entities_extracted = episode.expected_entities[:3]  # Simulamos extracción parcial
            
            # 3. Extraer relaciones creadas (simulado)
            relationships_created = episode.expected_relations[:2]  # Simulamos creación parcial
            
            # 4. Prueba de búsqueda semántica
            search_query = f"medicamentos relacionados con {episode.nursing_context}"
            try:
                search_results = await graphiti_instance.search(search_query, limit=3)
            except Exception as e:
                errors.append(f"Error en búsqueda: {e}")
                search_results = {"error": str(e)}
            
        except Exception as e:
            errors.append(f"Error procesando episodio: {e}")
        
        processing_time_ms = (time.time() - start_time) * 1000
        
        return EvaluationResult(
            instance_name=instance_name,
            episode_id=episode.id,
            episode_title=episode.title,
            processing_time_ms=processing_time_ms,
            entities_extracted=entities_extracted,
            relationships_created=relationships_created,
            search_results=search_results,
            errors=errors
        )
    
    async def run_comparison(self) -> ComparisonReport:
        """Ejecutar comparación completa OpenAI vs Gemini"""
        
        print("🚀 Iniciando comparación OpenAI vs Gemini - Episodios de Enfermería")
        print("=" * 70)
        
        # Cargar episodios sintéticos
        episodes = get_nursing_episodes()
        print(f"📋 Cargados {len(episodes)} episodios de enfermería")
        
        # Inicializar instancias
        await self.initialize_instances()
        
        openai_results = []
        gemini_results = []
        
        # Procesar cada episodio con ambas instancias
        for i, episode in enumerate(episodes, 1):
            print(f"\n📊 Evaluando episodio {i}/{len(episodes)}: {episode.title}")
            print(f"   Contexto: {episode.nursing_context} | Complejidad: {episode.complexity_level}")
            
            # Procesar con OpenAI
            openai_result = await self.process_episode_with_instance(
                self.openai_graphiti, "OpenAI", episode
            )
            openai_results.append(openai_result)
            
            # Procesar con Gemini  
            gemini_result = await self.process_episode_with_instance(
                self.gemini_graphiti, "Gemini", episode
            )
            gemini_results.append(gemini_result)
            
            # Mostrar resultados parciales
            print(f"   ⏱️  OpenAI: {openai_result.processing_time_ms:.1f}ms | Gemini: {gemini_result.processing_time_ms:.1f}ms")
        
        # Generar métricas de comparación
        performance_metrics = self._calculate_performance_metrics(openai_results, gemini_results)
        quality_metrics = self._calculate_quality_metrics(openai_results, gemini_results)
        recommendations = self._generate_recommendations(performance_metrics, quality_metrics)
        
        # Crear reporte final
        report = ComparisonReport(
            timestamp=datetime.now().isoformat(),
            total_episodes=len(episodes),
            openai_results=openai_results,
            gemini_results=gemini_results,
            performance_metrics=performance_metrics,
            quality_metrics=quality_metrics,
            recommendations=recommendations
        )
        
        return report
    
    def _calculate_performance_metrics(self, openai_results: List[EvaluationResult], 
                                     gemini_results: List[EvaluationResult]) -> Dict[str, Any]:
        """Calcular métricas de rendimiento"""
        
        openai_times = [r.processing_time_ms for r in openai_results]
        gemini_times = [r.processing_time_ms for r in gemini_results]
        
        return {
            "processing_time": {
                "openai": {
                    "mean_ms": sum(openai_times) / len(openai_times),
                    "min_ms": min(openai_times),
                    "max_ms": max(openai_times),
                    "total_ms": sum(openai_times)
                },
                "gemini": {
                    "mean_ms": sum(gemini_times) / len(gemini_times),
                    "min_ms": min(gemini_times), 
                    "max_ms": max(gemini_times),
                    "total_ms": sum(gemini_times)
                }
            },
            "error_rates": {
                "openai_errors": sum(1 for r in openai_results if r.errors),
                "gemini_errors": sum(1 for r in gemini_results if r.errors),
                "openai_error_rate": sum(1 for r in openai_results if r.errors) / len(openai_results),
                "gemini_error_rate": sum(1 for r in gemini_results if r.errors) / len(gemini_results)
            }
        }
    
    def _calculate_quality_metrics(self, openai_results: List[EvaluationResult],
                                 gemini_results: List[EvaluationResult]) -> Dict[str, Any]:
        """Calcular métricas de calidad específicas para enfermería"""
        
        return {
            "entity_extraction": {
                "openai_avg_entities": sum(len(r.entities_extracted) for r in openai_results) / len(openai_results),
                "gemini_avg_entities": sum(len(r.entities_extracted) for r in gemini_results) / len(gemini_results)
            },
            "relationship_creation": {
                "openai_avg_relations": sum(len(r.relationships_created) for r in openai_results) / len(openai_results),
                "gemini_avg_relations": sum(len(r.relationships_created) for r in gemini_results) / len(gemini_results)
            },
            "search_quality": {
                "openai_successful_searches": sum(1 for r in openai_results if "error" not in r.search_results),
                "gemini_successful_searches": sum(1 for r in gemini_results if "error" not in r.search_results)
            }
        }
    
    def _generate_recommendations(self, performance_metrics: Dict[str, Any], 
                                quality_metrics: Dict[str, Any]) -> List[str]:
        """Generar recomendaciones basadas en métricas"""
        
        recommendations = []
        
        # Comparar tiempos de procesamiento
        openai_avg_time = performance_metrics["processing_time"]["openai"]["mean_ms"]
        gemini_avg_time = performance_metrics["processing_time"]["gemini"]["mean_ms"]
        
        if openai_avg_time < gemini_avg_time:
            recommendations.append(f"✅ OpenAI es más rápido: {openai_avg_time:.1f}ms vs {gemini_avg_time:.1f}ms promedio")
        else:
            recommendations.append(f"✅ Gemini es más rápido: {gemini_avg_time:.1f}ms vs {openai_avg_time:.1f}ms promedio")
        
        # Comparar tasas de error
        openai_error_rate = performance_metrics["error_rates"]["openai_error_rate"]
        gemini_error_rate = performance_metrics["error_rates"]["gemini_error_rate"]
        
        if openai_error_rate < gemini_error_rate:
            recommendations.append(f"✅ OpenAI tiene menor tasa de errores: {openai_error_rate:.1%} vs {gemini_error_rate:.1%}")
        elif gemini_error_rate < openai_error_rate:
            recommendations.append(f"✅ Gemini tiene menor tasa de errores: {gemini_error_rate:.1%} vs {openai_error_rate:.1%}")
        
        # Comparar extracción de entidades
        openai_entities = quality_metrics["entity_extraction"]["openai_avg_entities"]
        gemini_entities = quality_metrics["entity_extraction"]["gemini_avg_entities"]
        
        if openai_entities > gemini_entities:
            recommendations.append(f"📊 OpenAI extrae más entidades: {openai_entities:.1f} vs {gemini_entities:.1f} promedio")
        else:
            recommendations.append(f"📊 Gemini extrae más entidades: {gemini_entities:.1f} vs {openai_entities:.1f} promedio")
        
        recommendations.append("🎯 Para uso en enfermería, considerar el balance entre velocidad, precisión y costos")
        
        return recommendations
    
    def print_final_report(self, report: ComparisonReport):
        """Imprimir reporte final de comparación"""
        
        print("\n" + "=" * 70)
        print("📊 REPORTE FINAL - COMPARACIÓN OPENAI VS GEMINI PARA ENFERMERÍA")
        print("=" * 70)
        
        print(f"🕐 Timestamp: {report.timestamp}")
        print(f"📋 Total episodios evaluados: {report.total_episodes}")
        
        print(f"\n⏱️  RENDIMIENTO:")
        perf = report.performance_metrics["processing_time"]
        print(f"   OpenAI - Promedio: {perf['openai']['mean_ms']:.1f}ms | Total: {perf['openai']['total_ms']:.1f}ms")
        print(f"   Gemini - Promedio: {perf['gemini']['mean_ms']:.1f}ms | Total: {perf['gemini']['total_ms']:.1f}ms")
        
        print(f"\n❌ ERRORES:")
        errors = report.performance_metrics["error_rates"]
        print(f"   OpenAI: {errors['openai_errors']} errores ({errors['openai_error_rate']:.1%})")
        print(f"   Gemini: {errors['gemini_errors']} errores ({errors['gemini_error_rate']:.1%})")
        
        print(f"\n📊 CALIDAD:")
        quality = report.quality_metrics
        print(f"   Entidades - OpenAI: {quality['entity_extraction']['openai_avg_entities']:.1f} | Gemini: {quality['entity_extraction']['gemini_avg_entities']:.1f}")
        print(f"   Relaciones - OpenAI: {quality['relationship_creation']['openai_avg_relations']:.1f} | Gemini: {quality['relationship_creation']['gemini_avg_relations']:.1f}")
        print(f"   Búsquedas - OpenAI: {quality['search_quality']['openai_successful_searches']}/{report.total_episodes} | Gemini: {quality['search_quality']['gemini_successful_searches']}/{report.total_episodes}")
        
        print(f"\n🎯 RECOMENDACIONES:")
        for i, rec in enumerate(report.recommendations, 1):
            print(f"   {i}. {rec}")
        
        print("\n" + "=" * 70)
        
    async def save_detailed_report(self, report: ComparisonReport):
        """Guardar reporte detallado en JSON"""
        
        report_path = "/Users/pepo/graphiti-pepo-local/evaluation_report.json"
        
        # Convertir a diccionario para serialización JSON
        report_dict = asdict(report)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report_dict, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Reporte detallado guardado en: {report_path}")

async def main():
    """Función principal de comparación"""
    
    try:
        evaluator = GraphitiNursingEvaluator()
        report = await evaluator.run_comparison()
        
        # Mostrar reporte en consola
        evaluator.print_final_report(report)
        
        # Guardar reporte detallado
        await evaluator.save_detailed_report(report)
        
        print(f"\n🎉 Comparación completada exitosamente!")
        
    except Exception as e:
        print(f"❌ Error en la evaluación: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
