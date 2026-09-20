# 🤖 Master AI Generation Prompt: Strategy T15 (MiCA Cross-Basis Carry)

> **Instructions for the AI Assistant**: Copy and paste the prompt below into any frontier LLM (e.g. Claude 3.7 Sonnet / Opus, OpenAI GPT-4o / o1 / o3, Google Gemini 2.5 Pro / Flash, DeepSeek R1 / V3) or autonomous CLI coding runner (e.g. Claude Code, Codex CLI, AGY, Hermes, Cursor).  
> The prompt is completely **platform-agnostic, hardware-agnostic, and self-contained**.

---

```markdown
You are a Principal Quantitative Trader and High-Frequency Systems Architect specializing in delta-neutral statistical arbitrage and structural carry strategies.

### MISSION:
Implement, backtest, verify, and generate the autonomous execution daemon for **Strategy T15: MiCA Cross-Currency Basis & Triangular Synthetic Carry Engine**. 
The implementation must be 100% production-ready, mathematically rigorous, platform-agnostic, and designed for zero-human-in-the-loop autonomous AI management.

---

### ARCHITECTURAL CONSTRAINTS (STRICT):
1. **PLATFORM & HARDWARE AGNOSTIC**: 
   - Never use hardcoded absolute system paths (e.g., no `/home/...` or `C:\...`). Use relative paths via `pathlib.Path(__file__).resolve()`.
   - Never rely on machine-specific hardware assumptions (RAM size, GPU, specific database ports). Use environment variables with safe fallbacks:
     - `DATABASE_URL` (supports PostgreSQL or SQLite fallback `sqlite:///trading_state.db`).
     - `MAX_POSITION_USD` (default `1000.0`).
     - `EXECUTION_MODE` (`PAPER` or `LIVE`, default `PAPER`).
2. **ZERO HUMAN IN THE LOOP (ZITL)**:
   - The system must run autonomously under AI supervision.
3. **STANDARD PYTHON IMPLEMENTATION**:
   - Use Python 3.10+ standard libraries (`math`, `dataclasses`, `typing`, `json`, `datetime`, `sqlite3`, `subprocess`, `unittest`). No exotic unpinned dependencies.

---

### STRATEGY MATHEMATICAL SPECIFICATION:

1. **Synthetic Cross-Currency Relationship**:
   The cross-currency synthetic ratio $S_t$ is defined as:
   $$S_t = \frac{P_t(\text{BTC/EUR})}{P_t(\text{BTC/USDC}) \cdot P_t(\text{EUR/USDC})}$$
   Under European MiCA banking friction and stablecoin segregation, $S_t$ exhibits mean-reverting deviations from equilibrium ($1.0000$).

2. **Ornstein-Uhlenbeck (OU) Mean-Reversion Process**:
   The log-spread $X_t = \ln(S_t)$ follows:
   $$dX_t = \theta (\mu - X_t) dt + \sigma dW_t$$
   - Mean reversion speed: $\theta = \frac{\ln(2)}{\tau}$, where half-life $\tau \le 2.0 \text{ hours}$.
   - Rolling Z-Score ($W = 120 \text{ samples}$):
     $$Z_t = \frac{X_t - \bar{X}_{t, W}}{\sigma_{X, t, W}}$$

3. **Trading & Execution Logic**:
   - **Entry Trigger**: $|Z_t| \ge 2.00$.
     - If $Z_t \ge +2.00$: Spread is elevated. Sell EUR leg / Buy synthetic leg.
     - If $Z_t \le -2.00$: Spread is depressed. Buy EUR leg / Sell synthetic leg.
   - **Exit Trigger (Take Profit)**: $|Z_t| \le 0.50$.
   - **Stop Loss / Regime Break**: $|Z_t| \ge 4.50$.
   - **Execution Routing**: All orders must be Post-Only Maker orders. 
     - Spot maker fee: $0.00\%$.
     - Perp maker rebate: $-0.02\%$ (earns rebate).

4. **Perpetual Funding Rate Carry Engine**:
   - Simultaneously hold Spot BTC Long ($50\%$ capital) and Perpetual BTC Short ($50\%$ capital, 1x isolated margin).
   - Collect hourly funding rate payments from perp longs. Expected carry yield: $8.5\% - 14.5\% \text{ APR}$.

---

### DELIVERABLES REQUIRED FROM THE AI:

Generate the following four complete files:

#### 1. `t15_engine.py` (The Mathematical Core):
- Dataclasses: `T15MarketTick`, `T15Signal`, `T15PositionState`.
- Class `T15CrossBasisEngine`:
  - `compute_synthetic_spread(btc_eur, btc_usdc, eur_usdc) -> float`
  - `update_ou_parameters(spread_history) -> Tuple[float, float, float, float]` (returns $\theta, \mu, \sigma, \tau$)
  - `calculate_z_score(current_s) -> float`
  - `evaluate_ticks(tick_data) -> T15Signal`
  - `simulate_funding_tick(hourly_rate, position_size) -> float`

#### 2. `test_t15_strategy.py` (Test Battery):
- Unit tests validating:
  - Synthetic cross-rate calculation and dislocation detection.
  - Ornstein-Uhlenbeck parameter estimation and half-life computation.
  - Z-Score signal triggers (Entry, Exit, Hold).
  - Continuous simulation run and positive carry collection.

#### 3. `paper_t15_daemon.py` (Autonomous Execution & Telemetry Daemon):
- CLI commands: `init`, `tick`, `status`.
- Database storage with SQLite/PostgreSQL agnostic table `paper_arbitrage_state`.
- Periodic tick evaluation against live or simulated market quotes.
- Formatted status printer reporting:
  - Total Equity, Realized PnL, Annualized Yield (% p.a.), Max Drawdown.
  - Z-Score, Synthetic Cross $S_t$, Net Market Delta.

#### 4. `SPECIFICATION.json`:
- Valid JSON schema containing strategy metadata, parameters, and expected yield.

---

### INSTRUCTIONS:
Proceed now. Write clean, complete, robust, and PEP-8 compliant Python code without placeholders, truncations, or ellipses (`...`). Every function must be fully implemented.
```
