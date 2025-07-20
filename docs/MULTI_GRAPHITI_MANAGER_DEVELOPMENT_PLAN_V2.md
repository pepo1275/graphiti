# 📋 PLAN DE DESARROLLO: MultiGraphitiManager v2.0

**Fecha:** 2025-07-20  
**Branch actual:** `feature/multi-graphiti-manager`  
**Objetivo:** Implementar MultiGraphitiManager con integración Docker Hub MCP  
**Versión:** 2.0 (actualizada con Docker Hub MCP)

---

## 🆕 CAMBIOS EN LA VERSIÓN 2.0

### **Nuevas Características:**
- ✅ **Docker Hub MCP Integration**: Gestión robusta de contenedores
- ✅ **Auto-Recovery**: Restart automático de contenedores fallidos
- ✅ **Health Monitoring**: Monitoreo continuo de estado
- ✅ **Container Logs**: Acceso centralizado a logs para debugging

### **Credenciales Extraídas:**
```yaml
instances:
  graphiti:
    uri: "bolt://localhost:7687"
    user: "neo4j" 
    password: "pepo_graphiti_2025"
    container_name: "graphiti-neo4j"
    namespace: "graphiti"
    
  pproc:
    uri: "bolt://localhost:7689"
    user: "neo4j"
    password: "docker_test"
    container_name: "pproc"
    namespace: "pproc"
    
  sigma2:
    uri: "bolt://localhost:7691"
    user: "neo4j"
    password: "desktop_test"
    container_name: "sigma2"
    namespace: "sigma2"
    
  materno:
    uri: "bolt://localhost:7692"
    user: "neo4j"
    password: "desktop_test"
    container_name: "materno_infantil"
    namespace: "materno"
```

---

## 🛡️ MEJORES PRÁCTICAS A SEGUIR

### **1. CONTROL DE VERSIONES** ✅
- ✅ **Backup completo**: Commit actual realizado
- ✅ **Branch nueva**: `feature/multi-graphiti-manager` activa
- ✅ **Commits granulares**: Un feature por commit
- ✅ **Mensajes descriptivos**: Convención conventional commits

### **2. DOCUMENTACIÓN**
- ✅ **Plan de desarrollo**: Este documento v2.0
- ✅ **Documentación técnica**: README del MultiGraphitiManager
- ✅ **Docstrings**: Documentación inline completa
- ✅ **Ejemplos de uso**: Scripts de ejemplo
- 🆕 **Docker Integration**: Documentación de integración MCP

### **3. TESTING**
- ✅ **Tests previos**: Verificar estado actual
- ✅ **Tests unitarios**: Para cada método del manager
- ✅ **Tests integración**: Con instancias Docker reales
- ✅ **Tests post**: Validación completa
- 🆕 **Docker MCP Tests**: Tests de integración con MCP Docker Hub

### **4. CONFIGURACIÓN**
- ✅ **Variables entorno**: Configuración externalizada
- ✅ **Validación**: Verificar conexiones Docker
- ✅ **Fallbacks**: Manejo de errores robusto
- 🆕 **MCP Integration**: Configuración Docker Hub MCP

### **5. ARQUITECTURA**
- ✅ **Separación responsabilidades**: Clases enfocadas
- ✅ **Interfaces claras**: APIs bien definidas
- ✅ **Extensibilidad**: Fácil agregar nuevas instancias
- 🆕 **Docker Layer**: Capa de abstracción para gestión contenedores

---

## 📅 PLAN DE EJECUCIÓN DETALLADO v2.0

### **FASE 0: PREPARACIÓN CON DOCKER MCP (20 min)**

#### **0.1 Verificar MCP Docker Hub**
```bash
# Verificar que Docker Hub MCP está funcionando
# Usar @dockerhub search neo4j para validar conectividad
```

#### **0.2 Mapear Contenedores Neo4j Existentes**
```bash
# Obtener lista de contenedores Neo4j activos
# Usar @dockerhub listRepositoriesByNamespace library
# Verificar imágenes neo4j disponibles
```

#### **0.3 Test Conectividad Instancias**
```python
# Crear script de verificación usando credenciales extraídas
# test_docker_instances_connectivity.py
```

### **FASE 1: ANÁLISIS Y DISEÑO CON DOCKER (35 min)**

#### **1.1 Documentar Arquitectura Docker**
```yaml
# docker_architecture.yaml
containers:
  graphiti-neo4j:
    image: "neo4j:5.26.0"
    ports: ["7687:7687", "7474:7474"]
    environment:
      NEO4J_AUTH: "neo4j/pepo_graphiti_2025"
    status: "running"
    
  pproc:
    image: "neo4j:5.20"
    ports: ["7689:7687", "8689:7474"]
    environment:
      NEO4J_AUTH: "neo4j/docker_test"
    status: "running"
```

#### **1.2 Diseñar Interface Extendida**
```python
# Diseño con Docker integration
class MultiGraphitiManager:
    def __init__(self, config_file: str | dict = None)
    async def initialize_instances(self)
    async def add_episode_to_all(self, episode: str)
    async def search_across_instances(self, query: str)
    async def get_instance_stats(self)
    async def health_check_all(self)
    
    # 🆕 Docker Management
    async def verify_docker_containers(self)
    async def restart_failed_containers(self)
    async def get_container_logs(self, instance_name: str)
    async def scale_instance(self, instance_name: str, action: str)

class DockerManager:
    """Manages Docker containers using Docker Hub MCP"""
    async def check_container_health(self, container_name: str)
    async def restart_container(self, container_name: str)
    async def get_container_status(self, container_name: str)
    async def get_container_logs(self, container_name: str)
```

#### **1.3 Crear Tests Previos Extendidos**
```python
# tests/test_current_docker_setup.py
# Verificar que todas las instancias Docker funcionan
# Usar tanto conexiones directas como MCP Docker Hub
```

### **FASE 2: CONFIGURACIÓN MULTI-LAYER (25 min)**

#### **2.1 Configuración MultiGraphiti con Docker**
```yaml
# config/multi_graphiti_config.yaml
instances:
  graphiti:
    # Graphiti connection
    uri: "bolt://localhost:7687"
    user: "neo4j"
    password: "pepo_graphiti_2025"
    embedder_type: "openai"
    
    # Docker management
    container_name: "graphiti-neo4j"
    docker_image: "neo4j:5.26.0"
    ports: ["7687:7687", "7474:7474"]
    restart_policy: "auto"
    health_check_interval: 30
    
  pproc:
    uri: "bolt://localhost:7689"
    user: "neo4j"
    password: "docker_test"
    embedder_type: "gemini"
    
    container_name: "pproc"
    docker_image: "neo4j:5.20"
    ports: ["7689:7687", "8689:7474"]
    restart_policy: "auto"
    health_check_interval: 30

# Docker Hub MCP configuration
docker_hub:
  username: "pepo1275"
  use_mcp: true
  mcp_namespace: "dockerhub"
  
# MultiGraphiti settings
multi_graphiti:
  auto_recovery: true
  health_monitoring: true
  parallel_operations: true
  max_retries: 3
  timeout_seconds: 30
```

#### **2.2 Variables de Entorno Extendidas**
```bash
# .env.multi_graphiti
MULTI_GRAPHITI_CONFIG_PATH=./config/multi_graphiti_config.yaml
MULTI_GRAPHITI_LOG_LEVEL=INFO
MULTI_GRAPHITI_TIMEOUT=30

# Docker Hub MCP
DOCKER_HUB_USERNAME=pepo1275
DOCKER_HUB_MCP_ENABLED=true
DOCKER_AUTO_RECOVERY=true
DOCKER_HEALTH_CHECK_INTERVAL=30
```

### **FASE 3: IMPLEMENTACIÓN MULTI-LAYER (60 min)**

#### **3.1 Core MultiGraphitiManager**
```python
# graphiti_core/managers/multi_graphiti_manager.py
class MultiGraphitiManager:
    """
    Manages multiple Graphiti instances across Docker containers
    with auto-recovery and health monitoring via Docker Hub MCP
    """
    
    def __init__(self, config: MultiGraphitiConfig):
        self.config = config
        self.instances: Dict[str, Graphiti] = {}
        self.docker_manager = DockerManager(config.docker_hub)
        self.health_monitor = HealthMonitor(self.docker_manager)
        
    async def initialize_instances(self):
        """Initialize all Graphiti instances with Docker verification"""
        
    async def add_episode_to_all(self, episode: str):
        """Add episode to all healthy instances in parallel"""
        
    async def search_across_instances(self, query: str):
        """Search across all instances and aggregate results"""
        
    async def get_instance_stats(self):
        """Get comprehensive stats including Docker health"""
        
    async def auto_recovery_check(self):
        """Check and recover failed containers automatically"""
```

#### **3.2 Docker Manager**
```python
# graphiti_core/managers/docker_manager.py
class DockerManager:
    """Manages Docker containers using Docker Hub MCP integration"""
    
    def __init__(self, docker_config: DockerConfig):
        self.config = docker_config
        self.mcp_client = DockerHubMCPClient()
        
    async def check_container_health(self, container_name: str) -> ContainerHealth:
        """Check container health using Docker Hub MCP"""
        
    async def restart_container(self, container_name: str) -> bool:
        """Restart container if unhealthy"""
        
    async def get_container_logs(self, container_name: str, lines: int = 100) -> str:
        """Get container logs for debugging"""
        
    async def verify_all_containers(self) -> Dict[str, ContainerStatus]:
        """Verify all required containers are running"""
```

#### **3.3 Configuration Handler**
```python
# graphiti_core/managers/config.py
class MultiGraphitiConfig:
    """Handles configuration loading and validation with Docker integration"""
    
    @classmethod
    def from_file(cls, config_path: str) -> 'MultiGraphitiConfig':
        """Load configuration from YAML file"""
        
    @classmethod 
    def from_claude_desktop_config(cls, mcp_config: dict) -> 'MultiGraphitiConfig':
        """Extract configuration from Claude Desktop MCP config"""
        
    def validate_docker_connectivity(self) -> bool:
        """Validate all Docker containers are accessible"""
```

#### **3.4 Health Monitor**
```python
# graphiti_core/managers/health_monitor.py
class HealthMonitor:
    """Continuous health monitoring with auto-recovery"""
    
    def __init__(self, docker_manager: DockerManager):
        self.docker_manager = docker_manager
        self.monitoring_active = False
        
    async def start_monitoring(self, interval: int = 30):
        """Start continuous health monitoring"""
        
    async def health_check_cycle(self):
        """Single health check cycle for all instances"""
        
    async def handle_unhealthy_container(self, container_name: str):
        """Handle unhealthy container with recovery strategies"""
```

### **FASE 4: TESTING MULTI-LAYER (40 min)**

#### **4.1 Tests Unitarios**
```python
# tests/managers/test_multi_graphiti_manager.py
class TestMultiGraphitiManager:
    def test_init_with_config()
    def test_instance_creation_with_docker()
    def test_health_check_integration()
    def test_auto_recovery_workflow()
    def test_parallel_episode_addition()
    def test_error_handling_scenarios()

# tests/managers/test_docker_manager.py  
class TestDockerManager:
    def test_container_health_check()
    def test_container_restart()
    def test_mcp_integration()
    def test_log_retrieval()
```

#### **4.2 Tests Integración**
```python
# tests/integration/test_docker_mcp_integration.py
class TestDockerMCPIntegration:
    def test_real_docker_hub_mcp_connectivity()
    def test_container_management_workflow()
    def test_neo4j_container_health_monitoring()
    def test_auto_recovery_full_cycle()

# tests/integration/test_multi_instance_workflows.py
class TestMultiInstanceWorkflows:
    def test_parallel_episode_processing()
    def test_cross_instance_search()
    def test_failover_scenarios()
    def test_performance_under_load()
```

#### **4.3 Tests Performance y Stress**
```python
# tests/performance/test_multi_instance_performance.py
class TestPerformance:
    def test_parallel_vs_sequential_performance()
    def test_auto_recovery_impact()
    def test_docker_overhead_analysis()
    def test_scalability_limits()
```

### **FASE 5: DOCUMENTACIÓN COMPLETA (25 min)**

#### **5.1 README MultiGraphitiManager v2.0**
```markdown
# MultiGraphitiManager v2.0

## Overview
Advanced manager for multiple Graphiti instances with Docker integration,
auto-recovery, and health monitoring via Docker Hub MCP.

## Features
- Multi-instance Graphiti management
- Docker container health monitoring
- Auto-recovery of failed containers
- Docker Hub MCP integration
- Parallel operations across instances
- Comprehensive logging and debugging

## Quick Start
## Configuration
## Docker Integration
## Auto-Recovery
## API Reference
## Troubleshooting
```

#### **5.2 Docker Integration Guide**
```markdown
# Docker Integration Guide

## Prerequisites
## Container Setup
## MCP Configuration
## Health Monitoring
## Auto-Recovery
## Troubleshooting
```

#### **5.3 Ejemplos de Uso**
```python
# examples/basic_multi_graphiti_usage.py
# examples/docker_integration_example.py
# examples/auto_recovery_demo.py
# examples/health_monitoring_setup.py
# examples/evaluation_with_multi_manager.py
```

### **FASE 6: VALIDACIÓN FINAL EXTENDIDA (20 min)**

#### **6.1 Test Suite Completo**
```bash
# Ejecutar todos los tests incluyendo Docker integration
uv run pytest tests/ -v
uv run pytest tests/integration/ -v --docker-required --mcp-required
uv run pytest tests/performance/ -v --slow
```

#### **6.2 Verificación Funcional End-to-End**
```python
# End-to-end test con Docker Hub MCP
async def test_full_workflow():
    # 1. Initialize MultiGraphitiManager
    manager = MultiGraphitiManager.from_config("config/multi_graphiti_config.yaml")
    
    # 2. Verify Docker containers
    health_status = await manager.verify_docker_containers()
    assert all(status.healthy for status in health_status.values())
    
    # 3. Initialize Graphiti instances
    await manager.initialize_instances()
    
    # 4. Test parallel episode addition
    episode = "Test episode for multi-instance evaluation"
    results = await manager.add_episode_to_all(episode)
    assert len(results) == len(manager.instances)
    
    # 5. Test cross-instance search
    search_results = await manager.search_across_instances("test")
    assert len(search_results) == len(manager.instances)
    
    # 6. Test auto-recovery (simulate container failure)
    await manager.docker_manager.restart_container("pproc")
    recovery_status = await manager.auto_recovery_check()
    assert recovery_status.all_healthy
    
    # 7. Get comprehensive stats
    stats = await manager.get_instance_stats()
    assert stats.docker_health.all_containers_healthy
```

---

## 🗂️ ESTRUCTURA DE ARCHIVOS RESULTANTE v2.0

```
graphiti_core/
├── managers/
│   ├── __init__.py
│   ├── multi_graphiti_manager.py          # Clase principal v2.0
│   ├── docker_manager.py                  # 🆕 Gestión Docker con MCP
│   ├── health_monitor.py                  # 🆕 Monitoreo salud continuo
│   ├── config.py                          # Configuración extendida
│   └── instance_factory.py                # Factory de instancias

config/
├── multi_graphiti_config.yaml             # Configuración principal
├── docker_architecture.yaml               # 🆕 Arquitectura Docker
└── multi_graphiti_config.example.yaml     # Ejemplo configuración

tests/
├── managers/
│   ├── test_multi_graphiti_manager.py     # Tests unitarios v2.0
│   ├── test_docker_manager.py             # 🆕 Tests Docker Manager
│   ├── test_health_monitor.py             # 🆕 Tests Health Monitor
│   ├── test_config.py                     # Tests configuración
│   └── test_instance_factory.py           # Tests factory
├── integration/
│   ├── test_docker_mcp_integration.py     # 🆕 Tests MCP Docker Hub
│   ├── test_multi_instance_workflows.py   # Tests workflows
│   └── test_auto_recovery.py              # 🆕 Tests auto-recovery
└── performance/
    ├── test_multi_instance_performance.py # Tests performance
    └── test_docker_overhead.py            # 🆕 Tests overhead Docker

examples/
├── basic_multi_graphiti_usage.py          # Uso básico
├── docker_integration_example.py          # 🆕 Ejemplo Docker
├── auto_recovery_demo.py                  # 🆕 Demo auto-recovery
├── health_monitoring_setup.py             # 🆕 Setup monitoreo
└── evaluation_with_multi_manager.py       # Evaluación multi-engine

docs/
├── MULTI_GRAPHITI_MANAGER_README.md       # Documentación técnica v2.0
├── DOCKER_INTEGRATION_GUIDE.md            # 🆕 Guía integración Docker
└── MULTI_GRAPHITI_ARCHITECTURE.md         # Documentación arquitectura
```

---

## ⚠️ RIESGOS Y MITIGACIONES v2.0

### **Riesgos Identificados**
1. **Docker Hub MCP dependency**: Fallos en MCP afectan gestión contenedores
2. **Container management complexity**: Mayor superficie de error
3. **Performance overhead**: Docker operations pueden ser lentas
4. **Network dependencies**: Múltiples layers de conectividad

### **Mitigaciones**
1. **Fallback mechanisms**: Comandos Docker directos como backup
2. **Robust error handling**: Manejo granular de errores Docker
3. **Async operations**: Operaciones Docker no-bloqueantes
4. **Connection pooling**: Reutilización de conexiones MCP

---

## ✅ CRITERIOS DE ACEPTACIÓN v2.0

### **Funcionales**
- ✅ Manager inicializa múltiples instancias Graphiti
- ✅ Auto-recovery de contenedores fallidos
- ✅ Health monitoring continuo via Docker Hub MCP
- ✅ Operaciones paralelas en todas las instancias
- ✅ Logs centralizados y debugging robusto
- 🆕 **Gestión Docker containers via MCP**
- 🆕 **Auto-restart de contenedores Neo4j**
- 🆕 **Monitoring health tiempo real**

### **No Funcionales**
- ✅ Performance: operaciones paralelas >50% más rápidas
- ✅ Reliability: 99% success rate + auto-recovery
- ✅ Usability: API intuitiva Docker-aware
- ✅ Maintainability: >90% test coverage
- 🆕 **Docker reliability: auto-recovery <30 segundos**
- 🆕 **MCP integration: <5 segundos response time**

### **Técnicos**
- ✅ Zero breaking changes en Graphiti existente
- ✅ Compatible con configuración Docker actual
- ✅ Extensible para nuevas instancias
- 🆕 **Docker Hub MCP integration seamless**
- 🆕 **Backward compatibility con versión 1.0**

---

## 🚀 PRÓXIMOS PASOS POST-IMPLEMENTACIÓN v2.0

1. **Integración Evaluación**: Usar MultiGraphitiManager v2.0 en evaluación multi-engine
2. **MCP Orchestration**: Extender MCP integration para orquestación completa
3. **Auto-scaling**: Creación dinámica de instancias Docker
4. **Monitoring Dashboard**: Dashboard web para monitoreo en tiempo real
5. **Performance Optimization**: Optimización específica Docker operations

---

## 🎯 MEJORAS ESPECÍFICAS v2.0

### **Docker Hub MCP Integration**
- Gestión robusta de contenedores via APIs oficiales
- Health checks automáticos y recovery
- Logs centralizados para debugging
- Monitoreo continuo de estado

### **Auto-Recovery System**
- Detección automática de fallos de contenedor
- Restart inteligente con backoff exponencial
- Notificaciones de recovery events
- Preservación de estado durante recovery

### **Enhanced Configuration**
- Configuración Docker-aware
- Extracción automática desde Claude Desktop config
- Validación de conectividad pre-initialization
- Support para múltiples environments

---

## 📝 CHECKPOINT DE APROBACIÓN v2.0

**Antes de proceder, confirmar:**
- [ ] Plan v2.0 con Docker Hub MCP aprobado
- [ ] Estructura de archivos extendida aceptada  
- [ ] Criterios de aceptación v2.0 claros
- [ ] Riesgos Docker identificados y mitigados
- [ ] Timeline estimado actualizado (3.5 horas total)
- [ ] Docker Hub MCP integration requirements claros

**¿Proceder con la implementación v2.0?** ⚡🐳