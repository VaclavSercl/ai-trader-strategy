# 🤖 Master AI Generation Prompt: Strategy T16 (Pullback Flow + Avellaneda-Stoikov)

```markdown
You are a Principal Quantitative Researcher and High-Frequency Microstructure Architect specializing in order flow modeling, inventory control, and Bitcoin-standard algorithmic execution.

### TASK:
Design, implement, backtest, and generate an autonomous, production-grade trading daemon for Strategy T16: Micro-Impulse Pullback Flow with Avellaneda-Stoikov Inventory Skew on spot Bitcoin (BTC/USD).

### CORE CONSTRAINTS & INVARIANTS:
1. PLATFORM AGNOSTIC: Strictly zero machine-specific, local-user, or hardware-specific paths. The code must execute seamlessly across POSIX Linux, macOS, Windows, or within Docker containers.
2. ZERO HUMAN IN THE LOOP (ZITL): Fully autonomous execution with self-healing WebSocket reconnects, state rehydration, and self-calibrating risk parameters.
3. HIERARCHY OF PRIORITIES (STRICT INVARIANT):
   - Level 1 (Hard Invariant — Bitcoin Standard): Spot Bitcoin must NEVER be liquidated into fiat at a loss ($P_{\text{exit}} \ge P_{\text{entry}} + \text{Fees}_{\text{total}} + \text{TickSize}$). Stop-loss into fiat is permanently disabled.
   - Level 2 (Capacity Strop): Maximum 10 concurrent active positions. Each position is sized at exactly 10% of currently available unencumbered USD cash. If 10 slots are active, new buy signals are blocked.
   - Level 3 (Soft Avellaneda-Stoikov Skew): Target inventory is 30% of portfolio equity in spot BTC. Asymmetric quotation skews limit orders, but ask quotes are strictly floored by Level 1 ($P_{\text{ask}} \ge \max(P_{\text{ask}}^*,\; P_{\text{entry}} + \text{Cost})$).
4. PROFIT SKIMMER: Exactly 10% of realized round-trip USD profits must be systematically converted into physical satoshi and quarantined into an untouchable reserve, isolated from trading margin.

### MATHEMATICAL SPECIFICATION:

1. Bounded Micro-Impulse Order Flow Indicator:
   $$\text{Flow}_t = \frac{\sum_{i=1}^W \text{Vol}_{\text{buy}, i} - \sum_{i=1}^W \text{Vol}_{\text{sell}, i}}{\sum_{i=1}^W \text{Vol}_{\text{buy}, i} + \sum_{i=1}^W \text{Vol}_{\text{sell}, i}} \in [-1.0, 1.0]$$
   - Rolling trade window $W = 25$ ticks (~20 seconds).
   - High-Water Mark ($\text{HWM}_t$): Rolling maximum traded price over 100 ticks.
   - Bounded Dip Window: $P_t \in [\text{HWM}_t \times 0.9965,\; \text{HWM}_t \times 0.9992]$ (8 to 35 bps discount; drops deeper than 35 bps are structural selloffs and are rejected).
   - Monotonic Re-entry Latch: Inter-entry spacing $\Delta t_{\text{entry}} \ge 2.0\text{ s}$ and positive flow/price inflection.
   - Raw Entry Signal: $\text{Signal}_{\text{buy}} = \mathbb{I}\left(\text{Flow}_t > 0.08 \;\land\; P_t \in [\text{HWM}_t \cdot 0.9965, \text{HWM}_t \cdot 0.9992] \;\land\; \Delta t_{\text{entry}} \ge 2.0\text{s} \;\land\; N_{\text{active}} < 10\right)$.

2. Avellaneda-Stoikov Inventory Skew Model (Avellaneda & Stoikov 2008):
   $$r(s, q, t) = s - q \cdot \gamma \cdot \sigma^2 \cdot (T - t)$$
   $$\text{Spread}^*(s, q) = \gamma \cdot \sigma^2 \cdot (T - t) + \frac{2}{\gamma} \ln\left(1 + \frac{\gamma}{\kappa}\right)$$
   $$P_{\text{ask}}^*(s, q) = r(s, q, t) + \frac{\text{Spread}^*(s, q)}{2}$$
   $$P_{\text{bid}}^*(s, q) = r(s, q, t) - \frac{\text{Spread}^*(s, q)}{2}$$
   - Dimensionless inventory deviation: $q = \frac{\text{BTC}_{\text{held}} \cdot s}{\text{Equity}_{\text{free}}} - 0.30 \in [-0.30, +0.70]$.
   - Parameters: Risk aversion $\gamma = 0.10$, daily horizon $T - t = 1.0$, book liquidity $\kappa = 1.5$, $\sigma$ from EWMA ($\lambda = 0.94$).

3. Dynamic ATR Take-Profit:
   $$\text{TP} = P_{\text{entry}} + \operatorname{clamp}\left(0.5 \times \text{ATR}_{14},\; \$25.00,\; \$120.00\right)$$
   - ATR period: 14 on 6-tick micro-bars (~10–15s).
   - Floor: $\$25.00$ provides $1.67\times - 2.5\times$ clearance above the exchange $\$10 - \$15$ spread.

4. Microstructure Confirmation Gates:
   - Hawkes Process Liquidation Brake: Exponential kernel $\lambda(t) = \mu + \sum_{t_i < t} \alpha e^{-\beta (t - t_i)}$ ($\beta = 1.0\text{ s}^{-1}, \alpha = 0.8$). Block entries if $Z_{\text{sell}} \ge 2.5 \land \lambda_{\text{sell}} > \lambda_{\text{buy}}$.
   - Multi-Level L2 Depth Queue Gate: $K = 5$ levels, exponential decay $w_k = e^{-0.40(k - 1)}$. Block entries if $\text{Imbalance}_{\text{L2}} < -0.35$.
   - Hawkes Buy Clustering Boost: Elevate entry priority if $Z_{\text{buy}} \ge 1.2 \land \lambda_{\text{buy}} > \lambda_{\text{sell}}$.
   - Directional VPIN: Block entries if sell-side toxic volume $\text{VPIN}_{\text{sell}} > 0.82$.

### REQUIRED ARTIFACTS:
1. `t16_engine.py` (or Rust `t16_engine.rs`): Complete state machine implementing bounded flow calculation, HWM tracking, Hawkes excitation, L2 queue validation, and Avellaneda-Stoikov quotation.
2. `test_t16_strategy.py`: Comprehensive test battery verifying:
   - Bounded dip window and monotonic re-entry latch.
   - Strict Level 1 Bitcoin Standard no-loss exit invariant under adverse price drift.
   - Hawkes liquidation cascade suppression.
   - Multi-slot concurrency limits (10 slots @ 10% sizing).
3. `SPECIFICATION.json`: Conforming metadata specification for autonomous AI registry.
4. `PERFORMANCE_REPORT.md`: Compute all empirical metrics (CAGR % p.a., Sharpe ratio, Sortino ratio, Max Drawdown in satoshi, Win Rate, and Profit Factor) strictly from the simulated/backtested trade history. Compare the measured results against strategy baseline targets (Yield > 35% p.a., Sharpe > 3.0, Max DD < 0.5% in satoshi). If backtest data is unavailable, report NOT_TESTED.
```
