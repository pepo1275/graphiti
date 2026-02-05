# ADR-001: Estrategia de Embeddings Mejorados

## Estado
**Propuesto** - Pendiente de aprobación

## Fecha
2026-01-31

## Contexto

El fork de Graphiti necesita mejorar la calidad de búsqueda semántica. La investigación reveló:

1. **Bug actual**: Embeddings con dimensión < 3072 no se normalizan, causando similaridad coseno incorrecta
2. **Características no usadas**: Gemini Embedding API ofrece 8 task_types que no aprovechamos
3. **Modelo desactualizado**: Usamos `text-embedding-001` en lugar de `gemini-embedding-001`
4. **Dimensión subóptima**: Default actual es 1024D, podríamos usar 3072D

### Requisitos
- Mantener compatibilidad con upstream getzep/graphiti
- Permitir experimentación A/B entre configuraciones
- No romper datos existentes
- Documentar todos los cambios

## Decisión

Implementar **mejoras aditivas con campos duales** siguiendo esta estrategia:

### 1. Fix de Normalización (Prioritario)
```python
# Añadir normalización condicional con flag
NORMALIZE_EMBEDDINGS = os.getenv('GRAPHITI_NORMALIZE_EMBEDDINGS', 'true')

if NORMALIZE_EMBEDDINGS and dim < 3072:
    embedding = normalize(embedding)
```

### 2. Soporte para Task Types (Opcional)
```python
# Añadir parámetro opcional, default None (comportamiento upstream)
task_type: str | None = Field(default=None)
```

### 3. Campos Duales para Experimentación
```python
# Campos nuevos opcionales (no afectan upstream)
name_embedding_enhanced: list[float] | None = Field(default=None)
name_embedding_config: dict | None = Field(default=None)
```

### 4. Configuración por Variables de Entorno
```bash
GRAPHITI_NORMALIZE_EMBEDDINGS=true    # Default: true
GRAPHITI_EMBEDDING_DIM=3072           # Default: 1024 (upstream)
GRAPHITI_EMBEDDING_MODEL=gemini-embedding-001
GRAPHITI_TASK_TYPE=RETRIEVAL_DOCUMENT # Default: None (upstream)
```

## Consecuencias

### Positivas
- Mejora calidad de búsqueda sin romper compatibilidad
- Permite experimentación A/B con datos reales
- Fácil rollback desactivando flags
- Documentación completa de cambios

### Negativas
- Aumento de almacenamiento (~3x para campos duales)
- Complejidad adicional en código
- Posibles conflictos en futuros syncs con upstream

### Riesgos
- Si upstream implementa normalización diferente, podría haber conflictos
- Campos duales pueden quedar obsoletos si se decide migrar completamente

## Alternativas Consideradas

### Alternativa A: Migración directa a 3072D
- **Pro**: Más simple, sin campos duales
- **Contra**: No permite experimentación, riesgo de regresión

### Alternativa B: No hacer nada
- **Pro**: Sin riesgo de conflictos
- **Contra**: Bug de normalización persiste, calidad subóptima

### Alternativa C: Contribuir a upstream
- **Pro**: Beneficia a toda la comunidad
- **Contra**: Proceso lento, requiere aprobación de Zep

## Plan de Implementación

Ver [PLAN-EMBEDDINGS-GEMINI-AVANZADO.md](../projects/PLAN-EMBEDDINGS-GEMINI-AVANZADO.md)

1. Fase 0: Sync con upstream
2. Fase 1: Fix normalización
3. Fase 2: Task types
4. Fase 3: Campos duales
5. Fase 4: Reprocesamiento
6. Fase 5: Evaluación
7. Fase 6: Release

## Referencias

- [Gemini Embedding API](https://ai.google.dev/gemini-api/docs/embeddings)
- [Matryoshka Representation Learning](https://arxiv.org/abs/2205.13147)
- [Plan Maestro](../projects/PLAN-MAESTRO-MEJORAS-GRAPHITI.md)
- [CHANGELOG-FORK](../changelog/CHANGELOG-FORK.md)
