# Contributing

The contributor guide lives at [`docs/contributing.md`](./docs/contributing.md)
so that it is published as part of the documentation site. This file exists so
that GitHub's "Contributing guidelines" link resolves.

Coding agents should read [`AGENTS.md`](./AGENTS.md) instead.

Short version:

```sh
just bootstrap        # sync venv + build the FFI extension
just check            # lint + test + docs-test: the full gate
just audit            # cargo-deny
```

Architecturally significant changes ship with a decision record in
[`docs/adr/`](./docs/adr/). Create one with `just adr short-kebab-title`.
