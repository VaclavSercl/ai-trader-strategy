# 🤖 Master AI Generation Prompt: Strategy T14 (Triangular FX Dislocation)

```markdown
You are a Principal Quantitative Trader specializing in high-frequency statistical arbitrage and cross-currency triangulation.

### TASK:
Implement a platform-agnostic, zero-human-in-the-loop triangular arbitrage engine exploiting synthetic cross-rate dislocations between BTC, USD, and EUR.

### CONSTRAINTS:
1. PLATFORM AGNOSTIC: Use standard Python (>=3.10), environment variables, and zero machine-specific paths.
2. ZERO TAKER FEES: The engine must use Post-Only Maker orders. On venues with 0.00% maker fees, all gross dislocation is captured as net profit.
3. ABSOLUTE INVENTORY LIMIT: No unhedged foreign exchange inventory may be carried. Triangular cycles must close atomically.

### MATHEMATICAL SPECIFICATION:
- Synthetic Price: $P_{\text{synthetic}} = P(\text{BTC/USD}) / P(\text{EUR/USD})$
- Dislocation: $\text{Dislocation (bps)} = \frac{P_{\text{synthetic}} - P(\text{BTC/EUR})}{P(\text{BTC/EUR})} \times 10,000$
- Signal Trigger: Execute when $|\text{Dislocation}| \ge 5.0 \text{ bps}$.

### DELIVERABLES:
1. `t14_engine.py`: Triangular opportunity detector and signal generator.
2. `test_t14_strategy.py`: Test battery testing synthetic pricing accuracy, zero taker fee invariant, and atomic cycle execution.
3. `SPECIFICATION.json`: Metadata schema with performance parameters.
```
