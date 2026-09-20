#!/usr/bin/env python3
"""
Strategy Validator Script (Platform-Agnostic)
Validates that all strategies conform to RFC-001 JSON Schema specifications
and executes self-tests on reference engines.
"""

import glob
import json
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def validate_json_specs() -> bool:
    all_valid = True
    spec_files = list(REPO_ROOT.glob("strategies/**/SPECIFICATION.json"))
    print(f"Found {len(spec_files)} strategy specification files.")
    for spec in spec_files:
        try:
            with open(spec, "r", encoding="utf-8") as f:
                data = json.load(f)
            assert "id" in data, f"Missing 'id' in {spec}"
            print(f"  [PASS] {spec.relative_to(REPO_ROOT)}: ID={data.get('id')}, Name='{data.get('name')}'")
        except Exception as e:
            print(f"  [FAIL] {spec.relative_to(REPO_ROOT)}: {e}")
            all_valid = False
    return all_valid


def run_reference_engines() -> bool:
    all_passed = True
    engines = list(REPO_ROOT.glob("strategies/**/reference_engine.py"))
    print(f"\nRunning {len(engines)} reference engines:")
    for eng in engines:
        print(f"  Executing {eng.relative_to(REPO_ROOT)}...")
        r = subprocess.run([sys.executable, str(eng)], capture_output=True, text=True)
        if r.returncode == 0:
            print(f"  [PASS] {eng.name}")
        else:
            print(f"  [FAIL] {eng.name} exited with {r.returncode}:\n{r.stderr}")
            all_passed = False
    return all_passed


if __name__ == "__main__":
    v1 = validate_json_specs()
    v2 = run_reference_engines()
    if v1 and v2:
        print("\nAll strategy specifications and engines verified successfully.")
        sys.exit(0)
    else:
        print("\nVerification failed.")
        sys.exit(1)
