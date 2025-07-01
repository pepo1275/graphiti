# CLAUDE_CODE_COMPLETE.md

## Project Overview

Graphiti is a Python framework for building temporally-aware knowledge graphs designed for AI agents. It enables real-time incremental updates to knowledge graphs without batch recomputation, making it suitable for dynamic environments.

**Key Features:**
- Bi-temporal data model with explicit tracking of event occurrence times
- Hybrid retrieval combining semantic embeddings, keyword search (BM25), and graph traversal
- Support for custom entity definitions via Pydantic models
- Integration with Neo4j and FalkorDB as graph storage backends

**Current Project Scope:** Adding multi-engine support (Gemini + Claude Sonnet 4) to existing OpenAI-based system while maintaining full transparency, traceability, and rollback capabilities.

---

## Current Status & Context

### ✅ Working Configuration
- **Location**: `/Users/pepo/graphiti-pepo-local`
- **Branch**: `feature/dual-embedding-engines`
- **System**: macOS (MacBook Air)
- **Python**: uv (located at `/Users/pepo/.local/bin/uv`)
- **Neo4j**: bolt://localhost:7687 (user: neo4j, password: pepo_graphiti_2025)

### ✅ Currently Operational
- **LLM**: OpenAI (gpt-4o) - **KEEP AS PRIMARY**
- **Embeddings**: OpenAI (text-embedding-3-small) - **KEEP AS PRIMARY**  
- **MCP Server**: 100% functional at `/Users/pepo/graphiti-pepo-local/mcp_server/graphiti_mcp_server.py`
- **Repository**: Synced with https://github.com/pepo1275/graphiti

### ✅ Infrastructure Ready
- **Multi-engine classes**: `config_multi_engine.py` with Pydantic schemas
- **Environment templates**: `.env.multi-engine.example`
- **Implementation files**: `mcp_dual_engine_complete.py`
- **Token Monitoring System**: Complete implementation in `graphiti_core/telemetry/`
  - See [Token Monitoring Documentation](../token_monitoring/README.md)
- **Git status**: Clean working tree, all changes committed

---

## Critical Instructions

### 🚨 MANTENER FUNCIONALIDAD EXISTENTE (OBLIGATORIO)

**NEVER break what currently works:**
- ✅ **OpenAI**: gpt-4o, gpt-4-mini (PRINCIPAL actual - NO cambiar)
- ✅ **OpenAI Embeddings**: text-embedding-3-small (PRINCIPAL actual - NO cambiar)
- ✅ **Anthropic**: claude-sonnet-4-20250514 (YA configurado - NO eliminar)

**TO ADD (without replacing existing):**
- 🆕 **Gemini**: gemini-2.5-pro, gemini-2.5-flash
- 🆕 **Gemini Embeddings**: text-embedding-005, gemini-embedding-exp-03-07
- 🆕 **Claude Sonnet 4**: Enhanced support with API key configuration

### 🛑 STOP CONDITIONS - When to Halt and Consult

**DO NOT proceed without confirmation if you encounter:**
- ❌ Errors in Gemini or Google API imports
- ❌ API key configuration failures (401, 403, etc.)
- ❌ Claude Desktop startup errors or MCP failures
- ❌ Basic tests (`add_memory`, `search_memory_nodes`) failing
- ❌ Missing dependencies or version conflicts

**ALWAYS create safety commits before:**
- 🔄 Changing MCP configuration files
- 🔄 Modifying `claude_desktop_config.json`
- 🔄 Installing new dependencies with `uv`
- 🔄 Changing critical environment variables

**Rollback procedure if anything fails:**
```bash
git reset --hard HEAD~1  # Return to previous commit
# Restore claude_desktop_config.json from backup
```

---

## Structured Development Framework

### Schema-First Multi-Engine Configuration

All development decisions must follow structured schemas for transparency and traceability:

```json
{
  "multi_engine_state": {
    "current_active": {
      "llm_engine": "openai",
      "llm_model": "gpt-4o",
      "embedding_engine": "openai", 
      "embedding_model": "text-embedding-3-small"
    },
    "available_engines": {
      "llm_engines": {
        "openai": {"status": "active", "models": ["gpt-4o", "gpt-4-mini"]},
        "anthropic": {"status": "configured", "models": ["claude-sonnet-4-20250514"]},
        "gemini": {"status": "pending", "models": ["gemini-2.5-pro", "gemini-2.5-flash"]}
      },
      "embedding_engines": {
        "openai": {"status": "active", "models": ["text-embedding-3-small", "text-embedding-3-large"]},
        "vertex_ai": {"status": "pending", "models": ["text-embedding-005"]},
        "gemini": {"status": "pending", "models": ["gemini-embedding-exp-03-07"]}
      }
    }
  }
}
```

### Mandatory Transparency Logging

```json
{
  "operation_trace": {
    "timestamp": "2025-06-30T11:30:00Z",
    "operation_type": "add_memory|search_nodes|engine_switch",
    "engine_used": "openai|anthropic|gemini",
    "model_used": "specific_model_name",
    "response_time_ms": 1500,
    "success": true,
    "tokens_used": {"input": 150, "output": 300},
    "error_details": null,
    "rollback_available": true
  }
}
```

### Engine Transition Validation

```json
{
  "engine_transition": {
    "transition_id": "uuid",
    "from_config": {"engine": "openai", "model": "gpt-4o"},
    "to_config": {"engine": "gemini", "model": "gemini-2.5-pro"},
    "reason": "performance_testing|research|fallback",
    "pre_validation_tests": ["basic_memory_test", "search_functionality"],
    "post_validation_tests": ["regression_test", "performance_benchmark"],
    "success_criteria": ["same_functionality", "acceptable_performance"],
    "rollback_plan": "specific_steps_to_revert"
  }
}
```

---

## 5-Phase Implementation Plan

### PHASE 1: VERIFICATION AND BACKUP (20 min)

**✅ CHECKPOINT 1.1 - Verify Current System**
- [x] Confirm MCP works correctly with OpenAI
- [x] Backup current Claude Desktop configuration
- [x] Verify Neo4j connectivity
- [x] Confirm repository is clean and synced

**✅ CHECKPOINT 1.2 - Repository Status** 
- [x] Current branch: `feature/dual-embedding-engines`
- [x] Multi-engine infrastructure files present
- [x] GitHub fork synchronized
- [x] No uncommitted changes

**🔄 ACTION REQUIRED:** Confirm everything works before proceeding

---

### PHASE 2: ENHANCED API PREPARATION (40 min)

**✅ CHECKPOINT 2.1 - Configure API Keys**
- [ ] Obtain/verify GOOGLE_API_KEY for Gemini (LLM + embeddings)
- [ ] Verify ANTHROPIC_API_KEY for Claude Sonnet 4
- [ ] Test API connectivity with basic calls
- [ ] Document API limits and quotas

**✅ CHECKPOINT 2.2 - Enhanced Environment Setup**
- [ ] Copy `.env.multi-engine.example` to `.env`
- [ ] Configure with OpenAI as primary + Gemini + Claude as secondary
- [ ] Add structured logging configuration
- [ ] **MAINTAIN** OpenAI as default engine

**✅ CHECKPOINT 2.3 - Expand Multi-Engine Configuration**
```python
# Expand config_multi_engine.py to include:
class LLMEngine(str, Enum):
    OPENAI = "openai"           # Current primary
    ANTHROPIC = "anthropic"     # Claude Sonnet 4
    GEMINI = "gemini"           # New addition

class EmbeddingEngine(str, Enum):
    OPENAI = "openai"           # Current primary  
    VERTEX_AI = "vertex_ai"     # Google embeddings
    GEMINI = "gemini"           # Gemini embeddings
```

**✅ CHECKPOINT 2.4 - Safety Commit**
- [ ] Add enhanced configuration files
- [ ] Commit: "feat: enhance multi-engine config for Gemini + Claude Sonnet 4"
- [ ] Push to backup: `git push origin feature/dual-embedding-engines`

---

### PHASE 3: CONSERVATIVE ACTIVATION (30 min)

**✅ CHECKPOINT 3.1 - Transparent MCP Enhancement**
- [ ] Modify MCP server to use enhanced multi-engine configuration
- [ ] Implement structured operation logging
- [ ] Add engine transition tracking
- [ ] **MAINTAIN** OpenAI as primary LLM and embeddings

**✅ CHECKPOINT 3.2 - Transparency Implementation**
```python
# Add to graphiti_mcp_server.py:
class OperationLogger:
    def log_operation(self, operation_type, engine_used, success, metadata):
        # Structured logging implementation
        
class EngineManager:
    def switch_engine(self, target_engine, reason, validation_tests):
        # Structured engine switching with validation
```

**✅ CHECKPOINT 3.3 - Functionality Verification**
- [ ] Restart Claude Desktop
- [ ] Verify `add_memory` works identically to before
- [ ] Verify `search_memory_nodes` works identically to before
- [ ] Confirm structured logging is working

**✅ CHECKPOINT 3.4 - Stability Commit**
- [ ] Document MCP enhancements
- [ ] Commit: "feat: implement transparent multi-engine MCP (OpenAI primary)"
- [ ] Push and create stable tag: `v1.0-transparent-multi-engine`

---

### PHASE 4: CONTROLLED EXPERIMENTATION (60 min)

**✅ CHECKPOINT 4.1 - Experimental Branch**
- [ ] Create: `git checkout -b experiment/multi-engine-testing`
- [ ] Push experimental branch for backup

**✅ CHECKPOINT 4.2 - Engine Testing Protocol**
```json
{
  "testing_protocol": {
    "test_cases": [
      {"operation": "add_memory", "content": "test content", "engines": ["openai", "gemini", "claude"]},
      {"operation": "search_memory_nodes", "query": "test", "engines": ["openai", "gemini", "claude"]},
      {"operation": "performance_benchmark", "engines": ["all"], "metrics": ["speed", "accuracy"]}
    ],
    "success_criteria": {
      "functionality": "all_engines_produce_valid_results",
      "performance": "acceptable_response_times", 
      "consistency": "similar_results_across_engines"
    }
  }
}
```

**✅ CHECKPOINT 4.3 - Gemini LLM Testing**
- [ ] Temporarily switch to Gemini LLM
- [ ] Run identical memory operations
- [ ] Document results in structured format
- [ ] Compare with OpenAI baseline
- [ ] **REVERT** to OpenAI as primary

**✅ CHECKPOINT 4.4 - Claude Sonnet 4 Testing**
- [ ] Temporarily switch to Claude Sonnet 4
- [ ] Run identical memory operations  
- [ ] Document performance and quality differences
- [ ] **REVERT** to OpenAI as primary

**✅ CHECKPOINT 4.5 - Embedding Engine Testing**
- [ ] Test Vertex AI embeddings (text-embedding-005)
- [ ] Test Gemini embeddings (gemini-embedding-exp-03-07)
- [ ] Compare retrieval quality with OpenAI baseline
- [ ] Document structured benchmark results

**✅ CHECKPOINT 4.6 - Experimental Documentation**
- [ ] Commit all experiments: "experiment: comprehensive multi-engine testing"
- [ ] Push experimental branch
- [ ] Return to main feature branch: `git checkout feature/dual-embedding-engines`

---

### PHASE 5: PRODUCTION CONFIGURATION (45 min)

**✅ CHECKPOINT 5.1 - Optimal Configuration Selection**
- [ ] Analyze structured test results
- [ ] Choose optimal LLM configuration based on performance data
- [ ] Choose optimal embedding configuration based on retrieval quality
- [ ] Merge valuable experimental changes

**✅ CHECKPOINT 5.2 - Production Documentation**
```markdown
# Create comprehensive documentation:
- ENGINE_COMPARISON.md: Structured benchmark results
- CONFIGURATION_GUIDE.md: How to switch between engines  
- TROUBLESHOOTING.md: Common issues and solutions
- API_LIMITS.md: Rate limits and best practices per provider
```

**✅ CHECKPOINT 5.3 - Final Implementation**
- [ ] Implement chosen production configuration
- [ ] Add engine switching commands for runtime changes
- [ ] Implement automatic fallback mechanisms
- [ ] Add comprehensive error handling with structured outputs

**✅ CHECKPOINT 5.4 - Release Preparation**
- [ ] Final commit: "feat: complete transparent multi-engine implementation"
- [ ] Create comprehensive release notes
- [ ] Tag release: `v2.0-multi-engine-complete`
- [ ] Push to GitHub for backup

---

## Development Commands

### Environment Setup
```bash
# Navigate to project
cd /Users/pepo/graphiti-pepo-local

# Check status
git status && git branch

# Install dependencies  
uv sync --extra dev

# Test current MCP server
uv run python mcp_server/graphiti_mcp_server.py --help
```

### Testing Commands
```bash
# Test MCP server manually
cd /Users/pepo/graphiti-pepo-local/mcp_server
uv run python graphiti_mcp_server.py --transport stdio --group-id pepo_phd_research

# Run tests
make test

# Format and lint
make format && make lint
```

### Claude Desktop Management
```bash
# Backup current config
cp ~/.config/Claude Desktop/claude_desktop_config.json ~/claude_desktop_config_backup.json

# Restart Claude Desktop after changes:
# 1. Quit Claude Desktop completely (Cmd+Q)
# 2. Reopen Claude Desktop  
# 3. Check for MCP errors in console
```

### Git Workflow
```bash
# Safety commits
git add . && git commit -m "feat: descriptive message"
git push origin feature/dual-embedding-engines

# Create experimental branches
git checkout -b experiment/specific-test
# Make experimental changes
git add . && git commit -m "experiment: description"  
git push origin experiment/specific-test

# Return to safe state
git checkout feature/dual-embedding-engines
```

---

## Troubleshooting & Rollback

### Structured Error Categories

```json
{
  "error_taxonomy": {
    "api_errors": {
      "authentication": ["invalid_key", "expired_token", "rate_limit"],
      "connectivity": ["timeout", "network_error", "service_unavailable"],
      "validation": ["invalid_model", "malformed_request", "quota_exceeded"]
    },
    "mcp_errors": {
      "startup": ["import_error", "config_error", "dependency_missing"],
      "runtime": ["engine_switch_failed", "memory_operation_failed", "search_failed"]
    },
    "system_errors": {
      "environment": ["missing_env_var", "invalid_path", "permission_denied"],
      "database": ["neo4j_connection_failed", "query_error", "timeout"]
    }
  }
}
```

### Rollback Procedures

**Level 1: Configuration Rollback**
```bash
git checkout HEAD~1 -- mcp_server/graphiti_mcp_server.py
git checkout HEAD~1 -- mcp_server/config_multi_engine.py
# Restart Claude Desktop
```

**Level 2: Full Commit Rollback**  
```bash
git reset --hard HEAD~1
git push origin feature/dual-embedding-engines --force
# Restore Claude Desktop config from backup
```

**Level 3: Branch Rollback**
```bash
git checkout main
git branch -D feature/dual-embedding-engines  
git checkout -b feature/dual-embedding-engines origin/feature/dual-embedding-engines
```

### Validation Tests

**Basic Functionality Test:**
```python
# Must pass after every change:
def test_basic_functionality():
    # Test 1: add_memory works
    result = add_memory("test multi-engine integration")
    assert result.success == True
    
    # Test 2: search_memory_nodes works  
    search_result = search_memory_nodes("test multi-engine")
    assert len(search_result.nodes) > 0
    
    # Test 3: current engine responds
    assert get_current_engine_status().status == "active"
```

**Performance Baseline Test:**
```python
def test_performance_baseline():
    # Response time should be reasonable
    start_time = time.time()
    result = add_memory("performance test content")
    response_time = (time.time() - start_time) * 1000
    
    assert response_time < 5000  # Less than 5 seconds
    assert result.success == True
```

---

## Next Actions

**Current Phase**: Phase 2.1 - Configure API Keys  
**Immediate Task**: Obtain GOOGLE_API_KEY and verify API connectivity
**Success Criteria**: All API keys working, structured logging active, OpenAI remaining as primary

**Claude Code Command:**
```
Implement Phase 2.1 of docs/claude_code/CLAUDE_CODE_COMPLETE.md: Configure Gemini and Claude Sonnet 4 API keys while maintaining OpenAI as primary engine. Use structured logging and validation schemas as specified.
```