# Proposal P019: DEX-CEX Synthetic Funding Rate Carry & Liquidity Hook Engine

> **Asset Classes**: BTC/USDC, ETH/USDC (Decentralized & Centralized Venues)  
> **Proposed Venues**: Hyperliquid CLOB + Uniswap v4 Hook / Aerodrome Slipstream  
> **Target Annual Yield (Projected)**: **+30.0% – +38.0% p.a.**  
> **Status**: 💡 **Proposal (Incubator Stage, Pending Historical Backtesting)**

---

## 1. Executive Summary & Market Edge
In the 2026 decentralized liquidity landscape, automated market maker (AMM) pools utilizing dynamic fee hooks (e.g. Uniswap v4 hooks) display predictable fee-rate premiums over central-limit-order-book (CLOB) perpetual funding rates. 

By simultaneously:
1. Providing concentrated out-of-the-money delta-neutral liquidity on high-fee AMM hooks (harvesting LP swap fees).
2. Hedging inventory risk with perpetual short contracts on low-cost CLOBs (Hyperliquid).
3. The strategy aims to capture the **AMM Swap Fee vs. Perpetual Funding Rate basis spread**.

---

## 2. Invariant Requirements for Backtesting
- Must simulate exact L2/Rollup gas costs and MEV sandwich protection.
- Impermanent loss must be dynamic and delta-hedged every block.
- Maximum allowable gas-to-profit ratio: $\le 15.0\%$.
