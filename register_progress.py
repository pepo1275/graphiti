"""
Register Phase 1 Progress in Main Graphiti Instance
Documents all learning and progress for future reference
"""

import asyncio
import os
from datetime import datetime, timezone
from graphiti_core import Graphiti
from graphiti_core.nodes import EpisodeType
from graphiti_core.llm_client.config import LLMConfig
from graphiti_core.llm_client.openai_client import OpenAIClient

async def register_phase1_progress():
    """Register all Phase 1 progress and learnings in main Graphiti instance."""
    
    print("📝 Registering Phase 1 progress in main Graphiti instance...")
    
    try:
        # Create LLM configuration (using proven working config)
        llm_config = LLMConfig(
            api_key=os.environ.get("OPENAI_API_KEY"),
            model="gpt-4o",
            small_model="gpt-4o-mini"
        )
        
        # Create LLM client
        llm_client = OpenAIClient(llm_config)
        
        # Connect to main Graphiti instance (original)
        graphiti_main = Graphiti(
            uri="bolt://localhost:7687",  # Original instance
            user="neo4j",
            password="pepo_graphiti_2025",
            llm_client=llm_client
        )
        
        print("✅ Connected to main Graphiti instance")
        
        # EPISODIO 1: Infrastructure Setup
        await graphiti_main.add_episode(
            name="Phase 1 Setup - Embeddings Evaluation Infrastructure",
            episode_body="""
            Completado setup de infraestructura para evaluación de embeddings OpenAI vs Gemini:
            
            INFRAESTRUCTURA CREADA:
            - Neo4j instance OpenAI: graphiti-neo4j-openai (bolt://localhost:7694)
            - Neo4j instance Gemini: graphiti-neo4j-gemini (bolt://localhost:7693)
            - Branch evaluation: evaluation/embeddings-comparison
            - Environment config: .env.evaluation con URIs correctas
            
            FRAMEWORK DESARROLLADO:
            - evaluation_framework_basic.py: Framework mínimo funcional
            - test_openai_instance.py: Test OpenAI completamente funcional
            - Configuración de mejores prácticas en CLAUDE_CODE_COMPLETE.md
            
            ESTADO: OpenAI instance 100% funcional, listo para Gemini setup
            """,
            source_description="Phase 1 Infrastructure Progress Documentation",
            reference_time=datetime.now(timezone.utc),
            source=EpisodeType.text,
            group_id="embeddings_evaluation_2025"
        )
        
        print("✅ Episode 1: Infrastructure setup registered")
        
        # EPISODIO 2: Technical Learnings
        await graphiti_main.add_episode(
            name="Technical Learnings - OpenAI Configuration Resolution",
            episode_body="""
            Lecciones críticas aprendidas durante setup OpenAI Graphiti:
            
            PROBLEMA RESUELTO - json_schema error:
            - Error: "response_format type json_schema not supported with this model"
            - Causa: Configuración incorrecta o falta de small_model
            - Solución: LLMConfig con model="gpt-4o" Y small_model="gpt-4o-mini"
            
            CONFIGURACIÓN WORKING:
            ```python
            llm_config = LLMConfig(
                api_key=os.environ.get("OPENAI_API_KEY"),
                model="gpt-4o",
                small_model="gpt-4o-mini"  # CRÍTICO: debe estar presente
            )
            
            embedder_config = OpenAIEmbedderConfig(
                api_key=os.environ.get("OPENAI_API_KEY"),
                embedding_model="text-embedding-3-large"  # Mejorado
            )
            ```
            
            IMPORTS CORRECTOS:
            - from graphiti_core.embedder.openai import OpenAIEmbedder, OpenAIEmbedderConfig
            - from graphiti_core.llm_client.config import LLMConfig
            - from graphiti_core.llm_client.openai_client import OpenAIClient
            
            MÉTODO EXITOSO: Usar ejemplos funcionantes como referencia (test_with_correct_config.py)
            """,
            source_description="Technical Knowledge Capture and Problem Resolution",
            reference_time=datetime.now(timezone.utc),
            source=EpisodeType.text,
            group_id="embeddings_evaluation_2025"
        )
        
        print("✅ Episode 2: Technical learnings registered")
        
        # EPISODIO 3: Development Best Practices Applied
        await graphiti_main.add_episode(
            name="Development Best Practices Successfully Applied",
            episode_body="""
            Mejores prácticas de desarrollo aplicadas exitosamente en Phase 1:
            
            BACKUP Y SEGURIDAD:
            - Safety commits antes de cambios críticos: ✅ Aplicado
            - Backup claude_desktop_config.json: ✅ Realizado pero excluido de git por seguridad
            - Push regular a remote: ✅ Branch respaldado
            - Rollback procedures: ✅ Documentados y probados
            
            DESARROLLO INCREMENTAL:
            - Framework básico primero, luego complejidad: ✅ Seguido
            - Test cada cambio individualmente: ✅ Aplicado
            - No inventar la rueda: ✅ Usamos ejemplos funcionantes
            - Progressive testing: ✅ unit → integration
            
            TODOWRITE TRACKING:
            - Planificación con TodoWrite: ✅ 9 tareas tracked
            - Marcar in_progress antes de trabajar: ✅ Seguido
            - Marcar completed inmediatamente: ✅ Cumplido
            - Solo una tarea in_progress: ✅ Respetado
            
            DOCUMENTACIÓN:
            - Documentation-first: ✅ CLAUDE_CODE_COMPLETE.md actualizado
            - Commits descriptivos: ✅ Mensajes detallados
            - Configuración por defecto: ✅ Mejores prácticas documentadas
            
            GESTIÓN DE SECRETOS:
            - .gitignore para archivos sensibles: ✅ Implementado
            - GitHub push protection respetado: ✅ Sin leaks
            - Backups locales seguros: ✅ Mantenidos
            """,
            source_description="Best Practices Documentation and Application Results",
            reference_time=datetime.now(timezone.utc),
            source=EpisodeType.text,
            group_id="embeddings_evaluation_2025"
        )
        
        print("✅ Episode 3: Best practices registered")
        
        # EPISODIO 4: Working Configurations and Scripts
        await graphiti_main.add_episode(
            name="Working Configurations and Scripts Repository",
            episode_body="""
            Configuraciones y scripts funcionantes para referencia futura:
            
            ARCHIVOS WORKING:
            - test_openai_instance.py: Test completo OpenAI Graphiti ✅ FUNCIONA
            - evaluation_framework_basic.py: Framework evaluación mínimo ✅ FUNCIONA
            - .env.evaluation: Variables entorno evaluación ✅ CONFIGURADO
            - backup_claude_desktop_config_20250720.json: Backup config (local only)
            
            INSTANCIAS NEO4J OPERATIVAS:
            - graphiti-neo4j-openai: bolt://localhost:7694 ✅ READY
            - graphiti-neo4j-gemini: bolt://localhost:7693 ✅ READY  
            - graphiti-neo4j: bolt://localhost:7687 ✅ ORIGINAL (intacta)
            
            CONFIGURACIÓN EMBEDDINGS:
            - OpenAI text-embedding-3-large: ✅ CONFIGURADO
            - Gemini embeddings: 🔄 PENDIENTE configurar
            
            COMMANDS PARA CONTINUAR:
            ```bash
            # Verificar estado
            git status && git log --oneline -3
            docker ps | grep neo4j
            
            # Continuar con Gemini
            uv run python setup_gemini_instance.py
            ```
            
            BRANCH ACTUAL: evaluation/embeddings-comparison
            PROGRESO: 6/9 tareas completadas según TodoWrite
            """,
            source_description="Working Configurations and Scripts Documentation",
            reference_time=datetime.now(timezone.utc),
            source=EpisodeType.text,
            group_id="embeddings_evaluation_2025"
        )
        
        print("✅ Episode 4: Working configurations registered")
        
        # EPISODIO 5: Next Steps and Roadmap
        await graphiti_main.add_episode(
            name="Phase 1 Status and Next Steps Roadmap",
            episode_body="""
            Estado actual Phase 1 y próximos pasos definidos:
            
            COMPLETADO (6/9 tareas):
            ✅ Pre-execution plan with best practices
            ✅ Evaluation branch and environment variables
            ✅ Neo4j evaluation databases
            ✅ Basic evaluation framework structure
            ✅ Test basic framework with metrics
            ✅ Setup and test OpenAI Graphiti instance
            
            EN PROGRESO (1/9 tareas):
            🔄 Setup and test Gemini Graphiti instance
            
            PENDIENTE (2/9 tareas):
            ⏳ Run simple comparison between instances
            ⏳ Analyze results and create recommendation report
            
            PRÓXIMOS PASOS INMEDIATOS:
            1. Implementar Gemini custom clients (LLM + Embedder)
            2. Test Gemini instance en bolt://localhost:7693
            3. Ejecutar comparación simple entre instancias
            4. Generar reporte con recomendaciones
            
            OBJETIVO FINAL:
            Determinar configuración óptima embeddings (OpenAI vs Gemini) para 
            Sistema de Conocimiento Vivo - MVP Administración Medicamentos
            
            TIMELINE: Phase 1 completada en ~4 horas siguiendo mejores prácticas
            """,
            source_description="Phase 1 Status Report and Roadmap Documentation",
            reference_time=datetime.now(timezone.utc),
            source=EpisodeType.text,
            group_id="embeddings_evaluation_2025"
        )
        
        print("✅ Episode 5: Status and roadmap registered")
        
        await graphiti_main.close()
        print("✅ All progress successfully registered in main Graphiti instance")
        return True
        
    except Exception as e:
        print(f"❌ Failed to register progress: {e}")
        try:
            await graphiti_main.close()
        except:
            pass
        return False

if __name__ == "__main__":
    success = asyncio.run(register_phase1_progress())
    if success:
        print("\n🎉 Phase 1 progress fully documented in main Graphiti instance")
        print("📍 Group ID: embeddings_evaluation_2025")
        print("🔍 Query to view: MATCH (n:Episodic {group_id: 'embeddings_evaluation_2025'}) RETURN n.name, n.created_at ORDER BY n.created_at")
    else:
        print("\n💥 Progress registration failed")