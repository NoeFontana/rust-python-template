# rust-python-template

A lean, opinionated template for **Rust-core + Python-frontend (PyO3)**
libraries. Hand it to an agent or a teammate; you should be running tests
on the wheel within a minute of cloning.

## What you get

- A pure-Rust core crate (`-core`) with `#![forbid(unsafe_code)]`, the
  source of truth for your library's logic.
- A thin PyO3 FFI crate (`-ffi`) — conversion only, no business logic.
- A Python wrapper package with `.pyi` type stubs.
- `maturin` + `uv` build, `just` as the single task surface.
- abi3 wheels: one wheel per (OS, arch) covers Python 3.10–3.14.
- A workspace `[lints]` table that denies `unwrap`, `expect`, `panic`,
  `todo`, `unimplemented`, `dbg!`.
- Architectural decision records under `docs/decisions/` with a
  draft → ready → implemented lifecycle.
- CI for PRs (lint + test + abi3 wheel build, tested on 3.10 and 3.14
  from the same wheel) and a release workflow with tag-anchored version
  checking and PyPI Trusted Publisher OIDC.
- Dual MIT / Apache-2.0 license.

## Using this template

1. Create a new repo from this template on GitHub (or `git clone` it).
2. Run `./setup.sh` from the repo root. It will prompt for the project
   name, author, email, and GitHub owner; rename the crates, the Python
   package, and the metadata across files; commit the result; and delete
   itself.
3. Run `just bootstrap` to sync the Python environment and build the FFI
   extension.

## Quickstart

```sh
just bootstrap        # uv sync + maturin develop --release
just test             # cargo nextest + pytest
just lint             # cargo fmt --check + clippy + ruff + pyright
```

A complete recipe list: `just --list`.

## Project shape

```
crates/
├── rust-python-template-core/   pure Rust, the source of truth
└── rust-python-template-ffi/    PyO3 bindings, publish = false
python/rust_python_template/     Python wrapper + .pyi stubs
tests/rust/                      cargo integration tests against -core
tests/python/                    pytest against the FFI boundary
docs/decisions/                  architectural decision records
```

Detailed prerequisites and contributor workflow: [`CONTRIBUTING.md`](./CONTRIBUTING.md).
Agent guidance: [`CLAUDE.md`](./CLAUDE.md).

## License

Dual-licensed under either of [Apache-2.0](./LICENSE-APACHE) or
[MIT](./LICENSE-MIT) at your option.
