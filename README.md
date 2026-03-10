# abinit-analysis

Standalone skill for post-run ABINIT result analysis and multi-run comparison.

## Install

```bash
npx skills add chatmaterials/abinit-analysis -g -y
```

## Local Validation

```bash
python3 -m py_compile scripts/*.py
npx skills add . --list
python3 scripts/analyze_abinit_result.py fixtures/completed --json
python3 scripts/compare_abinit_results.py fixtures/compare/alpha fixtures/compare/beta --json
python3 scripts/analyze_abinit_dos.py fixtures/completed --json
python3 scripts/analyze_abinit_band.py fixtures/completed --json
python3 scripts/export_analysis_report.py fixtures/completed
python3 scripts/run_regression.py
```
