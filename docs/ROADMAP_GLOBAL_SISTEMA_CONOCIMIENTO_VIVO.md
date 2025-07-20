# 🚀 ROADMAP GLOBAL: Sistema de Conocimiento Vivo Co-creativo

**Fecha:** 2025-07-20  
**Estado:** Análisis completado - Ready for implementation  
**Branch actual:** `feature/multi-graphiti-manager`  
**Objetivo:** Construir Sistema de Conocimiento Vivo con MVP de Administración de Medicamentos

---

## 📊 CONTEXTO Y VISIÓN

### **VISIÓN A LARGO PLAZO**
Crear un **Sistema de Conocimiento Vivo Co-creativo** donde:
- 🧠 **Aprendizaje bidireccional**: Sistema aprende de usuarios, usuarios aprenden del sistema
- 📚 **Conocimiento dual**: Formal (normativas) + Episódico (experiencias)
- 🌐 **Multi-dominio**: Salud, administración pública, configuración técnica
- 🔄 **Evolución continua**: El conocimiento mejora con cada interacción

### **MVP INMEDIATO: Sistema Administración de Medicamentos**
- **Usuarios**: Enfermeras consultando medicamentos inyectables
- **Datos**: 1300 medicamentos AEMPS + episodios de uso
- **Timeline**: 4 semanas (gracias a Graphiti)
- **Arquitectura**: Dual MCP (Graphiti episódico + AEMPS dominio)

---

## 🎯 OBJETIVO CRÍTICO INMEDIATO

### **Evaluación y Selección de Embeddings Óptimos**

**¿Por qué es crítico?**
- Los embeddings son el **puente semántico** entre consultas y conocimiento
- Determinan la **calidad de búsqueda** en ambos grafos
- Impactan directamente la **experiencia de usuario** (precisión y velocidad)

**Opciones a evaluar:**
1. **OpenAI text-embedding-3-small**: General purpose, probado
2. **Gemini con CODE_RETRIEVAL_QUERY**: Optimizado para código/consultas técnicas
3. **Futuro**: Voyage-code-3, Jina v4, Qwen3, BGE-M3

---

## 🏗️ ARQUITECTURA TÉCNICA DEFINITIVA

### **Stack Tecnológico Seleccionado**

```yaml
# Infraestructura Base
databases:
  episodic_memory: 
    engine: "Neo4j + Graphiti"
    status: "✅ Funcionando"
    mcp_server: "graphiti-mcp"
    
  domain_knowledge:
    engine: "Neo4j AEMPS"
    status: "🔧 A desarrollar"
    mcp_server: "aemps-mcp"

# Gestión de Instancias
orchestration:
  manager: "MCPGraphitiManager"
  approach: "MCP-First"
  benefits: "Vendor agnostic, escalable, testeable"

# LLMs y Embeddings
ai_models:
  llms: ["gpt-4o", "gemini-2.5-flash", "claude-3-sonnet"]
  embeddings: ["openai", "gemini", "future_models"]
  routing: "MedGemma para interpretación médica"

# Desarrollo
development:
  language: "Python"
  testing: "pytest + integration tests"
  deployment: "Docker containers"
  monitoring: "Token monitoring system"
```

### **Arquitectura MCP-First**

```python
# Nueva arquitectura simplificada
class MCPGraphitiManager:
    """Gestiona todas las operaciones via MCP"""
    
    def __init__(self):
        self.mcp_clients = {
            # Memoria episódica
            "graphiti": MCPClient("graphiti-mcp"),
            
            # Conocimiento dominio
            "aemps": MCPClient("aemps-mcp"),
            
            # Infraestructura
            "docker": MCPClient("dockerhub"),
            
            # Future: otros dominios
            "contratacion": MCPClient("contratacion-mcp"),
            "config_tech": MCPClient("tech-config-mcp")
        }
```

---

## 📅 ROADMAP DETALLADO POR FASES

### **FASE 1: EVALUACIÓN DE EMBEDDINGS (1 semana)**
**Branch**: `evaluation/embeddings-comparison`

#### Objetivos
- ✅ Determinar mejor modelo de embeddings para búsquedas médicas
- ✅ Validar si CODE_RETRIEVAL_QUERY mejora búsqueda de código Cypher
- ✅ Establecer baseline de performance (P95 < 300ms)

#### Tareas
1. **Setup evaluación** (Día 1)
   ```bash
   # Crear databases Neo4j
   CREATE DATABASE eval_openai_embeddings;
   CREATE DATABASE eval_gemini_embeddings;
   ```

2. **Poblar instancias** (Día 2)
   ```bash
   uv run populate_instances.py --dataset medical_test_set
   ```

3. **Ejecutar evaluación** (Día 3-4)
   ```bash
   uv run run_multi_engine_evaluation.py
   uv run graphiti-tokens summary -p all -d 1  # Monitor costs
   ```

4. **Análisis resultados** (Día 5)
   ```bash
   uv run analyze_results.py
   # Generar reporte con recomendaciones
   ```

#### Entregables
- `evaluation_results_YYYYMMDD.csv`: Resultados comparativos
- `EMBEDDINGS_RECOMMENDATION.md`: Recomendación fundamentada
- Configuración óptima seleccionada

#### Archivos clave
- `/docs/PLAN_EVALUACION_COMPLETO.md`: Plan detallado
- `evaluation_framework_complete.py`: Framework de evaluación
- `test_suites_definition.py`: Casos de prueba

---

### **FASE 2: IMPLEMENTACIÓN MCPGraphitiManager (1 semana)**
**Branch**: `feature/mcp-graphiti-manager`

#### Objetivos
- ✅ Implementar gestión MCP-First de instancias
- ✅ Integrar con embeddings seleccionados en Fase 1
- ✅ Preparar foundation para agentes futuros

#### Tareas
1. **Core implementation** (Día 1-2)
   ```python
   # graphiti_core/managers/mcp_graphiti_manager.py
   class MCPGraphitiManager:
       async def add_episode_to_instance(self, instance, episode)
       async def search_across_instances(self, query)
       async def get_comprehensive_stats(self)
   ```

2. **MCP client abstraction** (Día 3)
   ```python
   # graphiti_core/managers/mcp_client.py
   class MCPClient:
       async def call_tool(self, tool_name, parameters)
       async def health_check(self)
   ```

3. **Testing** (Día 4-5)
   ```bash
   pytest tests/managers/test_mcp_graphiti_manager.py
   pytest tests/integration/test_mcp_ecosystem.py
   ```

#### Entregables
- `MCPGraphitiManager`: Clase funcional y testeada
- Tests unitarios e integración pasando
- Documentación de API

#### Archivos clave
- `/docs/MULTI_GRAPHITI_MANAGER_DEVELOPMENT_PLAN_V3_MCP_FIRST.md`: Plan implementación
- `/docs/MCP_STRATEGIC_ANALYSIS_AGENTIC_WORKFLOWS.md`: Análisis estratégico

---

### **FASE 3: DESARROLLO AEMPS MCP SERVER (1 semana)**
**Branch**: `feature/aemps-mcp-server`

#### Objetivos
- ✅ Parsear y cargar nomenclátor AEMPS (1300 medicamentos)
- ✅ Crear MCP server para consultas de medicamentos
- ✅ Integrar con MCPGraphitiManager

#### Tareas
1. **Parse AEMPS data** (Día 1)
   ```python
   # aemps_parser.py
   def parse_aemps_nomenclator(xml_file):
       # Extraer medicamentos inyectables
       # Crear estructura para Neo4j
   ```

2. **Neo4j schema design** (Día 2)
   ```cypher
   // Medicamentos, principios activos, dosis, interacciones
   (:Medicamento)-[:CONTIENE]->(:PrincipioActivo)
   (:Medicamento)-[:AJUSTE_RENAL]->(:AjusteRenal)
   ```

3. **MCP server implementation** (Día 3-4)
   ```python
   # aemps_mcp/server.py
   class AEMPSMCPServer:
       tools = [
           "buscar_medicamento",
           "calcular_dosis", 
           "verificar_interacciones"
       ]
   ```

4. **Integration testing** (Día 5)
   ```bash
   # Test dual MCP setup
   claude_desktop_config.json con ambos MCPs
   ```

#### Entregables
- AEMPS MCP Server funcional
- Base de datos Neo4j poblada
- Integración con Graphiti MCP validada

#### Datos fuente
- https://cima.aemps.es/cima/publico/nomenclator.html
- https://sede.aemps.gob.es/datos-abiertos/

---

### **FASE 4: MVP SISTEMA MEDICAMENTOS (1 semana)**
**Branch**: `feature/medication-system-mvp`

#### Objetivos
- ✅ Sistema completo funcionando end-to-end
- ✅ Validación con casos reales de enfermería
- ✅ Métricas de performance y utilidad

#### Tareas
1. **Integration pipeline** (Día 1-2)
   ```python
   # Flujo completo: Consulta → Routing → Dual search → Synthesis
   ```

2. **Custom entities for Graphiti** (Día 3)
   ```python
   class ConsultaMedicamento(Entity)
   class EpisodioResolucion(Entity)
   class PatronEmergente(Entity)
   ```

3. **Real world testing** (Día 4-5)
   - Casos de prueba con enfermeras
   - Ajustes basados en feedback
   - Validación médica

#### Entregables
- MVP funcional completo
- Documentación de uso
- Métricas de validación

#### Archivos clave
- `/docs/domain_knowledge_system_project/medication_system_mvp.md`: Especificación MVP

---

## 🎯 CRITERIOS DE ÉXITO

### **Fase 1: Embeddings**
- ✅ Identificar configuración óptima con métricas claras
- ✅ CODE_RETRIEVAL_QUERY demuestra mejora >10% en búsqueda técnica
- ✅ Performance P95 < 300ms confirmado

### **Fase 2: MCPGraphitiManager**
- ✅ Gestión unificada de múltiples instancias funcionando
- ✅ Tests pasando con >90% cobertura
- ✅ Cambio de embeddings sin modificar código

### **Fase 3: AEMPS MCP**
- ✅ 1300 medicamentos cargados correctamente
- ✅ Consultas básicas funcionando via MCP
- ✅ Integración con Graphiti validada

### **Fase 4: MVP**
- ✅ Sistema responde consultas reales <2 segundos
- ✅ Enfermeras validan utilidad >8/10
- ✅ Al menos 10 episodios registrados automáticamente

---

## 🚀 COMANDOS PARA CONTINUAR

### **Para retomar en cualquier sesión:**

```bash
# 1. Verificar estado actual
git status
git log --oneline -5

# 2. Cargar entorno
source .env.evaluation
export GOOGLE_API_KEY="$GEMINI_API_KEY"

# 3. Verificar infraestructura
docker ps | grep neo4j
uv run graphiti-tokens status

# 4. Continuar según fase actual
# Fase 1: Evaluación
uv run run_multi_engine_evaluation.py

# Fase 2: MCPGraphitiManager
pytest tests/managers/ -v

# Fase 3: AEMPS
uv run aemps_parser.py

# Fase 4: MVP
uv run medication_system_test.py
```

### **Archivos de referencia rápida:**
```bash
# Planes y documentación
cat docs/ROADMAP_GLOBAL_SISTEMA_CONOCIMIENTO_VIVO.md  # Este documento
cat docs/PLAN_EVALUACION_COMPLETO.md                  # Plan evaluación embeddings
cat docs/MULTI_GRAPHITI_MANAGER_DEVELOPMENT_PLAN_V3_MCP_FIRST.md  # Plan MCP

# Contexto del proyecto
cat docs/domain_knowledge_system_project/medication_system_mvp.md
cat docs/domain_knowledge_system_project/knowledge_system_context.md

# Estado actual
cat docs/GRAPHITI_MULTI_DATABASE_INVESTIGATION.md
cat docs/MCP_STRATEGIC_ANALYSIS_AGENTIC_WORKFLOWS.md
```

---

## 📊 ESTADO ACTUAL Y PRÓXIMOS PASOS

### **Estado al 2025-07-20:**
- ✅ Investigación multi-database completada
- ✅ Estrategia MCP-First definida
- ✅ Plan de evaluación embeddings listo
- ✅ Arquitectura MVP medicamentos clara
- 🔄 **PRÓXIMO**: Iniciar Fase 1 - Evaluación embeddings

### **Acción inmediata recomendada:**
```bash
# Crear branch para evaluación
git checkout -b evaluation/embeddings-comparison

# Iniciar setup de evaluación
uv run python manage_neo4j_databases.py --create-eval-databases
```

### **Riesgos identificados:**
1. **Costos API**: Monitorear con token monitoring system
2. **Performance**: Validar P95 < 300ms constantemente
3. **Calidad datos AEMPS**: Validar parsing XML correcto
4. **Adopción usuarios**: Involucrar enfermeras temprano

---

## 🔮 VISIÓN POST-MVP

### **Expansión a otros dominios:**
1. **Contratación Pública**: Normativas + casos previos
2. **Configuración Técnica**: Docker/MCP + troubleshooting
3. **Protocolos Clínicos**: Guías médicas + experiencias

### **Evolución hacia agentes especializados:**
- Knowledge Agent: Construcción de grafos de conocimiento
- Analytics Agent: Análisis de patrones
- Research Agent: Investigación autónoma
- DevOps Agent: Gestión de infraestructura

### **Métricas de éxito a largo plazo:**
- 1000+ episodios registrados/mes
- 90%+ consultas resueltas sin intervención
- <2 segundos tiempo respuesta promedio
- 95%+ satisfacción usuarios

---

## 📝 NOTAS PARA CONTINUIDAD

### **Para Claude Code:**
- Branch actual documentado al inicio
- Archivos clave referenciados con paths completos
- Comandos específicos para cada fase
- Estado actual claramente marcado

### **Para Gemini CLI:**
- Misma estructura de archivos
- Comandos bash compatibles
- Referencias a documentación sin dependencias Claude

### **Checkpoints importantes:**
1. Después de cada fase, crear tag git
2. Documentar resultados en `/docs/results/`
3. Actualizar este roadmap con progreso
4. Backup de bases de datos Neo4j

---

*Documento maestro para continuidad del proyecto - Actualizar después de cada fase completada*

**Última actualización:** 2025-07-20  
**Próxima revisión:** Al completar Fase 1