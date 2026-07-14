#!/usr/bin/env python3
"""Validate that GitHub Action commands match markdown docs."""

import re
import sys
import textwrap
from pathlib import Path

import yaml

NO_TEST = "<!-- no-test -->"
CODE_BLOCK_PATTERN = re.compile(r"```sh\n(.*?)```", re.DOTALL)
SOURCE_PATTERN = re.compile(r"#\s*source:\s*(.+)")


def find_line_number(file_path: Path, search_str: str) -> int | None:
    """Find the line number where a string appears in a file."""
    content = file_path.read_text()
    for i, line in enumerate(content.split("\n"), 1):
        if search_str in line:
            return i
    return None


def extract_md_commands(docs_dir: Path) -> list[str]:
    """Extract all shell commands from markdown docs in order."""
    commands = []
    for md_file in sorted(docs_dir.rglob("*.md")):
        content = md_file.read_text()
        blocks = CODE_BLOCK_PATTERN.finditer(content)
        for block in blocks:
            raw_code = block.group(1)

            before = content[: block.start()]
            last_line = before.split("\n")[-2] if len(before.split("\n")) > 1 else ""
            if NO_TEST in last_line:
                continue

            code = textwrap.dedent(raw_code).strip()
            commands.extend(line.strip() for line in code.split("\n") if line.strip())
    return commands


def extract_md_commands_by_file(docs_dir: Path) -> dict[str, list[str]]:
    """Extract commands grouped by source file."""
    by_file = {}
    for md_file in sorted(docs_dir.rglob("*.md")):
        content = md_file.read_text()
        commands = []
        blocks = CODE_BLOCK_PATTERN.finditer(content)
        for block in blocks:
            raw_code = block.group(1)

            before = content[: block.start()]
            last_line = before.split("\n")[-2] if len(before.split("\n")) > 1 else ""
            if NO_TEST in last_line:
                continue

            code = textwrap.dedent(raw_code).strip()
            commands.extend(line.strip() for line in code.split("\n") if line.strip())
        if commands:
            by_file[str(md_file)] = commands
    return by_file


def parse_action_steps(action_path: Path) -> list[dict]:
    """Parse Action steps with source comments."""
    content = action_path.read_text()
    lines = content.split("\n")

    # Find source comments and the line they appear on
    source_map = {}
    for i, line in enumerate(lines):
        source_match = SOURCE_PATTERN.search(line)
        if source_match:
            source_map[i] = source_match.group(1).strip()

    # Parse YAML to get steps
    data = yaml.safe_load(content)
    steps = []

    for job in data.get("jobs", {}).values():
        for step in job.get("steps", []):
            run = step.get("run", "")
            cmds = [l.strip() for l in run.split("\n") if l.strip()] if run else []
            steps.append({"commands": cmds, "source": None})

    # Match source comments to steps by finding which step follows each comment
    # Find line numbers of each step's run: block in the raw text
    run_positions = []
    for i, line in enumerate(lines):
        if line.strip().startswith("run:") or "run: |" in line:
            run_positions.append(i)

    # Assign sources to steps that have run blocks
    step_with_run = 0
    for pos, source in source_map.items():
        # Find which step this source comment belongs to
        for j, run_pos in enumerate(run_positions):
            if run_pos > pos and j < len(steps) and steps[j]["commands"]:
                steps[j]["source"] = source
                break

    return steps


def main():
    docs_dir = Path("docs")
    action_path = Path(".github/workflows/test-docs.yml")

    if not action_path.exists():
        print(f"✗ Action not found: {action_path}")
        sys.exit(1)

    # Check source links
    steps = parse_action_steps(action_path)
    md_by_file = extract_md_commands_by_file(docs_dir)

    errors = []
    for step in steps:
        if not step.get("source"):
            continue
        source = step["source"]
        if not Path(source).exists():
            errors.append(f"Source file not found: {source}")
            continue
        expected = md_by_file.get(source, [])
        # Check that all expected commands appear in the step (in order)
        step_cmds = step["commands"]
        j = 0
        for cmd in expected:
            while j < len(step_cmds) and step_cmds[j] != cmd:
                j += 1
            if j >= len(step_cmds):
                errors.append(f"Missing command in {source}: {cmd}")
                break
            j += 1

    if errors:
        print("✗ Source link errors:\n")
        for err in errors:
            print(f"  {err}")
        print()

    # Check that all docs commands appear in the Action
    md_commands = extract_md_commands(docs_dir)
    action_commands = []
    for step in steps:
        action_commands.extend(step.get("commands", []))

    missing_in_action = []
    for cmd in md_commands:
        if cmd not in action_commands:
            missing_in_action.append(cmd)

    if errors or missing_in_action:
        if missing_in_action:
            print("Commands in docs but not in Action:")
            for cmd in missing_in_action:
                for md_file in docs_dir.rglob("*.md"):
                    line_num = find_line_number(md_file, cmd)
                    if line_num:
                        print(f"  + {cmd}")
                        print(f"    → {md_file}:{line_num}")
                        break
            print("\n  Fix: Add these commands to .github/workflows/test-docs.yml")
        sys.exit(1)

    print("✓ Docs and Action are in sync")


if __name__ == "__main__":
    main()
