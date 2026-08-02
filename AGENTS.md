# AGENTS.md

Instructions for coding agents working in this repository. Humans should read
`docs/contributing.md` instead — this file is the machine-facing subset.

## Read before you change anything

`docs/adr/` holds this project's architecture decision records. **Before
proposing a change to structure, tooling, dependencies, public API, crate
boundaries, or project-wide convention, read the records in that directory.**

- Records with status `accepted` are binding constraints. Follow them.
- Records with status `superseded by ADR-NNNN` or `deprecated` are history.
  Do **not** follow them; read the superseding record instead.
- Records with status `proposed` are under discussion. Do not treat them as
  decided, and do not implement them unless the task says so.
- The status is the second line of each record's body. Check it before using
  anything the record says.

If a task conflicts with an `accepted` record, stop and say so rather than
silently working around it. The correct resolution is a new ADR that
supersedes the old one, not an undocumented exception.

### The handoff bar

What you may assume when handed an `accepted` record:

- **The decision is final.** Implement it as stated. Do not redesign it
  mid-flight because you would have chosen differently.
- **There are zero open questions.** If you find one while implementing,
  **stop and ask.** Do not invent an answer.
- The rejected alternatives in *Considered options* were rejected on purpose.
  Re-proposing one requires a new record, not a comment in a PR.

## Writing a new record

Significant changes need an ADR: anything touching the public API (Rust or
Python), the crate boundary, the build system, or the release process. Bug
fixes, behaviour-preserving refactors, and dependency bumps do not.

- Run `just adr <short-kebab-title>`, which copies `docs/adr/template.md`.
- Filename `NNNN-short-kebab-title.md`, title in imperative mood.
- Use `NNNN` as the number placeholder in a draft; the number is assigned on
  merge.
- Ship the record in the same PR as the change it describes.
- Never edit an accepted record. Supersede it, and update the old record's
  status line to `superseded by ADR-NNNN` — that status edit is the one
  permitted modification. Implementation PRs are linked under *Links and
  references* as they land; the status does not change when code ships.

## Project shape

A mixed Rust/Python monorepo: a pure-Rust core, a thin PyO3 FFI layer, and a
Python wrapper. Built with `maturin` + `uv`, tasks run through `just`.

```
crates/
├── rust-python-template-core/   pure Rust; #![forbid(unsafe_code)]; source of truth
└── rust-python-template-ffi/    PyO3 → rust_python_template._core; publish = false;
                                 data conversion only, no business logic
python/rust_python_template/     user-facing Python wrapper + .pyi stubs
tests/rust/                      cargo integration tests against -core
tests/python/                    pytest against the FFI boundary
docs/adr/                        architecture decision records (unpublished)
docs/engineering/                opt-in extension catalogue (unpublished)
tools/docs/                      generators for the generated reference pages
```

**Hard rules:**

- `-core` is `#![forbid(unsafe_code)]`. No unsafe, no exceptions. If you
  need unsafe interop, it goes in `-ffi` with a `// SAFETY:` comment that
  states the invariants relied on.
- `-core` has zero Python dependencies. It must compile and test without
  libpython.
- `-ffi` does conversion only. Business logic must live in `-core`.
- Stable Rust only. Channel is pinned by `rust-toolchain.toml`.
- The workspace `[lints]` table denies `unwrap_used`, `expect_used`,
  `panic`, `todo`, `unimplemented`, `dbg_macro`. If you reach for any of
  these, you are signaling that a real error type is missing.

## Commands

Every workflow goes through `just`. CI invokes the same recipes, so the local
gate and the CI gate cannot drift apart.

| Recipe | What it does |
| --- | --- |
| `just bootstrap` | `uv sync --all-groups` + `uv run maturin develop --release`. Run once after clone. |
| `just develop` | Rebuild the FFI extension in debug mode (fast iteration). |
| `just build` | Build a release wheel into `target/wheels/`. |
| `just test` | Full suite: `cargo nextest run --workspace` then `pytest`. |
| `just test-rust` | Rust tests only. |
| `just test-py` | Python tests only. |
| `just lint` | `cargo fmt --check`, `clippy -D warnings`, `ruff check`, `ruff format --check`, `pyright`. |
| `just fmt` | Auto-fix: `cargo fmt`, `ruff format`, `ruff check --fix`. |
| `just check` | The default gate: `lint`, `test`, `docs-test`. |
| `just docs` | Serve the documentation site locally. |
| `just docs-test` | Every fenced Python block in `docs/` + wrapper doctests. |
| `just docs-build` | `mkdocs build --strict`. |
| `just docs-index` | Regenerate the generated reference pages. |
| `just adr TITLE` | Scaffold a new ADR from the template. |
| `just audit` | `cargo deny check` (advisories, licenses, bans, sources). |
| `just clean` | Remove `target/`, `.venv/`, built `_core*.so` artifacts. |
| `just versions` | Print toolchain versions. |

## Single-test invocations

- Rust: `cargo nextest run -p rust-python-template-core -- add_works`
- Python: `uv run pytest tests/python/test_add.py::test_add`

## Conventions you might not pick up from the code

- **Errors:** use `thiserror` in `-core` for typed errors. `-ffi` converts
  them to `PyErr` at the boundary.
- **Docs:** `missing_docs` is a warn-by-default lint. Every public item in
  `-core` should have a doc comment.
- **PyO3 version:** 0.29 with `abi3-py310`. One wheel covers Python
  3.10–3.14. Do not pin a specific Python version.
- **`unreachable_pub`** is a warn lint; prefer `pub(crate)` for items not in
  the public API.
- **Documentation follows Diátaxis** per ADR-0003. A new page goes in
  `tutorials/`, `how-to/`, `reference/`, or `explanation/` — decide which
  quadrant before writing, and don't create a fifth.
- **Two reference surfaces.** rustdoc on docs.rs documents `-core`; the mkdocs
  site documents the Python wrapper. Don't mirror one into the other.
- **Generated pages are generated.** `docs/reference/adr-index.md` is written
  by `tools/docs/`. Change the generator or the source, never the page.
- **Fenced `python` blocks in `docs/` run as tests.** Tutorial pages carry
  state between blocks with the `continuation` fence option; how-to blocks
  stand alone. Use `notest` only when a block genuinely cannot run.

## What's deliberately out of scope

CLI, fuzzing, benchmarks, reference-impl oracle, real-model integration
tests, design docs, slow-tier CI workflow. See
`docs/engineering/opt-in-extensions.md`. These are documented recipes, not
promised features. Adopting one needs its own ADR.

## Before you say you're done

```bash
just check        # lint, tests, and documentation examples
just docs-index   # regenerate the generated reference pages
just docs-build   # mkdocs build --strict
just audit        # cargo-deny
```

`just check` must pass, and `just docs-index` must leave the working tree
clean — CI runs the same generator and fails on any diff. `just docs-test`
needs a built extension module; run `just develop` first on a clean tree. If
you changed a public symbol, its doc comment changes in the same commit.
