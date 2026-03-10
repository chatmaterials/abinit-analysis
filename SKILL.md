---
name: "abinit-analysis"
description: "Use when the task is to analyze completed or partially completed ABINIT results, including extracting total energies, convergence or restart status, comparing multiple ABINIT runs, and summarizing .abo outputs."
---

# ABINIT Analysis

Use this skill for post-run ABINIT result analysis rather than workflow setup.

## When to use

- analyze a completed or incomplete ABINIT run
- compare energies across multiple ABINIT directories
- summarize status from `.abi` and `.abo`
- write a compact report from existing ABINIT results

## Use the bundled helpers

- `scripts/analyze_abinit_result.py`
  Summarize a single ABINIT result directory.
- `scripts/compare_abinit_results.py`
  Compare multiple ABINIT result directories by energy and status.
- `scripts/analyze_abinit_dos.py`
  Extract DOS-oriented summary data from ABINIT DOS output.
- `scripts/analyze_abinit_band.py`
  Extract band-gap-oriented summary data from ABINIT band output.
- `scripts/export_analysis_report.py`
  Export a markdown analysis report from an ABINIT result directory.

## Guardrails

- Do not claim comparability when restart dependencies differ or runs are incomplete.
- Distinguish extracted quantities from scientific interpretation.
