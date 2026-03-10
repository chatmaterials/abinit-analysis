#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def read_text(path: Path) -> str:
    return path.read_text(errors="ignore") if path.exists() else ""


def find_input(path: Path) -> Path | None:
    candidates = sorted(path.glob("*.abi"))
    return candidates[0] if candidates else None


def find_output(path: Path) -> Path | None:
    for name in ("run.abo", "abinit.abo"):
        candidate = path / name
        if candidate.exists():
            return candidate
    candidates = sorted(path.glob("*.abo")) + sorted(path.glob("*.out"))
    return candidates[0] if candidates else None


def analyze_path(path: Path) -> dict[str, object]:
    input_file = find_input(path)
    output_file = find_output(path)
    input_text = read_text(input_file) if input_file else ""
    output_text = read_text(output_file) if output_file else ""
    natom_match = re.search(r"\bnatom\s+(\d+)", input_text)
    energy_match = re.findall(r"\betotal\s+([\-0-9.DdEe+]+)", output_text)
    natoms = int(natom_match.group(1)) if natom_match else None
    final_energy = float(energy_match[-1].replace("D", "e").replace("d", "e")) if energy_match else None
    completed = "Calculation completed." in output_text or "leave_new" in output_text
    observations = ["ABINIT run completed." if completed else "ABINIT run appears incomplete."]
    energy_per_atom = final_energy / natoms if final_energy is not None and natoms else None
    return {
        "path": str(path),
        "completed": completed,
        "natoms": natoms,
        "final_etotal_Ha": final_energy,
        "energy_per_atom_Ha": energy_per_atom,
        "observations": observations,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze an ABINIT result directory.")
    parser.add_argument("path", nargs="?", default=".")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    record = analyze_path(Path(args.path).expanduser().resolve())
    if args.json:
        print(json.dumps(record, indent=2))
        return
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()
