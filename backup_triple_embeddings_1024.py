#!/usr/bin/env python3
"""
Script Triple Backup para Embeddings 1024 - Graphiti
=====================================================
OBJETIVO: Backup crítico de 10 entidades con embeddings 1024 antes de pérdida
BASADO EN: /Users/pepo/Downloads/graphiti_backup_plan_2025.md

Autor: Graphiti Recovery System
Fecha: 2025-08-18
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List
from neo4j import GraphDatabase

# ============================================
# CONFIGURACIÓN - COPIADO DEL SCRIPT ORIGINAL QUE FUNCIONA
# ============================================

CONFIG = {
    "paths": {
        "backup_dir": f"/Users/pepo/Documents/BACKUPS_GRAPHITI/backup_20250818_185213"
    },
    "neo4j": {
        "uri": "bolt://localhost:7687",
        "user": "neo4j", 
        "password": "pepo_graphiti_2025"
    }
}

class TripleBackupEmbeddings1024:
    """Triple backup específico para embeddings 1024 que se van a perder"""
    
    def __init__(self):
        self.driver = None
        self.stats = {
            "start_time": datetime.now(),
            "backups_created": [],
            "entities_backed_up": 0,
            "errors": []
        }
    
    # COPIADO DEL SCRIPT ORIGINAL - FUNCIONA
    def connect_neo4j(self) -> bool:
        """Conectar a Neo4j"""
        try:
            self.driver = GraphDatabase.driver(
                CONFIG["neo4j"]["uri"],
                auth=(CONFIG["neo4j"]["user"], CONFIG["neo4j"]["password"])
            )
            # Test connection
            with self.driver.session() as session:
                result = session.run("RETURN 1 as test")
                result.single()
            print("✅ Conexión a Neo4j establecida")
            return True
        except Exception as e:
            print(f"❌ Error conectando a Neo4j: {e}")
            self.stats["errors"].append(f"Neo4j connection: {str(e)}")
            return False
    
    def test_pre_backup(self) -> bool:
        """TEST PRE: Verificar que existen las 10 entidades con embeddings 1024"""
        print("\n🧪 TEST PRE-BACKUP...")
        
        if not self.driver:
            return False
            
        with self.driver.session() as session:
            result = session.run("""
                MATCH (n:Entity)
                WHERE size(n.name_embedding) = 1024
                RETURN count(n) as entities_1024
            """)
            count = result.single()["entities_1024"]
            
            if count == 10:
                print(f"✅ TEST PRE: {count} entidades con embeddings 1024 detectadas")
                return True
            else:
                print(f"❌ TEST PRE: Se esperaban 10 entidades, encontradas {count}")
                self.stats["errors"].append(f"Pre-test failed: {count} entities found")
                return False
    
    def backup_schema(self) -> bool:
        """BACKUP 1/3: Esquema ontológico"""
        print("\n💾 BACKUP 1/3: Esquema ontológico...")
        
        try:
            with self.driver.session() as session:
                # Query del plan original
                result = session.run("""
                    CALL db.labels() YIELD label
                    WITH collect(label) as all_labels
                    CALL db.relationshipTypes() YIELD relationshipType  
                    WITH all_labels, collect(relationshipType) as all_rels
                    RETURN {
                        timestamp: datetime(),
                        total_node_types: size(all_labels),
                        total_relationship_types: size(all_rels),
                        node_types: all_labels,
                        relationship_types: all_rels,
                        schema_version: "enriched_2025_08_18"
                    } as schema_backup
                """)
                
                schema_data = result.single()["schema_backup"]
                
                # Formatear para guardar
                backup_data = {
                    "backup_metadata": {
                        "timestamp": datetime.now().isoformat(),
                        "device_id": "macbook-air-de-pepo_macos_pepo_001", 
                        "backup_version": "enriched_v2.0",
                        "backup_type": "schema"
                    },
                    "data": [schema_data],
                    "verification": {"record_count": 1}
                }
                
                # Guardar archivo
                schema_file = Path(CONFIG["paths"]["backup_dir"]) / "estructura_enriquecida" / "schema_backup.json"
                schema_file.parent.mkdir(parents=True, exist_ok=True)
                
                with open(schema_file, 'w') as f:
                    json.dump(backup_data, f, indent=2, default=str)
                
                print(f"✅ Schema guardado: {schema_file}")
                self.stats["backups_created"].append(str(schema_file))
                return True
                
        except Exception as e:
            print(f"❌ Error en backup schema: {e}")
            self.stats["errors"].append(f"Schema backup: {str(e)}")
            return False
    
    def backup_entities_1024(self) -> bool:
        """BACKUP 2/3: Entidades 1024 CRÍTICAS"""
        print("\n💾 BACKUP 2/3: Entidades críticas 1024...")
        
        try:
            entities_data = []
            
            # Primero obtener lista de UUIDs
            with self.driver.session() as session:
                result = session.run("""
                    MATCH (n:Entity)
                    WHERE size(n.name_embedding) = 1024
                    RETURN n.uuid as uuid, n.name as name
                    ORDER BY n.created_at DESC
                """)
                
                entity_list = [{"uuid": record["uuid"], "name": record["name"]} 
                             for record in result]
            
            print(f"  Procesando {len(entity_list)} entidades...")
            
            # Procesar cada entidad individualmente (evitar límite tokens)
            for entity in entity_list:
                with self.driver.session() as session:
                    result = session.run("""
                        MATCH (n:Entity {uuid: $uuid})
                        WHERE size(n.name_embedding) = 1024
                        RETURN {
                            core_data: {
                                uuid: n.uuid,
                                name: n.name,
                                group_id: n.group_id,
                                entity_type: n.entity_type,
                                created_at: n.created_at,
                                updated_at: n.updated_at
                            },
                            embeddings: {
                                name_embedding: n.name_embedding,
                                embedding_dimension: size(n.name_embedding)
                            },
                            metadata: {
                                summary: n.summary,
                                all_properties: keys(n)
                            },
                            backup_info: {
                                backup_timestamp: datetime(),
                                backup_reason: "Pre-cleanup safety backup - critical embeddings 1024"
                            }
                        } as entity_backup
                    """, uuid=entity["uuid"])
                    
                    entity_data = result.single()
                    if entity_data:
                        entities_data.append(entity_data["entity_backup"])
                        print(f"  ✅ {entity['name']}")
            
            # Guardar archivo de entidades completas
            backup_data = {
                "backup_metadata": {
                    "timestamp": datetime.now().isoformat(),
                    "device_id": "macbook-air-de-pepo_macos_pepo_001",
                    "backup_version": "enriched_v2.0", 
                    "backup_type": "entities",
                    "statistics": {
                        "total_records": len(entities_data),
                        "embedding_dimension": 1024,
                        "affected_groups": ["problem_solving"]
                    }
                },
                "data": entities_data,
                "verification": {"record_count": len(entities_data)}
            }
            
            entities_file = Path(CONFIG["paths"]["backup_dir"]) / "entidades_afectadas" / "entities_1024_complete.json"
            entities_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(entities_file, 'w') as f:
                json.dump(backup_data, f, indent=2, default=str)
            
            print(f"✅ Entidades guardadas: {entities_file}")
            self.stats["backups_created"].append(str(entities_file))
            self.stats["entities_backed_up"] = len(entities_data)
            
            return True
            
        except Exception as e:
            print(f"❌ Error en backup entidades: {e}")
            self.stats["errors"].append(f"Entities backup: {str(e)}")
            return False
    
    def backup_relationships(self) -> bool:
        """BACKUP 3/3: Relaciones de entidades 1024"""
        print("\n💾 BACKUP 3/3: Relaciones...")
        
        try:
            with self.driver.session() as session:
                result = session.run("""
                    MATCH (n:Entity)-[r]-(m)
                    WHERE size(n.name_embedding) = 1024
                    WITH n, r, m, 
                         CASE WHEN startNode(r) = n THEN "OUTBOUND" ELSE "INBOUND" END as direction
                    RETURN {
                        relationship_data: {
                            source_entity: {
                                uuid: n.uuid,
                                name: n.name
                            },
                            relationship: {
                                type: type(r),
                                properties: properties(r),
                                direction: direction
                            },
                            target_node: {
                                uuid: CASE WHEN m.uuid IS NOT NULL THEN m.uuid ELSE "no_uuid_" + toString(id(m)) END,
                                name: CASE WHEN m.name IS NOT NULL THEN m.name ELSE "unnamed_" + toString(id(m)) END,
                                labels: labels(m)
                            }
                        },
                        backup_info: {
                            backup_timestamp: datetime()
                        }
                    } as relationship_backup
                """)
                
                relationships_data = [record["relationship_backup"] for record in result]
                
                backup_data = {
                    "backup_metadata": {
                        "timestamp": datetime.now().isoformat(),
                        "device_id": "macbook-air-de-pepo_macos_pepo_001",
                        "backup_version": "enriched_v2.0",
                        "backup_type": "relationships"
                    },
                    "data": relationships_data,
                    "verification": {"record_count": len(relationships_data)}
                }
                
                relationships_file = Path(CONFIG["paths"]["backup_dir"]) / "relaciones_especializadas" / "relationships_1024.json"
                relationships_file.parent.mkdir(parents=True, exist_ok=True)
                
                with open(relationships_file, 'w') as f:
                    json.dump(backup_data, f, indent=2, default=str)
                
                print(f"✅ Relaciones guardadas: {relationships_file}")
                self.stats["backups_created"].append(str(relationships_file))
                return True
                
        except Exception as e:
            print(f"❌ Error en backup relaciones: {e}")
            self.stats["errors"].append(f"Relationships backup: {str(e)}")
            return False
    
    def create_restore_scripts(self) -> bool:
        """Crear scripts de restauración .cypher"""
        print("\n📝 Creando scripts de restauración...")
        
        try:
            restore_dir = Path(CONFIG["paths"]["backup_dir"]) / "restauracion_adaptada"
            restore_dir.mkdir(parents=True, exist_ok=True)
            
            # Script para restaurar entidades
            restore_entities_script = '''-- restore_entities_1024.cypher
-- Script para restaurar entidades con embeddings 1024

:param backup_data => [/* JSON array from entities_1024_complete.json */];

UNWIND $backup_data as entity
MERGE (n:Entity {uuid: entity.core_data.uuid})
ON CREATE SET 
  n.name = entity.core_data.name,
  n.group_id = entity.core_data.group_id,
  n.entity_type = entity.core_data.entity_type,
  n.created_at = entity.core_data.created_at,
  n.updated_at = entity.core_data.updated_at,
  n.summary = entity.metadata.summary,
  n.name_embedding = entity.embeddings.name_embedding,
  n.restored_at = datetime(),
  n.restore_type = "created_from_backup"
ON MATCH SET
  n.backup_exists = true,
  n.last_backup_check = datetime(),
  n.restore_note = "Entity already existed - embeddings preserved"
RETURN 
  count(DISTINCT n) as total_processed,
  sum(CASE WHEN n.restore_type = "created_from_backup" THEN 1 ELSE 0 END) as newly_created,
  sum(CASE WHEN n.backup_exists = true THEN 1 ELSE 0 END) as already_existed;
'''
            
            restore_entities_file = restore_dir / "restore_entities_1024.cypher"
            with open(restore_entities_file, 'w') as f:
                f.write(restore_entities_script)
            
            print(f"✅ Script restauración creado: {restore_entities_file}")
            self.stats["backups_created"].append(str(restore_entities_file))
            
            return True
            
        except Exception as e:
            print(f"❌ Error creando scripts: {e}")
            self.stats["errors"].append(f"Restore scripts: {str(e)}")
            return False
    
    def test_post_backup(self) -> bool:
        """TEST POST: Verificar que el backup se creó correctamente"""
        print("\n🧪 TEST POST-BACKUP...")
        
        try:
            backup_dir = Path(CONFIG["paths"]["backup_dir"])
            
            # Verificar archivos críticos
            required_files = [
                "estructura_enriquecida/schema_backup.json",
                "entidades_afectadas/entities_1024_complete.json", 
                "relaciones_especializadas/relationships_1024.json",
                "restauracion_adaptada/restore_entities_1024.cypher"
            ]
            
            missing_files = []
            for file_path in required_files:
                full_path = backup_dir / file_path
                if not full_path.exists():
                    missing_files.append(file_path)
                else:
                    print(f"✅ TEST POST: {file_path} existe")
            
            if missing_files:
                print(f"❌ TEST POST: Archivos faltantes: {missing_files}")
                return False
            
            # Verificar contenido del archivo crítico
            entities_file = backup_dir / "entidades_afectadas" / "entities_1024_complete.json"
            with open(entities_file, 'r') as f:
                entities_data = json.load(f)
            
            entities_count = entities_data["verification"]["record_count"]
            if entities_count == 10:
                print(f"✅ TEST POST: {entities_count} entidades respaldadas correctamente")
                return True
            else:
                print(f"❌ TEST POST: Se esperaban 10 entidades, respaldadas {entities_count}")
                return False
                
        except Exception as e:
            print(f"❌ Error en test post: {e}")
            self.stats["errors"].append(f"Post-test: {str(e)}")
            return False
    
    def generate_report(self) -> str:
        """Generar reporte final"""
        duration = (datetime.now() - self.stats["start_time"]).total_seconds()
        
        report = f"""
{'=' * 60}
REPORTE TRIPLE BACKUP EMBEDDINGS 1024
{'=' * 60}

Fecha: {self.stats['start_time'].strftime('%Y-%m-%d %H:%M:%S')}
Duración: {duration:.1f} segundos

ARCHIVOS CREADOS:
{chr(10).join(f'  • {b}' for b in self.stats['backups_created']) if self.stats['backups_created'] else '  Ninguno'}

ENTIDADES RESPALDADAS: {self.stats['entities_backed_up']}

ERRORES:
{chr(10).join(f'  • {e}' for e in self.stats['errors']) if self.stats['errors'] else '  Ninguno'}

{'=' * 60}
"""
        return report
    
    def cleanup(self):
        """Limpiar recursos"""
        if self.driver:
            self.driver.close()

def main():
    """Función principal - Triple backup siguiendo CLAUDE.md"""
    
    print("=" * 60)
    print("TRIPLE BACKUP CRÍTICO - EMBEDDINGS 1024")
    print("=" * 60)
    
    backup = TripleBackupEmbeddings1024()
    
    try:
        # PASO 1: Conectar a Neo4j
        if not backup.connect_neo4j():
            print("\n❌ No se pudo conectar a Neo4j. Abortando.")
            return 1
        
        # PASO 2: TEST PRE (criterios de aceptación)
        if not backup.test_pre_backup():
            print("\n❌ Test pre-backup falló. Abortando.")
            return 1
        
        # PASO 3: Ejecutar triple backup
        print("\n🚀 EJECUTANDO TRIPLE BACKUP...")
        
        success = True
        success &= backup.backup_schema()
        success &= backup.backup_entities_1024()
        success &= backup.backup_relationships() 
        success &= backup.create_restore_scripts()
        
        if not success:
            print("\n⚠️ Algunos backups fallaron, revisando errores...")
        
        # PASO 4: TEST POST (criterios de aceptación)
        if not backup.test_post_backup():
            print("\n❌ Test post-backup falló.")
            return 1
        
        # PASO 5: Reporte final
        report = backup.generate_report()
        print(report)
        
        # Guardar reporte
        report_file = Path(CONFIG["paths"]["backup_dir"]) / "BACKUP_REPORT.txt"
        with open(report_file, 'w') as f:
            f.write(report)
        print(f"📄 Reporte guardado: {report_file}")
        
        print("\n✅ TRIPLE BACKUP COMPLETADO EXITOSAMENTE")
        return 0
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Operación interrumpida por el usuario")
        return 1
    
    except Exception as e:
        print(f"\n❌ Error crítico: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    finally:
        backup.cleanup()

if __name__ == "__main__":
    sys.exit(main())