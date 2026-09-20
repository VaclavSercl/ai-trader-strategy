# CLAUDE.md — Claude Code Project Guidelines

See [AGENTS.md](AGENTS.md) for authoritative, binding instructions for AI agents.

### Repository Purpose:
- This repository is a platform-agnostic **knowledge registry of quantitative trading strategy descriptions, mathematical models, performance histories (% p.a.), and master AI prompts**.
- Actual implementation code and private execution pipelines reside in separate execution repositories. Do not commit concrete implementation scripts here.

### Quick Commands:
- Validate strategy specifications, descriptions, prompts, and performance histories:
  ```bash
  python3 scripts/validate_strategies.py
  ```

### Key Standards:
- Platform & hardware agnostic: completely general descriptions and prompts for any server, OS, or AI agent.
- Every strategy entry must contain: `README.md`, `AI_GENERATION_PROMPT.md`, `PERFORMANCE_HISTORY.md`, `SPECIFICATION.json`.
