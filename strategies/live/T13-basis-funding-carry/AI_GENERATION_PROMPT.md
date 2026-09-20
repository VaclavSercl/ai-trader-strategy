# 🤖 Master AI Generation Prompt: Strategy T13 (Basis & Funding Carry)

```markdown
You are a Principal Quantitative Engineer specializing in delta-neutral basis carry architectures.

### TASK:
Implement a platform-agnostic, zero-human-in-the-loop cash-and-carry engine that harvests perpetual futures funding rates hedged with spot inventory.

### CONSTRAINTS:
1. PLATFORM AGNOSTIC: Use standard Python (>=3.10), environment variable configuration, and no hardcoded machine paths.
2. ZERO DIRECTIONAL RISK: Net delta must remain strictly 0.000000 BTC.
3. MAKER-ONLY EXECUTION: Spot leg (0.00% maker fee) + Perp short leg (-0.02% maker rebate). Zero taker execution allowed.
4. ISOLATED MARGIN: 1x leverage cap. Cross-margin is prohibited.

### MATHEMATICAL SPECIFICATION:
- Position Sizing: Capital is divided 50% into Spot Long BTC and 50% into USDC collateral for Short Perp.
- Funding Yield: Collect hourly payments $C_h = Q_{\text{perp}} \cdot P \cdot F_h$.
- Entry Condition: Perpetual price premium over spot $\ge +0.02\%$.
- Rebalancing Drift: If BTC price moves $\ge 30\%$ from entry, re-hedge to maintain 50/50 capital balance.

### DELIVERABLES:
1. `t13_engine.py`: Core mathematical state machine and position calculator.
2. `test_t13_strategy.py`: Unit test battery testing delta neutrality, negative fee rebate harvesting, and drift rebalancing.
3. `SPECIFICATION.json`: Metadata schema with annual yield parameters and invariants.
```
