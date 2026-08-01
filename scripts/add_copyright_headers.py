# Copyright (c) 2026 Southeast University
# This program is free software, you can redistribute it and/or modify it under the terms and conditions of
# CANN Open Software License Agreement Version 2.0 (the "License").
# Please refer to the License for details. You may not use this file except in compliance with the License.
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR A PARTICULAR PURPOSE.
# See LICENSE in the root of the software repository for the full text of the License.

"""Add CANN-2.0 copyright headers to source files that support comments."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

HASH_HEADER = """# Copyright (c) 2026 Southeast University
# This program is free software, you can redistribute it and/or modify it under the terms and conditions of
# CANN Open Software License Agreement Version 2.0 (the "License").
# Please refer to the License for details. You may not use this file except in compliance with the License.
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR A PARTICULAR PURPOSE.
# See LICENSE in the root of the software repository for the full text of the License.
"""

XML_HEADER = """<!--
Copyright (c) 2026 Southeast University
This program is free software, you can redistribute it and/or modify it under the terms and conditions of
CANN Open Software License Agreement Version 2.0 (the "License").
Please refer to the License for details. You may not use this file except in compliance with the License.
THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR A PARTICULAR PURPOSE.
See LICENSE in the root of the software repository for the full text of the License.
-->
"""

MD_HEADER = XML_HEADER

NB_SOURCE = [line + "\n" for line in HASH_HEADER.strip("\n").split("\n")]

SKIP_SUFFIXES = {".json", ".parquet", ".log", ".csv", ".png", ".jpg", ".jpeg", ".gif", ".svg"}
SKIP_NAMES = {"LICENSE", "add_copyright_headers.py"}


def already_has_copyright(text: str) -> bool:
    head = text[:1200]
    return "Copyright (c)" in head and "CANN Open Software License Agreement Version 2.0" in head


def add_hash_style(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if already_has_copyright(text):
        return False
    if text.startswith("#!"):
        first, _, rest = text.partition("\n")
        path.write_text(first + "\n" + HASH_HEADER + ("\n" if rest and not rest.startswith("\n") else "") + rest, encoding="utf-8")
    else:
        path.write_text(HASH_HEADER + ("\n" if text and not text.startswith("\n") else "") + text, encoding="utf-8")
    return True


def add_md_style(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if already_has_copyright(text):
        return False
    path.write_text(MD_HEADER + "\n" + text, encoding="utf-8")
    return True


def add_xml_style(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if already_has_copyright(text):
        return False
    if text.startswith("<?xml"):
        first, _, rest = text.partition("\n")
        path.write_text(first + "\n" + XML_HEADER + rest, encoding="utf-8")
    else:
        path.write_text(XML_HEADER + text, encoding="utf-8")
    return True


def add_notebook(path: Path) -> bool:
    nb = json.loads(path.read_text(encoding="utf-8"))
    cells = nb.get("cells", [])
    if cells:
        first = cells[0]
        src = first.get("source", [])
        joined = src if isinstance(src, str) else "".join(src)
        if "CANN Open Software License Agreement Version 2.0" in joined[:800]:
            return False
    copyright_cell = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": NB_SOURCE,
    }
    nb["cells"] = [copyright_cell] + cells
    path.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return True


def main() -> None:
    updated = []
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file():
            continue
        if ".git" in path.parts:
            continue
        if path.name in SKIP_NAMES or path.suffix.lower() in SKIP_SUFFIXES:
            continue
        if path.resolve() == Path(__file__).resolve():
            continue

        changed = False
        if path.suffix == ".py" or path.suffix == ".sh" or path.name.endswith(".yaml") or path.name.endswith(".yml"):
            changed = add_hash_style(path)
        elif path.suffix == ".md":
            changed = add_md_style(path)
        elif path.suffix == ".xml":
            changed = add_xml_style(path)
        elif path.suffix == ".ipynb":
            changed = add_notebook(path)

        if changed:
            updated.append(str(path.relative_to(ROOT)))

    print(f"updated {len(updated)} files")
    for item in updated:
        print(f"  - {item}")


if __name__ == "__main__":
    main()
