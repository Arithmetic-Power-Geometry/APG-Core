# Contributing to APG-Core

Thank you for your interest in APG-Core.

## Contribution rules

1. Keep all contributions compatible with GPL-3.0-or-later.
2. Do not submit proprietary code.
3. Keep mathematical notation aligned with the APG papers.
4. Add tests for every new descriptor or formula.
5. Update documentation when formulas or public APIs change.

## Development setup

```bash
git clone https://github.com/Arithmetic-Power-Geometry/APG-Core.git
cd APG-Core
python -m pip install -e ".[dev]"
pytest
```

## Pull requests

Each pull request should include:

- clear description,
- test coverage,
- formula reference if mathematical,
- no unrelated formatting changes.

## Citation requirement

Research using APG-Core should cite the APG framework and this software package.
