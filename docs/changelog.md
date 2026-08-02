# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Documentation site: Diátaxis information architecture on mkdocs-material,
  with a generated Python API reference and decision-record index (ADR-0003).
- Code-example gate: every fenced `python` block in `docs/` and every wrapper
  docstring example runs in CI.

### Changed

- Decision records moved from `docs/decisions/` to `docs/adr/` and adopted the
  MADR format, matching the sibling `python-template` (ADR-0002).
- Agent guidance moved from `CLAUDE.md` to `AGENTS.md`; `CLAUDE.md` now defers
  to it.

## [0.1.0]

### Added

- Initial release of the Rust-core + PyO3 + Python-wrapper template
- Two-crate workspace: pure-Rust `-core` and PyO3 `-ffi`
- `maturin` + `uv` build with abi3 wheels covering Python 3.10–3.14
- `just` task surface mirrored by CI
- `cargo-deny` supply-chain auditing
- Architectural decision records
