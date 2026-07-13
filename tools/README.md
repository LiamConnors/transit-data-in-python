# Documentation testing

This directory contains tools to ensure documentation commands stay accurate and in sync with CI.

## How it works

```
docs/*.md  ←→  .github/workflows/test-docs.yml
     ↑                  ↑
     └── validate-sync.py ──┘
```

1. **Markdown is the source of truth** — shell commands in docs define what should work
2. **GitHub Action runs the same commands** — hand-written in `test-docs.yml`
3. **Validator keeps them in sync** — fails CI if they drift apart

## Tools

### `test-docs.py`

Run documentation commands locally:

```sh
python tools/test-docs.py
python tools/test-docs.py --verbose
```

Parses all `.md` files in `docs/`, extracts `sh` code blocks, and runs them. Use `<!-- no-test -->` before a code block to skip it.

### `validate-sync.py`

Check that the GitHub Action matches the docs:

```sh
python tools/validate-sync.py
```

Fails if:
- A command is in docs but not the Action
- A command is in the Action but not docs
- Commands appear in different order
- A `# source:` comment points to a file that doesn't exist
- A `# source:` comment's commands don't match the file

## CI integration

Both tools run in CI via `.github/workflows/build.yml`:
- `check-docs-sync` job runs the validator on every push/PR
- `test-docs` job (in `test-docs.yml`) runs the actual commands

## Excluding blocks

Add `<!-- no-test -->` before a code block to skip it:

```markdown
<!-- no-test -->
```sh
echo "This won't run in CI"
`` `
```

## Adding new commands

1. Add the `sh` code block to your markdown
2. Add the same command to `.github/workflows/test-docs.yml` with a `# source:` comment above the step
3. Run `python tools/validate-sync.py` to verify

The `# source:` comment links the Action step back to the markdown file. The validator checks:
- The file exists
- The commands in the step match the commands in that file (in order)

Example:

```yaml
# source: docs/tutorials/realtime-dashboard/1-setup.md
- name: "Set up your development environment"
  run: |
    mkdir transit-dashboard
    cd transit-dashboard
```
