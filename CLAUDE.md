# CLAUDE.md — Claude Code Project Guidelines

See [AGENTS.md](AGENTS.md) for authoritative, binding instructions for AI agents.

### Quick Commands:
- Validate strategies: `python3 scripts/validate_strategies.py`
- Run reference engine smoke tests: `python3 strategies/paper-trading/T15-mica-cross-basis/reference_engine.py`

### Key Invariants:
- Platform agnostic (no hardcoded paths like `/home/...`)
- Delta-neutrality (`|delta| <= 0.0001 BTC`)
- Stablecoin de-peg circuit breaker (`<= 100 bps`)
- Maker-only execution (`POST_ONLY`)
