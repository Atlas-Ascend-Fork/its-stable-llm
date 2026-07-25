#!/usr/bin/env bash
# Copyright (c) 2026 Southeast University
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Lightweight OAT-oriented compliance check for local pre-commit.
# 1) Ensure OAT.xml exists
# 2) Ensure comment-capable source files contain Copyright + Apache-2.0 header
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

${PYTHON_BIN} - <<'PY'
from pathlib import Path
import sys

root = Path(".")
skip_suffix = {".json", ".parquet", ".csv", ".log", ".png", ".jpg", ".jpeg", ".gif", ".svg", ".pyc"}
skip_names = {"LICENSE"}
check_suffix = {".py", ".sh", ".md", ".yaml", ".yml", ".xml", ".ipynb"}

missing = []
for path in root.rglob("*"):
    if not path.is_file():
        continue
    if ".git" in path.parts or ".venv" in path.parts:
        continue
    if path.name in skip_names or path.suffix.lower() in skip_suffix:
        continue
    if path.suffix.lower() not in check_suffix:
        continue
    if path.as_posix().startswith("data/"):
        continue

    text = path.read_text(encoding="utf-8", errors="ignore")
    head = text[:2000]
    has_copyright = "Copyright (c)" in head
    has_apache = "Apache License, Version 2.0" in head or "Licensed under the Apache License" in head
    if not (has_copyright and has_apache):
        missing.append(path.as_posix())

if missing:
    print("[oat-check] ERROR: missing Copyright / Apache-2.0 header in:")
    for item in missing:
        print(f"  - {item}")
    sys.exit(1)

print("[oat-check] PASS: OAT.xml present; source headers look compliant.")
PY

if command -v oat >/dev/null 2>&1; then
  echo "[oat-check] Detected oat binary, running full scan..."
  oat -f OAT.xml -s .
else
  echo "[oat-check] INFO: oat binary not found; skipped full OSS Audit Tool scan."
fi
