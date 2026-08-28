# Changelog

All notable changes to this project are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-08-27

### Added
- Core fingerprinting API: `fp.fingerprint()`, `fp.get_components()`, and
  `fp.machine_id()` — a stable SHA-256 device fingerprint from system
  attributes, using only the Python standard library.
- Optional HTTP client helpers (`fp.client`): `get_fingerprint()` and
  `post_fingerprint()`, built on `urllib.request`.
- Command-line entry point: `python -m fp` (and `--components`).
- `pyproject.toml` packaging with `src/` layout and empty runtime dependencies.
- `unittest` test suite with coverage.
- Stdlib-only `dev.py` task runner (`check`, `test`, `cov`, `guard`) and a
  zero-dependency guard (`tools/dep_guard.py`).

[Unreleased]: https://github.com/nativelite/fp-py/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/nativelite/fp-py/releases/tag/v0.1.0
