#!/usr/bin/env python3
"""
Verificación rápida de configuración para comparación Graphiti
Verifica que todo esté listo antes de ejecutar run_simple_comparison.py

Proyecto: /Users/pepo/graphiti-pepo-local
"""

import os
import sys
import asyncio
import docker
from pathlib import Path

def check_environment_variables():
    """Verificar variables de entorno necesarias"""
    print("🔧 Verificando variables de entorno...")
    
    required_vars = ["OPENAI_API_KEY", "GOOGLE_API_KEY"]
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Faltan variables de entorno: {', '.join(missing_vars)}")
        return False
    else:
        print("✅ Variables de entorno configuradas")
        return True

def check_docker_instances():
    """Verificar que las instancias Neo4j Docker estén corriendo"""
    print("🐳 Verificando instancias Docker Neo4j...")
    
    try:
        client = docker.from_env()
        containers = client.containers.list()
        
        required_containers = [
            "graphiti-neo4j-openai",
            "graphiti-neo4j-gemini"
        ]
        
        running_containers = [c.name for c in containers if c.status == 'running']
        
        missing_containers = []
        for required in required_containers:
            if required not in running_containers:
                missing_containers.append(required)
        
        if missing_containers:
            print(f"❌ Contenedores no encontrados o no corriendo: {', '.join(missing_containers)}")
            print("📋 Contenedores corriendo actualmente:")
            for container in running_containers:
                print(f"   - {container}")
            return False
        else:
            print("✅ Instancias Docker Neo4j corriendo:")
            for required in required_containers:
                container = client.containers.get(required)
                ports = container.attrs['NetworkSettings']['Ports']
                neo4j_port = None
                if '7687/tcp' in ports and ports['7687/tcp']:
                    neo4j_port = ports['7687/tcp'][0]['HostPort']
                print(f"   - {required}: puerto {neo4j_port}")
            return True
            
    except Exception as e:
        print(f"❌ Error verificando Docker: {e}")
        return False

def check_python_dependencies():
    """Verificar dependencias de Python"""
    print("🐍 Verificando dependencias de Python...")
    
    required_packages = [
        "graphiti",
        "docker",
        "asyncio"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Paquetes Python faltantes: {', '.join(missing_packages)}")
        print("💡 Instalar con: uv add <package_name>")
        return False
    else:
        print("✅ Dependencias de Python disponibles")
        return True

def check_synthetic_data():
    """Verificar que los datos sintéticos estén disponibles"""
    print("📋 Verificando datos sintéticos de enfermería...")
    
    try:
        # Añadir path de datos sintéticos
        sys.path.append('/Users/pepo/graphiti-pepo-local/synthetic_data')
        
        # Importar y probar episodios
        from nursing_episodes import get_nursing_episodes, get_evaluation_metrics
        
        episodes = get_nursing_episodes()
        metrics = get_evaluation_metrics()
        
        print(f"✅ Datos sintéticos cargados:")
        print(f"   - {len(episodes)} episodios de enfermería")
        print(f"   - {len(metrics)} categorías de métricas")
        
        # Mostrar algunos episodios como ejemplo
        print(f"📝 Episodios de ejemplo:")
        for ep in episodes[:3]:
            print(f"   - {ep.id}: {ep.title} ({ep.complexity_level})")
        
        return True
        
    except Exception as e:
        print(f"❌ Error cargando datos sintéticos: {e}")
        return False

def check_file_structure():
    """Verificar estructura de archivos del proyecto"""
    print("📁 Verificando estructura de archivos...")
    
    base_path = Path("/Users/pepo/graphiti-pepo-local")
    
    required_files = [
        "run_simple_comparison.py",
        "test_openai_instance.py", 
        "test_gemini_instance.py",
        "synthetic_data/nursing_episodes.py"
    ]
    
    missing_files = []
    
    for file_path in required_files:
        full_path = base_path / file_path
        if not full_path.exists():
            missing_files.append(file_path)
        else:
            size_mb = full_path.stat().st_size / (1024 * 1024)
            print(f"   ✅ {file_path} ({size_mb:.2f} MB)")
    
    if missing_files:
        print(f"❌ Archivos faltantes: {', '.join(missing_files)}")
        return False
    else:
        print("✅ Estructura de archivos completa")
        return True

async def test_neo4j_connectivity():
    """Probar conectividad con instancias Neo4j"""
    print("🔌 Probando conectividad Neo4j...")
    
    try:
        import neo4j
        
        # Test OpenAI instance (puerto 8694)
        openai_driver = neo4j.GraphDatabase.driver(
            "bolt://localhost:8694",
            auth=("neo4j", "pepo_graphiti_2025")
        )
        
        with openai_driver.session() as session:
            result = session.run("RETURN 'OpenAI instance' as test")
            print("✅ Conexión OpenAI Neo4j (puerto 8694) exitosa")
        
        openai_driver.close()
        
        # Test Gemini instance (puerto 8693)
        gemini_driver = neo4j.GraphDatabase.driver(
            "bolt://localhost:8693", 
            auth=("neo4j", "pepo_graphiti_2025")
        )
        
        with gemini_driver.session() as session:
            result = session.run("RETURN 'Gemini instance' as test")
            print("✅ Conexión Gemini Neo4j (puerto 8693) exitosa")
        
        gemini_driver.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Error conectividad Neo4j: {e}")
        print("💡 Verificar que las instancias estén corriendo y los puertos sean correctos")
        return False

def print_next_steps():
    """Mostrar próximos pasos para ejecutar la comparación"""
    print("\n" + "=" * 60)
    print("🚀 PRÓXIMOS PASOS PARA EJECUTAR LA COMPARACIÓN")
    print("=" * 60)
    print("1. Ejecutar comparación completa:")
    print("   cd /Users/pepo/graphiti-pepo-local")
    print("   uv run python run_simple_comparison.py")
    print()
    print("2. Revisar reporte generado:")
    print("   evaluation_report.json")
    print()
    print("3. Verificar resultados en Neo4j:")
    print("   OpenAI: http://localhost:7474 (puerto 8694)")
    print("   Gemini: http://localhost:7474 (puerto 8693)")
    print("=" * 60)

async def main():
    """Ejecutar todas las verificaciones"""
    print("🔍 VERIFICACIÓN DE CONFIGURACIÓN GRAPHITI COMPARISON")
    print("=" * 60)
    
    checks = [
        ("Variables de entorno", check_environment_variables),
        ("Instancias Docker", check_docker_instances),
        ("Dependencias Python", check_python_dependencies),
        ("Datos sintéticos", check_synthetic_data),
        ("Estructura de archivos", check_file_structure),
        ("Conectividad Neo4j", test_neo4j_connectivity)
    ]
    
    all_passed = True
    
    for check_name, check_func in checks:
        print(f"\n🔍 {check_name}...")
        try:
            if asyncio.iscoroutinefunction(check_func):
                result = await check_func()
            else:
                result = check_func()
            
            if not result:
                all_passed = False
        except Exception as e:
            print(f"❌ Error en {check_name}: {e}")
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 TODAS LAS VERIFICACIONES EXITOSAS")
        print("✅ Sistema listo para ejecutar comparación")
        print_next_steps()
    else:
        print("❌ ALGUNAS VERIFICACIONES FALLARON")
        print("🔧 Revisar y corregir los errores antes de continuar")
    
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
