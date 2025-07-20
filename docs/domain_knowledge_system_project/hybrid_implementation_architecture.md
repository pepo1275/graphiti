# Implementación Híbrida: Sistema Medicamentos con Web UX + Sequential Thinking

## 📋 Contexto de Artefactos Relacionados

**IMPORTANTE**: Este artefacto se basa en decisiones previas documentadas en:
- `knowledge_system_context`: Visión general del sistema de conocimiento vivo co-creativo
- `medication_system_mvp`: Arquitectura optimizada con Graphiti para medicamentos

## 🎯 Decisión Arquitectural Final: Mix Inteligente

### **Arquitectura Híbrida Seleccionada**
- **Frontend**: Interface web limpia y transparente para enfermeras
- **Backend**: Sequential thinking sofisticado con Claude API + MCP orchestration
- **Development**: Evolución natural desde Claude Code → Web Interface
- **UX**: Proceso complejo oculto, experiencia simple y clara

---

## 🏗️ Arquitectura Técnica Híbrida

### **Stack Tecnológico Completo**

```
┌─────────────────────────────────────────────────────┐
│                 FRONTEND WEB                        │
│              React/Vue + FastAPI                    │
│            (UX Transparente)                        │
├─────────────────────────────────────────────────────┤
│                ORQUESTADOR HÍBRIDO                  │
│         TransparentMedicationSystem                 │
│        (Sequential Thinking + MCP)                  │
├─────────────────┬───────────────────────────────────┤
│   Sequential    │        MCP Orchestration          │
│   Thinking      │                                   │
│   (Claude API)  │   ┌─ Graphiti ─┐ ┌─ AEMPS ─┐     │
│                 │   │ Episodes   │ │ Neo4j   │     │
│   ┌─ Analysis ─┐│   │ Memory     │ │ Drugs   │     │
│   ├─ Strategy ─┤│   └────────────┘ └─────────┘     │
│   ├─ Synthesis─┤│                                   │
│   └─ Validation│└───────────────────────────────────┤
├─────────────────┴───────────────────────────────────┤
│              AI Models Integration                  │
│   ┌─ MedGemma ─┐  ┌─ BGE-M3 ─┐  ┌─ Claude ─┐      │
│   │ Medical    │  │ Embeddings│  │ Sonnet  │      │
│   │ Analysis   │  │ Semantic  │  │ Thinking│      │
│   └────────────┘  └───────────┘  └─────────┘      │
└─────────────────────────────────────────────────────┘
```

### **Separación de Responsabilidades**

#### **Frontend (React/Vue)**
- Interface limpia para enfermeras
- Contexto clínico rápido (unidad, turno, experiencia)
- Loading states elegantes
- Respuestas integradas y accionables

#### **Backend Orquestador (FastAPI)**
- Sequential thinking proceso interno
- Orchestración MCP transparente
- Síntesis inteligente de múltiples fuentes
- Auto-registro episódico

#### **MCP Layer**
- **Graphiti**: Memoria episódica (YA FUNCIONA)
- **AEMPS Custom**: Conocimiento medicamentos (A DESARROLLAR)

#### **AI Models**
- **MedGemma**: Interpretación médica contextual
- **BGE-M3**: Embeddings semánticos unificados
- **Claude Sonnet**: Sequential thinking + síntesis

---

## 🔄 Flujo de Funcionamiento Detallado

### **Perspectiva UX - Enfermera**

#### **1. Interface de Consulta**
```html
<div class="sistema-medicamentos">
    <!-- Contexto rápido -->
    <div class="contexto-clinico">
        <div class="badge-group">
            <span class="badge unidad">UCI</span>
            <span class="badge turno">Noche</span>
            <span class="badge enfermera">Carmen M. (5 años)</span>
        </div>
        <button class="config-contexto">⚙️ Configurar</button>
    </div>
    
    <!-- Consulta principal -->
    <div class="consulta-container">
        <label>Consulta médica:</label>
        <textarea 
            placeholder="Ej: ¿Dosis omeprazol IV paciente 70kg con insuficiencia renal?"
            class="consulta-input"
            rows="3">
        </textarea>
        
        <!-- Contexto paciente rápido -->
        <div class="paciente-rapido">
            <input type="text" placeholder="Peso (kg)" class="peso-input">
            <select class="funcion-renal">
                <option>Función renal normal</option>
                <option>Insuficiencia leve</option>
                <option>Insuficiencia moderada</option>
                <option>Insuficiencia severa</option>
            </select>
            <input type="text" placeholder="Medicamentos actuales" class="medicamentos-actuales">
        </div>
        
        <button class="btn-consultar" onclick="procesarConsulta()">
            Consultar Sistema
        </button>
    </div>
</div>
```

#### **2. Loading States (Mientras Sequential Thinking trabaja)**
```html
<div class="loading-processo">
    <div class="step active">
        <span class="icon">🔍</span>
        <span class="text">Analizando consulta médica...</span>
        <span class="tiempo">0.5s</span>
    </div>
    <div class="step active">
        <span class="icon">📚</span>
        <span class="text">Consultando protocolos AEMPS...</span>
        <span class="tiempo">1.2s</span>
    </div>
    <div class="step active">
        <span class="icon">🧠</span>
        <span class="text">Revisando casos similares...</span>
        <span class="tiempo">0.8s</span>
    </div>
    <div class="step current">
        <span class="icon">⚡</span>
        <span class="text">Sintetizando respuesta...</span>
        <span class="spinner"></span>
    </div>
</div>
```

#### **3. Respuesta Integrada**
```html
<div class="respuesta-completa">
    <!-- Header con medicamento -->
    <div class="medicamento-header">
        <h3>💊 Omeprazol IV</h3>
        <span class="categoria">Inhibidor bomba protones</span>
        <span class="urgencia media">Urgencia: Media</span>
    </div>
    
    <!-- Recomendación principal -->
    <div class="recomendacion-principal">
        <div class="dosis-container">
            <span class="label">Dosis recomendada:</span>
            <span class="dosis-valor">20mg IV cada 24 horas</span>
            <span class="ajuste">(Reducción 50% por función renal)</span>
        </div>
        
        <div class="via-administracion">
            <span class="label">Vía:</span>
            <span class="via">Intravenosa lenta (2-5 minutos)</span>
        </div>
        
        <div class="duracion">
            <span class="label">Duración:</span>
            <span class="tiempo">Según evolución clínica</span>
        </div>
    </div>
    
    <!-- Precauciones y monitorización -->
    <div class="precauciones">
        <h4>⚠️ Precauciones importantes:</h4>
        <ul>
            <li>Monitorizar función renal cada 48h</li>
            <li>Verificar niveles creatinina antes de siguiente dosis</li>
            <li>Evaluar respuesta clínica a las 72h</li>
            <li>Vigilar signos de toxicidad gastrointestinal</li>
        </ul>
    </div>
    
    <!-- Fuentes de evidencia -->
    <div class="evidencia-sources">
        <h4>📋 Fuentes de evidencia:</h4>
        <div class="source oficial">
            <span class="tipo">Oficial</span>
            <span class="detalle">AEMPS - Ficha técnica omeprazol</span>
            <span class="confianza">Confianza: 100%</span>
        </div>
        <div class="source experiencial">
            <span class="tipo">Experiencial</span>
            <span class="detalle">3 casos similares UCI (últimos 2 meses)</span>
            <span class="confianza">Confianza: 94%</span>
        </div>
        <div class="source validacion">
            <span class="tipo">Validación</span>
            <span class="detalle">Dr. Martinez - Farmacia Clínica</span>
            <span class="confianza">Validado ✅</span>
        </div>
    </div>
    
    <!-- Casos similares (expandible) -->
    <div class="casos-similares collapsible">
        <button class="toggle-casos">
            📊 Ver casos similares (3) ▼
        </button>
        <div class="casos-content hidden">
            <div class="caso">
                <span class="fecha">15/07/2025</span>
                <span class="contexto">Paciente 75kg, clearance 45ml/min</span>
                <span class="resultado">✅ Exitoso - Sin complicaciones</span>
            </div>
            <div class="caso">
                <span class="fecha">28/06/2025</span>
                <span class="contexto">Paciente 68kg, insuf. moderada</span>
                <span class="resultado">✅ Exitoso - Buena tolerancia</span>
            </div>
        </div>
    </div>
    
    <!-- Acciones disponibles -->
    <div class="acciones-enfermera">
        <button class="btn primary" onclick="aplicarProtocolo()">
            ✅ Aplicar protocolo
        </button>
        <button class="btn secondary" onclick="consultarDudas()">
            ❓ Tengo dudas adicionales
        </button>
        <button class="btn tertiary" onclick="marcarUtil()">
            👍 Marcar como útil
        </button>
        <button class="btn danger" onclick="reportarProblema()">
            🚨 Reportar problema
        </button>
    </div>
</div>
```

---

## 💻 Implementación Backend - Sequential Thinking

### **Core Orchestrator Class**

```python
from typing import Dict, List, Optional, Union
import asyncio
from datetime import datetime
from dataclasses import dataclass
from enum import Enum

from anthropic import Anthropic
from mcp_client import MCPClient
from medgemma_client import MedGemmaClient
from bge_embeddings import BGEModel

@dataclass
class MedicalQuery:
    """Estructura de consulta médica"""
    query: str
    context: Dict
    patient_context: Optional[Dict] = None
    urgency_level: str = "media"
    timestamp: datetime = datetime.now()

@dataclass
class MedicalResponse:
    """Respuesta médica estructurada"""
    main_recommendation: str
    dosage: str
    administration_route: str
    precautions: List[str]
    evidence_sources: List[Dict]
    confidence_score: float
    similar_cases: List[Dict]
    validation_required: bool
    follow_up_actions: List[str]

class ThinkingStep(Enum):
    ANALYSIS = "analysis"
    STRATEGY = "strategy"
    EXECUTION = "execution"
    SYNTHESIS = "synthesis"
    VALIDATION = "validation"

class TransparentMedicationSystem:
    """
    Sistema híbrido que combina Sequential Thinking con MCP orchestration
    Proceso interno complejo, UX externa simple
    """
    
    def __init__(self):
        # AI Models
        self.claude = Anthropic()
        self.medgemma = MedGemmaClient()
        self.bge_model = BGEModel("BAAI/bge-m3")
        
        # MCP Clients
        self.graphiti_mcp = MCPClient("graphiti")
        self.aemps_mcp = MCPClient("aemps_medicamentos")
        
        # Internal state
        self.thinking_history = []
        self.current_session = None
        
    async def process_medical_consultation(
        self, 
        query: MedicalQuery
    ) -> MedicalResponse:
        """
        Proceso principal - Sequential thinking interno, respuesta limpia
        """
        
        # Initialize session
        session_id = self._create_session(query)
        
        try:
            # PHASE 1: Internal Analysis (Sequential Thinking)
            analysis_result = await self._sequential_thinking_analysis(query)
            
            # PHASE 2: Parallel MCP Queries (Based on thinking)
            aemps_data, graphiti_episodes = await self._parallel_knowledge_search(
                query, analysis_result
            )
            
            # PHASE 3: Intelligent Synthesis
            medical_response = await self._synthesize_medical_response(
                query, analysis_result, aemps_data, graphiti_episodes
            )
            
            # PHASE 4: Auto-registration (Background)
            asyncio.create_task(self._register_episode_background(
                query, analysis_result, medical_response
            ))
            
            return medical_response
            
        except Exception as e:
            # Error handling with graceful fallback
            return await self._handle_error_gracefully(query, e)
            
        finally:
            self._close_session(session_id)
    
    async def _sequential_thinking_analysis(
        self, 
        query: MedicalQuery
    ) -> Dict:
        """
        Sequential thinking process - interno, no visible al usuario
        """
        
        thinking_steps = {}
        
        # STEP 1: Medical Query Analysis
        analysis_prompt = f"""
        <thinking>
        Consulta médica de enfermería: "{query.query}"
        
        Contexto clínico:
        - Unidad: {query.context.get('unidad', 'No especificada')}
        - Experiencia enfermera: {query.context.get('experiencia', 'No especificada')}
        - Urgencia: {query.urgency_level}
        
        Contexto paciente:
        {query.patient_context if query.patient_context else 'No especificado'}
        
        ANÁLISIS REQUERIDO:
        1. ¿Qué medicamento específico se consulta?
        2. ¿Qué factores de ajuste son relevantes? (renal, hepático, edad, peso)
        3. ¿Qué riesgos de seguridad debo evaluar?
        4. ¿Qué información oficial (AEMPS) necesito?
        5. ¿Qué tipo de experiencia previa sería relevante?
        6. ¿Nivel de validación médica requerida?
        </thinking>
        
        Analiza esta consulta médica paso a paso, identificando todos los componentes críticos.
        """
        
        analysis_response = await self.claude.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1000,
            messages=[{"role": "user", "content": analysis_prompt}]
        )
        
        thinking_steps[ThinkingStep.ANALYSIS] = analysis_response.content[0].text
        
        # STEP 2: Search Strategy Planning
        strategy_prompt = f"""
        <thinking>
        Basado en el análisis médico: {thinking_steps[ThinkingStep.ANALYSIS]}
        
        Necesito planificar la estrategia de búsqueda:
        
        PARA AEMPS (Conocimiento oficial):
        - ¿Qué campos específicos consultar? (dosis, contraindicaciones, ajustes)
        - ¿Qué filtros aplicar? (vía administración, indicaciones)
        - ¿Qué interacciones verificar?
        
        PARA GRAPHITI (Experiencia episódica):
        - ¿Qué tipo de episodios buscar?
        - ¿Qué entidades médicas son relevantes?
        - ¿Qué filtros temporales aplicar?
        - ¿Qué nivel de similitud requerir?
        
        PRIORIZACIÓN:
        - ¿Orden de importancia de fuentes?
        - ¿Criterios de confianza?
        - ¿Umbrales de validación?
        </thinking>
        
        Define la estrategia óptima de búsqueda de conocimiento médico.
        """
        
        strategy_response = await self.claude.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=800,
            messages=[{"role": "user", "content": strategy_prompt}]
        )
        
        thinking_steps[ThinkingStep.STRATEGY] = strategy_response.content[0].text
        
        # Extract structured data from thinking
        structured_analysis = self._extract_structured_analysis(thinking_steps)
        
        return {
            "thinking_steps": thinking_steps,
            "structured": structured_analysis,
            "timestamp": datetime.now()
        }
    
    async def _parallel_knowledge_search(
        self, 
        query: MedicalQuery, 
        analysis: Dict
    ) -> tuple:
        """
        Búsquedas paralelas en MCP servers basadas en análisis
        """
        
        # Extract search parameters from analysis
        medication = analysis["structured"]["medication"]
        adjustments = analysis["structured"]["adjustments"]
        context_factors = analysis["structured"]["context_factors"]
        
        # Generate embeddings for semantic search
        search_text = f"{medication} {' '.join(adjustments)} {' '.join(context_factors)}"
        query_embedding = self.bge_model.encode(search_text)
        
        # PARALLEL SEARCH
        aemps_task = self._search_aemps_knowledge(
            medication=medication,
            adjustments=adjustments,
            context=query.context
        )
        
        graphiti_task = self._search_graphiti_episodes(
            query_text=query.query,
            embedding=query_embedding,
            context=query.context,
            medication=medication
        )
        
        aemps_results, graphiti_results = await asyncio.gather(
            aemps_task, graphiti_task, return_exceptions=True
        )
        
        return aemps_results, graphiti_results
    
    async def _search_aemps_knowledge(
        self, 
        medication: str, 
        adjustments: List[str], 
        context: Dict
    ) -> Dict:
        """
        Consulta específica a AEMPS MCP server
        """
        
        try:
            # Call AEMPS MCP with structured parameters
            aemps_response = await self.aemps_mcp.call_tool(
                "query_medication_comprehensive",
                {
                    "medication_name": medication,
                    "adjustments_required": adjustments,
                    "include_interactions": True,
                    "include_contraindications": True,
                    "include_dosage_ranges": True,
                    "clinical_context": context
                }
            )
            
            return {
                "source": "AEMPS",
                "medication_info": aemps_response.get("medication", {}),
                "dosage_info": aemps_response.get("dosage", {}),
                "adjustments": aemps_response.get("adjustments", {}),
                "interactions": aemps_response.get("interactions", []),
                "contraindications": aemps_response.get("contraindications", []),
                "confidence": 1.0,  # Fuente oficial
                "timestamp": datetime.now()
            }
            
        except Exception as e:
            return {
                "source": "AEMPS",
                "error": str(e),
                "confidence": 0.0,
                "timestamp": datetime.now()
            }
    
    async def _search_graphiti_episodes(
        self, 
        query_text: str, 
        embedding: List[float], 
        context: Dict, 
        medication: str
    ) -> Dict:
        """
        Búsqueda semántica en episodios Graphiti
        """
        
        try:
            # Search similar episodes using Graphiti MCP
            episodes_response = await self.graphiti_mcp.call_tool(
                "search_episodes",
                {
                    "query": query_text,
                    "embedding": embedding.tolist(),
                    "entity_types": [
                        "ConsultaMedicamento", 
                        "EpisodioResolucion",
                        "PatronEmergente"
                    ],
                    "filters": {
                        "medicamento_principal": medication,
                        "unidad": context.get("unidad"),
                        "temporal_filter": "last_6_months"
                    },
                    "limit": 10,
                    "min_similarity": 0.75
                }
            )
            
            # Also search for learned patterns
            patterns_response = await self.graphiti_mcp.call_tool(
                "search_patterns",
                {
                    "medication": medication,
                    "clinical_context": context,
                    "min_evidence_count": 3,
                    "min_confidence": 0.8
                }
            )
            
            return {
                "source": "Graphiti",
                "similar_episodes": episodes_response.get("episodes", []),
                "learned_patterns": patterns_response.get("patterns", []),
                "total_episodes": len(episodes_response.get("episodes", [])),
                "confidence": episodes_response.get("avg_similarity", 0.0),
                "timestamp": datetime.now()
            }
            
        except Exception as e:
            return {
                "source": "Graphiti", 
                "error": str(e),
                "similar_episodes": [],
                "learned_patterns": [],
                "confidence": 0.0,
                "timestamp": datetime.now()
            }
    
    async def _synthesize_medical_response(
        self,
        query: MedicalQuery,
        analysis: Dict,
        aemps_data: Dict,
        graphiti_data: Dict
    ) -> MedicalResponse:
        """
        Síntesis inteligente con Claude - thinking interno avanzado
        """
        
        synthesis_prompt = f"""
        <thinking>
        CONTEXTO DE SÍNTESIS MÉDICA:
        
        Consulta original: "{query.query}"
        Análisis realizado: {analysis["structured"]}
        
        CONOCIMIENTO OFICIAL (AEMPS):
        {aemps_data}
        
        EXPERIENCIA EPISÓDICA (Graphiti):
        {graphiti_data}
        
        SÍNTESIS REQUERIDA:
        1. Dosis específica recomendada (considerando ajustes)
        2. Vía de administración óptima
        3. Precauciones específicas para este caso
        4. Nivel de confianza de la recomendación
        5. Necesidad de validación médica adicional
        6. Acciones de seguimiento requeridas
        
        CRITERIOS DE DECISIÓN:
        - Priorizar siempre seguridad del paciente
        - Conocimiento oficial AEMPS tiene máxima autoridad
        - Experiencia episódica complementa y contextualiza
        - Ser específico y accionable para enfermera
        - Indicar claramente nivel de confianza
        </thinking>
        
        Como experto en farmacología clínica, sintetiza una respuesta práctica y segura para esta consulta de enfermería.
        
        Estructura tu respuesta en:
        1. RECOMENDACIÓN PRINCIPAL (dosis, vía, frecuencia)
        2. PRECAUCIONES ESPECÍFICAS
        3. EVIDENCIA Y CONFIANZA
        4. ACCIONES DE SEGUIMIENTO
        """
        
        synthesis_response = await self.claude.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1200,
            messages=[{"role": "user", "content": synthesis_prompt}]
        )
        
        # Parse response into structured format
        response_text = synthesis_response.content[0].text
        
        # Extract structured components (would need actual parsing logic)
        medical_response = self._parse_medical_response(
            response_text, aemps_data, graphiti_data
        )
        
        return medical_response
    
    def _parse_medical_response(
        self, 
        response_text: str, 
        aemps_data: Dict, 
        graphiti_data: Dict
    ) -> MedicalResponse:
        """
        Parse Claude response into structured medical response
        """
        
        # This would need sophisticated parsing logic
        # For now, simplified version
        
        return MedicalResponse(
            main_recommendation=self._extract_main_recommendation(response_text),
            dosage=self._extract_dosage(response_text),
            administration_route=self._extract_route(response_text),
            precautions=self._extract_precautions(response_text),
            evidence_sources=self._compile_evidence_sources(aemps_data, graphiti_data),
            confidence_score=self._calculate_confidence_score(aemps_data, graphiti_data),
            similar_cases=graphiti_data.get("similar_episodes", [])[:3],
            validation_required=self._assess_validation_requirement(response_text),
            follow_up_actions=self._extract_follow_up_actions(response_text)
        )
    
    async def _register_episode_background(
        self,
        query: MedicalQuery,
        analysis: Dict,
        response: MedicalResponse
    ):
        """
        Registro automático en Graphiti (background task)
        """
        
        try:
            episode_content = f"""
            EPISODIO MÉDICO COMPLETO:
            
            Consulta: {query.query}
            Contexto enfermera: {query.context}
            Contexto paciente: {query.patient_context}
            
            Análisis realizado: {analysis["structured"]}
            
            Respuesta final: {response.main_recommendation}
            Dosis: {response.dosage}
            Precauciones: {response.precautions}
            Confianza: {response.confidence_score}
            
            Timestamp: {datetime.now().isoformat()}
            """
            
            # Register in Graphiti using MCP
            await self.graphiti_mcp.call_tool(
                "create_episode",
                {
                    "content": episode_content,
                    "entities": [
                        {
                            "type": "ConsultaMedicamento",
                            "data": {
                                "pregunta_original": query.query,
                                "medicamento_principal": analysis["structured"]["medication"],
                                "contexto_clinico": str(query.context)
                            }
                        },
                        {
                            "type": "EpisodioResolucion", 
                            "data": {
                                "respuesta_final": response.main_recommendation,
                                "dosis_recomendada": response.dosage,
                                "nivel_confianza": response.confidence_score
                            }
                        }
                    ]
                }
            )
            
        except Exception as e:
            # Log error but don't fail main process
            print(f"Error registering episode: {e}")
    
    # Helper methods (simplified for brevity)
    def _extract_structured_analysis(self, thinking_steps: Dict) -> Dict:
        # Extract medication, adjustments, etc. from thinking text
        return {
            "medication": "omeprazol",  # Would extract from analysis
            "adjustments": ["renal"],   # Would extract from analysis
            "context_factors": ["UCI"], # Would extract from analysis
        }
    
    def _extract_main_recommendation(self, response_text: str) -> str:
        # Parse main recommendation from response
        return "Omeprazol 20mg IV cada 24 horas"
    
    def _calculate_confidence_score(self, aemps_data: Dict, graphiti_data: Dict) -> float:
        # Calculate confidence based on data sources
        aemps_conf = aemps_data.get("confidence", 0.0)
        graphiti_conf = graphiti_data.get("confidence", 0.0)
        return (aemps_conf * 0.7) + (graphiti_conf * 0.3)
    
    # ... other helper methods
```

---

## 🌐 Frontend Implementation

### **React Components Structure**

```typescript
// types/medical.ts
interface MedicalQuery {
  query: string;
  context: {
    unidad: string;
    experiencia: string;
    turno: string;
  };
  patientContext?: {
    peso?: number;
    funcionRenal?: string;
    medicamentosActuales?: string[];
  };
}

interface MedicalResponse {
  mainRecommendation: string;
  dosage: string;
  administrationRoute: string;
  precautions: string[];
  evidenceSources: EvidenceSource[];
  confidenceScore: number;
  similarCases: CaseSimilar[];
  validationRequired: boolean;
  followUpActions: string[];
}

// components/MedicationConsultation.tsx
import React, { useState } from 'react';
import { ConsultationForm } from './ConsultationForm';
import { LoadingProcess } from './LoadingProcess';
import { MedicalResponse } from './MedicalResponse';
import { useMedicationAPI } from '../hooks/useMedicationAPI';

export const MedicationConsultation: React.FC = () => {
  const [currentStep, setCurrentStep] = useState<'form' | 'loading' | 'response'>('form');
  const { submitQuery, isLoading, response, error } = useMedicationAPI();

  const handleSubmit = async (query: MedicalQuery) => {
    setCurrentStep('loading');
    try {
      await submitQuery(query);
      setCurrentStep('response');
    } catch (err) {
      // Handle error
      setCurrentStep('form');
    }
  };

  return (
    <div className="medication-consultation">
      {currentStep === 'form' && (
        <ConsultationForm onSubmit={handleSubmit} />
      )}
      
      {currentStep === 'loading' && (
        <LoadingProcess />
      )}
      
      {currentStep === 'response' && response && (
        <MedicalResponse 
          response={response} 
          onNewConsultation={() => setCurrentStep('form')}
        />
      )}
    </div>
  );
};

// components/LoadingProcess.tsx
export const LoadingProcess: React.FC = () => {
  const [currentStep, setCurrentStep] = useState(0);
  
  const steps = [
    { icon: '🔍', text: 'Analizando consulta médica...', duration: 800 },
    { icon: '📚', text: 'Consultando protocolos AEMPS...', duration: 1200 },
    { icon: '🧠', text: 'Revisando casos similares...', duration: 900 },
    { icon: '⚡', text: 'Sintetizando respuesta...', duration: 600 },
  ];

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentStep(prev => Math.min(prev + 1, steps.length - 1));
    }, 800);
    
    return () => clearInterval(timer);
  }, []);

  return (
    <div className="loading-process">
      <h3>Procesando consulta médica...</h3>
      <div className="steps-container">
        {steps.map((step, index) => (
          <div 
            key={index}
            className={`step ${index <= currentStep ? 'completed' : ''} ${index === currentStep ? 'active' : ''}`}
          >
            <span className="icon">{step.icon}</span>
            <span className="text">{step.text}</span>
            {index === currentStep && <Spinner />}
            {index < currentStep && <CheckIcon />}
          </div>
        ))}
      </div>
    </div>
  );
};

// hooks/useMedicationAPI.ts
export const useMedicationAPI = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [response, setResponse] = useState<MedicalResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const submitQuery = async (query: MedicalQuery) => {
    setIsLoading(true);
    setError(null);
    
    try {
      const response = await fetch('/api/consulta', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(query),
      });
      
      if (!response.ok) {
        throw new Error('Error en la consulta');
      }
      
      const data = await response.json();
      setResponse(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return { submitQuery, isLoading, response, error };
};
```

---

## 🚀 Plan de Desarrollo Evolutivo

### **Sprint 1: Core Orchestrator (1 semana)**

#### **Objetivos:**
- TransparentMedicationSystem class básica
- Sequential thinking con Claude API
- Conexión MCP Graphiti (ya funciona)
- CLI testing interface

#### **Entregables:**
```python
# medication_orchestrator.py (CLI version)
if __name__ == "__main__":
    system = TransparentMedicationSystem()
    
    query = MedicalQuery(
        query="¿Dosis omeprazol IV paciente 70kg insuficiencia renal?",
        context={"unidad": "UCI", "experiencia": "5_años"}
    )
    
    response = await system.process_medical_consultation(query)
    print(response)
```

#### **Testing:**
- Consultas básicas con Graphiti MCP
- Sequential thinking proceso completo
- Parsing respuestas estructuradas
- Error handling básico

### **Sprint 2: AEMPS Integration + API Server (1 semana)**

#### **Objetivos:**
- AEMPS MCP server desarrollado e integrado
- FastAPI server wrapper
- Parallel knowledge search funcionando
- Testing dual MCP

#### **Entregables:**
```python
# api_server.py
from fastapi import FastAPI
from medication_orchestrator import TransparentMedicationSystem

app = FastAPI()
system = TransparentMedicationSystem()

@app.post("/consulta")
async def medical_consultation(request: MedicalQuery):
    response = await system.process_medical_consultation(request)
    return response
```

#### **Testing:**
- AEMPS data retrieval
- Dual search paralelo
- API endpoints funcionando
- Performance benchmarks

### **Sprint 3: Frontend + UX (1 semana)**

#### **Objetivos:**
- React frontend completo
- Loading states elegantes
- Respuesta integrada accionable
- Mobile responsive

#### **Entregables:**
- Interface web funcional
- UX flow completo enfermera
- Integration frontend-backend
- Testing con usuarios piloto

### **Sprint 4: Advanced Features + Production (1 semana)**

#### **Objetivos:**
- Auto-registration background
- Analytics y métricas
- Error handling robusto
- Production deployment

#### **Entregables:**
- Sistema production-ready
- Métricas y monitoring
- Documentation completa
- Training material enfermeras

---

## 📊 Métricas y Monitoring

### **KPIs Técnicos**
```python
class MedicationSystemMetrics:
    # Performance metrics
    avg_response_time: float  # Target: <3 segundos
    p95_response_time: float  # Target: <5 segundos
    
    # Accuracy metrics  
    aemps_success_rate: float   # Target: >98%
    graphiti_success_rate: float # Target: >95%
    synthesis_quality: float     # Target: >90%
    
    # Usage metrics
    daily_consultations: int
    unique_users: int
    repeat_usage_rate: float    # Target: >70%
    
    # Medical metrics
    validation_success_rate: float  # Target: >95%
    error_rate: float               # Target: <2%
    user_satisfaction: float        # Target: >8.5/10
```

### **Dashboards**
- **Enfermeras**: Estadísticas uso personal, consultas frecuentes
- **Supervisores**: Métricas unidad, validaciones pendientes, trends
- **Técnico**: Performance sistema, errores, usage patterns
- **Médico**: Validaciones requeridas, casos complejos, accuracy

---

## 🎯 Decisiones Técnicas Finales

### **Architecture Pattern: Hybrid Orchestration**
- **Frontend**: Clean UX con progressive enhancement
- **Backend**: Sequential thinking + MCP orchestration
- **AI**: Multi-model approach (MedGemma + Claude + BGE-M3)
- **Data**: Dual knowledge (Graphiti episódico + AEMPS dominio)

### **Development Strategy: Evolutionary**
- **Week 1**: CLI MVP con core orchestrator
- **Week 2**: API server + AEMPS integration  
- **Week 3**: Web frontend + UX
- **Week 4**: Production features + deployment

### **Success Criteria**
- **Technical**: <3s response time, >95% accuracy, >98% uptime
- **Medical**: >8.5/10 satisfaction, <2% error rate, 100% critical validations
- **Business**: >70% adoption, >10 consultas/usuario/semana, ROI positivo

---

*Implementación híbrida completa - Ready for development sprint execution*