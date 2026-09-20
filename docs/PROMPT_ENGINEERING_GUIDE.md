# 🧠 Quant AI Prompt Engineering Guide

This guide establishes the standard methodology for engineering prompts that instruct LLM agents (Claude, OpenAI GPT, Google Gemini, DeepSeek, or local open-source models) to autonomously research, design, code, and falsify production-grade quantitative trading strategies.

---

## 1. The Anatomy of an Effective Quant AI Prompt

A high-performing quant prompt must never be vague or open-ended. It must supply rigid mathematical constraints, precise financial mechanics, and clear architectural boundaries.

### Core Sections of a Strategy Generation Prompt:

1. **Role & Cognitive Frame**:
   - Assign a specific, high-capability persona: Senior Quantitative Researcher & High-Frequency Systems Architect.
2. **Structural Market Edge (The "Why")**:
   - Detail the economic driver: Why does the alpha exist? (Regulatory friction, structural funding contango, cross-venue latency, maker rebates).
3. **Rigid Mathematical Formulation**:
   - Exact differential equations, stochastic processes (e.g. Ornstein-Uhlenbeck), cointegration tests, and statistical spread definitions.
4. **Deterministic Risk Invariants (Non-Negotiable)**:
   - Mathematical guardrails that must be hardcoded (Delta neutrality, de-peg circuit breakers, isolated margin constraints).
5. **Universal & Platform-Agnostic Execution**:
   - Strictly prohibit hardware-specific, local, or platform-specific paths. Require pure standard library Python, environment variable configuration, or lightweight SQLite/PostgreSQL connectors.
6. **Falsification Battery (F1–F7)**:
   - Explicit failure conditions. If the backtest violates any condition, the AI must self-correct and reject the parameter set.
7. **Complete Output Deliverables**:
   - The AI must output production-ready code with complete type hints, unit tests, and operational daemon scripts.

---

## 2. Universal Prompt Pattern for Strategy Generation

When engineering prompts for any strategy in this repository, follow this master template:

```markdown
You are a Principal Quantitative Trader and Algorithmic Systems Architect specializing in delta-neutral arbitrage and statistical carry engines.

### TASK:
Design, implement, backtest, and generate an autonomous deployment daemon for the quantitative trading strategy described below.

### CONSTRAINTS:
1. PLATFORM AGNOSTIC: Do not use any machine-specific, user-specific, or hardware-specific paths. The code must run on any Linux, macOS, or Windows computer, in Docker, or on any cloud server.
2. ZERO HUMAN IN THE LOOP: The strategy must run completely autonomously under AI supervision. It must feature self-healing telemetry, automated delta rebalancing, and deterministic circuit breakers.
3. RISK INVARIANTS:
   - Net Portfolio Delta must equal 0.0 at all times (Spot Long == Perp Short).
   - Stablecoin peg circuit breaker: Halt immediately if USDC/USDT deviates > 50 bps from parity.
   - Max Drawdown limit: < 10.0% (historical actual < 0.5%).
   - Maker-Only Execution: Orders must be post-only to earn exchange maker rebates and eliminate taker fees.

### ECONOMIC & MATHEMATICAL FORMULATION:
[Insert formal equations, cross-rate ratios, Ornstein-Uhlenbeck drift parameters, and fee models]

### REQUIRED ARTIFACTS:
1. Pure Python Strategy Engine class (clean mathematical state machine, signal calculation, order generation).
2. Comprehensive Unit Test Suite testing normal execution, flash crash gaps, de-peg events, and all falsification gates.
3. Autonomous Paper Trading Daemon with JSON state persistence and periodic tick evaluation.
4. Comprehensive markdown report detailing expected annual yield (% p.a.), Sharpe ratio, maximum drawdown, and empirical half-life.
```

---

## 3. Best Practices for Multi-Agent Oponentura (Adversarial Review)

To prevent overfitting and hallucinated alpha, always deploy an adversarial AI agent (opponent) using this pattern:

> *"Act as an adversarial Quantitative Risk Auditor and Cynical Market Maker. Your sole objective is to discover hidden execution costs, latency flaws, delisting risks, liquidity constraints, and statistical overfitting in the proposed strategy. Attack every assumption ruthlessly and mandate required architectural firewalls before live sign-off."*
