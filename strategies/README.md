# 🧭 Quantitative Strategy Lifecycle Directory

All strategies in this repository progress through an immutable, autonomous 4-stage pipeline:

```mermaid
flowchart LR
    P["1. proposals/<br><i>(Návrhy k otestování)</i>"] -->|AI Backtest & Falsification| B["2. backtested/<br><i>(Otestované na datech)</i>"]
    B -->|Passed F1-F7 Gates| PT["3. paper-trading/<br><i>(V paper tradingu)</i>"]
    PT -->|30-Day Qualification Battery| L["4. live/<br><i>(Reálně nasazené)</i>"]
```

---

## 📁 Directory Structure & Stage Definition

### 1. `strategies/proposals/` — Strategie k otestování (Návrhy strategií / Incubator)
- **Status**: Teoretické koncepty, matematické hypotézy a nové trendy pro rok 2026.
- **Kritéria pro vstup**: Formální ekonomická hypotéza, matematická definice spreadu a Master AI Prompt.
- **Obsah**:
  - [`P019-dex-cex-synthetic-carry/`](proposals/P019-dex-cex-synthetic-carry/) — Cross DEX-CEX Perpetual Carry Arbitrage (Hyperliquid vs. Uniswap v4).

### 2. `strategies/backtested/` — Strategie testované na historických datech (Backtest Verified)
- **Status**: Úspěšně otestované na 1222 dnech historických dat (PostgreSQL ground truth).
- **Kritéria pro postup**: Splnění všech 7 falsifikačních bran (F1–F7), Sharpe $> 1.0$, Max Drawdown $< 10\%$, Net Delta $= 0$.
- **Obsah**:
  - [`T12-kalman-cross-market/`](backtested/T12-kalman-cross-market/) — Adaptivní Kalmanův filtr pro křížovou kointegraci trhů (+22.4 % p.a., Max DD 0.28 %).

### 3. `strategies/paper-trading/` — Strategie v paper tradingu (Live Qualification Staging)
- **Status**: Běžící v reálném čase proti live orderbookům bez rizika kapitálu (30denní kvalifikační baterie).
- **Kritéria pro postup**: Minimálně 30 po sobě jdoucích dnů bez porušení invariantů, $\ge 100$ maker exekucí, ověřený nulový skluz.
- **Obsah**:
  - [`T15-mica-cross-basis/`](paper-trading/T15-mica-cross-basis/) — MiCA Cross-Basis Carry & Triangular Arbitrage (+28.4 % p.a., Den 1/30).

### 4. `strategies/live/` — Reálně nasazené a otestované v živém obchodování (Live Production)
- **Status**: Plně certifikované strategie obchodující reálný kapitál s aktivním risk perimetrem.
- **Kritéria**: Absolvovaná 30denní paper fáze, nulový delta drift, deterministické circuit-breakery.
- **Obsah**:
  - [`T13-basis-funding-carry/`](live/T13-basis-funding-carry/) — Delta-Neutral Basis & Funding Carry Engine (+13.2 % p.a.).
  - [`T14-triangular-fx-dislocation/`](live/T14-triangular-fx-dislocation/) — Triangular FX Currency Dislocation Engine (+16.5 % p.a.).
