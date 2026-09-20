# AGENTS.md — Authoritative Directives for AI Coding Agents

> **ATTENTION AI AGENTS (Claude Code, OpenAI Codex, Hermes Agent, Devin, Cursor, Copilot, AGY, and Autonomous Bots)**:  
> This file contains **MANDATORY, BINDING INSTRUCTIONS** for interacting with, developing, and contributing strategies to the `ai-trader-strategy` repository.  
> You must strictly observe the architectural constraints, lifecycle pipeline, and validation gates defined herein.

---

## 1. Project Mission & Operational Invariants

This repository is an authoritative, platform-agnostic library of quantitative and statistical arbitrage strategies managed **100% autonomously by AI agents — Zero Human in the Loop (ZITL)**.

### Non-Negotiable Invariants (NEVER OVERRIDE):
1. **PLATFORM & HARDWARE AGNOSTIC**:
   - **NEVER** write machine-specific, user-specific, or hardware-dependent paths (e.g. `/home/...`, `C:\...`, `/tmp/...`).
   - Use relative paths via `pathlib.Path(__file__).resolve()`.
   - All runtime settings must be configurable via standard environment variables.
2. **ABSOLUTE DELTA NEUTRALITY**:
   - Any multi-leg carry or basis strategy must enforce $|\Delta_{\text{net}}| \le 0.0001 \text{ BTC}$ ($Q_{\text{spot}} + Q_{\text{perp}} = 0$).
3. **DETERMINISTIC CIRCUIT BREAKERS**:
   - Immediate halt if any stablecoin (USDC, USDT, FDUSD) deviates $> 50 \text{ bps}$ ($0.50\%$) from $\$1.0000$.
   - Max Drawdown hard stop: $< 10.0\%$ (historical limit $< 0.5\%$).
4. **POST-ONLY MAKER EXECUTION**:
   - All order routing must specify maker-only flags (`POST_ONLY`) to harvest exchange rebates and eliminate taker fees.

---

## 2. Strategy Lifecycle Stages (`strategies/`)

Every strategy belongs to exactly one of the 4 lifecycle folders:

| Directory | Stage | Entry Criteria |
| :--- | :--- | :--- |
| `strategies/proposals/<ID>-<slug>/` | **1. Proposals & Incubator** | Formal economic hypothesis + mathematical spread definition + Master AI Prompt. |
| `strategies/backtested/<ID>-<slug>/` | **2. Backtest Verified** | $\ge 1,000$ days multi-venue data, Sharpe $> 1.0$, Max DD $< 10\%$, all F1-F7 gates passed. |
| `strategies/paper-trading/<ID>-<slug>/` | **3. Paper Trading** | Completed Python reference engine, live orderbook paper daemon running in continuous simulation. |
| `strategies/live/<ID>-<slug>/` | **4. Live Production** | $\ge 30$ consecutive days in paper trading without invariant violations, $\ge 100$ maker fills, zero slippage. |

---

## 3. Required Files per Strategy Entry

Whenever you create or modify a strategy in `strategies/<stage>/<ID>-<slug>/`, you **MUST** ensure all 4 standard files exist:

1. `README.md` — Formal mathematical equations, stochastic model (e.g. Ornstein-Uhlenbeck), and risk invariants.
2. `AI_GENERATION_PROMPT.md` — Complete, self-contained master prompt allowing any *other* AI agent to recreate the strategy from scratch.
3. `PERFORMANCE_HISTORY.md` — Empirical track record, annualized return (**`% p.a. CAGR`**), Sharpe, Sortino, Max Drawdown, and monthly returns matrix.
4. `SPECIFICATION.json` — Machine-readable JSON metadata strictly adhering to the schema.
5. `reference_engine.py` — (Required for stages 2–4) Zero-external-dependency Python implementation.

---

## 4. Autonomous Validation Command (MANDATORY BEFORE COMMIT)

Before committing changes, you **MUST** run the automated validator:

```bash
python3 scripts/validate_strategies.py
```

- **Exit Code 0**: All strategy JSON schemas and reference engine smoke tests passed. You may commit.
- **Exit Code 1**: Failure detected. You must parse the error output, fix the discrepancy, and re-run until it passes.

---

## 5. Git Commit & Documentation Conventions

- Commit messages must follow Conventional Commits:
  - `feat(strategy): add P020-volatility-carry to proposals`
  - `docs(strategy): update T15 paper trading performance`
  - `promote(strategy): promote T15 from paper-trading to live`
- When adding a strategy or changing its stage, you **MUST** update the master table in root [`README.md`](README.md).
- For complete developer guidelines and RFC-001/RFC-002 specs, see [`CONTRIBUTING.md`](CONTRIBUTING.md).
