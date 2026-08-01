#!/usr/bin/env bash
# Copyright (c) 2026 Southeast University
# This program is free software, you can redistribute it and/or modify it under the terms and conditions of
# CANN Open Software License Agreement Version 2.0 (the "License").
# Please refer to the License for details. You may not use this file except in compliance with the License.
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR A PARTICULAR PURPOSE.
# See LICENSE in the root of the software repository for the full text of the License.

# Lightweight OAT-oriented compliance check for local pre-commit.
# 1) Ensure OAT.xml exists
# 2) Ensure comment-capable source files contain Copyright + CANN-2.0 header
# If full OSS Audit Tool binary is available as `oat`, run it as well.

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT_DIR}"

if [[ ! -f OAT.xml ]]; then
  echo "[oat-check] ERROR: OAT.xml is missing in repository root."
  exit 1
fi

if [[ ! -f LICENSE ]]; then
  echo "[oat-check] ERROR: LICENSE is missing in repository root."
  exit 1
fi

if ! grep -q "CANN Open Software License Agreement Version 2.0" LICENSE; then
  echo "[oat-check] ERROR: LICENSE is not CANN Open Software License Agreement Version 2.0."
  exit 1
fi

PYTHON_BIN=""
if command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="python3"
elif command -v python >/dev/null 2>&1; then
  PYTHON_BIN="python"
elif command -v py >/dev/null 2>&1; then
  PYTHON_BIN="py -3"
else
  echo "[oat-check] ERROR: python interpreter not found."
  exit 1
fi

# Optional path args from pre-commit; empty means scan whole repo.
export OAT_CHECK_PATHS="${*:-}"

${PYTHON_BIN} - <<'PY'
from pathlib import Path
import os
import sys

root = Path(".")
skip_suffix = {".json", ".parquet", ".csv", ".log", ".png", ".jpg", ".jpeg", ".gif", ".svg", ".pyc"}
skip_names = {"LICENSE"}
check_suffix = {".py", ".sh", ".md", ".yaml", ".yml", ".xml", ".ipynb"}

raw_paths = os.environ.get("OAT_CHECK_PATHS", "").strip()
if raw_paths:
    candidates = []
    for item in raw_paths.split():
        p = Path(item)
        if p.is_file():
            candidates.append(p)
else:
    candidates = [p for p in root.rglob("*") if p.is_file()]

missing = []
for path in candidates:
    if ".git" in path.parts or ".venv" in path.parts:
        continue
    if path.name in skip_names or path.suffix.lower() in skip_suffix:
        continue
    if path.suffix.lower() not in check_suffix:
        continue
    if path.as_posix().startswith("data/"):
        continue

    text = path.read_text(encoding="utf-8", errors="ignore")
    head = text[:2500]
    has_copyright = "Copyright (c)" in head and "Southeast University" in head
    has_cann = "CANN Open Software License Agreement Version 2.0" in head
    if not (has_copyright and has_cann):
        missing.append(path.as_posix())

if missing:
    print("[oat-check] ERROR: missing Copyright / CANN-2.0 header in:")
    for item in missing:
        print(f"  - {item}")
    sys.exit(1)

print("[oat-check] PASS: OAT.xml present; source headers look compliant (CANN-2.0).")
PY

if command -v oat >/dev/null 2>&1; then
  echo "[oat-check] Detected oat binary, running full scan..."
  oat -f OAT.xml -s .
else
  echo "[oat-check] INFO: oat binary not found; skipped full OSS Audit Tool scan."
fi
