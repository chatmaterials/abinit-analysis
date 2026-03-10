#!/usr/bin/env python3

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, *args], cwd=ROOT, text=True, capture_output=True, check=True)


def run_json(*args: str):
    return json.loads(run(*args).stdout)


def ensure(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    single = run_json("scripts/analyze_abinit_result.py", "fixtures/completed", "--json")
    ensure(single["completed"] is True, "completed fixture should be complete")
    ensure(abs(single["final_etotal_Ha"] + 8.7654321) < 1e-6, "single-run energy should parse")

    compare = run_json("scripts/compare_abinit_results.py", "fixtures/compare/alpha", "fixtures/compare/beta", "--json")
    ensure(compare["results"][0]["path"].endswith("alpha"), "alpha should be lower in energy than beta")
    ensure(compare["results"][1]["relative_energy_mHa"] > 0, "beta should have positive relative energy")
    dos = run_json("scripts/analyze_abinit_dos.py", "fixtures/completed", "--json")
    ensure(abs(dos["dos_at_fermi"] - 0.05) < 1e-6, "DOS analysis should parse DOS at the Fermi level")
    band = run_json("scripts/analyze_abinit_band.py", "fixtures/completed", "--json")
    ensure(abs(band["band_gap_eV"] - 0.7) < 1e-6, "band analysis should parse the band gap")
    ensure(band["is_direct_gap"] is False, "fixture should produce an indirect band gap")
    temp_dir = Path(tempfile.mkdtemp(prefix="abinit-analysis-report-"))
    try:
        report_path = Path(run("scripts/export_analysis_report.py", "fixtures/completed", "--output", str(temp_dir / "ANALYSIS_REPORT.md")).stdout.strip())
        report_text = report_path.read_text()
        ensure("# Analysis Report" in report_text, "analysis report should have an analysis-report heading")
        ensure("## DOS" in report_text and "## Band" in report_text, "analysis report should include DOS and band sections when files are present")
    finally:
        shutil.rmtree(temp_dir)

    print("abinit-analysis regression passed")


if __name__ == "__main__":
    main()
