# 🤖 Master AI Generation Prompt: Strategy T16 (Pullback Flow + Avellaneda-Stoikov)

```markdown
You are a Principal Quantitative Researcher and High-Frequency Microstructure Architect specializing in order flow analysis, inventory skew models, and Bitcoin-standard algorithmic execution.

### TASK:
Design, implement, backtest, and generate an autonomous, production-grade trading daemon for Strategy T16: Micro-Impulse Pullback Flow with Avellaneda-Stoikov Inventory Skew on spot Bitcoin (BTC/USD).

### CORE CONSTRAINTS:
1. PLATFORM AGNOSTIC: Strictly zero machine-specific, local-user, or hardware-specific paths. The code must run seamlessly on any standard POSIX Linux, macOS, Windows system, or Docker container.
2. ZERO HUMAN IN THE LOOP (ZITL): Completely self-governing execution with automated health checks, state rehydration, and self-calibration.
3. BITCOIN STANDARD INVARIANT: The supreme accounting unit is satoshi. $P(\text{ruin}) \to 0$. Spot Bitcoin inventory must NEVER be liquidated into fiat at a loss ($\text{ExitPrice} \ge \text{EntryPrice} + \text{Fees} + \text{TickSize}$).
4. MULTI-SLOT CONCURRENCY: Manage up to 10 independent position slots, each sized at exactly 10% of available equity.

### MATHEMATICAL SPECIFICATION:

1. Micro-Impulse Order Flow Indicator:
   $$\text{Flow}_t = \frac{\sum_{i=1}^W \text{Vol}_{\text{buy}, i} - \sum_{i=1}^W \text{Vol}_{\text{sell}, i}}{\sum_{i=1}^W \text{Vol}_{\text{buy}, i} + \sum_{i=1}^W \text{Vol}_{\text{sell}, i}} \in [-1.0, 1.0]$$
   - Rolling trade window $W = 25$ ticks (~20 seconds).
   - High-Water Mark ($\text{HWM}_t$): Rolling maximum over 100 ticks.
   - Entry Dip Trigger: $P_t < \text{HWM}_t \times 0.9992$ (8 bps discount).
   - Entry Condition: $\text{Flow}_t > 0.08$ AND $P_t < \text{HWM}_t \times 0.9992$ AND $\text{OpenPositions} < 10$.

2. Avellaneda-Stoikov Inventory Skew:
   $$r(s, q, t) = s - q \cdot \gamma \cdot \sigma^2 \cdot (T - t)$$
   - Target inventory: $I_{\text{target}} = 0.30$ (30% of portfolio equity in spot BTC).
   - $q = \frac{\text{BTC}_{\text{held}} \cdot s}{\text{Equity}_{\text{total}}} - I_{\text{target}}$.
   - Asymmetric quotation: Tighten ask spread when $q > 0$; tighten bid spread when $q < 0$.

3. Dynamic ATR Take-Profit:
   $$\text{TP} = \text{EntryPrice} + \text{clamp}\left(0.5 \times \text{ATR}_{14},\; \$25.00,\; \$120.00\right)$$
   Enforce minimum $\$25.00 \text{ USD}$ profit floor to maintain $> 2.5\times$ clearance above venue bid-ask spread.

4. Microstructure Confirmation Gates:
   - Hawkes Liquidation Cascade Brake: Block entries if $Z_{\text{sell}} \ge 2.5$ and $\lambda_{\text{sell}} > \lambda_{\text{buy}}$.
   - Multi-Level L2 Depth Queue Confirmation: Block entries if L2 ask wall heavily dominates ($\text{Imbalance}_{\text{L2}} < -0.35$).
   - Hawkes Buy Clustering Conviction Boost: Elevate priority if $Z_{\text{buy}} \ge 1.2$.
   - Directional VPIN Filter: Block entries if sell-side toxic volume exceeds threshold ($\text{VPIN}_{\text{sell}} > 0.82$).

### REQUIRED ARTIFACTS:
1. `t16_engine.py` (or Rust `t16_engine.rs`): State machine implementing flow calculation, HWM tracking, Hawkes excitation, L2 queue validation, and Avellaneda-Stoikov reservation pricing.
2. `test_t16_strategy.py`: Comprehensive test battery verifying:
   - Flow calculation and HWM dip accuracy.
   - Bitcoin Standard no-loss exit invariant.
   - Hawkes liquidation cascade suppression.
   - Multi-slot concurrency boundaries (10 slots @ 10% sizing).
3. `SPECIFICATION.json`: Conforming metadata specification for autonomous AI registry.
4. `PERFORMANCE_REPORT.md`: Empirical performance summary documenting +48.5% p.a., Sharpe 4.85, and Max Drawdown 0.18%.
```
