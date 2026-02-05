#!/usr/bin/env bash
# =============================================================================
# check-upstream-impact.sh
# [FORK] Script de deteccion automatica de cambios upstream que impactan al fork
#
# Ejecutar desde la raiz del repo:
#   ./scripts/check-upstream-impact.sh
#
# Que hace:
#   1. Fetch upstream silencioso
#   2. Verifica si ramas "watch" fueron mergeadas a upstream/main
#   3. Detecta nuevos commits en upstream/main desde nuestro ultimo sync
#   4. Reporta impactos en archivos criticos para el fork
#
# Autor: Pepo + Claude
# Fecha: 2026-02-05
# =============================================================================

set -euo pipefail

# --- Colores ---
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# --- Config ---
# Ramas upstream a vigilar (FLAG: nombre_rama|descripcion|archivos_criticos)
WATCH_BRANCHES=(
  "chore/gemini-improvements|Refactor mayor: MCP rewrite + embedder simplificado + eliminacion Neptune/Kuzu/OTEL|mcp_server/src,graphiti_core/embedder/gemini.py,graphiti_core/driver/graph_operations"
)

# Archivos criticos para nuestro fork
CRITICAL_FILES=(
  "graphiti_core/embedder/gemini.py"
  "graphiti_core/embedder/client.py"
  "graphiti_core/nodes.py"
  "graphiti_core/edges.py"
  "graphiti_core/helpers.py"
  "graphiti_core/search/search_utils.py"
  "mcp_server/src/graphiti_mcp_server.py"
  "mcp_server/src/config/schema.py"
  "mcp_server/src/services/factories.py"
)

# Ultimo commit upstream que sincronizamos
LAST_SYNC_COMMIT="affca93"

# --- Funciones ---

header() {
  echo ""
  echo -e "${BOLD}=============================================${NC}"
  echo -e "${BOLD}  UPSTREAM IMPACT CHECK - graphiti fork${NC}"
  echo -e "${BOLD}=============================================${NC}"
  echo -e "  Fecha: $(date '+%Y-%m-%d %H:%M')"
  echo -e "  Ultimo sync: ${LAST_SYNC_COMMIT}"
  echo ""
}

check_upstream_remote() {
  if ! git remote | grep -q "^upstream$"; then
    echo -e "${RED}ERROR: Remote 'upstream' no configurado${NC}"
    echo "  Ejecutar: git remote add upstream https://github.com/getzep/graphiti.git"
    exit 1
  fi
}

fetch_upstream() {
  echo -e "${BLUE}>>> Fetching upstream...${NC}"
  git fetch upstream --quiet 2>/dev/null || {
    echo -e "${YELLOW}WARNING: No se pudo hacer fetch de upstream (sin conexion?)${NC}"
    echo "  Usando datos locales..."
  }
}

check_watch_branches() {
  echo -e "${BOLD}--- WATCH BRANCHES ---${NC}"
  echo ""

  local any_merged=false

  for entry in "${WATCH_BRANCHES[@]}"; do
    IFS='|' read -r branch description critical_paths <<< "$entry"

    # Verificar si la rama existe en upstream
    if ! git rev-parse --verify "upstream/${branch}" &>/dev/null; then
      echo -e "  ${GREEN}[OK]${NC} upstream/${branch}"
      echo -e "       Rama ya no existe (posiblemente mergeada o eliminada)"
      echo -e "       ${YELLOW}>>> VERIFICAR MANUALMENTE si fue mergeada a main${NC}"
      any_merged=true
      continue
    fi

    # Verificar si fue mergeada a upstream/main
    if git merge-base --is-ancestor "upstream/${branch}" upstream/main 2>/dev/null; then
      echo -e "  ${RED}[MERGEADA]${NC} upstream/${branch}"
      echo -e "       ${RED}>>> ${description}${NC}"
      echo -e "       ${RED}>>> ACCION REQUERIDA: Ver CHANGELOG-FORK.md seccion 'Upstream Watch Flags'${NC}"
      any_merged=true
    else
      # Ver actividad reciente
      last_commit_date=$(git log -1 --format="%cr" "upstream/${branch}" 2>/dev/null || echo "desconocido")
      commits_ahead=$(git rev-list --count "upstream/main..upstream/${branch}" 2>/dev/null || echo "?")

      echo -e "  ${GREEN}[NO MERGEADA]${NC} upstream/${branch}"
      echo -e "       ${description}"
      echo -e "       Ultimo commit: ${last_commit_date}"
      echo -e "       Commits por delante de main: ${commits_ahead}"
    fi
    echo ""
  done

  if $any_merged; then
    echo -e "${RED}${BOLD}!!! HAY RAMAS WATCH MERGEADAS — REQUIEREN ACCION !!!${NC}"
    echo ""
  fi
}

check_new_upstream_commits() {
  echo -e "${BOLD}--- NUEVOS COMMITS EN UPSTREAM/MAIN ---${NC}"
  echo ""

  local new_commits
  new_commits=$(git rev-list --count "${LAST_SYNC_COMMIT}..upstream/main" 2>/dev/null || echo "0")

  if [ "$new_commits" = "0" ]; then
    echo -e "  ${GREEN}[OK]${NC} Sincronizado — 0 commits nuevos desde ${LAST_SYNC_COMMIT}"
  else
    echo -e "  ${YELLOW}[DESYNC]${NC} ${new_commits} commits nuevos en upstream/main"
    echo ""
    echo "  Ultimos 10:"
    git log --oneline "${LAST_SYNC_COMMIT}..upstream/main" | head -10 | while read -r line; do
      echo "    $line"
    done

    # Verificar si tocan archivos criticos
    echo ""
    echo "  Archivos criticos tocados:"
    local any_critical=false
    for file in "${CRITICAL_FILES[@]}"; do
      if git diff --name-only "${LAST_SYNC_COMMIT}..upstream/main" -- "$file" 2>/dev/null | grep -q .; then
        echo -e "    ${RED}>>> ${file}${NC}"
        any_critical=true
      fi
    done

    if ! $any_critical; then
      echo -e "    ${GREEN}Ninguno${NC}"
    fi
  fi
  echo ""
}

check_fork_drift() {
  echo -e "${BOLD}--- ESTADO DEL FORK ---${NC}"
  echo ""

  local current_branch
  current_branch=$(git branch --show-current)
  local main_commit
  main_commit=$(git rev-parse --short HEAD 2>/dev/null)

  echo "  Rama actual: ${current_branch}"
  echo "  Commit main: ${main_commit}"

  # Verificar si hay cambios [FORK] pendientes de push
  local unpushed
  unpushed=$(git rev-list --count "origin/main..main" 2>/dev/null || echo "0")
  if [ "$unpushed" != "0" ]; then
    echo -e "  ${YELLOW}Commits sin push: ${unpushed}${NC}"
  else
    echo -e "  Push: ${GREEN}al dia${NC}"
  fi

  # Contar marcadores [FORK] en el codigo
  local fork_markers
  fork_markers=$(grep -r "\[FORK\]" graphiti_core/ .github/ 2>/dev/null | wc -l | tr -d ' ')
  echo "  Marcadores [FORK] en codigo: ${fork_markers}"

  echo ""
}

summary() {
  echo -e "${BOLD}=============================================${NC}"
  echo -e "${BOLD}  RESUMEN${NC}"
  echo -e "${BOLD}=============================================${NC}"
  echo ""
  echo "  Para mas detalle sobre impactos:"
  echo "    docs/changelog/CHANGELOG-FORK.md"
  echo ""
  echo "  Para sincronizar con upstream:"
  echo "    git fetch upstream"
  echo "    git merge upstream/main"
  echo ""
}

# --- Main ---
header
check_upstream_remote
fetch_upstream
check_watch_branches
check_new_upstream_commits
check_fork_drift
summary
