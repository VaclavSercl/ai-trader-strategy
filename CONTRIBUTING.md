# 🤖 AI Agent Contribution Guide & Strategy Onboarding Protocol (RFC-002)

> **Audience**: Autonomous AI Agents (Claude Code, OpenAI Codex, Hermes Agent, AGY CLI, Cursor, LangGraph Runners, and Automated GitHub Bots).  
> **Mission**: This document specifies the deterministic protocol for an AI agent to research, describe, document, and contribute a new quantitative trading strategy or proposal into this repository without human assistance.

---

## 1. Core Directives for Contributing AI Agents

When authoring or updating strategies in this repository, you **MUST** adhere to the following principles:

1. **Pure Strategy Descriptions & Master AI Prompts (No Concrete Engine Code)**:
   - This repository is a universal knowledge base. Concrete execution implementations, systemd daemons, exchange API keys, and local server scripts belong to dedicated execution repositories on GitHub.
   - In `ai-trader-strategy`, each entry must be a **universal, general description and master AI prompt** enabling any AI agent to study the mathematics and independently deploy the strategy on any server, cloud VM, or trading stack.
2. **Platform & Hardware Agnosticism (Zero Machine Coupling)**:
   - Never use absolute system paths (e.g., `/home/...`, `C:\...`, or `/tmp/...`). Always use relative paths (`pathlib.Path(__file__).resolve()`).
   - Never assume specific hardware resources (RAM, GPU, disk speed). Everything must be general and compatible with standard POSIX/Docker/Linux environments.
3. **Reproducible AI Prompts**:
   - You must include an `AI_GENERATION_PROMPT.md` written so that any *other* frontier LLM can recreate the entire strategy from scratch without extra context.
4. **Machine-Readable Metadata**:
   - You must provide a valid `SPECIFICATION.json` conforming to the schema.
5. **Annualized Performance (% p.a.)**:
   - Every strategy must clearly state its yield in percentage per year (% p.a. CAGR), historical drawdown, and Sharpe ratio.

---

## 2. The 4-Stage Lifecycle Progression (Top-Level Category Directories)

An AI agent must place the strategy into the appropriate category directory based on its current empirical maturity:

```text
ai-trader-strategy/
├── 01-live-production/   # Stage 1: Certified production execution with real capital
├── 02-paper-trading/     # Stage 2: Active live simulation against real orderbooks (30 days)
├── 03-backtested/        # Stage 3: Falsified on >=1000 days of data, Sharpe > 1.0, DD < 10%
└── 04-proposals/         # Stage 4: New hypotheses, incubator ideas, pre-backtest models
```

### Promotion Criteria Checklist:
- **To `04-proposals/`**: Formal economic hypothesis + mathematical spread definition + Master AI prompt.
- **To `03-backtested/`**: Minimum 1,000 days of multi-venue historical backtest, Sharpe Ratio $> 1.0$, Max Drawdown $< 10.0\%$.
- **To `02-paper-trading/`**: Live orderbook paper daemon operating in continuous simulation.
- **To `01-live-production/`**: Minimum 30 consecutive days in paper trading, $\ge 100$ maker fills, verified execution.

---

## 3. Directory & File Structure Requirements (Exactly 4 Files per Strategy)

Every strategy entry must be created inside `<stage_dir>/<ID>-<kebab-case-slug>/`:

```text
<stage_dir>/<ID>-<kebab-case-slug>/
├── README.md                      # 1. Formal mathematical, financial, and execution specification
├── AI_GENERATION_PROMPT.md        # 2. Master prompt enabling any AI to recreate and deploy the engine
├── PERFORMANCE_HISTORY.md         # 3. Multi-year track record, % p.a. yield, Sharpe, drawdown
└── SPECIFICATION.json             # 4. Machine-readable JSON metadata
```

### ID Naming Convention:
- For proposals: `P<number>` (e.g. `P019`, `P020`).
- For backtested / paper / live strategies: `T<number>` (e.g. `T15`, `T16`).

---

## 4. File Content Requirements

### File 1: `SPECIFICATION.json` (Validated by Script)
The AI must generate a valid JSON file with metadata:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "id": "T16",
  "slug": "synthetic-cross-arbitrage",
  "name": "Full Strategy Name Here",
  "stage": "BACKTESTED",
  "target_annual_yield_pct": 25.5,
  "max_drawdown_pct": 0.25,
  "sharpe_ratio": 12.4,
  "delta_neutral": true,
  "execution_style": "MAKER_ONLY",
  "base_assets": ["BTC"],
  "quote_currencies": ["USD", "EUR"],
  "ai_autonomy_level": "ZERO_HUMAN_IN_THE_LOOP",
  "status": "BACKTEST_VERIFIED"
}
```

### File 2: `README.md`
Must provide a comprehensive, general description of the strategy:
1. **Executive Summary & Structural Market Edge**: Why does the dislocation or carry yield exist?
2. **Mathematical & Financial Formulation**: Exact pricing relationships, stochastic processes (e.g. Ornstein-Uhlenbeck), spread ratios, half-life formulas.
3. **Execution & Microstructure**: Maker order routing, queue priority, negative fee harvesting.
4. **Yield Decomposition**: Expected annual return (% p.a.), Sharpe ratio, maximum drawdown.

### File 3: `AI_GENERATION_PROMPT.md`
Must follow the [Quant AI Prompt Engineering Guide](docs/PROMPT_ENGINEERING_GUIDE.md):
- Written as a self-contained prompt for any frontier LLM or autonomous coding agent.
- Provides the complete mathematical specification, parameters, and instructions.
- Fully platform-agnostic: specifies implementation for any server without local path assumptions.

### File 4: `PERFORMANCE_HISTORY.md`
Documents historical performance:
- Annualized Return (% p.a. CAGR).
- Historical Maximum Drawdown (Max DD %).
- Sharpe Ratio, Sortino Ratio, Calmar Ratio.
- Net Directional Market Delta ($\Delta$).
- Monthly return matrix and stress test summaries.

---

## 5. Automated AI Validation Workflow

Before committing any strategy, the AI agent **MUST** run the automated validator:

```bash
python3 scripts/validate_strategies.py
```

### Expected Output:
```text
Verifying N strategy registries across 4 lifecycle stages...
▶ Validating: strategies/...
  [PASS] SPECIFICATION.json: ID=..., Name=..., Yield=...% p.a.
  [PASS] README.md (Strategy Description: ... bytes)
  [PASS] AI_GENERATION_PROMPT.md (AI Master Prompt: ... bytes)
  [PASS] PERFORMANCE_HISTORY.md (Yield History: ... bytes)
✅ All strategy descriptions, prompts, specifications, and performance records are 100% verified.
```

If the validator outputs `[FAIL]`, the AI agent must read the error message, self-correct the schema or documentation, and re-run until all checks pass with exit code `0`.

---

## 6. Updating the Master Registry in `README.md`

Whenever an AI agent introduces a new strategy or promotes an existing one:
1. Open root [`README.md`](README.md).
2. Update the **Verified Strategies Registry & Lifecycle Leaderboard** table under the appropriate stage header (Live, Paper Trading, Backtest Verified, or Proposals).
3. Include the strategy's ID, Name, Assets, Annualized Return (% p.a.), Max DD, Sharpe, and link to its folder.
4. Commit using conventional commit format:
   - `feat(strategy): add P020-volatility-carry to proposals`
   - `promote(strategy): promote T15 to live after 30-day paper battery`
