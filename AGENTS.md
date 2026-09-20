# AGENTS.md — Authoritative Directives for AI Coding Agents

> **ATTENTION AI AGENTS (Claude Code, OpenAI Codex, Hermes Agent, Devin, Cursor, Copilot, AGY, and Autonomous Bots)**:  
> This file contains **MANDATORY, BINDING INSTRUCTIONS** for interacting with, developing, and contributing strategies to the `ai-trader-strategy` repository.  
> You must strictly observe the repository purpose, architectural constraints, lifecycle pipeline, and validation gates defined herein.

---

## 1. Project Mission & Pure Description Standard

This repository is an authoritative, universal knowledge base of quantitative and statistical arbitrage trading strategies designed for **autonomous AI agents — Zero Human in the Loop (ZITL)**.

### Core Architectural Standards:
1. **STRATEGY DESCRIPTIONS & PROMPTS ONLY (NO CONCRETE ENGINE CODE)**:
   - Concrete production implementations, exchange private keys, server daemons, and system scripts reside in separate execution repositories.
   - This repository (`ai-trader-strategy`) contains **purely general strategy descriptions, mathematical specifications, performance histories, and AI generation prompts**.
   - Every entry must be formulated so that **any AI agent can study the strategy specification and independently implement and deploy it on any arbitrary server, OS, or trading stack**.
2. **PLATFORM & HARDWARE AGNOSTIC**:
   - **NEVER** write machine-specific, user-specific, or hardware-dependent paths (e.g. `/home/...`, `C:\...`, `/tmp/...`).
   - Strategy descriptions and prompts must apply to any standard Linux/POSIX/Windows environment.
3. **REPRODUCIBILITY VIA MASTER AI PROMPTS**:
   - Every strategy must include an `AI_GENERATION_PROMPT.md` allowing any other LLM or autonomous agent to engineer the strategy from scratch.

---

## 2. Strategy Lifecycle Stages (`strategies/`)

Every strategy belongs to exactly one of the 4 lifecycle folders:

| Directory | Stage | Description |
| :--- | :--- | :--- |
| `strategies/proposals/<ID>-<slug>/` | **1. Proposals & Incubator** | Theoretical hypotheses, economic rationale, pre-backtest specifications, and AI master prompts. |
| `strategies/backtested/<ID>-<slug>/` | **2. Backtest Verified** | Strategies validated on historical multi-venue data ($\ge 1,000$ days), Sharpe $> 1.0$, Max DD $< 10\%$. |
| `strategies/paper-trading/<ID>-<slug>/` | **3. Paper Trading** | Strategies currently undergoing active live orderbook paper simulation qualification. |
| `strategies/live/<ID>-<slug>/` | **4. Live Production** | Strategies actively deployed and running with real capital in live market production. |

---

## 3. Required Files per Strategy Entry (Exactly 4 Files)

Whenever you create or modify a strategy in `strategies/<stage>/<ID>-<slug>/`, you **MUST** ensure all 4 standard descriptive files exist:

1. `README.md` — Complete, detailed strategy description: economic edge, mathematical formulation, stochastic processes, market dislocation definitions, and fee/rebate structure.
2. `AI_GENERATION_PROMPT.md` — Universal, self-contained master AI prompt allowing any other AI agent to implement the strategy on any server.
3. `PERFORMANCE_HISTORY.md` — Empirical track record, annualized return (**`% p.a. CAGR`**), Sharpe, Sortino, Max Drawdown, and performance log.
4. `SPECIFICATION.json` — Machine-readable JSON metadata with strategy ID, name, status, markets, and yield metrics.

> [!IMPORTANT]
> Do **NOT** commit concrete implementation code (e.g. `.py` scripts) into `strategies/`. Keep this repository clean as a pure strategy description and prompt library.

---

## 4. Autonomous Validation Command (MANDATORY BEFORE COMMIT)

Before committing changes, you **MUST** run the automated validator:

```bash
python3 scripts/validate_strategies.py
```

- **Exit Code 0**: All strategy descriptions, prompts, specifications, and performance records verified.
- **Exit Code 1**: Discrepancy detected. Parse the error output and resolve before committing.

---

## 5. Git Commit & Documentation Conventions

- Commit messages must follow Conventional Commits:
  - `feat(strategy): add P020-volatility-carry to proposals`
  - `docs(strategy): update T15 paper trading performance`
  - `promote(strategy): promote T15 from paper-trading to live`
- When adding a strategy or changing its stage, you **MUST** update the master table in root [`README.md`](README.md).
- For complete developer guidelines and RFC-001/RFC-002 specs, see [`CONTRIBUTING.md`](CONTRIBUTING.md).
