# ADR-0002: Adopt the MADR format and the shared `docs/adr/` path

- **Status:** accepted
- **Date:** 2026-08-02
- **Deciders:** project lead
- **Consulted:** —
- **Informed:** all contributors

## Context and problem statement

ADR-0001 established a decision-record practice for this repository: a single
document type at `docs/decisions/`, a four-status lifecycle
(`draft → ready → implemented → superseded by NNNN`), two gates, and an
agent-handoff bar spelled out in that directory's `README.md`. That practice
has worked. Nothing here is a complaint about it.

What has changed is that this repository is no longer the only project
template in use. A sibling Python-only template exists, the two are maintained
together, and the same contributors and the same coding agents move between
them. Both templates independently grew a decision-record practice, and they
grew *different* ones: different directory (`docs/decisions/` versus
`docs/adr/`), different template, different status vocabulary, different
header syntax (bold lines versus MADR bullet fields).

The cost of that divergence falls almost entirely on agents. An agent told to
"read the decision records before proposing changes" has to know which of two
paths to look in, which of two status vocabularies it is reading, and which of
two templates to copy when writing a new one. Every one of those is a chance
to silently do the wrong thing — and the whole point of ADR-0001 was to stop
agents from silently doing the wrong thing.

There is a second, smaller cost: tooling. A generated index of records is
worth having in both repositories, and one parser that works everywhere is
cheaper to maintain than two that each work in one place.

This decision triggers ADR-0001 §"Significant changes" (it changes a
project-wide convention) and is therefore itself recorded here.

## Decision drivers

- **Cross-repository consistency beats local optimality.** For a convention
  whose primary consumer is an agent reading an unfamiliar checkout, one
  convention that is slightly wrong everywhere beats two that are each locally
  perfect.
- **Nothing load-bearing from ADR-0001 may be lost.** The `draft → ready`
  review gate, the immutability lock, and the agent-handoff bar are the parts
  of ADR-0001 that actually do work. A format migration that drops them is a
  regression dressed up as a cleanup.
- **One index generator for both repositories.** The parser should be a copied
  file, byte-identical, not a fork.
- **The migration must not rewrite history.** ADR-0001 is a real decision that
  was really made. It becomes history; it does not become untrue.

## Considered options

1. **Keep `docs/decisions/` and this repository's format.** Port only the
   gates and the tooling, teaching the index generator a second parser.
2. **Rename the directory to `docs/adr/` but keep this repository's status
   vocabulary and template.** One path, two formats.
3. **Adopt `docs/adr/` and the MADR format wholesale**, superseding ADR-0001
   and folding its lifecycle guarantees into the new practice.

## Decision outcome

Chosen: **option 3.**

`docs/adr/` is the path. [MADR](https://adr.github.io/madr/) is the format, as
described in `docs/adr/template.md` — which is byte-identical to the sibling
template's copy. Statuses are `proposed`, `accepted`, `superseded by ADR-NNNN`,
and `deprecated`. Records are numbered sequentially, four digits, append-only,
with the number assigned on merge.

Option 1 was rejected because the divergence it preserves is exactly the thing
that costs agents, and because a two-parser index generator is a fork with
extra steps. Option 2 was rejected as the worst of both: it pays the full cost
of moving every inbound link while keeping the format difference that actually
causes the confusion, and it would leave ADR-0001's own text — which describes
`docs/decisions/` — inaccurate about its own location with nothing recording
why.

### Mapping the old lifecycle onto MADR

MADR has four statuses and this repository's practice had four, but they are
not the same four. The mapping, and where each guarantee now lives:

| ADR-0001 status | MADR status | What carries it now |
| --- | --- | --- |
| `draft` | `proposed` | Under discussion. Not binding. Do not implement. |
| `ready` | `accepted` | Decision final. Implement as stated. |
| `implemented` | `accepted`, with implementation PRs listed under *Links and references* | The record does not change when the code lands; the links accumulate. |
| `superseded by NNNN` | `superseded by ADR-NNNN` | Unchanged but for the `ADR-` prefix. |

The collapse of `ready` and `implemented` into `accepted` is the one real loss,
and it is deliberate. Those two statuses answered "has this shipped?", which is
a question about the code, not about the decision. Git and the linked PRs
answer it better than a status line that someone has to remember to update.
The immutability lock moves from `implemented` to `accepted`: once a record is
accepted, it is not edited, only superseded.

### What carries over unchanged

Three things from ADR-0001 and its `README.md` survive this migration verbatim
in substance, because they are the parts that do the work:

1. **The review gate.** A record is `proposed` while open questions remain.
   Moving to `accepted` *is* the architectural review: open questions resolved,
   alternatives named and their rejections recorded, the plan concrete enough
   that the implementer does not have to invent.
2. **The immutability lock.** An `accepted` record is never edited. Revise by
   writing a new record that supersedes it; the superseded record's status line
   is the only thing that ever changes, and only to point at its successor.
3. **The agent-handoff bar.** What an agent may assume on picking up an
   `accepted` record: the decision is final and is implemented as stated, not
   redesigned; there are zero open questions; **if the agent finds one while
   implementing, it stops and asks rather than inventing an answer.** This now
   lives in `AGENTS.md`, which is where an agent will actually look.

### Migrating the existing record

ADR-0001 stays where it is in the sequence, is renumbered not at all, and keeps
its body. Two mechanical changes are made to it, and this section is the
authorisation for them:

- Its header block is reformatted from bold lines into MADR bullet fields, so
  that the shared index generator can parse it. No field's meaning changes.
- Two relative links are repointed at files this migration moved or removed.

Its status becomes `superseded by ADR-0002`, and a banner at the top marks it
as history and points here. Its reasoning is untouched.

### The former `docs/decisions/README.md`

That file held three things. The lifecycle and the gates are absorbed above.
The agent-handoff bar moves to `AGENTS.md`. The "Opt-in extensions" list — the
catalogue of deliberately-unbuilt extensions like fuzzing, benchmarks, and a
CLI crate — is not a decision and does not belong in an ADR; it moves to
`docs/engineering/opt-in-extensions.md`, which is in-tree and unpublished by
the same mechanism that hides `docs/adr/`.

## What this ADR explicitly does *not* decide

- **The documentation site.** Whether this repository publishes user-facing
  documentation, and under what information architecture, is ADR-0003.
- **Any decision ADR-0001 made about the code.** ADR-0001 was about
  record-keeping only; superseding it changes no crate boundary, no lint, and
  no build step.
- **Retroactive reformatting of future records.** Records written from here on
  use the template; nothing else gets rewritten.

## Consequences

- **Positive.** One path, one template, one status vocabulary, one index
  generator across both templates. An agent that has read either repository
  can navigate the other. The MADR template's explicit *Considered options* and
  *Pros and cons* sections capture rejected alternatives more consistently than
  the free-form *Rationale* section did.
- **Negative.** Every inbound link to `docs/decisions/` had to be updated
  (`README.md`, `CONTRIBUTING.md`, the agent guidance file). One historical
  record carries a migration banner it did not ask for. The MADR template is
  longer than the one it replaces, which raises the activation energy for
  writing a record — the failure mode to watch for is contributors deciding a
  change is "not significant enough" to justify the form.
- **Neutral.** The record count is unchanged. No code changes.

## Pros and cons of the options

- **Option 1 — keep `docs/decisions/` and the local format.** 👍 zero churn;
  no edit to an existing record. 👎 preserves exactly the divergence that costs
  agents; forces a two-parser index generator.
- **Option 2 — `docs/adr/` path, local format.** 👍 one path for muscle
  memory; existing record body untouched. 👎 pays the link-churn cost without
  buying format consistency; leaves ADR-0001 describing a path that no longer
  exists.
- **Option 3 — MADR at `docs/adr/` (chosen).** 👍 full consistency across both
  templates; one shared generator; better-structured template. 👎 supersedes a
  working practice, and collapses `ready`/`implemented` into `accepted`.

## Links and references

- ADR-0001 — superseded by this record. The practice it established continues;
  only its format and location change.
- ADR-0003 — documentation framework; specifies how these records surface (and
  don't) on the documentation site.
- [MADR](https://adr.github.io/madr/) — the format adopted here.
- `AGENTS.md` — the agent entry point, and the new home of the handoff bar.
- `docs/engineering/opt-in-extensions.md` — the catalogue relocated from the
  former `docs/decisions/README.md`.
