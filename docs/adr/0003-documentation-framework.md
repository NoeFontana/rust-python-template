# ADR-0003: Documentation framework — Diátaxis on `mkdocs-material`, code-tested, gated in CI

- **Status:** accepted
- **Date:** 2026-08-02
- **Deciders:** project lead
- **Consulted:** —
- **Informed:** all contributors

## Context and problem statement

This repository ships no user-facing documentation. It has a `README.md`, a
`CONTRIBUTING.md`, rustdoc comments on the public items in `-core`, and a
`.pyi` stub for the Python wrapper. The former `docs/decisions/README.md`
listed "Diátaxis user docs" among the *opt-in extensions* — documented recipes
that the template deliberately did not build.

That was the right call for a template that stood alone. It is the wrong call
now, for the same reason ADR-0002 was: this template is maintained alongside a
Python-only sibling that *does* have a documentation framework, and the two are
meant to be interchangeable starting points. A contributor or agent who learns
the docs discipline in one repository should find it in the other. Shipping the
framework in one and an "opt-in recipe" in the other guarantees that projects
seeded from this template grow documentation by accretion, which is the exact
failure ADR-0002 of the sibling template exists to prevent.

There is a wrinkle this repository has and the sibling does not: **the public
API surface is split across two languages.** `-core` is a Rust library
documented by rustdoc; the Python wrapper is what most users actually import.
A single documentation framework has to say clearly which surface it covers
and where the other one lives, or readers will land in the wrong place.

This decision triggers ADR-0001 §"Significant changes" (project-wide
convention; new top-level dependencies) as carried forward by ADR-0002.

## Decision drivers

- **Parity with the sibling template.** The IA, the gates, the generator
  scripts, and the `just` recipe names should match, so that moving between the
  two repositories costs nothing.
- **Two API surfaces, one entry point.** A reader must never have to guess
  whether the thing they want is in rustdoc or on the docs site.
- **Code-example rot is the failure mode that destroys trust.** Examples must
  be executed by CI, not reviewed by eye. Rust already has this via
  `cargo test --doc`; the Python side has nothing equivalent today.
- **No new runtime dependencies.** The docs toolchain lives in a dependency
  group and never reaches the wheel. The Rust dependency graph is untouched.
- **The framework must survive `setup.sh`.** Everything added here has to work
  after the bootstrap script rewrites the project name, package name, crate
  directory names, author, and GitHub owner across the tree.
- **Agent-legibility.** Per ADR-0001 as carried forward by ADR-0002, agents are
  first-class readers. Quadrant discipline and stable paths are what let an
  agent answer "where does this page go?" without asking.

## Considered options

Same six axes as the sibling template's framework decision, so that the two can
be compared line by line, plus one axis this repository needs and the sibling
does not.

### Axis A — Information architecture

1. **Strict Diátaxis** — four top-level directories, no exceptions.
2. **Diátaxis plus one project-specific first-class section** — the four
   quadrants, plus license to promote a single highest-leverage section to a
   top-level peer.
3. **Custom IA** — user-journey-driven sections.
4. **Single-page docs** — README at scale. The status quo.

### Axis B — Toolchain

1. **mkdocs-material** with the Python plugin ecosystem.
2. **Sphinx** with myst-parser.
3. **rustdoc only**, with the Python wrapper documented in its `.pyi` stubs.
4. **mdBook**, the Rust-ecosystem default.

### Axis C — Code-example discipline

1. **All fenced Python blocks tested in CI**, plus `--doctest-modules` over the
   Python wrapper, alongside the existing `cargo test --doc` for Rust.
2. **Tutorials only** tested; how-to and reference exempt.
3. **No automated testing** — convention only. The status quo for Python; Rust
   already has C1-equivalent coverage.

### Axis D — Reference generation

1. **Auto-generated everywhere possible** — Python API via mkdocstrings, ADR
   index from the record fields.
2. **Hand-written, with generated cross-references.**
3. **Auto-generated API only**; hand-write the index pages.

### Axis E — Versioning policy

1. **Per minor release** via `mike`; patch releases overwrite within a minor.
2. **Per patch release.**
3. **Latest only.**

### Axis F — Maintenance ownership

1. **Project lead through 0.1.x**, reviewer rotation when external doc PRs
   become regular (>5/month).
2. **Dedicated docs maintainer from day one.**
3. **Round-robin** across all contributors.

### Axis G — Where the Rust API is documented

1. **rustdoc on docs.rs is the Rust reference; the mkdocs site covers the
   Python surface and links out to docs.rs.** Two surfaces, each documented by
   its native tool, one cross-link.
2. **Mirror the Rust API onto the mkdocs site** with a rustdoc-to-Markdown
   step.
3. **Document only the Python surface** and treat `-core` as an internal
   implementation detail with no published reference.

## Decision outcome

Chosen: **A2 + B1 + C1 + D1 + E1 + F1 + G1.**

### Information architecture (A2)

Diátaxis, with the same licensed bend the sibling template takes: a project may
promote exactly one project-specific section to a top-level peer when that
section is its dominant adoption surface. This template ships the four
quadrants and does not use the promotion.

`docs/adr/` and `docs/engineering/` are **not user-facing**. They stay in-tree,
reviewed like code, and are excluded from the published site via mkdocs 1.6's
`draft_docs` — which keeps them visible in `mkdocs serve` for local review while
publishing nothing — together with `not_in_nav` to suppress the omitted-files
warning. `reference/adr-index.md` exposes ADR numbers, titles, and statuses.

The tree lands as:

```
docs/
├── index.md                       # landing — value prop, install, 60-second example
├── tutorials/                     # learning-oriented; cap at 3
│   └── getting-started.md
├── how-to/                        # task-oriented; one page per task
│   └── index.md
├── reference/                     # information-oriented; mostly generated
│   ├── api.md                     # mkdocstrings over the Python wrapper
│   └── adr-index.md               # generated from docs/adr/
├── explanation/                   # understanding-oriented
│   └── architecture-overview.md   # the crate split, and why -core is pure
├── contributing.md
├── changelog.md
├── adr/                           # unpublished: decision records
└── engineering/                   # unpublished: opt-in extension catalogue
```

A1 was rejected for the reason the sibling template rejects it. A3 loses the
quadrant discipline that is the point of adopting a framework. A4 — the status
quo — does not scale and defeats generated reference.

### Toolchain (B1)

mkdocs-material, matching the sibling template, with mkdocstrings (Python
handler), mike, mkdocs-redirects, lychee, pytest-markdown-docs, and codespell.

B3 (rustdoc only) is what the repository does today; it was rejected because
rustdoc documents `-core`, and `-core` is explicitly *not* the surface most
users touch — the Python wrapper is. B4 (mdBook) is the natural Rust-ecosystem
choice and was rejected only because it would diverge from the sibling template
for no gain; it has no mkdocstrings equivalent for the Python side, which is
the surface that needs generating. B2 (Sphinx) was rejected as heavyweight and
RST-encumbered.

### Code-example discipline (C1)

Every fenced `python` block in `docs/` runs as a test, and the Python wrapper's
docstrings run under `--doctest-modules`. Rust examples already run under
`cargo test --doc`, which CI has run since the initial commit; this decision
brings the Python side up to the standard the Rust side already meets.

- **Tutorials**: blocks run in sequence, carrying state via the `continuation`
  fence option.
- **How-to guides**: blocks run in isolation.
- **Reference**: examples live in docstrings and in rustdoc, and run under
  `pytest --doctest-modules python/` and `cargo test --doc` respectively.

Both pytest invocations pass `--no-cov` so that a docs-only run is not judged
against a package coverage threshold.

**These gates require a built extension module.** `python/` re-exports from
`._core`, so importing it in a doc example fails unless `maturin develop` has
run. The docs recipes therefore depend on a built extension, and the CI docs
job builds one before running them. This is the one place where this
repository's docs gate is meaningfully more expensive than the sibling's.

C2 and C3 were rejected for the reasons the sibling template gives: how-to
guides are the most-clicked pages in adoption, and hand-discipline does not
survive contributor turnover or agents.

### Reference generation (D1)

- **Python API** — mkdocstrings over `python/`, rendering the wrapper's
  docstrings. One page, one `:::` directive per public module.
- **ADR index** — generated by `tools/docs/gen_adr_index.py`, byte-identical to
  the sibling template's copy.
- **CLI** — not applicable. This template ships no CLI; a CLI crate remains an
  opt-in extension. If that extension is adopted, its reference page is
  generated from the parser definition, not hand-written, and not scraped from
  `--help`.

### Versioning (E1)

`mike` versions the docs per minor release; patch releases overwrite within
their minor. `stable` points at the latest tagged release, `latest` at `main`.

Because this repository has never published a documentation site, adopting E1
here costs nothing to migrate — there is no existing Pages deployment to
replace. It does still require the repository's Pages source to be set to
*Deploy from a branch → `gh-pages` → `/`* by hand, once, before the first
deploy will serve anything.

### Ownership (F1)

Project lead through 0.1.x. Every PR that changes a public symbol — Rust or
Python — updates its doc comment in the same PR.

### Rust API location (G1)

**rustdoc is the Rust reference and docs.rs is where it lives.** The mkdocs
site documents the Python surface and links out. `-core` already carries
`missing_docs` as a warn lint and CI already builds rustdoc with
`-D warnings`; that machinery stays exactly as it is.

G2 (mirroring rustdoc into mkdocs) was rejected: it means maintaining a
conversion step, and it produces a second copy of the Rust reference that can
drift from docs.rs — which is where Rust users will look regardless of what we
publish. G3 (Python only, `-core` undocumented) was rejected because `-core` is
a publishable crate that a Rust consumer can depend on directly; leaving it
without a published reference would be a real loss for a real audience.

The consequence to accept: **there are two reference surfaces, and the site
must say so.** `reference/api.md` opens by naming the split and linking to
docs.rs.

### CI gates

Six gates, all new to this repository except the fourth:

1. **Docstring/doc-comment coverage** — `missing_docs` on the Rust side
   (already enforced); ruff's `D` rules adopted for the Python side.
2. **Code-example testing** — `pytest --markdown-docs docs/ --no-cov` and
   `pytest --doctest-modules python/ --no-cov`, wired into `just docs-test` and
   therefore into `just check`. Rust examples continue under
   `cargo test --doc`.
3. **Link checking** — internal links on published pages are gated per-PR by
   `mkdocs build --strict` (gate 4). `lychee` runs weekly over the Markdown
   sources, covering external URLs plus `docs/adr/`, `docs/engineering/` and
   the root Markdown files that mkdocs does not build. External link checks
   are too flaky for a merge gate.
4. **Build success** — `mkdocs build --strict`.
5. **Spelling** — `codespell`, as a CI step so it gates PRs from forks.
6. **Generated-page freshness** — regenerate `reference/adr-index.md` and
   `git diff --exit-code`.

## What this ADR explicitly does *not* decide

- **Specific tutorial / how-to content.** This sets the framework and the
  gates. Content lands PR by PR with the code-example gate as the quality bar.
- **AI-generated prose.** Hard no, matching the sibling template. Agents may
  scaffold structure, wire gates, and generate what is mechanically
  generatable; the prose is written by a human.
- **Whether `-core` gets its own long-form Rust book.** If the Rust surface
  ever outgrows rustdoc, that is a later decision.
- **Publishing the crate to crates.io**, or the release process generally.
- **Translations, video, third-party analytics, a custom domain.** Same
  rejections as the sibling template, for the same reasons.

## Consequences

- **Positive.** The two templates become genuinely interchangeable: same IA,
  same gates, same recipe names, same generator. Python examples stop being
  unverified. The Python wrapper gets a real reference page instead of a stub
  file readers have to find in the source tree.
- **Negative.** A documentation site is now a thing this template has to keep
  working: a `mkdocs.yml`, a plugin set, two CI jobs, and a Pages setting.
  The docs gate needs a built extension module, so `just check` now costs a
  `maturin develop` on a clean tree — the slowest gate in the repository. The
  opt-in-extensions catalogue loses an entry, which is a small admission that
  "opt-in" was doing work "we haven't decided yet" should have been doing.
- **Neutral.** No new runtime dependencies and no change to the Rust dependency
  graph. The wheel is byte-for-byte unaffected.

## Pros and cons of the options

### A. Information architecture

- **A1 strict Diátaxis.** 👍 unambiguous. 👎 no room for a dominant adoption
  surface.
- **A2 Diátaxis + one licensed peer (chosen).** 👍 discipline where it pays,
  promotion where it matters. 👎 a bend purists will question.
- **A3 custom IA.** 👍 flexible. 👎 loses the anti-drift discipline.
- **A4 single page (status quo).** 👍 zero cost. 👎 doesn't scale; defeats
  generated reference.

### B. Toolchain

- **B1 mkdocs-material (chosen).** 👍 parity with the sibling; mkdocstrings
  generates the Python reference. 👎 a plugin set to keep current, in a repo
  that previously had no site at all.
- **B2 Sphinx.** 👍 Python heritage. 👎 heavyweight, RST-encumbered.
- **B3 rustdoc only (status quo).** 👍 nothing to build. 👎 documents the
  surface users don't import.
- **B4 mdBook.** 👍 native to the Rust ecosystem. 👎 no generated Python
  reference; diverges from the sibling for no gain.

### C. Code-example testing

- **C1 all blocks tested (chosen).** 👍 brings Python up to the standard Rust
  already meets. 👎 the gate needs a built extension module.
- **C2 tutorials only.** 👍 cheaper. 👎 broken how-to guides break adoption.
- **C3 convention only.** 👍 free. 👎 doesn't survive turnover or agents.

### D. Reference generation

- **D1 generate everywhere possible (chosen).** 👍 mechanically true to the
  code. 👎 generators to maintain.
- **D2 hand-written + cross-refs.** 👍 nicer prose. 👎 rots silently.
- **D3 API only.** 👍 less machinery. 👎 leaves the index page manual.

### E. Versioning

- **E1 per minor (chosen).** 👍 clean URLs at 0.x velocity; nothing to migrate
  here. 👎 needs a one-time Pages setting.
- **E2 per patch.** 👍 every release pinned. 👎 noisy selector.
- **E3 latest only.** 👍 simplest. 👎 breaks pinned readers.

### F. Ownership

- **F1 lead through 0.1.x (chosen).** 👍 consistent voice. 👎 single point of
  failure.
- **F2 dedicated maintainer.** 👍 clear ownership. 👎 nobody to dedicate.
- **F3 round-robin.** 👍 spreads context. 👎 too thin to catch IA drift.

### G. Rust API location

- **G1 rustdoc on docs.rs, linked from the site (chosen).** 👍 each surface
  documented by its native tool; no conversion step; docs.rs is where Rust
  users look anyway. 👎 two places to look; the site must be explicit about the
  split.
- **G2 mirror rustdoc into mkdocs.** 👍 one URL for everything. 👎 a
  conversion step to maintain and a second copy that can drift from docs.rs.
- **G3 Python surface only.** 👍 simplest site. 👎 abandons the Rust consumers
  of a publishable crate.

## Links and references

- ADR-0001 — the original decision-record practice, superseded by ADR-0002.
- ADR-0002 — MADR format and the shared `docs/adr/` path; establishes the
  cross-template consistency argument this record extends to documentation.
- `docs/engineering/opt-in-extensions.md` — the catalogue this record removes
  "Diátaxis user docs" from.
- [Diátaxis](https://diataxis.fr/) — the documentation framework.
- [mkdocs-material](https://squidfunk.github.io/mkdocs-material/) — the
  toolchain.
- [docs.rs](https://docs.rs/) — where the Rust reference is published.
