#!/bin/bash
# Script de ejecución para reparación de embeddings
# Uso: ./run_repair.sh [simulate|execute]

set -e  # Salir en caso de error

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/../.." &> /dev/null && pwd )"

echo "🔧 GRAPHITI EMBEDDING REPAIR"
echo "================================"
echo "Script dir: $SCRIPT_DIR"
echo "Project root: $PROJECT_ROOT"
echo ""

# Verificar que estamos en el directorio correcto
if [[ ! -f "$PROJECT_ROOT/graphiti_core/graphiti.py" ]]; then
    echo "❌ Error: No se encontró graphiti_core/graphiti.py"
    echo "   Ejecutar desde el directorio raíz del proyecto Graphiti"
    exit 1
fi

# Cambiar al directorio del script
cd "$SCRIPT_DIR"

# Verificar dependencias
echo "📦 Verificando dependencias..."
if ! python3 -c "import google.generativeai" 2>/dev/null; then
    echo "⚠️  google-generativeai no instalado"
    echo "   Instalando con uv..."
    cd "$PROJECT_ROOT"
    uv add google-generativeai
    cd "$SCRIPT_DIR"
    echo "✅ Dependencia instalada"
fi

# Verificar conexión Neo4j
echo "🔍 Verificando conexión Neo4j..."
if ! python3 -c "
from neo4j import GraphDatabase
try:
    driver = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', 'pepo_graphiti_2025'))
    with driver.session() as session:
        session.run('RETURN 1')
    print('✅ Neo4j conectado')
except Exception as e:
    print(f'❌ Error Neo4j: {e}')
    exit(1)
"; then
    echo "❌ No se pudo conectar a Neo4j"
    exit 1
fi

# Crear directorio de logs si no existe
mkdir -p logs

# Ejecutar el script
MODE="${1:-simulate}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="logs/repair_${MODE}_${TIMESTAMP}.log"

echo "🚀 Ejecutando reparación en modo: $MODE"
echo "📝 Log: $LOG_FILE"
echo ""

if [[ "$MODE" == "execute" ]]; then
    echo "⚠️  MODO EJECUCIÓN REAL - Los cambios serán permanentes"
    echo "   Presiona Enter para continuar o Ctrl+C para cancelar"
    read -r
fi

# Ejecutar script principal con logging
python3 embedding_repair_main.py 2>&1 | tee "$LOG_FILE"

echo ""
echo "✅ Proceso completado"
echo "📄 Log guardado en: $LOG_FILE"

# Mostrar resumen de archivos generados
echo ""
echo "📁 Archivos generados:"
find backups logs -type f -newer /tmp/repair_start_marker 2>/dev/null || echo "   (ejecutar 'touch /tmp/repair_start_marker' antes del script para ver archivos nuevos)"

echo ""
echo "🔍 Para revisar resultados:"
echo "   tail -f $LOG_FILE"
echo "   ls -la backups/"