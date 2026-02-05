# Problemas de CI/CD para el Fork

**Estado**: Análisis completado
**Fecha**: 2026-01-31
**Prerequisito para**: Fase 0 (Sincronización con Upstream)

---

## 1. Resumen de Problemas

Los workflows de GitHub Actions del upstream están configurados para la infraestructura de Zep y **NO funcionarán** en tu fork sin modificaciones.

| Problema | Archivos Afectados | Impacto |
|----------|-------------------|---------|
| Runner privado `depot-ubuntu-*` | 5 workflows | Crítico - Jobs fallarán |
| Secret `DANIEL_PAT` | cla.yml | Medio - CLA no funcionará |
| Secret `ANTHROPIC_API_KEY` | 3 workflows | Bajo - Reviews automáticos |
| Secrets `DOCKERHUB_*` | 2 workflows | Bajo - No publicas imágenes |

---

## 2. Problema 1: Runner Privado Depot

### Descripción

Zep usa [Depot](https://depot.dev/) como proveedor de runners para GitHub Actions. Los runners `depot-ubuntu-22.04` y `depot-ubuntu-24.04-small` son **privados de Zep** y no están disponibles para forks.

### Archivos Afectados

```yaml
# unit_tests.yml (líneas 14, 48)
runs-on: depot-ubuntu-22.04

# lint.yml (línea 12)
runs-on: depot-ubuntu-22.04

# typecheck.yml (línea 14)
runs-on: depot-ubuntu-22.04

# release-mcp-server.yml (línea 19)
runs-on: depot-ubuntu-24.04-small

# release-server-container.yml (línea 20)
runs-on: depot-ubuntu-24.04-small
```

### Solución

Cambiar a runners estándar de GitHub:

```yaml
# ANTES (Zep)
runs-on: depot-ubuntu-22.04

# DESPUÉS (Fork)
runs-on: ubuntu-22.04
# o
runs-on: ubuntu-latest
```

### Script de Migración

```bash
# Reemplazar en todos los workflows
cd .github/workflows
sed -i '' 's/depot-ubuntu-22.04/ubuntu-22.04/g' *.yml
sed -i '' 's/depot-ubuntu-24.04-small/ubuntu-24.04/g' *.yml
```

---

## 3. Problema 2: Secret DANIEL_PAT

### Descripción

El workflow de CLA (Contributor License Agreement) usa un token personal de un desarrollador de Zep:

```yaml
# cla.yml (línea 25)
GITHUB_TOKEN: ${{ secrets.DANIEL_PAT }}
```

Este token es necesario para que el bot de CLA funcione con permisos elevados.

### Impacto

- El CLA check fallará en PRs
- No es crítico para uso personal del fork

### Soluciones

**Opción A: Desactivar CLA (Recomendado para fork personal)**
```yaml
# Renombrar o eliminar
cla.yml -> cla.yml.disabled
```

**Opción B: Usar tu propio PAT**
1. Crear Personal Access Token en GitHub
2. Añadir como secret `PEPO_PAT` en tu fork
3. Modificar workflow:
```yaml
GITHUB_TOKEN: ${{ secrets.PEPO_PAT }}
```

**Opción C: Usar GITHUB_TOKEN estándar (limitado)**
```yaml
GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```
Nota: Puede no tener todos los permisos necesarios.

---

## 4. Problema 3: Secret ANTHROPIC_API_KEY

### Descripción

Tres workflows usan Claude para revisión automática de código:

```yaml
# claude-code-review.yml (línea 41)
anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}

# claude-code-review-manual.yml (línea 38)
anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}

# claude.yml (línea 37)
anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
```

### Impacto

- Reviews automáticos no funcionarán
- No es crítico - puedes revisar manualmente

### Soluciones

**Opción A: Desactivar workflows de Claude (Recomendado)**
```bash
# Renombrar para desactivar
mv claude-code-review.yml claude-code-review.yml.disabled
mv claude-code-review-manual.yml claude-code-review-manual.yml.disabled
mv claude.yml claude.yml.disabled
```

**Opción B: Añadir tu propia API key**
1. Obtener API key de Anthropic
2. Añadir como secret en tu fork: Settings -> Secrets -> Actions
3. Los workflows funcionarán (pero gastarás tu crédito)

---

## 5. Problema 4: Secrets de DockerHub

### Descripción

Workflows de release publican imágenes a DockerHub de Zep:

```yaml
# release-mcp-server.yml (líneas 83-84)
username: ${{ secrets.DOCKERHUB_USERNAME }}
password: ${{ secrets.DOCKERHUB_TOKEN }}

# release-server-container.yml (líneas 113-114)
username: ${{ secrets.DOCKERHUB_USERNAME }}
password: ${{ secrets.DOCKERHUB_TOKEN }}
```

### Impacto

- No puedes publicar a DockerHub de Zep (correcto)
- Si necesitas publicar, usarías tu propio DockerHub

### Soluciones

**Opción A: Desactivar releases (Recomendado)**
```bash
# Renombrar para desactivar
mv release-mcp-server.yml release-mcp-server.yml.disabled
mv release-server-container.yml release-server-container.yml.disabled
```

**Opción B: Configurar tu propio DockerHub**
1. Crear cuenta en DockerHub
2. Crear token de acceso
3. Añadir secrets: `DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN`
4. Modificar nombres de imagen en workflows

---

## 6. Plan de Acción Recomendado

### Fase 0.1: Preparación de Workflows (ANTES del sync)

```bash
cd /Users/josemanuelsanchezsantana/Devs/graphiti-new

# 1. Crear directorio para workflows desactivados
mkdir -p .github/workflows-upstream-disabled

# 2. Mover workflows que no necesitas
mv .github/workflows/cla.yml .github/workflows-upstream-disabled/
mv .github/workflows/claude-code-review.yml .github/workflows-upstream-disabled/
mv .github/workflows/claude-code-review-manual.yml .github/workflows-upstream-disabled/
mv .github/workflows/claude.yml .github/workflows-upstream-disabled/
mv .github/workflows/release-mcp-server.yml .github/workflows-upstream-disabled/
mv .github/workflows/release-server-container.yml .github/workflows-upstream-disabled/

# 3. Crear versiones modificadas de workflows esenciales
# (Se crearán archivos nuevos con runners corregidos)
```

### Fase 0.2: Crear Workflows Adaptados

Crear versiones modificadas de los workflows esenciales:

**`.github/workflows/unit_tests.yml` (modificado)**
```yaml
# Cambiar líneas 14 y 48
runs-on: ubuntu-22.04  # Era: depot-ubuntu-22.04
```

**`.github/workflows/lint.yml` (modificado)**
```yaml
# Cambiar línea 12
runs-on: ubuntu-22.04  # Era: depot-ubuntu-22.04
```

**`.github/workflows/typecheck.yml` (modificado)**
```yaml
# Cambiar línea 14
runs-on: ubuntu-22.04  # Era: depot-ubuntu-22.04
```

### Fase 0.3: Documentar Cambios

Añadir a CHANGELOG-FORK.md:
```markdown
### Changed
- [FORK] Workflows adaptados para runners de GitHub estándar
- [FORK] Desactivados workflows de CLA, Claude review, y releases
```

---

## 7. Matriz de Workflows

| Workflow | Estado Propuesto | Cambios Necesarios |
|----------|------------------|-------------------|
| `unit_tests.yml` | **Mantener** | Cambiar runner |
| `lint.yml` | **Mantener** | Cambiar runner |
| `typecheck.yml` | **Mantener** | Cambiar runner |
| `codeql.yml` | **Mantener** | Ninguno (usa ubuntu-latest) |
| `ai-moderator.yml` | **Mantener** | Ninguno (usa ubuntu-latest) |
| `cla.yml` | Desactivar | Mover a disabled/ |
| `claude-code-review.yml` | Desactivar | Mover a disabled/ |
| `claude-code-review-manual.yml` | Desactivar | Mover a disabled/ |
| `claude.yml` | Desactivar | Mover a disabled/ |
| `release-mcp-server.yml` | Desactivar | Mover a disabled/ |
| `release-server-container.yml` | Desactivar | Mover a disabled/ |
| `release-graphiti-core.yml` | Evaluar | Puede necesitar cambios |

---

## 8. Consideraciones para Sync con Upstream

### Durante el Merge

Cuando hagas `git merge upstream/main`, los workflows vendrán con la configuración de Zep. Estrategia:

1. **Antes del merge**: Tener tus workflows modificados commitados
2. **Durante el merge**: Resolver conflictos manteniendo TUS versiones
3. **Después del merge**: Verificar que runners están correctos

### Archivo .github/workflows/.gitattributes (Opcional)

Para evitar conflictos automáticos:
```
# .github/workflows/.gitattributes
*.yml merge=ours
```

Esto hace que tus versiones de workflows siempre "ganen" en merges.

---

## 9. Checklist Pre-Sync

- [ ] Workflows esenciales modificados con runners estándar
- [ ] Workflows innecesarios movidos a `workflows-upstream-disabled/`
- [ ] Cambios commitados en branch actual
- [ ] CHANGELOG-FORK.md actualizado
- [ ] Backup del estado actual creado

---

## 10. Referencias

- [GitHub Hosted Runners](https://docs.github.com/en/actions/using-github-hosted-runners/about-github-hosted-runners)
- [Depot Runners](https://depot.dev/docs/github-actions/overview)
- [Managing Workflow Runs](https://docs.github.com/en/actions/managing-workflow-runs)
