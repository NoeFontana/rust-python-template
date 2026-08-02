# Opt-in extensions

Relocated from the former `docs/decisions/README.md` by ADR-0002. This is a
catalogue, not a decision: nothing here is built, and adopting any of it is a
change significant enough to need its own record under `docs/adr/`.

Like `docs/adr/`, this directory is in-tree and reviewed like code, but is not
published to the documentation site.

These extensions are documented but unimplemented. Adopt only when the project
genuinely needs them:

- **CLI crate** — promote a third workspace member `<name>-cli`, pure-Rust
  (depends on `-core` only, no PyO3). Add `dist-workspace.toml` and a
  cargo-dist-generated `release.yml`. Earns its keep only when there is a
  file-in/file-out batch operation for non-Python users. Per ADR-0003, its
  reference page is generated from the parser definition, never hand-written.
- **Fuzzing** — `tools/fuzz/` with detached `[workspace]`, cargo-fuzz, and a
  slow-tier workflow.
- **Benchmarks** — `bench/` with its own uv env, `divan` or `criterion`, and
  `just bench` recipes.
- **Reference-impl oracle** — vendoring policy, `THIRD_PARTY_NOTICES.md`,
  test-only vendored code that never ships in the wheel.
- **Additional feature crates** — sibling-to-`-core` pattern; `-ffi`
  re-exports.
- **Real-model integration tests** — `[project.optional-dependencies]
  real-models = [...]` with `@pytest.mark.real_models` that skips cleanly
  when the extra is not installed.
- **Design docs** — `docs/design/` for living subsystem documentation when
  the codebase outgrows "read the decisions + the code."
- **`slow.yml` workflow** — release-mode tests, full Python-version matrix,
  env-gated whole-dataset smokes; triggered by `workflow_dispatch` before
  cutting a release tag.

## Adopted since

- **Diátaxis user docs** — previously listed here as an opt-in extension.
  Adopted by ADR-0003; the four quadrants now ship with the template.
