#!/usr/bin/env python3
"""
Script Todo-en-Uno para Reparación de Embeddings en Graphiti
=============================================================
Este script automatiza todo el proceso de reparación de embeddings:
1. Backup de configuraciones
2. Análisis del estado actual
3. Configuración de Gemini
4. Regeneración de embeddings
5. Validación de resultados

Autor: Sistema de Recuperación Graphiti
Fecha: 2025-08-17
"""

import os
import sys
import time
import json
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from neo4j import GraphDatabase

# Intentar importar google.generativeai
try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    print("⚠️ google-generativeai no instalado. Instalar con: pip install google-generativeai")

# ============================================
# CONFIGURACIÓN GLOBAL
# ============================================

CONFIG = {
    "paths": {
        "graphiti_base": "/Users/pepo/graphiti-pepo-local",
        "embedder_client": "/Users/pepo/graphiti-pepo-local/graphiti_core/embedder/client.py",
        "claude_config": "/Users/pepo/Library/Application Support/Claude/claude_desktop_config.json",
        "backup_dir": f"/Users/pepo/graphiti-pepo-local/scripts/embedding_repair/backups/backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    },
    "neo4j": {
        "uri": "bolt://localhost:7687",
        "user": "neo4j",
        "password": "pepo_graphiti_2025"
    },
    "gemini": {
        "api_key": os.environ.get("GEMINI_API_KEY", "AIzaSyAiFOP6yBk2qyDi6c0JsrL9GnngYqPvCFw"),
        "model": "models/embedding-001",
        "dimensions": 3072,
        "task_type": "RETRIEVAL_DOCUMENT"
    }
}

class GraphitiEmbeddingsFixer:
    """Clase principal para reparar embeddings en Graphiti"""
    
    def __init__(self):
        self.driver = None
        self.stats = {
            "start_time": datetime.now(),
            "backups_created": [],
            "config_changes": [],
            "embeddings_regenerated": 0,
            "errors": []
        }
    
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
    
    def analyze_current_state(self) -> Dict:
        """Analizar el estado actual de los embeddings"""
        print("\n📊 ANALIZANDO ESTADO ACTUAL...")
        
        if not self.driver:
            return {"error": "No hay conexión a Neo4j"}
        
        with self.driver.session() as session:
            # Estado general
            result = session.run("""
                MATCH (n:Entity)
                RETURN 
                    count(n) as total,
                    count(n.name_embedding) as with_embedding,
                    count(CASE WHEN n.name_embedding IS NULL THEN 1 END) as without_embedding
            """)
            stats = result.single()
            
            # Dimensiones actuales
            result = session.run("""
                MATCH (n:Entity)
                WHERE n.name_embedding IS NOT NULL
                RETURN DISTINCT size(n.name_embedding) as dimension, count(*) as count
            """)
            dimensions = [dict(record) for record in result]
            
            # Grupos afectados
            result = session.run("""
                MATCH (n:Entity)
                WHERE n.name_embedding IS NULL
                RETURN n.group_id as group_id, count(*) as count
                ORDER BY count DESC
            """)
            affected_groups = [dict(record) for record in result]
            
            state = {
                "total_entities": stats["total"],
                "with_embedding": stats["with_embedding"],
                "without_embedding": stats["without_embedding"],
                "dimensions": dimensions,
                "affected_groups": affected_groups
            }
            
            # Mostrar resumen
            print(f"  Total entidades: {state['total_entities']}")
            print(f"  Con embeddings: {state['with_embedding']}")
            print(f"  Sin embeddings: {state['without_embedding']}")
            
            if dimensions:
                print(f"\n  Dimensiones actuales:")
                for dim in dimensions:
                    print(f"    • {dim['dimension']} dims: {dim['count']} entidades")
            
            if affected_groups:
                print(f"\n  Grupos sin embeddings:")
                for group in affected_groups[:5]:
                    print(f"    • {group['group_id']}: {group['count']} entidades")
            
            return state
    
    def create_backups(self) -> bool:
        """Crear backups de archivos críticos"""
        print("\n💾 CREANDO BACKUPS...")
        
        try:
            # Crear directorio de backup
            backup_dir = Path(CONFIG["paths"]["backup_dir"])
            backup_dir.mkdir(parents=True, exist_ok=True)
            
            # Archivos a respaldar
            files_to_backup = [
                (CONFIG["paths"]["embedder_client"], "embedder_client.py"),
                (CONFIG["paths"]["claude_config"], "claude_desktop_config.json")
            ]
            
            for source_path, backup_name in files_to_backup:
                source = Path(source_path)
                if source.exists():
                    dest = backup_dir / backup_name
                    shutil.copy2(source, dest)
                    print(f"  ✅ Respaldado: {backup_name}")
                    self.stats["backups_created"].append(str(dest))
                else:
                    print(f"  ⚠️ No encontrado: {source_path}")
            
            # Backup de estado Neo4j
            if self.driver:
                state = self.analyze_current_state()
                state_file = backup_dir / "neo4j_state.json"
                with open(state_file, 'w') as f:
                    json.dump(state, f, indent=2)
                print(f"  ✅ Estado Neo4j guardado")
                self.stats["backups_created"].append(str(state_file))
            
            print(f"\n📁 Backups guardados en: {backup_dir}")
            return True
            
        except Exception as e:
            print(f"❌ Error creando backups: {e}")
            self.stats["errors"].append(f"Backup creation: {str(e)}")
            return False
    
    def update_configuration(self) -> bool:
        """Actualizar configuración de embeddings"""
        print("\n⚙️ ACTUALIZANDO CONFIGURACIÓN...")
        
        try:
            # 1. Actualizar EMBEDDING_DIM en client.py
            client_path = Path(CONFIG["paths"]["embedder_client"])
            if client_path.exists():
                content = client_path.read_text()
                if "EMBEDDING_DIM = 1024" in content:
                    new_content = content.replace("EMBEDDING_DIM = 1024", "EMBEDDING_DIM = 3072")
                    client_path.write_text(new_content)
                    print("  ✅ Actualizado EMBEDDING_DIM: 1024 → 3072")
                    self.stats["config_changes"].append("EMBEDDING_DIM updated to 3072")
                else:
                    print("  ℹ️ EMBEDDING_DIM ya configurado o no encontrado")
            
            # 2. Crear archivo de configuración Gemini
            gemini_config_path = Path(CONFIG["paths"]["graphiti_base"]) / "mcp_server" / "config_gemini_embedding.py"
            gemini_config_path.parent.mkdir(parents=True, exist_ok=True)
            
            gemini_config_content = '''"""
Configuración de Gemini Embeddings para Graphiti MCP Server
"""

import os
from typing import Optional
from pydantic import BaseModel, Field
import google.generativeai as genai

class GeminiEmbeddingConfig(BaseModel):
    model_name: str = "models/embedding-001"
    embedding_dim: int = 3072
    api_key: str = Field(default_factory=lambda: os.environ.get("GEMINI_API_KEY"))
    task_type_storage: str = "RETRIEVAL_DOCUMENT"
    task_type_search: str = "RETRIEVAL_QUERY"
    task_type_code: str = "CODE_RETRIEVAL_QUERY"
'''
            
            gemini_config_path.write_text(gemini_config_content)
            print("  ✅ Creado config_gemini_embedding.py")
            self.stats["config_changes"].append("Gemini config file created")
            
            return True
            
        except Exception as e:
            print(f"❌ Error actualizando configuración: {e}")
            self.stats["errors"].append(f"Config update: {str(e)}")
            return False
    
    def regenerate_embeddings(self, dry_run: bool = True) -> int:
        """Regenerar embeddings faltantes"""
        
        if not GENAI_AVAILABLE:
            print("\n❌ google-generativeai no está instalado")
            print("Instalar con: pip install google-generativeai")
            return 0
        
        if not self.driver:
            print("\n❌ No hay conexión a Neo4j")
            return 0
        
        print(f"\n{'🔍 MODO SIMULACIÓN' if dry_run else '🚀 REGENERANDO EMBEDDINGS'}...")
        
        # Configurar Gemini
        genai.configure(api_key=CONFIG["gemini"]["api_key"])
        
        regenerated = 0
        errors = 0
        
        with self.driver.session() as session:
            # Obtener entidades sin embeddings
            result = session.run("""
                MATCH (n:Entity)
                WHERE n.name_embedding IS NULL
                RETURN n.uuid as uuid, n.name as name, 
                       n.summary as summary, n.group_id as group_id
                ORDER BY n.group_id, n.name
                LIMIT 10
            """)  # Limitado a 10 para demo
            
            entities = list(result)
            total = len(entities)
            
            if total == 0:
                print("  ✅ No hay entidades sin embeddings")
                return 0
            
            print(f"  Procesando {total} entidades...\n")
            
            for i, entity in enumerate(entities, 1):
                try:
                    # Preparar texto
                    text = entity['name']
                    if entity['summary']:
                        text += f" - {entity['summary']}"
                    
                    print(f"  [{i}/{total}] {entity['name'][:40]}...")
                    
                    if not dry_run:
                        # Crear embedding
                        result = genai.embed_content(
                            model=CONFIG["gemini"]["model"],
                            content=text,
                            task_type=CONFIG["gemini"]["task_type"],
                            output_dimensionality=CONFIG["gemini"]["dimensions"]
                        )
                        
                        embedding = result['embedding']
                        
                        # Actualizar en Neo4j
                        session.run("""
                            MATCH (n:Entity {uuid: $uuid})
                            SET n.name_embedding = $embedding
                        """, uuid=entity['uuid'], embedding=embedding)
                        
                        print(f"    ✅ Regenerado ({len(embedding)} dims)")
                        regenerated += 1
                        
                        # Rate limiting
                        time.sleep(0.1)
                    else:
                        print(f"    🔍 [SIMULACIÓN] Se regeneraría")
                    
                except Exception as e:
                    print(f"    ❌ Error: {str(e)[:50]}")
                    errors += 1
        
        if not dry_run:
            self.stats["embeddings_regenerated"] = regenerated
        
        print(f"\n  Procesados: {total}")
        print(f"  Regenerados: {regenerated}")
        print(f"  Errores: {errors}")
        
        return regenerated
    
    def generate_report(self) -> str:
        """Generar reporte final"""
        duration = (datetime.now() - self.stats["start_time"]).total_seconds()
        
        report = f"""
{'=' * 60}
REPORTE DE REPARACIÓN DE EMBEDDINGS
{'=' * 60}

Fecha: {self.stats['start_time'].strftime('%Y-%m-%d %H:%M:%S')}
Duración: {duration:.1f} segundos

BACKUPS CREADOS:
{chr(10).join(f'  • {b}' for b in self.stats['backups_created']) if self.stats['backups_created'] else '  Ninguno'}

CAMBIOS DE CONFIGURACIÓN:
{chr(10).join(f'  • {c}' for c in self.stats['config_changes']) if self.stats['config_changes'] else '  Ninguno'}

EMBEDDINGS REGENERADOS: {self.stats['embeddings_regenerated']}

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
    """Función principal"""
    
    print("=" * 60)
    print("REPARACIÓN COMPLETA DE EMBEDDINGS GRAPHITI")
    print("=" * 60)
    
    fixer = GraphitiEmbeddingsFixer()
    
    try:
        # 1. Conectar a Neo4j
        if not fixer.connect_neo4j():
            print("\n❌ No se pudo conectar a Neo4j. Abortando.")
            return 1
        
        # 2. Analizar estado inicial
        initial_state = fixer.analyze_current_state()
        
        if initial_state.get("without_embedding", 0) == 0:
            print("\n✅ No hay embeddings que reparar. Sistema OK.")
            return 0
        
        # 3. Confirmar con usuario
        print("\n" + "=" * 60)
        print(f"⚠️  ACCIONES A REALIZAR:")
        print(f"  1. Crear backups de configuración")
        print(f"  2. Actualizar EMBEDDING_DIM a 3072")
        print(f"  3. Configurar Gemini embeddings")
        print(f"  4. Regenerar {initial_state['without_embedding']} embeddings")
        print("=" * 60)
        
        response = input("\n¿Continuar? (s=simular / e=ejecutar / n=cancelar): ").lower()
        
        if response == 'n':
            print("\n❌ Operación cancelada")
            return 0
        
        dry_run = (response == 's')
        
        # 4. Crear backups
        if not dry_run:
            if not fixer.create_backups():
                print("\n⚠️ Problemas creando backups, pero continuando...")
        
        # 5. Actualizar configuración
        if not dry_run:
            if not fixer.update_configuration():
                print("\n❌ Error actualizando configuración. Abortando.")
                return 1
        
        # 6. Regenerar embeddings
        regenerated = fixer.regenerate_embeddings(dry_run=dry_run)
        
        # 7. Analizar estado final
        if not dry_run and regenerated > 0:
            print("\n📊 ESTADO FINAL:")
            final_state = fixer.analyze_current_state()
        
        # 8. Generar reporte
        report = fixer.generate_report()
        print(report)
        
        # Guardar reporte
        if not dry_run and CONFIG["paths"]["backup_dir"]:
            report_path = Path(CONFIG["paths"]["backup_dir"]) / "repair_report.txt"
            report_path.write_text(report)
            print(f"📄 Reporte guardado en: {report_path}")
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Operación interrumpida por el usuario")
        return 1
    
    except Exception as e:
        print(f"\n❌ Error crítico: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    finally:
        fixer.cleanup()
    
    print("\n✅ Proceso completado")
    return 0

if __name__ == "__main__":
    sys.exit(main())