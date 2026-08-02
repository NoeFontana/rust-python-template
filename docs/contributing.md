# Contributing

Thanks for your interest in contributing to rust-python-template.

Coding agents should read `AGENTS.md` in the repository root, which is the
machine-facing subset of this guide.

## Repository layout

```
Cargo.toml                       workspace root: shared metadata, lints, deps
pyproject.toml                   maturin build backend + uv dev deps
rust-toolchain.toml              stable channel, pinned
justfile                         single task surface
mkdocs.yml                       documentation site
deny.toml                        cargo-deny configuration
crates/
├── rust-python-template-core/   pure-Rust core; #![forbid(unsafe_code)]
└── rust-python-template-ffi/    PyO3 bindings, publish = false
python/rust_python_template/     Python wrapper + .pyi type stubs
tests/
├── rust/                        cargo integration tests against -core
└── python/                      pytest against the FFI boundary
tools/docs/                      generators for the generated reference pages
docs/adr/                        architecture decision records (unpublished)
docs/engineering/                opt-in extension catalogue (unpublished)
```

The pure-Rust core lives in `crates/rust-python-template-core` and is the
source of truth for the library's behavior. The FFI crate is a thin shell
around it that handles Python ↔ Rust conversion. Keep business logic out
of `-ffi`.

## Prerequisites

- Rust (stable, pinned by `rust-toolchain.toml`) via `rustup`.
- [`uv`](https://docs.astral.sh/uv/) for Python + venv.
- [`just`](https://github.com/casey/just) for the task surface.
- `cargo-nextest` (`cargo install cargo-nextest --locked`).
- `cargo-deny` (`cargo install cargo-deny --locked`).

## Quickstart

```sh
just bootstrap        # sync venv + build FFI extension in release mode
just check            # lint + test + docs-test: the full gate
just fmt              # auto-fix: cargo fmt + ruff format + ruff --fix
just audit            # cargo-deny: advisories, licenses, bans, sources
just build            # produce a release wheel in target/wheels/
```

`just` is the task surface; run `just --list` for everything. CI invokes the
same recipes, so a green `just check` locally means a green CI.

Day-to-day iteration: `just develop` (debug build of the FFI extension) is
faster than rebuilding in release mode. Re-run `just develop` after any
Rust change.

## Decision records

Architecturally significant changes ship with an Architecture Decision Record
in `docs/adr/`. A record is required for anything that touches the public API
(Rust or Python), the crate boundaries, the build system, or the release
process. Bug fixes, behavior-preserving refactors, and dependency bumps do
not need one.

To create a record:

```sh
just adr short-kebab-title
```

That copies `docs/adr/template.md` to `docs/adr/NNNN-short-kebab-title.md`.
Leave the number as `NNNN` — **numbers are assigned on merge**, not on draft,
so concurrent PRs don't collide. Ship the record in the same PR as the change
it describes; it starts at status `proposed` and becomes `accepted` when the
PR merges.

Moving a record from `proposed` to `accepted` is the architectural review:
open questions resolved, alternatives named and their rejections recorded, the
plan concrete enough that the implementer does not have to invent anything.

**An accepted record is never edited.** If circumstances change, write a new
record that supersedes it and set the old record's status line to
`superseded by ADR-NNNN`. That status edit is the only permitted modification.
Implementation PRs are linked under *Links and references* as they land; the
status does not change when the code ships.

Records are not published to this site — they are engineering history, not
user documentation. The [decision record index](reference/adr-index.md) lists
their numbers, titles, and statuses.

## Documentation

Documentation follows [Diátaxis](https://diataxis.fr/) per ADR-0003. Every page
belongs to exactly one quadrant; decide which before you start writing:

| Quadrant | Directory | Purpose |
| --- | --- | --- |
| Tutorial | `docs/tutorials/` | Learning-oriented. A guaranteed-to-succeed path. |
| How-to | `docs/how-to/` | Task-oriented. One page per task the reader arrives with. |
| Reference | `docs/reference/` | Information-oriented. Mostly generated. |
| Explanation | `docs/explanation/` | Understanding-oriented. Why, not how. |

Three rules that CI enforces:

- **There are two reference surfaces.** rustdoc on docs.rs documents the
  `-core` crate; this site documents the Python wrapper. Don't mirror one into
  the other.
- **Generated pages are generated.** `reference/api.md` renders docstrings via
  mkdocstrings; `reference/adr-index.md` is written by `tools/docs/`. Change
  the docstring or the generator, never the page. Run `just docs-index` and
  commit the result — CI regenerates and fails on any diff.
- **Every fenced `python` block runs as a test.** Tutorial pages carry state
  across blocks using the `continuation` fence option; how-to blocks stand
  alone. Use `notest` only for a block that genuinely cannot execute.

```sh
just docs         # serve locally with auto-reload
just docs-test    # run every fenced block and wrapper doctest
just docs-build   # mkdocs build --strict
```

`just docs-test` imports the Python wrapper, which re-exports from the compiled
`._core` module. Run `just develop` first on a clean tree, or the import fails.

## Pull-request checklist

Before opening a PR:

- [ ] `just check` passes (lint, tests, and documentation examples).
- [ ] `just audit` is clean (or the failure is explained in the PR).
- [ ] `just docs-index` leaves the working tree clean.
- [ ] Public Rust items in `-core` have doc comments (`missing_docs` is a
      warn lint); public Python symbols have Google-style docstrings (ruff's
      `D` rules).
- [ ] If the change is architectural, the linked decision record is included.

## License

Contributions are dual-licensed under Apache-2.0 and MIT at the contributor's
option. By submitting a contribution you agree to these dual-license terms.
