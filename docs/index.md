# Rust Python Template

A Rust-core + PyO3 + Python-wrapper monorepo template. `maturin` + `uv` build,
`just` task surface, abi3 wheels (one per OS/arch covers Python 3.10–3.14),
dual MIT / Apache-2.0.

## Quick Start

1. Create a repository from the template, then clone it
2. Run `./setup.sh` to rename the project and make the initial commit
3. Run `just bootstrap` to sync the venv and build the extension
4. Run `just check` to confirm everything passes

```python
from rust_python_template import add

print(add(2, 3))
```

This block runs as a test on every commit, along with every other fenced
`python` block on this site — see [Contributing](contributing.md#documentation).

## Post-Setup

The documentation is published with [`mike`](https://github.com/jimporter/mike),
which commits the built site to a `gh-pages` branch. Configure your repository
to serve from that branch — **the deploy will silently publish nothing until
you do**:

1. Push to `main` once and let the `deploy-docs` job run. It creates the
   `gh-pages` branch.
2. Navigate to **Settings → Pages** and set the source to **Deploy from a
   branch**, then select **`gh-pages`** and the **`/` (root)** folder. Not
   "GitHub Actions" — that source is for artifact-based deploys, which this
   is not.
3. Check that **Settings → Actions → General → Workflow permissions** is set to
   **Read and write permissions**, so the deploy job can push that branch.

Once configured, `main` publishes under the `latest` alias and each release tag
publishes a `<major>.<minor>` version plus the `stable` alias, which the
version selector in the header exposes.

## Where things are documented

This project has two public API surfaces, documented by two different tools:

| Surface | Audience | Where |
| --- | --- | --- |
| Python wrapper | Most users | [API reference](reference/api.md) on this site |
| `-core` Rust crate | Rust consumers | rustdoc, published to [docs.rs](https://docs.rs/) |

New here? Start with the [getting-started tutorial](tutorials/getting-started.md).
