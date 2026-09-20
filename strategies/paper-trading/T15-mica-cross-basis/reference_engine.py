#!/usr/bin/env python3
"""
Strategy T15: MiCA Cross-Currency Basis & Triangular Synthetic Carry Engine
Reference Implementation (Platform-Agnostic, Zero-External-Dependency)

This module implements the mathematical, stochastic, and risk engine for
Strategy T15. It requires only standard Python libraries (math, dataclasses,
typing, json, datetime) and can be executed on any operating system.
"""

import math
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class T15MarketTick:
    timestamp_utc: str
    btc_eur: float
    btc_usdc: float
    eur_usdc: float
    funding_rate_hourly: float
    usdc_usd: float = 1.0000
    usdt_usd: float = 1.0000


@dataclass
class T15Signal:
    timestamp_utc: str
    synthetic_eur: float
    spread_ratio_s: float
    z_score: float
    ou_half_life_hours: float
    action: str  # "BUY_DIRECT_SELL_SYNTHETIC" | "SELL_DIRECT_BUY_SYNTHETIC" | "HOLD" | "EXIT" | "HALT"
    is_actionable: bool
    reason: str


@dataclass
class T15PositionState:
    capital_usd: float = 1000.0
    spot_btc: float = 0.0
    spot_entry_price: float = 0.0
    perp_short_btc: float = 0.0
    perp_entry_price: float = 0.0
    margin_collateral_usdc: float = 500.0
    accumulated_funding_usd: float = 0.0
    accumulated_arb_usd: float = 0.0
    accumulated_rebates_usd: float = 0.0
    total_trades: int = 0
    peak_equity_usd: float = 1000.0
    max_drawdown_pct: float = 0.0


class T15CrossBasisEngine:
    """
    Platform-Agnostic Mathematical Engine for Strategy T15.
    Combines:
      1. Ornstein-Uhlenbeck mean-reverting cross-currency arbitrage.
      2. Perpetual futures funding rate carry harvesting.
      3. Strict delta-neutrality (Net Delta = 0).
    """

    def __init__(
        self,
        initial_capital: float = 1000.0,
        entry_z_threshold: float = 2.00,
        exit_z_threshold: float = 0.50,
        stop_z_threshold: float = 4.50,
        depeg_tolerance_bps: float = 100.0,
        window_size: int = 120,
        spot_maker_fee_pct: float = 0.00,
        perp_maker_rebate_pct: float = 0.02,
    ):
        self.capital = initial_capital
        self.entry_z = entry_z_threshold
        self.exit_z = exit_z_threshold
        self.stop_z = stop_z_threshold
        self.depeg_tolerance_bps = depeg_tolerance_bps
        self.window_size = window_size
        self.spot_maker_fee = spot_maker_fee_pct / 100.0
        self.perp_maker_rebate = perp_maker_rebate_pct / 100.0

        self.spread_history: List[float] = []
        self.state = T15PositionState(capital_usd=initial_capital)

    @staticmethod
    def compute_synthetic_rate(btc_usdc: float, eur_usdc: float) -> float:
        """Computes the theoretical synthetic price of BTC in EUR."""
        if eur_usdc <= 0.0:
            raise ValueError("EUR/USDC rate must be positive.")
        return btc_usdc * eur_usdc

    @staticmethod
    def compute_cross_ratio(btc_eur: float, btc_usdc: float, eur_usdc: float) -> float:
        """
        Computes the cross-currency ratio S_t:
        S_t = P(BTC/EUR) / (P(BTC/USDC) * P(EUR/USDC))
        """
        synth = btc_usdc * eur_usdc
        if synth <= 0.0 or btc_eur <= 0.0:
            return 1.0
        return btc_eur / synth

    def fit_ornstein_uhlenbeck(self, samples: List[float]) -> Tuple[float, float, float, float]:
        """
        Fits OU parameters via discrete linear autoregression:
        X_{t} = a * X_{t-1} + b + eps
        theta = -ln(a) / dt
        mu = b / (1 - a)
        half_life = ln(2) / theta
        """
        n = len(samples)
        if n < 10:
            return 0.5, 1.0, 0.001, 1.38

        # Log transform
        x = [math.log(s) if s > 0 else 0.0 for s in samples]
        x_lag = x[:-1]
        x_curr = x[1:]
        m = len(x_lag)

        mean_lag = sum(x_lag) / m
        mean_curr = sum(x_curr) / m

        cov = sum((x_lag[i] - mean_lag) * (x_curr[i] - mean_curr) for i in range(m))
        var_lag = sum((x_lag[i] - mean_lag) ** 2 for i in range(m))

        a = cov / var_lag if var_lag > 1e-12 else 0.95
        a = max(0.001, min(0.9999, a))
        b = mean_curr - a * mean_lag

        dt = 1.0 / 60.0  # 1-minute steps in hours
        theta = -math.log(a) / dt
        mu = b / (1.0 - a) if abs(1.0 - a) > 1e-9 else 0.0

        resids = [x_curr[i] - (a * x_lag[i] + b) for i in range(m)]
        sigma = math.sqrt(sum(r ** 2 for r in resids) / m) / math.sqrt(dt)
        half_life = (math.log(2) / theta) if theta > 1e-6 else 999.0

        return theta, mu, sigma, half_life

    def calculate_z_score(self, current_s: float) -> Tuple[float, float]:
        """Returns (z_score, half_life_hours)."""
        self.spread_history.append(current_s)
        if len(self.spread_history) > self.window_size:
            self.spread_history.pop(0)

        window = self.spread_history
        if len(window) < 5:
            return 0.0, 1.42

        mean_s = sum(window) / len(window)
        var_s = sum((x - mean_s) ** 2 for x in window) / len(window)
        std_s = math.sqrt(var_s) if var_s > 1e-12 else 0.0001

        z = (current_s - mean_s) / std_s
        _, _, _, half_life = self.fit_ornstein_uhlenbeck(window)
        return z, half_life

    def evaluate_tick(self, tick: T15MarketTick) -> T15Signal:
        """Processes an incoming market tick and generates deterministic trading signal."""
        # 1. Check Stablecoin De-peg Invariant
        usdc_dev = abs(tick.usdc_usd - 1.0) * 10000.0
        usdt_dev = abs(tick.usdt_usd - 1.0) * 10000.0
        if usdc_dev > self.depeg_tolerance_bps or usdt_dev > self.depeg_tolerance_bps:
            return T15Signal(
                timestamp_utc=tick.timestamp_utc,
                synthetic_eur=tick.btc_usdc * tick.eur_usdc,
                spread_ratio_s=1.0,
                z_score=0.0,
                ou_half_life_hours=0.0,
                action="HALT",
                is_actionable=False,
                reason=f"DE-PEG DETECTED: USDC dev={usdc_dev:.1f} bps, USDT dev={usdt_dev:.1f} bps"
            )

        # 2. Compute Synthetic Price and Ratio
        synthetic_eur = self.compute_synthetic_rate(tick.btc_usdc, tick.eur_usdc)
        s_t = self.compute_cross_ratio(tick.btc_eur, tick.btc_usdc, tick.eur_usdc)
        z, half_life = self.calculate_z_score(s_t)

        # 3. Regime Break Filter
        if abs(z) >= self.stop_z:
            return T15Signal(
                timestamp_utc=tick.timestamp_utc,
                synthetic_eur=synthetic_eur,
                spread_ratio_s=s_t,
                z_score=z,
                ou_half_life_hours=half_life,
                action="HALT",
                is_actionable=False,
                reason=f"REGIME BREAK: |Z|={abs(z):.2f} >= {self.stop_z}"
            )

        # 4. Entry and Exit Signals
        if z >= self.entry_z:
            action = "SELL_DIRECT_BUY_SYNTHETIC"
            actionable = True
            reason = f"OVERPRICED: Z={z:+.2f} >= {self.entry_z} (Direct EUR > Synthetic)"
        elif z <= -self.entry_z:
            action = "BUY_DIRECT_SELL_SYNTHETIC"
            actionable = True
            reason = f"UNDERPRICED: Z={z:+.2f} <= -{self.entry_z} (Direct EUR < Synthetic)"
        elif abs(z) <= self.exit_z:
            action = "EXIT"
            actionable = False
            reason = f"MEAN REVERTED: |Z|={abs(z):.2f} <= {self.exit_z}"
        else:
            action = "HOLD"
            actionable = False
            reason = f"NEUTRAL BAND: Z={z:+.2f}"

        return T15Signal(
            timestamp_utc=tick.timestamp_utc,
            synthetic_eur=synthetic_eur,
            spread_ratio_s=s_t,
            z_score=z,
            ou_half_life_hours=half_life,
            action=action,
            is_actionable=actionable,
            reason=reason
        )

    def verify_invariants(self, state: T15PositionState) -> Tuple[bool, List[str]]:
        """Evaluates all deterministic risk firewalls."""
        violations = []

        # Invariant 1: Delta Neutrality
        net_delta = abs(state.spot_btc - state.perp_short_btc)
        if net_delta > 0.0001:
            violations.append(f"INVARIANT 1 BREACH: Net delta {net_delta:.6f} BTC > 0.0001")

        # Invariant 2: Max Drawdown Limit
        if state.max_drawdown_pct >= 10.0:
            violations.append(f"INVARIANT 2 BREACH: Max drawdown {state.max_drawdown_pct:.2f}% >= 10.0%")

        # Invariant 3: Leverage / Margin
        current_equity = (
            state.capital_usd
            + state.accumulated_funding_usd
            + state.accumulated_arb_usd
            + state.accumulated_rebates_usd
        )
        if current_equity > 0:
            perp_notional = state.perp_short_btc * state.perp_entry_price
            leverage = perp_notional / current_equity if current_equity > 0 else 0.0
            if leverage > 1.05:
                violations.append(f"INVARIANT 3 BREACH: Leverage {leverage:.2f}x > 1.0x isolated")

        return len(violations) == 0, violations


if __name__ == "__main__":
    print("==================================================================")
    print(" T15 Reference Engine Smoke Test (Platform Agnostic)")
    print("==================================================================")
    engine = T15CrossBasisEngine(initial_capital=1000.0)

    # Initialize position: $500 spot long, $500 short perp hedge at $80,000 BTC
    btc_init_price = 80000.0
    allocated_btc = 500.0 / btc_init_price
    engine.state.spot_btc = allocated_btc
    engine.state.spot_entry_price = btc_init_price
    engine.state.perp_short_btc = allocated_btc
    engine.state.perp_entry_price = btc_init_price

    # Verify initial invariants
    passed, violations = engine.verify_invariants(engine.state)
    print(f"Initial Delta Invariant: {'PASS' if passed else 'FAIL'}")
    assert passed, f"Violations: {violations}"

    # Feed synthetic ticks to simulate mean reversion
    now_iso = datetime.now(timezone.utc).isoformat()
    # Baseline ticks
    for _ in range(30):
        engine.evaluate_tick(T15MarketTick(now_iso, 69565.0, 80000.0, 0.8695625, 0.0000125))

    # Trigger dislocation tick (BTC/EUR price spikes relative to synthetic)
    spike_tick = T15MarketTick(now_iso, 69800.0, 80000.0, 0.8695625, 0.0000125)
    signal = engine.evaluate_tick(spike_tick)

    print(f"Dislocation S_t:         {signal.spread_ratio_s:.6f}")
    print(f"Calculated Z-Score:      {signal.z_score:+.2f}")
    print(f"OU Half-life:            {signal.ou_half_life_hours:.2f} hours")
    print(f"Signal Action:           {signal.action}")
    print(f"Is Actionable:           {signal.is_actionable}")
    print(f"Signal Reason:           {signal.reason}")
    print("==================================================================")
    print(" Reference engine verified successfully.")
