# Graphiti MCP Server - Claude Memory Setup

Este directorio contiene la configuración para usar Graphiti como sistema de memoria episódica para Claude Desktop y Claude Code.

## Arquitectura

```
┌─────────────────────────────────────────────────────────────────┐
│                    CLIENTES CLAUDE (MCP)                        │
│  ┌──────────────────┐         ┌──────────────────┐              │
│  │  Claude Desktop  │         │   Claude Code    │              │
│  │   (macOS app)    │         │    (terminal)    │              │
│  └────────┬─────────┘         └────────┬─────────┘              │
│           │ stdio                      │ stdio                  │
│           └────────────┬───────────────┘                        │
│                        ▼                                        │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │              GRAPHITI MCP SERVER                            ││
│  │           (config-claude-memory.yaml)                       ││
│  │  • Transport: stdio                                         ││
│  │  • LLM: Gemini 2.5 Flash                                    ││
│  │  • Embedder: Gemini embedding-001                           ││
│  └────────────────────────┬────────────────────────────────────┘│
│                           │ bolt://localhost:7696               │
│                           ▼                                     │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                     NEO4J                                   ││
│  │           (docker-compose-claude-memory.yml)                ││
│  │  • Puerto: 7696 (bolt), 7475 (http)                         ││
│  │  • Password: claudememory                                   ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

## Requisitos

- **uv**: Gestor de paquetes Python (https://docs.astral.sh/uv/)
- **Docker**: Para Neo4j
- **API Keys**: Google API Key (Gemini) y/o OpenAI API Key

## Instalación Paso a Paso

### 1. Clonar el repositorio

```bash
git clone https://github.com/pepo1275/graphiti.git
cd graphiti
git checkout claude-local-stdio
```

### 2. Instalar uv (si no está instalado)

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Verificar instalación
uv --version
# Anotar la ruta, típicamente: ~/.local/bin/uv
which uv
```

### 3. Levantar Neo4j

```bash
cd mcp_server/config
docker compose -f docker-compose-claude-memory.yml up -d

# Verificar que está corriendo
docker ps | grep claude-memory-neo4j
```

### 4. Configurar API Keys

Crear archivo `.env.claude-memory` basado en el ejemplo:

```bash
cp .env.claude-memory.example .env.claude-memory
# Editar con tus API keys
```

Contenido del archivo:
```bash
# Google Gemini (REQUERIDO - usado para LLM y Embeddings)
GOOGLE_API_KEY=tu_google_api_key_aqui

# OpenAI (OPCIONAL - alternativo)
OPENAI_API_KEY=tu_openai_api_key_aqui

# Neo4j (ya configurado en docker-compose)
NEO4J_URI=bolt://localhost:7696
NEO4J_USER=neo4j
NEO4J_PASSWORD=claudememory
```

### 5. Configurar Claude Desktop (macOS)

Ubicación del archivo de configuración:
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

Añadir la siguiente entrada en `mcpServers`:

```json
{
  "mcpServers": {
    "graphiti-memory": {
      "command": "/RUTA/A/TU/.local/bin/uv",
      "args": [
        "run",
        "--directory",
        "/RUTA/A/TU/graphiti/mcp_server",
        "--project",
        ".",
        "main.py",
        "--transport",
        "stdio",
        "--config",
        "/RUTA/A/TU/graphiti/mcp_server/config/config-claude-memory.yaml"
      ],
      "env": {
        "NEO4J_URI": "bolt://localhost:7696",
        "NEO4J_USER": "neo4j",
        "NEO4J_PASSWORD": "claudememory",
        "OPENAI_API_KEY": "tu_openai_api_key",
        "GOOGLE_API_KEY": "tu_google_api_key"
      }
    }
  }
}
```

**Reemplazar:**
- `/RUTA/A/TU/.local/bin/uv` → resultado de `which uv`
- `/RUTA/A/TU/graphiti/mcp_server` → ruta absoluta al directorio mcp_server

### 6. Configurar Claude Code

Ubicación del archivo de configuración:
```
~/.claude.json
```

Añadir la siguiente entrada en `mcpServers`:

```json
{
  "mcpServers": {
    "graphiti-memory": {
      "type": "stdio",
      "command": "/RUTA/A/TU/.local/bin/uv",
      "args": [
        "run",
        "--directory",
        "/RUTA/A/TU/graphiti/mcp_server",
        "--project",
        ".",
        "main.py",
        "--transport",
        "stdio",
        "--config",
        "/RUTA/A/TU/graphiti/mcp_server/config/config-claude-memory.yaml"
      ],
      "env": {
        "NEO4J_URI": "bolt://localhost:7696",
        "NEO4J_USER": "neo4j",
        "NEO4J_PASSWORD": "claudememory",
        "OPENAI_API_KEY": "tu_openai_api_key",
        "GOOGLE_API_KEY": "tu_google_api_key"
      }
    }
  }
}
```

### 7. Reiniciar los clientes

- **Claude Desktop**: Cerrar y volver a abrir la aplicación
- **Claude Code**: Iniciar nueva sesión con `claude`

### 8. Verificar la conexión

En cualquier cliente, pedir:
```
Usa la herramienta get_status de graphiti-memory para verificar la conexión
```

Respuesta esperada: estado "running" y conexión a Neo4j exitosa.

## Herramientas Disponibles

| Herramienta | Descripción |
|-------------|-------------|
| `add_memory` | Añadir episodios a la memoria |
| `search_nodes` | Buscar entidades en el grafo |
| `search_memory_facts` | Buscar relaciones/hechos |
| `get_episodes` | Obtener episodios recientes |
| `get_status` | Verificar estado del servidor |
| `clear_graph` | Limpiar memoria (usar con cuidado) |

## Uso de add_memory con JSON

**IMPORTANTE**: Cuando `source="json"`, el `episode_body` debe ser un string JSON escapado, no un diccionario Python:

```python
# CORRECTO
add_memory(
    name="Datos estructurados",
    episode_body='{"key": "value", "nested": {"a": 1}}',
    source="json"
)

# INCORRECTO - causará error de validación
add_memory(
    name="Datos estructurados",
    episode_body={"key": "value"},  # NO pasar dict directamente
    source="json"
)
```

## Estrategia de group_id

Los `group_id` permiten organizar la memoria por dominio:

| group_id | Uso |
|----------|-----|
| `claude_desktop_sync` | Uso general Claude Desktop |
| `claude_code_sessions` | Sesiones Claude Code |
| `graphiti_meta_analysis` | Todo sobre Graphiti |
| `{proyecto}_dev` | Por proyecto específico |

## Troubleshooting

### Error: "Neo4j connection refused"
```bash
# Verificar que Neo4j está corriendo
docker ps | grep neo4j
# Si no está, levantarlo
docker compose -f docker-compose-claude-memory.yml up -d
```

### Error: "MCP server not found"
- Verificar que la ruta a `uv` es correcta
- Verificar que la ruta al `mcp_server` es correcta
- Verificar que las API keys están configuradas

### Error: "episode_body validation error"
- Para `source="json"`, pasar el JSON como string, no como dict

## Archivos en este directorio

| Archivo | Descripción |
|---------|-------------|
| `config-claude-memory.yaml` | Configuración principal del servidor |
| `docker-compose-claude-memory.yml` | Docker Compose para Neo4j |
| `.env.claude-memory.example` | Plantilla de variables de entorno |
| `templates/` | Plantillas de configuración para clientes |
| `README-SETUP.md` | Este archivo |

## Referencias

- [Graphiti Documentation](https://github.com/getzep/graphiti)
- [MCP Protocol](https://modelcontextprotocol.io/)
- [Claude Desktop Config](https://claude.ai/docs/desktop)
