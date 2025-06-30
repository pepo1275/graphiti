# 🚨 INFORMACIÓN CRÍTICA PARA CLAUDE CODE/GEMINI CLI

## 📋 COMPLEMENTO AL ISSUE #2 - IMPLEMENTACIÓN MULTI-ENGINE

### 🚨 MANTENER FUNCIONALIDAD EXISTENTE (CRÍTICO)

**LLMs que DEBEN mantenerse disponibles:**
- ✅ **OpenAI**: gpt-4.1-mini, gpt-4.1-nano, gpt-4o (PRINCIPAL actual - NO cambiar)
- ✅ **Anthropic**: claude-sonnet-4-20250514 (YA configurado - NO eliminar)

**LLMs a AÑADIR (sin reemplazar los existentes):**
- 🆕 **Gemini**: gemini-2.5-pro, gemini-2.5-flash
- 🆕 **Azure OpenAI**: (si se requiere)

**Embeddings que DEBEN mantenerse:**
- ✅ **OpenAI**: text-embedding-3-small, text-embedding-3-large (PRINCIPAL actual)

## 📋 REVISIÓN DEL PLAN SOLICITADA

**Claude Code/Gemini CLI: Por favor revisa IMPLEMENTATION_PLAN.md y sugiere:**
- Mejoras en el enfoque gradual paso a paso
- Puntos de riesgo no considerados o mal evaluados  
- Pasos que podrían simplificarse o combinarse
- Verificaciones adicionales necesarias para seguridad
- Orden óptimo de implementación (¿hay mejor secuencia?)
- Dependencias o requisitos que falten

## 🖥️ CONFIGURACIÓN DEL ENTORNO

**Sistema:** macOS (MacBook Air de Pepo)  
**Python:** uv (ubicado en `/Users/pepo/.local/bin/uv`)  
**Proyecto:** `/Users/pepo/graphiti-pepo-local`  
**Neo4j:** bolt://localhost:7687 (usuario: neo4j, password: pepo_graphiti_2025)

**Claude Desktop Config:**  
`~/.config/Claude Desktop/claude_desktop_config.json`

**Servidor MCP actual:**  
`/Users/pepo/graphiti-pepo-local/mcp_server/graphiti_mcp_server.py`

## ⚡ COMANDOS ESPECÍFICOS A EJECUTAR

**Para verificar estado actual:**
```bash
cd /Users/pepo/graphiti-pepo-local
git status
git branch  
uv run python mcp_server/graphiti_mcp_server.py --help
```

**Para activar entorno y probar:**
```bash
cd /Users/pepo/graphiti-pepo-local/mcp_server
uv run python graphiti_mcp_server.py --transport stdio --group-id pepo_phd_research
```

**Para reiniciar Claude Desktop después de cambios:**
```bash
# 1. Cerrar Claude Desktop completamente (Cmd+Q)
# 2. Abrir Claude Desktop de nuevo  
# 3. Verificar que MCP carga sin errores en la consola
```

## ✅ CRITERIOS DE VERIFICACIÓN - CÓMO CONFIRMAR QUE FUNCIONA

**Prueba mínima obligatoria después de CADA cambio:**
1. **Test básico:** `add_memory("test gemini integration")` debe funcionar SIN errores
2. **Test búsqueda:** `search_memory_nodes("test")` debe encontrar el test anterior  
3. **Test regresión:** Verificar que funcionalidad OpenAI existente NO se rompió

**Criterios de éxito por fase:**
- **Fase 2:** Gemini API key funciona, archivos .env creados correctamente
- **Fase 3:** MCP inicia con configuración multi-engine, OpenAI sigue siendo principal
- **Fase 4:** Cambio temporal a Gemini funciona Y vuelta a OpenAI funciona
- **Fase 5:** Documentación completa, configuración definitiva estable

## 🛑 LÍMITES CLAROS - CUÁNDO PARAR Y CONSULTAR

**NO proceder sin confirmación si encuentras:**
- ❌ Errores en importaciones de Gemini o Google APIs
- ❌ Fallas en configuración de API keys (401, 403, etc.)
- ❌ Claude Desktop no inicia o muestra errores MCP
- ❌ Tests básicos (`add_memory`, `search_memory_nodes`) fallan
- ❌ Dependencias faltantes o conflictos de versiones

**SIEMPRE crear commit de seguridad antes de:**
- 🔄 Cambiar archivos de configuración MCP
- 🔄 Modificar `claude_desktop_config.json`  
- 🔄 Instalar nuevas dependencias con `uv`
- 🔄 Cambiar variables de entorno críticas

**Si algo falla - ROLLBACK inmediato a:**
```bash
git reset --hard HEAD~1  # Volver al commit anterior
# Restaurar claude_desktop_config.json desde backup
```

## 🎯 RESUMEN PARA AI TOOLS

**OBJETIVO:** Añadir soporte Gemini manteniendo OpenAI + Claude Sonnet 4 existentes
**ESTRATEGIA:** Implementación gradual, paso a paso, con commits frecuentes
**PRIORIDAD #1:** NO romper configuración actual que funciona
**PRIORIDAD #2:** Mantener OpenAI como principal durante todo el proceso
**PRIORIDAD #3:** Poder hacer rollback en cualquier momento

---

**Ver también:**
- Issue principal: #2 en GitHub
- Plan detallado: `IMPLEMENTATION_PLAN.md`
- Configuración: `mcp_server/config_multi_engine.py`
