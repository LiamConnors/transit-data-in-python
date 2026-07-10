# Transit data in Python

Static docs site for working with GFTS transit data in Python.

## Overview

This repository contains documentation built with `zensical` and published as a static site.

## Workflows

- `docs/` contains the source content.
- `site/` contains the generated site output.
- `.github/workflows/build.yml` runs the docs build.
- `.vale.ini` enables Vale linting for documentation.

## Local build

```bash
uvx zensical@latest build
```

## CI

The repository uses GitHub Actions to run a `lint` job with Vale and a `build` job for site generation.
