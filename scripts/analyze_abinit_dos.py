#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from pathlib import Path


def analyze_path(path: Path) -> dict[str, object]:
    dos_path = path / "dos.dat" if path.is_dir() else path
    rows = []
    for line in dos_path.read_text().splitlines():
        parts = line.split()
        if len(parts) < 2:
            continue
        energy = float(parts[0])
        dos = float(parts[1])
        intdos = float(parts[2]) if len(parts) > 2 else None
        rows.append((energy, dos, intdos))
    if not rows:
        raise SystemExit("No DOS rows found")
    nearest = min(rows, key=lambda item: abs(item[0]))
    peak = max(rows, key=lambda item: item[1])
    return {
        "path": str(path),
        "dos_at_fermi": nearest[1],
        "peak_dos": peak[1],
        "peak_energy_eV": peak[0],
        "observations": ["Sampled DOS summary extracted from the ABINIT DOS file."],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze an ABINIT DOS file or result directory.")
    parser.add_argument("path", nargs="?", default=".")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    payload = analyze_path(Path(args.path).expanduser().resolve())
    if args.json:
        print(json.dumps(payload, indent=2))
        return
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
