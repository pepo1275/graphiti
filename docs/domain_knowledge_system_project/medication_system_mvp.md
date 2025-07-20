# Sistema de Conocimiento Vivo - Administración de Medicamentos con Graphiti

## 🚀 Breakthrough: Arquitectura Optimizada con Graphiti

### **Ventaja Competitiva Clave**
- ✅ **Graphiti ya implementado** en equipos de escritorio
- ✅ **MCP Server funcionando**: https://github.com/getzep/graphiti/tree/main/mcp_server
- ✅ **Memoria episódica especializada** de clase mundial
- ✅ **P95 latency 300ms** - rendimiento excepcional
- ✅ **Temporal awareness nativa** - bi-temporal architecture

---

## 🏗️ Nueva Arquitectura Dual Optimizada

### **Separación de Responsabilidades Perfecta**

```
┌─────────────────────────────────────────────────────────┐
│                    CLAUDE DESKTOP                       │
├─────────────────────────────────────────────────────────┤
│                 Dual MCP Architecture                   │
├─────────────────────┬───────────────────────────────────┤
│   MCP SERVER 1      │        MCP SERVER 2              │
│   (Graphiti)        │        (AEMPS Custom)            │
│   ✅ YA FUNCIONA    │        🔧 A DESARROLLAR          │
└─────────────────────┴───────────────────────────────────┘
         │                           │
         ▼                           ▼
┌─────────────────────┐    ┌─────────────────────────────┐
│    MEMORIA          │    │     CONOCIMIENTO            │
│    EPISÓDICA        │    │     DE DOMINIO              │
│                     │    │                             │
│   🧠 Graphiti       │    │   📚 Neo4j AEMPS           │
│   - Episodios       │    │   - 1300 medicamentos      │
│   - Aprendizaje     │    │   - Interacciones           │
│   - Temporal        │    │   - Protocolos              │
│   - Auto-Entity     │    │   - Validaciones            │
└─────────────────────┘    └─────────────────────────────┘
```

### **Flujo de Datos Optimizado**

#### **1. Consulta Enfermera**
```
Enfermera: "¿Dosis omeprazol IV paciente 70kg insuficiencia renal?"
    ↓
Claude Desktop (con ambos MCP activos)
    ↓
MedGemma: Interpretación médica + routing inteligente
```

#### **2. Búsqueda Dual Paralela**
```
┌─ Graphiti MCP ────────────────┐    ┌─ AEMPS MCP ──────────────────┐
│ Buscar episodios similares:   │    │ Consultar knowledge oficial: │
│ - "omeprazol + renal"         │    │ - Medicamento: OMEPRAZOL     │
│ - Casos previos UCI           │    │ - Ajustes renales            │
│ - Validaciones registradas    │    │ - Contraindicaciones         │
│ - P95 latency: 300ms          │    │ - Dosis terapéuticas         │
└───────────────────────────────┘    └──────────────────────────────┘
```

#### **3. Síntesis y Validación**
```
MedGemma: Combinar conocimiento formal + experiencia episódica
Claude Sonnet: Generar código Cypher si necesario
Validaciones automáticas: Seguridad médica
Respuesta final: Contextualizada y validada
```

#### **4. Registro Automático en Graphiti**
```
Episodio completo → Graphiti (automático via MCP)
- Consulta original
- Proceso de pensamiento
- Código generado
- Resultado final
- Validación médica
- Timestamp bi-temporal
```

---

## 🎯 Beneficios Inmediatos de usar Graphiti

### **✅ Eliminación de Desarrollo Complejo**
- **No necesitamos construir** sistema episódico desde cero
- **No necesitamos diseñar** esquema temporal complejo
- **No necesitamos optimizar** retrieval episódico
- **No necesitamos implementar** MCP server para episodios

### **✅ Capacidades Avanzadas Inmediatas**
- **Bi-temporal model**: Tracking explícito de cuándo ocurrió evento y cuándo se ingirió
- **Real-time incremental updates**: Integración inmediata de nuevos episodios sin recomputación batch
- **Efficient hybrid retrieval**: Combina semantic embeddings, keyword (BM25), y graph traversal
- **Custom entity definitions**: Ontología flexible usando Pydantic models

### **✅ Performance de Clase Mundial**
- **P95 latency de 300ms**: Extremadamente bajo para retrieval
- **Hybrid indexing**: Vector + BM25 indexes para acceso near-constant time
- **Reducción tokens**: Utiliza menos del 2% de tokens vs baseline
- **Latency reduction**: Order of magnitude mejor que contexto completo

### **✅ Validación Científica**
- **State-of-the-art**: Supera MemGPT en Deep Memory Retrieval benchmark (94.8% vs 93.4%)
- **Research-backed**: Paper publicado con evaluaciones comprehensivas
- **Community adoption**: 14,000 GitHub stars, 25,000 weekly PyPI downloads

---

## 📊 Arquitectura Técnica Específica

### **Stack Tecnológico Redefinido**

#### **Memoria Episódica (Graphiti - YA FUNCIONA)**
```python
# Entidades Médicas Personalizadas (Pydantic)
class ConsultaEnfermera(Entity):
    pregunta: str
    unidad: str = Field(description="UCI, Planta, Urgencias")
    experiencia: str = Field(description="Años experiencia enfermera")
    
class EpisodioMedico(Entity):
    medicamento: str
    dosis_calculada: str
    validacion_farmaceutica: bool
    resultado_satisfactorio: bool
    
class PatronEmergente(Entity):
    situacion_clinica: str
    procedimiento_exitoso: str
    aplicabilidad: List[str]
```

#### **Conocimiento Dominio (Neo4j AEMPS - A DESARROLLAR)**
```cypher
// Esquema optimizado para complementar Graphiti
(:Medicamento)-[:CONTIENE]->(:PrincipioActivo)
(:Medicamento)-[:VIA]->(:Administracion)
(:Medicamento)-[:DOSIS_RANGO]->(:RangoDosis)
(:Medicamento)-[:AJUSTE_RENAL]->(:AjusteRenal)
(:Medicamento)-[:INTERACTUA]->(:Medicamento)
(:Medicamento)-[:CONTRAINDICADO]->(:Condicion)
```

### **Dual MCP Configuration**

#### **MCP Server 1: Graphiti (FUNCIONANDO)**
```json
{
  "name": "graphiti",
  "command": "python",
  "args": ["-m", "graphiti.mcp_server"],
  "env": {
    "NEO4J_URI": "bolt://localhost:7687",
    "NEO4J_USER": "neo4j",
    "NEO4J_PASSWORD": "password"
  }
}
```

#### **MCP Server 2: AEMPS Custom (A DESARROLLAR)**
```json
{
  "name": "aemps_medicamentos", 
  "command": "python",
  "args": ["-m", "aemps_mcp.server"],
  "env": {
    "NEO4J_URI": "bolt://localhost:7688",
    "AEMPS_DB": "medicamentos"
  }
}
```

---

## 🔄 Flujo Detallado de Funcionamiento

### **Caso Real: Consulta Compleja**
```
Enfermera UCI: "Paciente 80kg, clearance creatinina 45, necesito 
                omeprazol IV pero ya tiene digoxina. ¿Es seguro?"
```

#### **1. Routing Inteligente (MedGemma)**
```python
interpretacion = {
    "medicamentos": ["omeprazol", "digoxina"],
    "factores": ["insuficiencia_renal", "interaccion_potencial"],
    "queries_necesarias": {
        "graphiti": "casos_similares_omeprazol_digoxina_renal",
        "aemps": "interacciones_omeprazol_digoxina + ajuste_renal"
    }
}
```

#### **2. Graphiti Query (Automática)**
```python
# Graphiti MCP automáticamente busca:
episodios_similares = graphiti.search(
    "omeprazol digoxina insuficiencia renal UCI",
    entity_types=["ConsultaEnfermera", "EpisodioMedico", "PatronEmergente"]
)

# Resultado ejemplo:
{
    "episodios_relevantes": [
        {
            "episodio": "EPI_2024_341",
            "contexto": "UCI, clearance_45, omeprazol+digoxina",
            "resultado": "Administrado con monitorización, sin incidencias",
            "validado_por": "Dr_Martinez_Farmacia",
            "patron": "omeprazol_no_afecta_digoxina_significativamente"
        }
    ],
    "confidence": 0.94,
    "temporal_relevance": "reciente_<30_dias"
}
```

#### **3. AEMPS Query (Custom MCP)**
```cypher
// Consulta automática generada
MATCH (o:Medicamento {nombre_activo:'OMEPRAZOL'})
-[:INTERACTUA]-(d:Medicamento {nombre_activo:'DIGOXINA'})
MATCH (o)-[:AJUSTE_RENAL]->(ar:AjusteRenal)
WHERE ar.clearance_min <= 45 <= ar.clearance_max
RETURN o.dosis_ajustada, ar.protocolo, 
       interaction.severidad, interaction.recomendacion
```

#### **4. Síntesis Final (MedGemma + Claude)**
```
Respuesta integrada:
- Conocimiento AEMPS: "Interacción leve, monitorización recomendada"
- Experiencia Graphiti: "Caso similar UCI exitoso hace 2 semanas"
- Dosis ajustada: "20mg cada 24h (reducción 50% por clearance 45)"
- Validación: "Seguro con monitorización niveles digoxina"
- Evidencia: "Protocolo AEMPS + experiencia validada Dr. Martinez"
```

#### **5. Auto-registro en Graphiti**
```python
# Automático via MCP - sin código adicional
nuevo_episodio = {
    "timestamp_ocurrencia": "2025-07-20T14:30:00Z",
    "timestamp_ingestion": "2025-07-20T14:30:15Z", 
    "entities": [
        ConsultaEnfermera(
            pregunta="omeprazol IV + digoxina clearance 45",
            unidad="UCI",
            experiencia="5_años"
        ),
        EpisodioMedico(
            medicamento="omeprazol",
            dosis_calculada="20mg/24h",
            validacion_farmaceutica=True,
            resultado_satisfactorio=True
        )
    ],
    "relationships": [
        ("ConsultaEnfermera", "GENERO", "EpisodioMedico"),
        ("EpisodioMedico", "CONFIRMA", "PatronEmergente:omeprazol_digoxina_seguro")
    ]
}
```

---

## 📋 Desarrollo Simplificado - Nuevo Cronograma

### **🎯 Focus: Solo Desarrollar AEMPS MCP Server**

#### **Sprint 1 (1 semana): Setup AEMPS**
- ✅ Descarga y parseo XML nomenclátor
- ✅ Diseño esquema Neo4j medicamentos  
- ✅ Ingesta 1300 medicamentos inyectables
- ✅ Validación datos AEMPS

#### **Sprint 2 (1 semana): AEMPS MCP Server**
- ✅ MCP server custom para medicamentos
- ✅ Queries Cypher optimizadas (dosis, interacciones, ajustes)
- ✅ Validaciones automáticas básicas
- ✅ Testing con Graphiti MCP (dual server)

#### **Sprint 3 (1 semana): Integración y Testing**
- ✅ Configuración dual MCP en Claude Desktop
- ✅ Routing inteligente entre ambos servidores
- ✅ Testing casos reales con enfermeras
- ✅ Validación médica pipeline

#### **Sprint 4 (1 semana): Optimización**
- ✅ Performance tuning
- ✅ Casos de uso complejos
- ✅ Documentación y deployment
- ✅ Métricas y monitoring

### **Total: 4 semanas vs 8 semanas originales**
**🚀 Reducción 50% tiempo desarrollo gracias a Graphiti**

---

## 🎯 Entidades Médicas Personalizadas para Graphiti

### **Definiciones Pydantic Específicas**

```python
from graphiti import Entity, Relation
from typing import List, Optional
from datetime import datetime

class EnfermeraProfile(Entity):
    """Perfil de la enfermera que consulta"""
    nombre: str = Field(description="Nombre o ID anonimizado")
    unidad: str = Field(description="UCI, Planta, Urgencias, Quirofano")
    experiencia_años: int = Field(description="Años de experiencia")
    especialidad: Optional[str] = Field(description="Cardiología, Neurología, etc")
    turno_habitual: str = Field(description="Mañana, Tarde, Noche")

class ConsultaMedicamento(Entity):
    """Consulta específica sobre medicamento"""
    pregunta_original: str = Field(description="Pregunta exacta de la enfermera")
    medicamento_principal: str = Field(description="Medicamento principal consultado")
    via_administracion: str = Field(description="IV, IM, SC, Oral")
    contexto_clinico: str = Field(description="Contexto del paciente")
    urgencia_nivel: str = Field(description="Baja, Media, Alta, Crítica")
    
class PacienteContexto(Entity):
    """Contexto anónimo del paciente"""
    peso_kg: Optional[float] = Field(description="Peso en kilogramos")
    edad_años: Optional[int] = Field(description="Edad en años")
    funcion_renal: Optional[str] = Field(description="Normal, Leve, Moderada, Severa")
    funcion_hepatica: Optional[str] = Field(description="Normal, Alterada")
    patologias_principales: List[str] = Field(description="Diabetes, HTA, etc")
    medicamentos_actuales: List[str] = Field(description="Medicación concomitante")

class EpisodioResolucion(Entity):
    """Resolución del episodio médico"""
    respuesta_final: str = Field(description="Respuesta completa dada")
    dosis_recomendada: Optional[str] = Field(description="Dosis específica")
    frecuencia: Optional[str] = Field(description="Cada 8h, 12h, 24h")
    duracion_tratamiento: Optional[str] = Field(description="3 días, 7 días, etc")
    precauciones: List[str] = Field(description="Monitorizaciones necesarias")
    fuente_evidencia: str = Field(description="AEMPS, Protocolo UCI, Experiencia")
    
class ValidacionMedica(Entity):
    """Validación por personal médico"""
    validado_por: str = Field(description="Dr/Dra nombre o rol")
    especialidad_validador: str = Field(description="Farmacéutico, Intensivista, etc")
    resultado_validacion: str = Field(description="Aprobada, Modificada, Rechazada")
    comentarios: Optional[str] = Field(description="Observaciones del validador")
    timestamp_validacion: datetime = Field(description="Momento de validación")

class PatronEmergente(Entity):
    """Patrón aprendido del episodio"""
    tipo_patron: str = Field(description="Interacción, Dosis, Procedimiento")
    situacion_aplicable: str = Field(description="Cuándo aplicar este patrón")
    procedimiento_recomendado: str = Field(description="Qué hacer en esta situación")
    evidencia_acumulada: int = Field(description="Número de casos que confirman")
    confianza_patron: float = Field(description="0.0 a 1.0 confianza")
    dominios_aplicacion: List[str] = Field(description="UCI, Planta, Urgencias")

class CodigoGenerado(Entity):
    """Código Cypher/Python generado en el episodio"""
    tipo_codigo: str = Field(description="Cypher, Python, Validación")
    codigo_completo: str = Field(description="Código fuente completo")
    proposito: str = Field(description="Para qué se generó este código")
    exitoso: bool = Field(description="Si el código funcionó correctamente")
    error_mensaje: Optional[str] = Field(description="Error si falló")
    tiempo_ejecucion_ms: Optional[float] = Field(description="Tiempo de ejecución")

# Relaciones específicas del dominio médico
class ConsultoSobre(Relation):
    """Enfermera consultó sobre medicamento"""
    source: EnfermeraProfile
    target: ConsultaMedicamento
    timestamp: datetime
    contexto_consulta: str

class AplicadoEn(Relation):
    """Medicamento aplicado en contexto paciente"""
    source: ConsultaMedicamento  
    target: PacienteContexto
    riesgo_estimado: str = Field(description="Bajo, Medio, Alto")

class ResolvioEn(Relation):
    """Consulta resuelta con esta resolución"""
    source: ConsultaMedicamento
    target: EpisodioResolucion
    satisfactorio: bool = Field(description="Si resolvió la consulta")
    tiempo_resolucion_minutos: int

class ValidadoPor(Relation):
    """Episodio validado por médico"""
    source: EpisodioResolucion
    target: ValidacionMedica
    nivel_confianza: float = Field(description="0.0 a 1.0")

class GeneroPatron(Relation):
    """Episodio generó patrón aprendible"""
    source: EpisodioResolucion
    target: PatronEmergente
    fuerza_evidencia: float = Field(description="Qué tan fuerte es la evidencia")

class EjecutoScript(Relation):
    """Resolución ejecutó código específico"""
    source: EpisodioResolucion
    target: CodigoGenerado
    resultado_exitoso: bool
```

---

## 🔍 Casos de Uso Avanzados con Graphiti

### **Aprendizaje Temporal Automático**

#### **Ejemplo: Patrón Emergente Detectado**
```python
# Graphiti automáticamente identifica tras múltiples episodios:
patron_detectado = PatronEmergente(
    tipo_patron="ajuste_renal_omeprazol",
    situacion_aplicable="clearance_creatinina_30_60_ml_min",
    procedimiento_recomendado="reducir_dosis_50_porciento_monitorizar_24h",
    evidencia_acumulada=15,  # 15 casos similares exitosos
    confianza_patron=0.94,
    dominios_aplicacion=["UCI", "Planta_Medicina", "Urgencias"]
)

# Relaciones automáticas con episodios que lo generaron
episodios_relacionados = [
    "EPI_2024_341", "EPI_2024_389", "EPI_2024_445", ...
]
```

#### **Query Temporal Sofisticada**
```python
# Graphiti permite consultas como:
"¿Qué patrones de dosis hemos aprendido para omeprazol en insuficiencia 
 renal en los últimos 3 meses en UCI, validados por farmacéuticos?"

# Graphiti automáticamente:
# 1. Identifica entidades: omeprazol, insuficiencia_renal, UCI, farmacéuticos
# 2. Aplica filtros temporales: últimos 3 meses
# 3. Busca patrones con validación médica
# 4. Retorna evidencia consolidada con referencias
```

---

## 📊 Métricas Avanzadas con Graphiti

### **KPIs Automáticos de Aprendizaje**

#### **Métricas de Memoria Episódica**
- **Episodios acumulados**: Total registrados por dominio
- **Patrones emergentes**: Nuevos patrones detectados/semana
- **Validación médica**: % episodios validados por especialistas
- **Reutilización conocimiento**: % consultas que usan episodios previos
- **Temporal decay**: Relevancia episodios por antiguedad

#### **Métricas de Performance Graphiti**
- **Retrieval latency**: P95 < 300ms (target Graphiti)
- **Entity resolution**: Precisión identificación entidades médicas
- **Temporal accuracy**: Correctness consultas point-in-time
- **Graph growth**: Nodos/relaciones nuevos por episodio
- **Memory efficiency**: Compresión vs pérdida información

#### **Métricas Clínicas Específicas**
```python
# Consultas automáticas Graphiti para métricas:

# 1. Evolución patrones por unidad
query = """
¿Cómo han evolucionado los patrones de medicación en UCI 
en los últimos 6 meses comparado con Planta?
"""

# 2. Validación expertos por especialidad  
query = """
¿Qué porcentaje de episodios de cardiología fueron 
validados por cardiólogos vs farmacéuticos?
"""

# 3. Detección anomalías temporales
query = """
¿Hay episodios con patrones de medicación significativamente 
diferentes al histórico en las últimas 2 semanas?
"""
```

---

## 🚀 Próximos Pasos Inmediatos Optimizados

### **Sprint 1 Específico - Esta Semana**

#### **1. Validación Graphiti + AEMPS Compatibility**
```python
# Test que Graphiti puede manejar entidades médicas
from graphiti import Graphiti

# Setup entidades médicas personalizadas
graphiti_client = Graphiti()
graphiti_client.register_entities([
    EnfermeraProfile, ConsultaMedicamento, PacienteContexto,
    EpisodioResolucion, ValidacionMedica, PatronEmergente
])

# Test episodio médico básico
test_episode = """
Enfermera UCI consulta dosis omeprazol IV para paciente 70kg 
con insuficiencia renal moderada. Resuelto con 20mg/24h, 
validado por Dr. Martinez.
"""

# Verificar que Graphiti extrae entidades médicas correctamente
extracted = graphiti_client.process_episode(test_episode)
```

#### **2. Análisis Detallado AEMPS Data**
```python
# Parsear XML nomenclátor
import xml.etree.ElementTree as ET

def parse_aemps_nomenclator(xml_file):
    medicamentos_inyectables = []
    tree = ET.parse(xml_file)
    
    for medicamento in tree.findall('.//medicamento'):
        if 'inyectable' in medicamento.find('forma_farmaceutica').text.lower():
            medicamentos_inyectables.append({
                'codigo': medicamento.find('codigo_nacional').text,
                'nombre': medicamento.find('nombre').text,
                'principio_activo': medicamento.find('principio_activo').text,
                'via': medicamento.find('via_administracion').text,
                'laboratorio': medicamento.find('laboratorio').text
            })
    
    return medicamentos_inyectables

# Identificar estructura exacta para Neo4j schema
medicamentos = parse_aemps_nomenclator('nomenclator_actual.xml')
print(f"Total medicamentos inyectables: {len(medicamentos)}")
```

#### **3. Setup Dual MCP Configuration**
```json
// claude_desktop_config.json
{
  "mcpServers": {
    "graphiti": {
      "command": "python",
      "args": ["-m", "graphiti.mcp_server"],
      "env": {
        "NEO4J_URI": "bolt://localhost:7687",
        "NEO4J_USER": "neo4j", 
        "NEO4J_PASSWORD": "password"
      }
    },
    "aemps_medicamentos": {
      "command": "python",
      "args": ["-m", "aemps_mcp.server"],
      "env": {
        "NEO4J_URI": "bolt://localhost:7688",
        "AEMPS_DB": "medicamentos"
      }
    }
  }
}
```

---

## 🎯 Conclusión: Arquitectura Óptima Validada

### **Ventajas Transformacionales**

#### **✅ Desarrollo Acelerado**
- **50% reducción tiempo**: 4 semanas vs 8 semanas originales
- **Focus especializado**: Solo AEMPS MCP server necesario
- **Risk mitigation**: Graphiti ya probado y funcionando
- **Quality assurance**: State-of-the-art memory system incluido

#### **✅ Capacidades Superiores**
- **Temporal intelligence**: Bi-temporal tracking automático
- **Real-time learning**: Episodios ingestion sin batch processing
- **Hybrid retrieval**: Vector + BM25 + graph traversal integrado  
- **Custom entities**: Ontología médica específica con Pydantic

#### **✅ Performance Garantizada**
- **P95 latency 300ms**: Graphiti benchmark demostrado
- **Scalability proven**: 14K GitHub stars, 25K weekly downloads
- **Research validated**: State-of-the-art paper publicado
- **Enterprise ready**: Production deployments exitosos

### **🚀 Próximo Milestone**

**Objetivo Sprint 1**: Dual MCP funcionando con:
1. **Graphiti MCP**: Memoria episódica activa
2. **AEMPS MCP**: Conocimiento medicamentos básico  
3. **Test end-to-end**: Consulta real enfermera → dual retrieval → respuesta integrada
4. **Validación médica**: Pipeline básico funcionando

**Success metric**: Consulta "¿dosis omeprazol IV 70kg?" → respuesta integrada AEMPS + episodios Graphiti en <2 segundos.

---

*Arquitectura optimizada con Graphiti - Ready for accelerated development*