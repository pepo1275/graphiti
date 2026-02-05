# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Graphiti** is a Python framework for building temporally-aware knowledge graphs designed for AI agents. It enables real-time incremental updates to knowledge graphs without batch recomputation, making it suitable for dynamic environments.

**Este fork** incluye configuración personalizada para:
- Sistema de memoria episódica para Claude Desktop/Code
- 19 Entity Types para captura de episodios de agentes IA
- Metodología RPVEA 2.0 para desarrollo

---

## Subagentes Disponibles

### @memory-architect
**Role**: Diseño de Entity Types y schema de memoria
**Skill**: `.claude/skills/memory-architect/SKILL.md`
**Use for**:
- Diseñar Entity Types para nuevos dominios
- Evaluar modelos de embeddings
- Configurar estrategias de group_id
- Arquitectura bimodal episódica/operativa

### @deployment-engineer
**Role**: Despliegue Docker y configuración MCP
**Skill**: `.claude/skills/deployment-engineer/SKILL.md`
**Use for**:
- Configurar Docker Compose
- Gestionar puertos y redes
- Integrar con Claude Desktop/Code
- Troubleshooting de conexiones

### @graph-inspector
**Role**: Análisis y validación de grafos
**Skill**: `.claude/skills/graph-inspector/SKILL.md`
**Use for**:
- Verificar estado de base de datos
- Validar migraciones
- Debugging de datos
- Auditoría de integridad

---

## MCP Tools Available

### neo4j-docker-graphiti (Graphiti Legacy)
```
mcp__neo4j-docker-graphiti__graphiti-get_neo4j_schema
mcp__neo4j-docker-graphiti__graphiti-read_neo4j_cypher
mcp__neo4j-docker-graphiti__graphiti-write_neo4j_cypher
```

### neo4j-data-modeling (Validación de Modelos)
```
mcp__neo4j-data-modeling__validate_node
mcp__neo4j-data-modeling__validate_relationship
mcp__neo4j-data-modeling__validate_data_model
mcp__neo4j-data-modeling__get_mermaid_config_str
mcp__neo4j-data-modeling__export_to_arrows_json
```

---

## RPVEA 2.0 Metodología (Adaptada para Graphiti)

### Workflow para Configuración de Memoria

```
R - RESEARCH (15-20 min)
    Subagent: @memory-architect + @graph-inspector

    ### R.1 Análisis de Requisitos
    - Identificar dominio y casos de uso
    - Revisar Entity Types existentes
    - Documentar necesidades de búsqueda (semántica, código, general)

    ### R.2 Revisión de Infraestructura
    - Mapear puertos ocupados
    - Verificar MCPs existentes
    - Revisar configuraciones Neo4j activas

    Deliverable: docs/rpvea/[proyecto]_research.md

P - PREPARE (10-15 min)
    Subagent: @memory-architect
    - Diseñar Entity Types
    - Seleccionar embeddings (ver Decision Matrix)
    - Crear config YAML
    - Validar con MCP neo4j-data-modeling

    Deliverable: mcp_server/config/config-[proyecto].yaml

V - VALIDATE (10-15 min)
    Subagent: @graph-inspector
    - Verificar sintaxis YAML
    - Validar schema con MCP
    - Probar conexión Neo4j (si ya desplegado)

    Deliverable: Validation report

E - EXECUTE (variable)
    Subagent: @deployment-engineer
    - Crear docker-compose
    - Desplegar servicios
    - Configurar Claude Desktop
    - USUARIO verifica funcionamiento

    Deliverable: docker/docker-compose-[proyecto].yml

A - ASSESS (10 min)
    - Verificar MCP funciona en Claude Desktop
    - Test de add_memory / search
    - Documentar en checkpoint

    Deliverable: checkpoints/CHECKPOINT-[nn]-[proyecto].md
```

---

## Decision Matrix - Embeddings

| Caso de Uso | Proveedor | Modelo | Coste |
|-------------|-----------|--------|-------|
| **Desarrollo** | Gemini | gemini-embedding-001 | $0 |
| **Producción económica** | OpenAI | text-embedding-3-small | $0.02/1M |
| **Código especializado** | Voyage | voyage-code-3 | $0.06/1M |
| **Privacidad total** | Ollama | nomic-embed-text | $0 (local) |

**IMPORTANTE**: No usar `text-embedding-004` de Gemini (deprecado).

---

## Port Mapping (Este Fork)

| Proyecto | Neo4j HTTP | Neo4j Bolt | MCP Server |
|----------|------------|------------|------------|
| graphiti (legacy) | 8690 | 7690 | - |
| **claude-memory** | **7476** | **7696** | **8001** |

---

## Reglas de Oro

### 1. SIEMPRE verificar puertos antes de configurar
```bash
docker ps --format "{{.Names}}\t{{.Ports}}"
lsof -i -P -n | grep LISTEN | grep -E '747|768|769'
```

### 2. Naming Conventions
```yaml
# Containers
neo4j-{proyecto}
graphiti-{proyecto}

# Config files
config-{proyecto}.yaml
docker-compose-{proyecto}.yml

# Checkpoints
CHECKPOINT-{nn}-{descripcion}.md
```

### 3. NUNCA hardcodear credenciales
```yaml
# ✅ CORRECTO
password: ${NEO4J_PASSWORD:default}

# ❌ INCORRECTO
password: "mi_password_real"
```

---

## Estructura del Proyecto (Este Fork)

```
/graphiti-new/
├── CLAUDE.md                    # Este archivo
├── .claude/
│   └── skills/                  # Definición de agentes
│       ├── memory-architect/
│       ├── deployment-engineer/
│       └── graph-inspector/
├── checkpoints/                 # Checkpoints RPVEA
├── docs/
│   ├── EVALUACION-EMBEDDINGS-MEMORIA.md
│   └── rpvea/                   # Documentación RPVEA
├── graphiti_core/               # Core library (upstream)
├── mcp_server/
│   ├── config/
│   │   └── config-claude-memory.yaml  # Config personalizada
│   └── docker/
│       └── docker-compose-claude-memory.yml
├── server/                      # REST API (upstream)
└── tests/
```

---

## Quick Start - Claude Memory

```bash
# 1. Configurar variables de entorno
cd mcp_server
cp .env.example .env
# Editar .env con API keys

# 2. Desplegar
docker compose -f docker/docker-compose-claude-memory.yml up -d

# 3. Verificar
curl http://localhost:8001/health
open http://localhost:7476  # Neo4j Browser

# 4. Configurar Claude Desktop
# Editar ~/Library/Application Support/Claude/claude_desktop_config.json
```

---

Key features:

- Bi-temporal data model with explicit tracking of event occurrence times
- Hybrid retrieval combining semantic embeddings, keyword search (BM25), and graph traversal
- Support for custom entity definitions via Pydantic models
- Integration with Neo4j and FalkorDB as graph storage backends
- Optional OpenTelemetry distributed tracing support

## Development Commands

### Main Development Commands (run from project root)

```bash
# Install dependencies
uv sync --extra dev

# Format code (ruff import sorting + formatting)
make format

# Lint code (ruff + pyright type checking)
make lint

# Run tests
make test

# Run all checks (format, lint, test)
make check
```

### Server Development (run from server/ directory)

```bash
cd server/
# Install server dependencies
uv sync --extra dev

# Run server in development mode
uvicorn graph_service.main:app --reload

# Format, lint, test server code
make format
make lint
make test
```

### MCP Server Development (run from mcp_server/ directory)

```bash
cd mcp_server/
# Install MCP server dependencies
uv sync

# Run with Docker Compose
docker-compose up
```

## Code Architecture

### Core Library (`graphiti_core/`)

- **Main Entry Point**: `graphiti.py` - Contains the main `Graphiti` class that orchestrates all functionality
- **Graph Storage**: `driver/` - Database drivers for Neo4j and FalkorDB
- **LLM Integration**: `llm_client/` - Clients for OpenAI, Anthropic, Gemini, Groq
- **Embeddings**: `embedder/` - Embedding clients for various providers
- **Graph Elements**: `nodes.py`, `edges.py` - Core graph data structures
- **Search**: `search/` - Hybrid search implementation with configurable strategies
- **Prompts**: `prompts/` - LLM prompts for entity extraction, deduplication, summarization
- **Utilities**: `utils/` - Maintenance operations, bulk processing, datetime handling

### Server (`server/`)

- **FastAPI Service**: `graph_service/main.py` - REST API server
- **Routers**: `routers/` - API endpoints for ingestion and retrieval
- **DTOs**: `dto/` - Data transfer objects for API contracts

### MCP Server (`mcp_server/`)

- **MCP Implementation**: `graphiti_mcp_server.py` - Model Context Protocol server for AI assistants
- **Docker Support**: Containerized deployment with Neo4j

## Testing

- **Unit Tests**: `tests/` - Comprehensive test suite using pytest
- **Integration Tests**: Tests marked with `_int` suffix require database connections
- **Evaluation**: `tests/evals/` - End-to-end evaluation scripts

## Configuration

### Environment Variables

- `OPENAI_API_KEY` - Required for LLM inference and embeddings
- `USE_PARALLEL_RUNTIME` - Optional boolean for Neo4j parallel runtime (enterprise only)
- Provider-specific keys: `ANTHROPIC_API_KEY`, `GOOGLE_API_KEY`, `GROQ_API_KEY`, `VOYAGE_API_KEY`

### Database Setup

- **Neo4j**: Version 5.26+ required, available via Neo4j Desktop
  - Database name defaults to `neo4j` (hardcoded in Neo4jDriver)
  - Override by passing `database` parameter to driver constructor
- **FalkorDB**: Version 1.1.2+ as alternative backend
  - Database name defaults to `default_db` (hardcoded in FalkorDriver)
  - Override by passing `database` parameter to driver constructor

## Development Guidelines

### Code Style

- Use Ruff for formatting and linting (configured in pyproject.toml)
- Line length: 100 characters
- Quote style: single quotes
- Type checking with Pyright is enforced
- Main project uses `typeCheckingMode = "basic"`, server uses `typeCheckingMode = "standard"`

### Testing Requirements

- Run tests with `make test` or `pytest`
- Integration tests require database connections and are marked with `_int` suffix
- Use `pytest-xdist` for parallel test execution
- Run specific test files: `pytest tests/test_specific_file.py`
- Run specific test methods: `pytest tests/test_file.py::test_method_name`
- Run only integration tests: `pytest tests/ -k "_int"`
- Run only unit tests: `pytest tests/ -k "not _int"`

### LLM Provider Support

The codebase supports multiple LLM providers but works best with services supporting structured output (OpenAI, Gemini). Other providers may cause schema validation issues, especially with smaller models.

#### Current LLM Models (as of November 2025)

**OpenAI Models:**
- **GPT-5 Family** (Reasoning models, require temperature=0):
  - `gpt-5-mini` - Fast reasoning model
  - `gpt-5-nano` - Smallest reasoning model
- **GPT-4.1 Family** (Standard models):
  - `gpt-4.1` - Full capability model
  - `gpt-4.1-mini` - Efficient model for most tasks
  - `gpt-4.1-nano` - Lightweight model
- **Legacy Models** (Still supported):
  - `gpt-4o` - Previous generation flagship
  - `gpt-4o-mini` - Previous generation efficient

**Anthropic Models:**
- **Claude 4.5 Family** (Latest):
  - `claude-sonnet-4-5-latest` - Flagship model, auto-updates
  - `claude-sonnet-4-5-20250929` - Pinned Sonnet version from September 2025
  - `claude-haiku-4-5-latest` - Fast model, auto-updates
- **Claude 3.7 Family**:
  - `claude-3-7-sonnet-latest` - Auto-updates
  - `claude-3-7-sonnet-20250219` - Pinned version from February 2025
- **Claude 3.5 Family**:
  - `claude-3-5-sonnet-latest` - Auto-updates
  - `claude-3-5-sonnet-20241022` - Pinned version from October 2024
  - `claude-3-5-haiku-latest` - Fast model

**Google Gemini Models:**
- **Gemini 2.5 Family** (Latest):
  - `gemini-2.5-pro` - Flagship reasoning and multimodal
  - `gemini-2.5-flash` - Fast, efficient
- **Gemini 2.0 Family**:
  - `gemini-2.0-flash` - Experimental fast model
- **Gemini 1.5 Family** (Stable):
  - `gemini-1.5-pro` - Production-stable flagship
  - `gemini-1.5-flash` - Production-stable efficient

**Note**: Model names like `gpt-5-mini`, `gpt-4.1`, and `gpt-4.1-mini` used in this codebase are valid OpenAI model identifiers. The GPT-5 family are reasoning models that require `temperature=0` (automatically handled in the code).

### MCP Server Usage Guidelines

When working with the MCP server, follow the patterns established in `mcp_server/cursor_rules.md`:

- Always search for existing knowledge before adding new information
- Use specific entity type filters (`Preference`, `Procedure`, `Requirement`)
- Store new information immediately using `add_memory`
- Follow discovered procedures and respect established preferences