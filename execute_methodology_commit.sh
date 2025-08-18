#!/bin/bash
# Script para ejecutar commit selectivo de metodología
# Fecha: 2025-01-23
# REQUIERE APROBACIÓN ANTES DE EJECUTAR

set -e  # Salir si hay algún error

echo "================================================"
echo "📋 COMMIT SELECTIVO DE METODOLOGÍA"
echo "================================================"
echo ""

# Colores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Paso 1: Mostrar estado actual
echo "📊 Estado actual del repositorio:"
echo "--------------------------------"
git status --short
echo ""

# Confirmación de seguridad
echo -e "${YELLOW}⚠️  ADVERTENCIA: Este script ejecutará un commit selectivo${NC}"
echo "Solo se commitearán archivos de metodología."
echo ""
read -p "¿Confirmas que has leído TECHNICAL_DECISION_20250123.md? (s/n): " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Ss]$ ]]; then
    echo -e "${RED}❌ Operación cancelada${NC}"
    exit 1
fi

# Paso 2: Añadir archivos selectivamente
echo ""
echo "📁 Añadiendo archivos de metodología..."
echo "---------------------------------------"

git add CLAUDE.md
echo "✅ Added: CLAUDE.md"

git add docs/DEVELOPMENT_METHODOLOGY.md
echo "✅ Added: docs/DEVELOPMENT_METHODOLOGY.md"

git add docs/CHECKPOINTS.md
echo "✅ Added: docs/CHECKPOINTS.md"

git add docs/INDEX.md
echo "✅ Added: docs/INDEX.md"

git add docs/BACKUP_MODULE_INVESTIGATION.md
echo "✅ Added: docs/BACKUP_MODULE_INVESTIGATION.md"

git add docs/BACKUP_OPTIONS_ANALYSIS.md
echo "✅ Added: docs/BACKUP_OPTIONS_ANALYSIS.md"

git add docs/TECHNICAL_DECISION_20250123.md
echo "✅ Added: docs/TECHNICAL_DECISION_20250123.md"

git add .claude/check_methodology.py
echo "✅ Added: .claude/check_methodology.py"

git add .claude/pre-commit-validator.sh
echo "✅ Added: .claude/pre-commit-validator.sh"

git add .gitignore
echo "✅ Added: .gitignore (modified)"

echo ""
echo "📋 Archivos staged para commit:"
echo "-------------------------------"
git status --short | grep "^[AM]"

# Paso 3: Confirmación final
echo ""
echo -e "${YELLOW}🔄 A punto de crear commit con mensaje predefinido${NC}"
read -p "¿Proceder con el commit? (s/n): " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Ss]$ ]]; then
    echo -e "${RED}❌ Commit cancelado${NC}"
    git reset HEAD  # Unstage todo
    exit 1
fi

# Paso 4: Crear commit
echo ""
echo "💾 Creando commit..."
git commit -m "feat: implement development methodology and Claude Code automation

- Add CLAUDE.md for automatic instruction loading by Claude Code
- Create comprehensive development methodology (7 phases)
- Add validation scripts and checkpoint system
- Setup .claude/ directory with methodology validators
- Document backup module investigation and options
- Update .gitignore for .claude/ temporary files

This commit establishes a professional development workflow that will be
automatically applied by Claude Code in future sessions. The methodology
includes mandatory checkpoints, validation scripts, and clear documentation
structure.

No functional changes to the codebase are included in this commit."

echo -e "${GREEN}✅ Commit creado exitosamente${NC}"

# Paso 5: Mostrar información del commit
echo ""
echo "📝 Información del commit:"
echo "-------------------------"
git log --oneline -1

# Paso 6: Preguntar si hacer push
echo ""
echo -e "${YELLOW}📤 ¿Deseas hacer push a origin/evaluation/embeddings-comparison?${NC}"
read -p "(s/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Ss]$ ]]; then
    echo "Ejecutando push..."
    git push origin evaluation/embeddings-comparison
    echo -e "${GREEN}✅ Push completado${NC}"
else
    echo "⏸️  Push pospuesto. Puedes hacerlo luego con:"
    echo "   git push origin evaluation/embeddings-comparison"
fi

# Paso 7: Ofrecer hacer stash del resto
echo ""
echo "📦 ¿Deseas hacer stash de los archivos restantes?"
echo "   Esto guardará:"
git status --short | grep "^??"
read -p "(s/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Ss]$ ]]; then
    git stash push -m "WIP: retrieval tests + gemini changes + reports - needs review"
    echo -e "${GREEN}✅ Stash creado${NC}"
    echo "Para recuperarlo luego: git stash pop"
else
    echo "⏸️  Archivos sin stash. Permanecen en el working directory."
fi

echo ""
echo "================================================"
echo -e "${GREEN}✅ PROCESO COMPLETADO${NC}"
echo "================================================"
echo ""
echo "Próximos pasos recomendados:"
echo "1. Reiniciar Claude Code para probar CLAUDE.md"
echo "2. Revisar trabajo en stash con metodología activa"
echo "3. Crear branches específicas para cada objetivo"
echo ""