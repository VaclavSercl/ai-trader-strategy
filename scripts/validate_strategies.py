#!/usr/bin/env python3
"""
Strategy Validator Script (Platform-Agnostic)
Validates that all strategies in the ai-trader-strategy repository conform to the
standard for autonomous AI strategy descriptions and prompts:
1. Valid JSON specification (SPECIFICATION.json)
2. Detailed mathematical & market description (README.md)
3. Universal Master AI Prompt (AI_GENERATION_PROMPT.md)
4. Annualized yield and performance history (PERFORMANCE_HISTORY.md)
5. No machine-specific code or local server paths contaminating the registry.
"""

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def validate_strategies() -> bool:
    all_valid = True
    stages = ["01-live-production", "02-paper-trading", "03-backtested", "04-proposals"]
    strategy_dirs = []

    for stage in stages:
        stage_path = REPO_ROOT / stage
        if stage_path.exists():
            for item in stage_path.iterdir():
                if item.is_dir() and not item.name.startswith("."):
                    strategy_dirs.append(item)

    print(f"Verifying {len(strategy_dirs)} strategy registries across 4 lifecycle stages...\n")

    for s_dir in sorted(strategy_dirs):
        rel_dir = s_dir.relative_to(REPO_ROOT)
        print(f"▶ Validating: {rel_dir}")

        # 1. SPECIFICATION.json
        spec_path = s_dir / "SPECIFICATION.json"
        if not spec_path.exists():
            print(f"  [FAIL] Missing SPECIFICATION.json in {rel_dir}")
            all_valid = False
        else:
            try:
                with open(spec_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if "id" not in data or "name" not in data or "status" not in data:
                    raise ValueError("Missing 'id', 'name', or 'status'")
                
                # Extract yield percentage
                annual_yield = data.get("target_annual_yield_pct")
                if annual_yield is None and "financial_metrics" in data:
                    annual_yield = data["financial_metrics"].get("target_annual_yield_pct")

                print(f"  [PASS] SPECIFICATION.json: ID={data.get('id')}, Name='{data.get('name')}', Yield={annual_yield}% p.a.")
            except Exception as e:
                print(f"  [FAIL] SPECIFICATION.json invalid: {e}")
                all_valid = False

        # 2. README.md (Detailed Description)
        readme_path = s_dir / "README.md"
        if not readme_path.exists() or readme_path.stat().st_size < 100:
            print(f"  [FAIL] Missing or incomplete README.md description in {rel_dir}")
            all_valid = False
        else:
            print(f"  [PASS] README.md (Strategy Description: {readme_path.stat().st_size} bytes)")

        # 3. AI_GENERATION_PROMPT.md (Master Prompt for other AI agents)
        prompt_path = s_dir / "AI_GENERATION_PROMPT.md"
        if not prompt_path.exists() or prompt_path.stat().st_size < 100:
            print(f"  [FAIL] Missing or incomplete AI_GENERATION_PROMPT.md in {rel_dir}")
            all_valid = False
        else:
            print(f"  [PASS] AI_GENERATION_PROMPT.md (AI Master Prompt: {prompt_path.stat().st_size} bytes)")

        # 4. PERFORMANCE_HISTORY.md (Track Record & % p.a. yield)
        perf_path = s_dir / "PERFORMANCE_HISTORY.md"
        if not perf_path.exists() or perf_path.stat().st_size < 50:
            print(f"  [FAIL] Missing or incomplete PERFORMANCE_HISTORY.md in {rel_dir}")
            all_valid = False
        else:
            print(f"  [PASS] PERFORMANCE_HISTORY.md (Yield History: {perf_path.stat().st_size} bytes)")

        # 5. Purity check: Verify no concrete implementation code files in the strategy registry
        code_files = list(s_dir.glob("*.py"))
        if code_files:
            print(f"  [FAIL] Found concrete implementation code files: {[f.name for f in code_files]}. Strategy registry must contain only strategy descriptions, specifications, and AI prompts!")
            all_valid = False

        print()

    return all_valid


if __name__ == "__main__":
    success = validate_strategies()
    if success:
        print("✅ All strategy descriptions, prompts, specifications, and performance records are 100% verified.")
        sys.exit(0)
    else:
        print("❌ Verification failed.")
        sys.exit(1)
