# rust-python-template

Rust-core + PyO3 + Python-wrapper monorepo template. `maturin` + `uv` build,
`just` task surface, abi3 wheels (one per OS/arch covers Python 3.10–3.14),
dual MIT / Apache-2.0.

## Setup

```sh
# Create from template on GitHub, then clone, then:
./setup.sh          # prompt for project name / author / owner, rename, commit, self-delete
just bootstrap      # uv sync + maturin develop --release
```

## Commands

```sh
just check          # lint + test + docs-test: the full gate
just test           # cargo nextest + pytest
just lint           # fmt + clippy + ruff + pyright
just docs           # serve the documentation site locally
just build          # release wheel to target/wheels/
just audit          # cargo-deny
```

`just --list` for everything. CI invokes the same recipes, so a green
`just check` locally means a green CI.

## Layout

```
crates/<name>-core/    pure Rust, #![forbid(unsafe_code)], source of truth
crates/<name>-ffi/     PyO3 bindings, publish = false, conversion only
python/<name>/         Python wrapper + .pyi stubs
tests/{rust,python}/   integration tests at each boundary
docs/                  Diátaxis documentation site (mkdocs-material)
docs/adr/              architecture decision records (MADR, unpublished)
```

## Documentation

Two public API surfaces, two references: the Python wrapper is documented on
the docs site, and the `-core` crate by rustdoc on [docs.rs](https://docs.rs/).
See ADR-0003.

The site is published with [`mike`](https://github.com/jimporter/mike), which
commits to a `gh-pages` branch. After the first deploy creates that branch, set
**Settings → Pages** → **Deploy from a branch** → **`gh-pages`** → **`/`**
(not "GitHub Actions"), and **Settings → Actions → General → Workflow
permissions** → **Read and write permissions**.

[`docs/contributing.md`](./docs/contributing.md) for the workflow,
[`AGENTS.md`](./AGENTS.md) for agent guidance. Architecture decisions live in
[`docs/adr/`](./docs/adr/) — read them before proposing structural changes.
