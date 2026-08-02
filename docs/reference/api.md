# API reference

This project has **two public API surfaces**, and this page documents one of
them.

- **The Python wrapper** — documented below, rendered from the package's
  docstrings. This is what `import rust_python_template` gives you, and what
  most users want.
- **The `rust-python-template-core` Rust crate** — documented by rustdoc and
  published to [docs.rs](https://docs.rs/). If you are depending on the core
  library from Rust rather than from Python, that is the reference you want.

Per ADR-0003 the Rust reference is not mirrored here; each surface is
documented by its native tool.

## `rust_python_template`

::: rust_python_template
