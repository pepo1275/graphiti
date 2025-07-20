#!/usr/bin/env python3
"""
Test Graphiti with correct configuration (matching Claude Desktop MCP server)
"""
import asyncio
import os
from datetime import datetime
from graphiti_core import Graphiti
from graphiti_core.llm_client.config import LLMConfig
from graphiti_core.llm_client.openai_client import OpenAIClient

async def test_with_correct_config():
    """Test usando la configuración exacta del MCP server de Claude Desktop"""
    
    print("🔧 CONFIGURACIÓN CORRECTA:")
    print("="*50)
    
    # Aplicar las mismas variables de entorno que Claude Desktop
    os.environ["MODEL_NAME"] = "gpt-4o"
    os.environ["SMALL_MODEL_NAME"] = "gpt-4o-mini"
    os.environ["GROUP_ID"] = "pepo_phd_research"
    os.environ["USE_CUSTOM_ENTITIES"] = "true"
    
    print(f"✅ MODEL_NAME: {os.environ['MODEL_NAME']}")
    print(f"✅ SMALL_MODEL_NAME: {os.environ['SMALL_MODEL_NAME']}")
    print(f"✅ GROUP_ID: {os.environ['GROUP_ID']}")
    
    try:
        # Crear configuración LLM explícita (como hace el MCP server)
        llm_config = LLMConfig(
            api_key=os.environ.get("OPENAI_API_KEY"),
            model="gpt-4o",  # Modelo principal que soporta json_schema
            small_model="gpt-4o-mini"
        )
        
        # Crear cliente LLM explícito
        llm_client = OpenAIClient(llm_config)
        
        print(f"📊 LLM Client model: {llm_client.model}")
        print(f"📊 LLM Client small_model: {llm_client.small_model}")
        
        # Inicializar Graphiti con el cliente configurado
        graphiti = Graphiti(
            uri="bolt://localhost:7687",
            user="neo4j", 
            password="pepo_graphiti_2025",
            llm_client=llm_client
        )
        
        await graphiti.build_indices_and_constraints()
        
        test_content = """
        Test final con configuración correcta. Este episodio debería crearse 
        exitosamente usando gpt-4o como modelo principal, que sí soporta 
        json_schema structured outputs. La configuración replica exactamente 
        la que usa Claude Desktop con el MCP server.
        """
        
        print("\n📝 Creando episodio con configuración correcta...")
        
        result = await graphiti.add_episode(
            name="Test Configuración Correcta - Phase 2.1",
            episode_body=test_content,
            source_description="Python script con config correcta",
            reference_time=datetime.now(),
            group_id="pepo_phd_research"
        )
        
        print("✅ SUCCESS! Configuración correcta funciona")
        print(f"   Tipo resultado: {type(result)}")
        
        # Verificar que se creó
        query = """
        MATCH (n:Episodic)
        WHERE n.name CONTAINS "Test Configuración Correcta"
        RETURN n.name, n.created_at
        ORDER BY n.created_at DESC
        LIMIT 1
        """
        
        result_check = await graphiti.driver.execute_query(query)
        if result_check.records:
            record = result_check.records[0]
            print(f"   ✅ Verificado en Neo4j: {record['n.name']}")
            print(f"   📅 Creado: {record['n.created_at']}")
        
        await graphiti.close()
        return True
        
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        try:
            await graphiti.close()
        except:
            pass
        return False

async def main():
    print("🚀 TEST CONFIGURACIÓN CORRECTA - Phase 2.1")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    success = await test_with_correct_config()
    
    print("\n" + "="*60)
    print("📊 RESULTADO FINAL")
    print("="*60)
    
    if success:
        print("✅ ÉXITO: Configuración correcta identificada y funcionando")
        print("\n💡 SOLUCIÓN para Phase 2.1:")
        print("   1. Usar MODEL_NAME='gpt-4o' (no gpt-4o-mini)")
        print("   2. Configurar LLMConfig explícitamente")
        print("   3. Pasar llm_client a Graphiti")
        print("\n🎯 Listo para continuar con evaluaciones multi-engine")
    else:
        print("❌ Problema persiste - revisar configuración adicional")
    
    return success

if __name__ == "__main__":
    # Asegurar variables necesarias
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY requerida")
        exit(1)
    
    if os.getenv("GEMINI_API_KEY") and not os.getenv("GOOGLE_API_KEY"):
        os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")
    
    success = asyncio.run(main())
    exit(0 if success else 1)