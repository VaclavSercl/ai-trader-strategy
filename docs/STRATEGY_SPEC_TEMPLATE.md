# 📑 Strategy Specification Standard & Template (RFC-001)

Every strategy submitted or stored in this repository must contain the following standard files within `<stage_dir>/<STRATEGY_ID>-<slug>/` (under `01-live-production/`, `02-paper-trading/`, `03-backtested/`, or `04-proposals/`):

1. `README.md` — Formal mathematical, financial, and execution specification.
2. `AI_GENERATION_PROMPT.md` — Master prompt enabling any AI agent to recreate and deploy the strategy on any server.
3. `PERFORMANCE_HISTORY.md` — Historical track record, backtest results, and annualized yield (% p.a.).
4. `SPECIFICATION.json` — Machine-readable JSON metadata for autonomous AI ingestion.

*(Note: Concrete execution engine code belongs to target execution repositories, keeping this registry clean, platform-agnostic, and purely descriptive).*

---

## 1. Specification Template (`README.md`)

```markdown
# Strategy [ID]: [Full Strategy Name]

## 1. Executive Summary & Market Edge
- **Asset Classes Traded**: [e.g. BTC, ETH, USD, EUR, USDC, USDT]
- **Market Venues**: [e.g. Venue A Spot, Venue B Perpetual Futures]
- **Target Annualized Yield (% p.a.)**: [e.g. 25% - 35% p.a.]
- **Expected Sharpe Ratio**: [e.g. > 5.0]
- **Maximum Expected Drawdown**: [e.g. < 0.5%]
- **Core Economic Edge**: [Explain why the edge persists—regulatory segregation, funding contango, structural rebate]

## 2. Mathematical & Financial Model
### 2.1 Asset Relationship & Synthetic Pricing
[Mathematical formulas, e.g., cross-rate ratios, synthetic synthetic index]

### 2.2 Stochastic Process & Signal Generation
[Ornstein-Uhlenbeck SDE, cointegration test, rolling Z-score]

### 2.3 Portfolio Allocation & Delta Neutrality
[Proof of zero directional delta, position sizing formula]

## 3. Execution & Microstructure
- **Order Types**: Post-only Maker orders to earn rebates / avoid taker fees.
- **Queue Priority Model**: Fill estimation based on depth level and orderbook turnover.
- **Slippage & Cost Model**: Fee schedule and funding rate accounting.
```

---

## 2. Metadata JSON Schema (`SPECIFICATION.json`)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "id": "T15",
  "name": "MiCA Cross-Currency Basis & Triangular Synthetic Carry",
  "category": "Statistical Arbitrage / Carry",
  "version": "1.0.0",
  "target_annual_yield_pct": 28.4,
  "max_drawdown_pct": 0.131,
  "sharpe_ratio": 14.60,
  "delta_neutral": true,
  "execution_style": "MAKER_ONLY",
  "base_assets": ["BTC"],
  "quote_currencies": ["USD", "EUR", "USDC", "USDT"],
  "ai_autonomy_level": "ZERO_HUMAN_IN_THE_LOOP",
  "status": "LIVE_PAPER"
}
```
