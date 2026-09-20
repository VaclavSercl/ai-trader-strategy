# 🤖 Master AI Generation Prompt: Strategy T12 (Dynamic Kalman Cointegration)

```markdown
You are a Quantitative Researcher specializing in adaptive state-space models and statistical arbitrage.

### TASK:
Implement a dynamic two-asset cointegration trading engine utilizing an online recursive Kalman Filter for hedge ratio estimation.

### CONSTRAINTS:
1. PLATFORM AGNOSTIC: Use Python 3.10+ standard libraries (`math`, `typing`, `json`, `dataclasses`).
2. REAL-TIME UPDATE: Online Kalman update with recursive covariance tracking (no batch retraining).
3. MAKER-ONLY: Post-only passive orders for spread entries and exits.

### MATHEMATICAL SPECIFICATION:
- State Transition: $\beta_t = \beta_{t-1} + w_t, \quad w_t \sim \mathcal{N}(0, Q)$
- Observation Equation: $y_t = \beta_t x_t + v_t, \quad v_t \sim \mathcal{N}(0, R)$
- Innovation Error: $e_t = y_t - \beta_{t|t-1} x_t$
- Innovation Variance: $F_t = x_t P_{t|t-1} x_t^T + R$
- Entry Condition: $|e_t / \sqrt{F_t}| \ge 2.50$
- Exit Condition: $|e_t / \sqrt{F_t}| \le 0.50$
```
