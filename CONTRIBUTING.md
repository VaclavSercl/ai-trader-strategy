# 🤖 AI Agent Contribution Guide & Strategy Onboarding Protocol (RFC-002)

> **Audience**: Autonomous AI Agents (Claude Code, OpenAI Codex, Hermes Agent, AGY CLI, Cursor, LangGraph Runners, and Automated GitHub Bots).  
> **Mission**: This document specifies the deterministic protocol for an AI agent to research, structure, validate, and contribute a new quantitative strategy or proposal into this repository without human assistance.

---

## 1. Core Directives for Contributing AI Agents

When authoring or updating strategies in this repository, you **MUST** adhere to the following principles:

1. **Platform & Hardware Agnosticism (Zero Machine Coupling)**:
   - Never use absolute system paths (e.g., `/home/...`, `C:\...`, or `/tmp/...`). Always use relative paths (`pathlib.Path(__file__).resolve()`).
   - Never assume specific hardware resources (RAM, GPU, disk speed). Everything must execute in standard POSIX/Docker environments using standard library Python 3.10+ or standard environment variables.
2. **Reproducible AI Prompts**:
   - You must include an `AI_GENERATION_PROMPT.md` written so that any *other* frontier LLM can recreate the entire strategy from scratch without extra context.
3. **Machine-Readable Metadata**:
   - You must provide a valid `SPECIFICATION.json` conforming to the RFC-001 schema.

---

## 2. The 4-Stage Lifecycle Progression

An AI agent must place the strategy into the appropriate stage directory based on its current empirical maturity:

```text
strategies/
├── proposals/          # Stage 1: New hypotheses, incubator ideas, untracked models
├── backtested/         # Stage 2: Falsified on >=1000 days of data, Sharpe > 1.0, DD < 10%
├── paper-trading/      # Stage 3: Active live simulation against real orderbooks (30 days)
└── live/               # Stage 4: Certified production execution with real capital
```

### Promotion Criteria Checklist:
- **To `proposals/`**: Formal economic hypothesis + mathematical spread definition + AI generation prompt.
- **To `backtested/`**: Minimum 1,000 days of multi-venue historical backtest, Sharpe Ratio $> 1.0$, Max Drawdown $< 10.0\%$.
- **To `paper-trading/`**: Reference engine completed, live orderbook paper daemon operating in continuous simulation.
- **To `live/`**: Minimum 30 consecutive days in paper trading, $\ge 100$ maker fills, verified execution.

---

## 3. Directory & File Structure Requirements

Every strategy entry must be created inside `strategies/<stage>/<ID>-<slug>/`:

```text
strategies/<stage>/<ID>-<kebab-case-slug>/
├── README.md                      # 1. Formal mathematical, financial, and execution specification
├── AI_GENERATION_PROMPT.md        # 2. Master prompt enabling any AI to recreate the engine
├── PERFORMANCE_HISTORY.md         # 3. Multi-year track record, % p.a. yield, Sharpe, drawdown
├── SPECIFICATION.json             # 4. Machine-readable JSON metadata (RFC-001)
└── reference_engine.py            # 5. Zero-dependency Python reference engine (Stage 2-4)
```

### ID Naming Convention:
- For proposals: `P<number>` (e.g. `P019`, `P020`).
- For backtested / paper / live strategies: `T<number>` (e.g. `T15`, `T16`).

---

## 4. File Content Templates

### File 1: `SPECIFICATION.json` (Strictly Validated by CI)
The AI must generate a valid JSON file with this exact schema:

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
Must follow the RFC-001 Strategy Specification format:
1. **Executive Summary & Structural Market Edge**: Why does the alpha exist?
2. **Mathematical & Financial Formulation**: Exact differential equations, stochastic processes, spread ratios.
3. **Execution & Microstructure**: Maker order routing, queue priority, rebate harvesting.
4. **Performance Targets**: Expected annual yield (% p.a.), Sharpe ratio, maximum drawdown.

### File 3: `AI_GENERATION_PROMPT.md`
Must follow the [Quant AI Prompt Engineering Guide](docs/PROMPT_ENGINEERING_GUIDE.md):
- Clearly state the persona: Principal Quantitative Trader & Systems Architect.
- Include all mathematical formulas and boundary conditions.
- Specify exact deliverables required (`engine.py`, `tests.py`, `daemon.py`, `SPECIFICATION.json`).
- Ensure no machine-specific or environment-specific paths are mentioned.

### File 4: `PERFORMANCE_HISTORY.md`
Must document performance according to GIPS standards:
- Annualized Return (% p.a. CAGR).
- Historical Max Drawdown (Max DD %).
- Sharpe Ratio, Sortino Ratio, Calmar Ratio.
- Net Directional Market Delta ($\Delta$).
- Monthly return matrix and historical liquidity shock stress tests.

---

## 5. Automated AI Validation Workflow

Before committing any strategy, the AI agent **MUST** run the automated validator:

```bash
python3 scripts/validate_strategies.py
```

### Required Output:
```text
Found N strategy specification files.
  [PASS] strategies/.../SPECIFICATION.json: ID=..., Name=...
Running reference engines:
  [PASS] reference_engine.py
All strategy specifications and engines verified successfully.
```

If the validator outputs `[FAIL]`, the AI agent must read the error message, self-correct the schema or code, and re-run until all checks pass with exit code `0`.

---

## 6. Updating the Master Registry in `README.md`

Whenever an AI agent introduces a new strategy or promotes an existing one:
1. Open root [`README.md`](README.md).
2. Update the **Verified Strategies Registry & Lifecycle Leaderboard** table under the appropriate stage header (Live, Paper Trading, Backtest Verified, or Proposals).
3. Include the strategy's ID, Name, Assets, Annualized Return (% p.a.), Max DD, Sharpe, and link to its folder.
4. Commit using conventional commit format:
   - `feat(strategy): add P020-volatility-carry to proposals`
   - `promote(strategy): promote T15 to live after 30-day paper battery`
