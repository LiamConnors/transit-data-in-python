#!/usr/bin/env python3
"""Parse markdown docs and generate a GitHub Action to test shell commands."""

import re
import sys
import textwrap
from pathlib import Path

NO_TEST = "<!-- no-test -->"
CODE_BLOCK_PATTERN = re.compile(r"^[ \t]*```sh\n(.*?)^[ \t]*```", re.MULTILINE | re.DOTALL)
HEADER_PATTERN = re.compile(r"^#\s+(.+)$", re.MULTILINE)


def extract_tests(md_path: Path) -> list[dict]:
    """Extract testable code blocks from a markdown file."""
    content = md_path.read_text()
    tests = []

    # Get page title from first heading
    title_match = HEADER_PATTERN.search(content)
    page_title = title_match.group(1) if title_match else md_path.stem

    blocks = CODE_BLOCK_PATTERN.finditer(content)
    for block in blocks:
        start = block.start()
        raw_code = block.group(1)

        # Check if preceded by no-test annotation
        before = content[:start]
        last_line = before.split("\n")[-2] if len(before.split("\n")) > 1 else ""
        if NO_TEST in last_line:
            continue

        # Clean up indentation then strip
        code = textwrap.dedent(raw_code).strip()

        tests.append({"page": page_title, "file": str(md_path), "code": code})

    return tests


def generate_action(all_tests: list[dict]) -> str:
    """Generate GitHub Action YAML from extracted tests."""
    lines = [
        "name: Test documentation commands",
        "",
        "on:",
        "  push:",
        "    branches: [main]",
        "  pull_request:",
        "    branches: [main]",
        "",
        "jobs:",
        "  test-commands:",
        "    runs-on: ubuntu-latest",
        "    steps:",
        "      - uses: actions/checkout@v4",
        "      - uses: actions/setup-python@v5",
        "        with:",
        '          python-version: "3.12"',
        "",
    ]

    for i, test in enumerate(all_tests):
        lines.append(f'      - name: "{test["page"]} - block {i + 1}"')
        lines.append("        run: |")
        for line in test["code"].split("\n"):
            lines.append(f"          {line}")
        lines.append("")

    return "\n".join(lines)


def main():
    docs_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("docs")
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(".github/workflows/test-docs.yml")

    all_tests = []
    for md_file in sorted(docs_dir.rglob("*.md")):
        all_tests.extend(extract_tests(md_file))

    if not all_tests:
        print("No testable commands found.")
        return

    action_yaml = generate_action(all_tests)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(action_yaml)
    print(f"Generated {output_path} with {len(all_tests)} test(s)")


if __name__ == "__main__":
    main()
