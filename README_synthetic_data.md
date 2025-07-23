# 🏥 Datos Sintéticos de Enfermería - Evaluación Graphiti

## 📋 Resumen

Episodios sintéticos farmacéuticos basados en estructura AEMPS para evaluar embeddings **OpenAI vs Gemini** en Graphiti, enfocados en casos prácticos de enfermería hospitalaria.

---

## 📊 Episodios Generados

### **7 episodios de enfermería** que cubren:

1. **Administración Segura** - Paracetamol (básico)
2. **Control de Alergias** - Ibuprofeno (medio)  
3. **Interacciones Medicamentosas** - Warfarina + Omeprazol (alto)
4. **Cálculo Dosis Pediátrica** - Paracetamol (alto)
5. **Protocolos Diabetes** - Metformina (medio)
6. **Efectos Adversos** - Omeprazol (medio)
7. **Control Anticoagulación** - Warfarina INR (alto)

---

## 🏗️ Estructura de Datos

### **Entidades Farmacéuticas** (basadas en AEMPS):
- **Medicamentos comerciales**: PARACETAMOL CINFA, IBUPROFENO KERN PHARMA, etc.
- **Principios activos**: paracetamol, ibuprofeno, omeprazol, warfarina, metformina
- **Laboratorios**: CINFA, KERN PHARMA, SANDOZ, NORMON, TEVA, RATIOPHARM
- **Códigos ATC**: N02BE01, M01AE01, A02BC01, C09AA02, A10BA02
- **Pacientes**: Juan Pérez, María García, Carlos Ruiz, Ana Martín, etc.

### **Relaciones Esperadas**:
- `CONTIENE` (medicamento → principio activo)
- `FABRICADO_POR` (medicamento → laboratorio) 
- `CLASIFICADO_COMO` (medicamento → código ATC)
- `ALERGICO_A` (paciente → medicamento)
- `INTERACTUA_CON` (medicamento ↔ medicamento)
- `CAUSA_EFECTO_ADVERSO` (medicamento → efecto)

---

## 🎯 Métricas de Evaluación

### **Específicas para Enfermería**:
- **Detección entidades médicas** (medicamentos, principios activos, dosis)
- **Protocolos de administración segura** 
- **Control de alergias e interacciones**
- **Cálculos de dosis precisos**
- **Seguimiento de parámetros clínicos** (INR, glucemia)
- **Educación y registro de incidencias**

### **Comparación OpenAI vs Gemini**:
- ⏱️ **Tiempo de procesamiento**
- 📊 **Calidad extracción entidades**
- 🔗 **Precisión relaciones**
- 🔍 **Calidad búsqueda semántica**
- ❌ **Tasa de errores**

---

## 🚀 Uso de los Datos

### **1. Verificar configuración**:
```bash
cd /Users/pepo/graphiti-pepo-local
python3 verify_setup.py
```

### **2. Probar episodios**:
```bash
python3 synthetic_data/nursing_episodes.py
```

### **3. Ejecutar comparación completa**:
```bash
uv run python run_simple_comparison.py
```

### **4. Revisar resultados**:
- **Reporte consola**: Métricas en tiempo real
- **JSON detallado**: `evaluation_report.json`
- **Neo4j Browser**: 
  - OpenAI: http://localhost:7474 (puerto 8694)
  - Gemini: http://localhost:7474 (puerto 8693)

---

## 📁 Archivos Generados

```
/Users/pepo/graphiti-pepo-local/
├── synthetic_data/
│   └── nursing_episodes.py           # ✅ Episodios sintéticos
├── run_simple_comparison.py          # ✅ Comparación principal  
├── verify_setup.py                   # ✅ Verificación sistema
├── evaluation_report.json            # 📊 Reporte detallado
└── README_synthetic_data.md          # 📖 Esta documentación
```

---

## 🔧 Contexto Técnico

### **Instancias Configuradas**:
- **OpenAI Graphiti**: puerto 8694, embeddings 3072 dims
- **Gemini Graphiti**: puerto 8693, embeddings 3072 dims  

### **Casos de Uso Enfermería**:
- ✅ **Administración medicamentos** seguros
- ✅ **Verificación alergias** automática
- ✅ **Control interacciones** medicamentosas
- ✅ **Cálculo dosis** pediatría
- ✅ **Protocolos específicos** (diabetes, anticoagulación)
- ✅ **Seguimiento efectos** adversos

### **Basado en Estructura AEMPS**:
- Medicamentos reales del registro español
- Códigos ATC oficiales
- Laboratorios farmacéuticos españoles
- Principios activos estándar
- Protocolos clínicos reales

---

## 🎯 Objetivo Final

**Determinar qué embedding (OpenAI vs Gemini) es más efectivo** para:
1. **Apoyo decisional** a enfermeras
2. **Seguridad del paciente** (alergias, interacciones)
3. **Eficiencia operativa** (protocolos, cálculos)
4. **Gestión del conocimiento** farmacéutico

---

**Estado**: ✅ Listo para evaluación  
**Generado**: 22 julio 2025  
**Proyecto**: Graphiti Embedding Evaluation Phase 1
