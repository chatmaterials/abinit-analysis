#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from pathlib import Path


def analyze_path(path: Path, occupied_bands: int = 2) -> dict[str, object]:
    band_path = path / "bands.dat" if path.is_dir() else path
    rows = []
    for line in band_path.read_text().splitlines():
        parts = line.split()
        if len(parts) < occupied_bands + 2:
            continue
        k = float(parts[0])
        energies = [float(x) for x in parts[1:]]
        rows.append((k, energies))
    if not rows:
        raise SystemExit("No band rows found")
    vbm = max((energies[occupied_bands - 1], k) for k, energies in rows)
    cbm = min((energies[occupied_bands], k) for k, energies in rows)
    gap = cbm[0] - vbm[0]
    return {
        "path": str(path),
        "occupied_bands": occupied_bands,
        "vbm_eV": vbm[0],
        "cbm_eV": cbm[0],
        "band_gap_eV": gap,
        "is_direct_gap": abs(vbm[1] - cbm[1]) < 1e-12,
        "observations": ["Positive gap detected." if gap > 0 else "No positive gap detected."],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze an ABINIT band file or result directory.")
    parser.add_argument("path", nargs="?", default=".")
    parser.add_argument("--occupied-bands", type=int, default=2)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    payload = analyze_path(Path(args.path).expanduser().resolve(), args.occupied_bands)
    if args.json:
        print(json.dumps(payload, indent=2))
        return
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
