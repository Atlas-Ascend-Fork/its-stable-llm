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

"""Add Apache-2.0 copyright headers to source files that support comments."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

HASH_HEADER = """# Copyright (c) 2026 Southeast University
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
"""

XML_HEADER = """<!--
Copyright (c) 2026 Southeast University

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-->
"""

MD_HEADER = """<!--
Copyright (c) 2026 Southeast University

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-->
"""

NB_SOURCE = [
    "# Copyright (c) 2026 Southeast University\n",
    "#\n",
    '# Licensed under the Apache License, Version 2.0 (the "License");\n',
    "# you may not use this file except in compliance with the License.\n",
    "# You may obtain a copy of the License at\n",
    "#\n",
    "#     http://www.apache.org/licenses/LICENSE-2.0\n",
    "#\n",
    "# Unless required by applicable law or agreed to in writing, software\n",
    '# distributed under the License is distributed on an "AS IS" BASIS,\n',
    "# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n",
    "# See the License for the specific language governing permissions and\n",
    "# limitations under the License.\n",
]

SKIP_SUFFIXES = {".json", ".parquet", ".log", ".csv", ".png", ".jpg", ".jpeg", ".gif", ".svg"}
SKIP_NAMES = {"LICENSE", "add_copyright_headers.py"}


def already_has_copyright(text: str) -> bool:
    head = text[:800]
    return "Copyright (c)" in head or "Licensed under the Apache License" in head


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
        if isinstance(src, str):
            joined = src
        else:
            joined = "".join(src)
        if "Copyright (c)" in joined[:500]:
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
        # skip this helper once placed under scripts/
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
