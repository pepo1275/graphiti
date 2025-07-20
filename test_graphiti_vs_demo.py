#!/usr/bin/env python3
"""
Prueba comparativa: Graphiti normal vs Demo
Para identificar dónde está el problema de json_schema
"""

import asyncio
import os
from datetime import datetime
from graphiti_core import Graphiti

async def test_graphiti_normal():
    """Prueba 1: Usar Graphiti de manera normal (como siempre has usado)"""
    print("🔍 PRUEBA 1: Graphiti Normal")
    print("="*50)
    
    try:
        # Inicializar Graphiti de la manera normal
        uri = "bolt://localhost:7687"
        username = "neo4j"
        password = "pepo_graphiti_2025"
        
        graphiti = Graphiti(uri, username, password)
        await graphiti.build_indices_and_constraints()
        
        # Crear un episodio simple
        test_content = """
        This is a test episode to verify that normal Graphiti usage works correctly 
        with json_schema structured outputs. We are testing the standard add_episode 
        functionality that has been working previously.
        """
        
        print(f"📝 Adding episode with normal Graphiti...")
        
        result = await graphiti.add_episode(
            name="Normal Graphiti Test",
            episode_body=test_content,
            source_description="Test for json_schema compatibility",
            reference_time=datetime.now(),
            group_id="test_normal_graphiti"
        )
        
        print("✅ Graphiti Normal: SUCCESS!")
        print(f"   Episode created successfully")
        print(f"   Result type: {type(result)}")
        
        # Verificar que se creó
        nodes = await graphiti.get_episodic_nodes()
        test_nodes = [n for n in nodes if "Normal Graphiti Test" in str(n.name)]
        print(f"   Found {len(test_nodes)} matching nodes")
        
        await graphiti.close()
        return True
        
    except Exception as e:
        print(f"❌ Graphiti Normal: FAILED!")
        print(f"   Error: {str(e)}")
        print(f"   Error type: {type(e)}")
        
        # Si hay un cliente, cerrarlo
        try:
            await graphiti.close()
        except:
            pass
        
        return False

async def test_demo_approach():
    """Prueba 2: Usar el enfoque del demo con patching"""
    print("\n🔍 PRUEBA 2: Demo Approach (con patching)")
    print("="*50)
    
    try:
        # Importar las funciones del demo
        from examples.token_monitoring_real_demo import patch_graphiti_for_monitoring
        
        # Aplicar patches del demo
        print("🔧 Aplicando patches del demo...")
        patch_success = patch_graphiti_for_monitoring()
        
        if not patch_success:
            print("❌ Demo Approach: Patch failed!")
            return False
            
        print("✅ Patches aplicados")
        
        # Inicializar Graphiti igual que el demo
        uri = "bolt://localhost:7687"
        username = "neo4j"
        password = "pepo_graphiti_2025"
        
        graphiti = Graphiti(uri, username, password)
        await graphiti.build_indices_and_constraints()
        
        # Crear el mismo tipo de episodio que el demo
        test_content = """
        This is a test episode using the demo approach with token monitoring patches.
        We want to see if the patching process introduces the json_schema error.
        Testing whether the monitoring wrapper affects the response_format configuration.
        """
        
        print(f"📝 Adding episode with demo approach...")
        
        result = await graphiti.add_episode(
            name="Demo Approach Test",
            episode_body=test_content,
            source_description="Test with demo patches",
            reference_time=datetime.now(),
            group_id="test_demo_approach"
        )
        
        print("✅ Demo Approach: SUCCESS!")
        print(f"   Episode created successfully")
        print(f"   Result type: {type(result)}")
        
        await graphiti.close()
        return True
        
    except Exception as e:
        print(f"❌ Demo Approach: FAILED!")
        print(f"   Error: {str(e)}")
        print(f"   Error type: {type(e)}")
        
        # Buscar el error específico de json_schema
        if "json_schema" in str(e):
            print("   🎯 ENCONTRADO: Error de json_schema en demo approach!")
            print("   📊 Esto confirma que el problema está en el patching")
        
        try:
            await graphiti.close()
        except:
            pass
            
        return False

async def analyze_client_configuration():
    """Prueba 3: Analizar configuración del cliente"""
    print("\n🔍 PRUEBA 3: Análisis de Configuración")
    print("="*50)
    
    try:
        # Verificar configuración sin patches
        graphiti_normal = Graphiti("bolt://localhost:7687", "neo4j", "pepo_graphiti_2025")
        
        print("Cliente normal:")
        print(f"   LLM Client type: {type(graphiti_normal.llm_client)}")
        print(f"   Model: {getattr(graphiti_normal.llm_client, 'model', 'No model attr')}")
        print(f"   Client: {type(getattr(graphiti_normal.llm_client, 'client', None))}")
        
        await graphiti_normal.close()
        
        # Verificar configuración con patches
        from examples.token_monitoring_real_demo import patch_graphiti_for_monitoring
        patch_graphiti_for_monitoring()
        
        graphiti_patched = Graphiti("bolt://localhost:7687", "neo4j", "pepo_graphiti_2025")
        
        print("\nCliente con patches:")
        print(f"   LLM Client type: {type(graphiti_patched.llm_client)}")
        print(f"   Model: {getattr(graphiti_patched.llm_client, 'model', 'No model attr')}")
        print(f"   Client: {type(getattr(graphiti_patched.llm_client, 'client', None))}")
        
        await graphiti_patched.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Análisis: Error - {str(e)}")
        return False

async def main():
    """Ejecutar todas las pruebas comparativas"""
    print("🚀 PRUEBA COMPARATIVA: Graphiti Normal vs Demo")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    # Variables de entorno
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY no configurada")
        return
    
    print(f"✅ OPENAI_API_KEY: Configurada")
    
    # Ejecutar pruebas
    results = {
        "normal": await test_graphiti_normal(),
        "demo": await test_demo_approach(),
        "analysis": await analyze_client_configuration()
    }
    
    # Resumen
    print("\n" + "="*60)
    print("📊 RESUMEN DE RESULTADOS")
    print("="*60)
    
    for test, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"   {test.capitalize()}: {status}")
    
    # Conclusiones
    print("\n💡 CONCLUSIONES:")
    
    if results["normal"] and not results["demo"]:
        print("   🎯 El problema está en el DEMO/PATCHING")
        print("   📋 Graphiti normal funciona, el demo introduce el error")
        print("   🔧 Revisar: examples/token_monitoring_real_demo.py")
        
    elif not results["normal"] and not results["demo"]:
        print("   🚨 Problema en AMBOS - posible problema de configuración")
        print("   📋 Revisar: modelos OpenAI y configuración base")
        
    elif results["normal"] and results["demo"]:
        print("   ✅ Ambos funcionan - problema resuelto o intermitente")
        
    else:
        print("   🤔 Resultado inesperado - revisar logs")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    # Asegurar que GOOGLE_API_KEY esté configurada
    if os.getenv("GEMINI_API_KEY") and not os.getenv("GOOGLE_API_KEY"):
        os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")
    
    asyncio.run(main())