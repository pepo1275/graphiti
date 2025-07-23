#!/usr/bin/env python3
"""
Episodios Sintéticos de Enfermería para Evaluación Graphiti
Basados en estructura AEMPS para apoyo al trabajo de enfermería

Generado para comparación OpenAI vs Gemini embeddings
Proyecto: /Users/pepo/graphiti-pepo-local
"""

from typing import List, Dict, Any
from dataclasses import dataclass
from datetime import datetime

@dataclass
class NursingEpisode:
    """Episodio de enfermería para evaluación"""
    id: str
    title: str
    content: str
    expected_entities: List[str]
    expected_relations: List[str]
    nursing_context: str
    complexity_level: str

def get_nursing_episodes() -> List[NursingEpisode]:
    """Generar episodios sintéticos de enfermería basados en estructura AEMPS"""
    
    episodes = [
        NursingEpisode(
            id="nursing_001",
            title="Administración Segura - Paracetamol",
            content="""
            Turno de noche: Paciente Juan Pérez, 45 años, dolor postoperatorio.
            Orden médica: PARACETAMOL CINFA 500mg vía oral cada 8 horas.
            Enfermera verifica: sin alergias conocidas al paracetamol.
            Principio activo: paracetamol 500mg por comprimido.
            Laboratorio fabricante: CINFA. Código ATC: N02BE01.
            Forma farmacéutica: comprimidos recubiertos.
            Administrado a las 22:00h según protocolo.
            """,
            expected_entities=[
                "PARACETAMOL CINFA", "paracetamol", "CINFA", "N02BE01",
                "Juan Pérez", "dolor postoperatorio", "500mg", "comprimidos"
            ],
            expected_relations=[
                "CONTIENE", "FABRICADO_POR", "CLASIFICADO_COMO", "ADMINISTRADO_A",
                "INDICADO_PARA", "DOSIS_DE", "FORMA_FARMACEUTICA"
            ],
            nursing_context="administracion_medicamentos",
            complexity_level="basic"
        ),
        
        NursingEpisode(
            id="nursing_002", 
            title="Control de Alergias - Ibuprofeno",
            content="""
            Paciente María García, 38 años, ingreso por cefalea intensa.
            Historia clínica: ALERGIA CONOCIDA AL IBUPROFENO (urticaria).
            Nueva prescripción: IBUPROFENO KERN PHARMA 600mg cada 12 horas.
            ALERTA: Enfermera detecta contraindicación por alergia.
            Contacta con médico prescriptor para cambio de medicación.
            Principio activo contraindicado: ibuprofeno.
            Código ATC del ibuprofeno: M01AE01 (antiinflamatorio).
            Protocolo: registrar incidencia y solicitar alternativa.
            """,
            expected_entities=[
                "IBUPROFENO KERN PHARMA", "ibuprofeno", "KERN PHARMA",
                "María García", "alergia", "urticaria", "cefalea", "M01AE01"
            ],
            expected_relations=[
                "ALERGICO_A", "CONTRAINDICADO_PARA", "FABRICA",
                "CAUSA_REACCION", "REQUIERE_CAMBIO", "REGISTRAR_INCIDENCIA"
            ],
            nursing_context="control_alergias",
            complexity_level="medium"
        ),
        
        NursingEpisode(
            id="nursing_003",
            title="Interacción Medicamentosa - Warfarina y Omeprazol", 
            content="""
            Paciente Carlos Ruiz, 72 años, anticoagulado con warfarina.
            Medicación actual: WARFARINA NORMON 5mg/día.
            Nueva prescripción: OMEPRAZOL SANDOZ 20mg por gastritis.
            Enfermera revisa: posible interacción medicamentosa.
            El omeprazol puede potenciar efecto anticoagulante.
            Riesgo: aumento del INR y riesgo hemorrágico.
            Acción: consulta con farmacéutico del hospital.
            Recomendación: monitorización INR más frecuente.
            Laboratorios: NORMON (warfarina), SANDOZ (omeprazol).
            """,
            expected_entities=[
                "WARFARINA NORMON", "warfarina", "OMEPRAZOL SANDOZ", "omeprazol",
                "Carlos Ruiz", "INR", "NORMON", "SANDOZ", "anticoagulante"
            ],
            expected_relations=[
                "INTERACTUA_CON", "POTENCIA_EFECTO", "AUMENTA_RIESGO",
                "REQUIERE_MONITORIZACION", "CONSULTA_FARMACEUTICO"
            ],
            nursing_context="interacciones_medicamentosas", 
            complexity_level="high"
        ),
        
        NursingEpisode(
            id="nursing_004",
            title="Cálculo Dosis Pediátrica - Paracetamol",
            content="""
            Paciente pediátrico: Ana Martín, 6 años, peso 22kg, fiebre 38.5°C.
            Prescripción: PARACETAMOL KERN PHARMA solución oral.
            Dosis prescrita: 15mg/kg cada 6 horas.
            Cálculo enfermera: 22kg × 15mg/kg = 330mg por dosis.
            Presentación: 160mg/5ml (jarabe).
            Volumen a administrar: 330mg ÷ 160mg/5ml = 10.3ml.
            Principio activo: paracetamol. Laboratorio: KERN PHARMA.
            Vía administración: oral. Forma: solución oral.
            """,
            expected_entities=[
                "PARACETAMOL KERN PHARMA", "Ana Martín", "22kg", "15mg/kg",
                "330mg", "160mg/5ml", "10.3ml", "solución oral"
            ],
            expected_relations=[
                "PESO_PACIENTE", "DOSIS_POR_PESO", "CALCULO_DOSIS",
                "VOLUMEN_ADMINISTRAR", "VIA_ORAL", "CADA_6_HORAS"
            ],
            nursing_context="calculo_dosis_pediatrica",
            complexity_level="high"
        ),
        
        NursingEpisode(
            id="nursing_005",
            title="Protocolo Diabetes - Metformina",
            content="""
            Paciente diabético: Roberto López, 58 años, diabetes tipo 2.
            Medicación: METFORMINA TEVA 850mg dos veces al día.
            Protocolo enfermería: control glucemia antes de comidas.
            Glucemia actual: 180mg/dl (elevada).
            Principio activo: metformina, antidiabético oral.
            Código ATC: A10BA02. Laboratorio: TEVA.
            Acción: administrar metformina con desayuno y cena.
            Educación: importancia adherencia tratamiento.
            Seguimiento: registrar glucemias en hoja de evolución.
            """,
            expected_entities=[
                "METFORMINA TEVA", "metformina", "Roberto López", "diabetes tipo 2",
                "850mg", "180mg/dl", "glucemia", "TEVA", "A10BA02"
            ],
            expected_relations=[
                "DIAGNOSTICADO_CON", "TRATA", "CONTROLA_GLUCEMIA",
                "ADMINISTRAR_CON", "REQUIERE_SEGUIMIENTO", "EDUCAR_SOBRE"
            ],
            nursing_context="protocolos_diabetes",
            complexity_level="medium"
        ),
        
        NursingEpisode(
            id="nursing_006",
            title="Efectos Adversos - Omeprazol",
            content="""
            Paciente Elena Jiménez, 42 años, tratamiento con omeprazol.
            Medicación: OMEPRAZOL CINFA 20mg una vez al día.
            Paciente refiere: dolor abdominal y diarrea desde ayer.
            Sospecha: posible efecto adverso del omeprazol.
            Principio activo: omeprazol (inhibidor bomba protones).
            Código ATC: A02BC01. Laboratorio: CINFA.
            Acción enfermera: registro en hoja de efectos adversos.
            Comunicación: notificar médico responsable.
            Valorar: suspensión temporal del medicamento.
            """,
            expected_entities=[
                "OMEPRAZOL CINFA", "omeprazol", "Elena Jiménez",
                "dolor abdominal", "diarrea", "efecto adverso", "A02BC01", "CINFA"
            ],
            expected_relations=[
                "CAUSA_EFECTO_ADVERSO", "PRESENTA_SINTOMA", "REQUIERE_REGISTRO",
                "NOTIFICAR_MEDICO", "VALORAR_SUSPENSION"
            ],
            nursing_context="efectos_adversos",
            complexity_level="medium"
        ),
        
        NursingEpisode(
            id="nursing_007",
            title="Protocolo Anticoagulación - Control INR",
            content="""
            Paciente anticoagulado: Miguel Torres, 68 años, fibrilación auricular.
            Anticoagulante: WARFARINA RATIOPHARM 2.5mg diarios.
            Control semanal: INR actual 3.2 (rango terapéutico 2-3).
            Protocolo: INR ligeramente elevado, riesgo hemorrágico.
            Acción enfermera: contactar con hematología.
            Educación paciente: signos de sangrado (hematomas, epistaxis).
            Laboratorio warfarina: RATIOPHARM.
            Seguimiento: nuevo control INR en 3 días.
            """,
            expected_entities=[
                "WARFARINA RATIOPHARM", "warfarina", "Miguel Torres",
                "fibrilación auricular", "INR", "3.2", "2.5mg", "RATIOPHARM"
            ],
            expected_relations=[
                "ANTICOAGULADO_CON", "INR_ELEVADO", "RIESGO_HEMORRAGICO",
                "CONTACTAR_HEMATOLOGIA", "EDUCAR_SIGNOS_SANGRADO"
            ],
            nursing_context="control_anticoagulacion",
            complexity_level="high"
        )
    ]
    
    return episodes

def get_evaluation_metrics() -> Dict[str, Any]:
    """Métricas específicas para evaluación de embeddings en contexto enfermería"""
    
    return {
        "entity_extraction_metrics": {
            "medicamentos_comerciales": "Detección nombres comerciales completos",
            "principios_activos": "Identificación principios activos",
            "laboratorios": "Reconocimiento fabricantes",
            "codigos_atc": "Captura códigos de clasificación",
            "pacientes": "Identificación datos pacientes",
            "dosis_calculos": "Extracción dosis y cálculos",
            "efectos_adversos": "Detección efectos no deseados"
        },
        "relationship_quality_metrics": {
            "medicamento_principio_activo": "Relación CONTIENE",
            "medicamento_laboratorio": "Relación FABRICADO_POR", 
            "medicamento_clasificacion": "Relación CLASIFICADO_COMO",
            "paciente_alergia": "Relación ALERGICO_A",
            "medicamento_interaccion": "Relación INTERACTUA_CON",
            "medicamento_efecto_adverso": "Relación CAUSA_EFECTO_ADVERSO",
            "paciente_diagnostico": "Relación DIAGNOSTICADO_CON"
        },
        "nursing_specific_metrics": {
            "protocolo_administracion": "Protocolos de administración segura",
            "control_alergias": "Sistemas de alerta alergias",
            "calculo_dosis": "Precisión cálculos dosis",
            "monitorizacion_parametros": "Seguimiento parámetros clínicos",
            "educacion_paciente": "Contenidos educativos",
            "registro_incidencias": "Documentación eventos adversos"
        },
        "search_quality_metrics": {
            "busqueda_por_principio_activo": "Medicamentos con mismo principio activo",
            "busqueda_por_indicacion": "Medicamentos para misma patología",
            "busqueda_interacciones": "Identificar interacciones medicamentosas",
            "busqueda_alergias": "Medicamentos contraindicados por alergia",
            "busqueda_protocolos": "Protocolos específicos por medicamento"
        }
    }

def get_expected_graph_structure() -> Dict[str, Any]:
    """Estructura esperada del grafo de conocimiento para enfermería"""
    
    return {
        "node_types": [
            "Medicamento", "PrincipioActivo", "Laboratorio", "CodigoATC",
            "Paciente", "Diagnostico", "Alergia", "EfectoAdverso",
            "Protocolo", "Dosis", "ViaAdministracion"
        ],
        "relationship_types": [
            "CONTIENE", "FABRICADO_POR", "CLASIFICADO_COMO",
            "ADMINISTRADO_A", "ALERGICO_A", "INTERACTUA_CON",
            "CAUSA_EFECTO_ADVERSO", "DIAGNOSTICADO_CON", "REQUIERE_PROTOCOLO",
            "CALCULO_DOSIS", "VIA_ADMINISTRACION"
        ],
        "critical_paths": [
            "Medicamento → PrincipioActivo",
            "Paciente → Alergia → Medicamento", 
            "Medicamento → EfectoAdverso",
            "Medicamento ↔ Medicamento (interacciones)",
            "Paciente → Diagnostico → Medicamento"
        ]
    }

if __name__ == "__main__":
    # Generar y mostrar episodios para verificación
    episodes = get_nursing_episodes()
    print(f"✅ Generados {len(episodes)} episodios de enfermería")
    
    for ep in episodes[:2]:  # Mostrar primeros 2 como ejemplo
        print(f"\n📋 {ep.title}")
        print(f"   Contexto: {ep.nursing_context}")
        print(f"   Complejidad: {ep.complexity_level}")
        print(f"   Entidades esperadas: {len(ep.expected_entities)}")
        print(f"   Relaciones esperadas: {len(ep.expected_relations)}")
    
    print(f"\n🎯 Episodios listos para evaluación Graphiti OpenAI vs Gemini")
