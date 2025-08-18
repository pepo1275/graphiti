#!/usr/bin/env python3
"""
Test de Lectura de Embeddings Respaldados
==========================================
Verificar que los embeddings 1024 están correctamente guardados
"""

import json
import numpy as np
from pathlib import Path
from neo4j import GraphDatabase

# Configuración
BACKUP_FILE = "/Users/pepo/Documents/BACKUPS_GRAPHITI/backup_20250818_185213/entidades_afectadas/entities_1024_complete.json"
NEO4J_CONFIG = {
    "uri": "bolt://localhost:7687",
    "user": "neo4j", 
    "password": "pepo_graphiti_2025"
}

def test_backup_embeddings():
    """Test completo de embeddings respaldados"""
    print("=" * 60)
    print("TEST DE VERIFICACIÓN DE EMBEDDINGS RESPALDADOS")
    print("=" * 60)
    
    # 1. Leer archivo de backup
    print("\n📖 1. LEYENDO ARCHIVO DE BACKUP...")
    try:
        with open(BACKUP_FILE, 'r') as f:
            backup_data = json.load(f)
        
        metadata = backup_data["backup_metadata"]
        entities = backup_data["data"]
        
        print(f"✅ Archivo leído correctamente")
        print(f"   • Timestamp: {metadata['timestamp']}")
        print(f"   • Total records: {metadata['statistics']['total_records']}")
        print(f"   • Expected dimension: {metadata['statistics']['embedding_dimension']}")
        
    except Exception as e:
        print(f"❌ Error leyendo backup: {e}")
        return False
    
    # 2. Verificar estructura de cada entidad
    print("\n🧪 2. VERIFICANDO ESTRUCTURA DE ENTIDADES...")
    
    valid_embeddings = 0
    embedding_stats = []
    
    for i, entity in enumerate(entities, 1):
        try:
            # Extraer embedding
            embedding = entity["embeddings"]["name_embedding"]
            dimension = len(embedding)
            name = entity["core_data"]["name"]
            uuid = entity["core_data"]["uuid"]
            
            # Convertir a numpy para análisis
            embedding_array = np.array(embedding)
            
            # Estadísticas
            stats = {
                "name": name,
                "uuid": uuid,
                "dimension": dimension,
                "min_value": float(embedding_array.min()),
                "max_value": float(embedding_array.max()),
                "mean": float(embedding_array.mean()),
                "std": float(embedding_array.std()),
                "has_nans": bool(np.isnan(embedding_array).any()),
                "has_infs": bool(np.isinf(embedding_array).any())
            }
            
            embedding_stats.append(stats)
            
            # Verificar dimensión
            if dimension == 1024:
                valid_embeddings += 1
                print(f"   [{i:2d}] ✅ {name[:30]:30} | {dimension:4d} dims | μ={stats['mean']:7.4f}")
            else:
                print(f"   [{i:2d}] ❌ {name[:30]:30} | {dimension:4d} dims | WRONG DIMENSION!")
            
        except Exception as e:
            print(f"   [{i:2d}] ❌ Error procesando entidad: {e}")
    
    # 3. Resumen de validación
    print(f"\n📊 3. RESUMEN DE VALIDACIÓN:")
    print(f"   • Entidades procesadas: {len(entities)}")
    print(f"   • Embeddings válidos (1024d): {valid_embeddings}")
    print(f"   • Embeddings inválidos: {len(entities) - valid_embeddings}")
    
    # 4. Verificar contra Neo4j (opcional)
    print(f"\n🔍 4. VERIFICACIÓN CONTRA NEO4J...")
    try:
        driver = GraphDatabase.driver(
            NEO4J_CONFIG["uri"],
            auth=(NEO4J_CONFIG["user"], NEO4J_CONFIG["password"])
        )
        
        with driver.session() as session:
            result = session.run("""
                MATCH (n:Entity)
                WHERE size(n.name_embedding) = 1024
                RETURN n.uuid as uuid, n.name as name, size(n.name_embedding) as dim
                ORDER BY n.name
            """)
            
            neo4j_entities = [dict(record) for record in result]
        
        driver.close()
        
        print(f"   • Entidades en Neo4j: {len(neo4j_entities)}")
        print(f"   • Entidades en backup: {len(entities)}")
        
        # Comparar UUIDs
        backup_uuids = {e["core_data"]["uuid"] for e in entities}
        neo4j_uuids = {e["uuid"] for e in neo4j_entities}
        
        missing_in_backup = neo4j_uuids - backup_uuids
        extra_in_backup = backup_uuids - neo4j_uuids
        
        if not missing_in_backup and not extra_in_backup:
            print("   ✅ Todos los UUIDs coinciden perfectamente")
        else:
            if missing_in_backup:
                print(f"   ⚠️ Faltantes en backup: {len(missing_in_backup)}")
            if extra_in_backup:
                print(f"   ⚠️ Extras en backup: {len(extra_in_backup)}")
    
    except Exception as e:
        print(f"   ⚠️ No se pudo verificar contra Neo4j: {e}")
    
    # 5. Generar reporte detallado
    print(f"\n📋 5. REPORTE DETALLADO DE EMBEDDINGS:")
    print(f"{'#':>2} {'Name':25} {'Dims':>5} {'Min':>8} {'Max':>8} {'Mean':>8} {'Std':>8} {'Valid':>6}")
    print("-" * 70)
    
    for i, stats in enumerate(embedding_stats, 1):
        valid = "✅" if stats["dimension"] == 1024 and not stats["has_nans"] and not stats["has_infs"] else "❌"
        print(f"{i:2d} {stats['name'][:24]:25} {stats['dimension']:5d} "
              f"{stats['min_value']:8.3f} {stats['max_value']:8.3f} "
              f"{stats['mean']:8.3f} {stats['std']:8.3f} {valid:>6}")
    
    # 6. Conclusión
    print(f"\n🎯 CONCLUSIÓN:")
    if valid_embeddings == len(entities) == 10:
        print("   ✅ BACKUP COMPLETAMENTE VÁLIDO")
        print("   ✅ Todas las 10 entidades tienen embeddings 1024d correctos")
        print("   ✅ Los vectores están listos para restauración")
        return True
    else:
        print("   ❌ PROBLEMAS DETECTADOS EN EL BACKUP")
        return False

if __name__ == "__main__":
    success = test_backup_embeddings()
    exit(0 if success else 1)