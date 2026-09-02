---
name: harness-survey-source-chapter
description: Write, review, or maintain the Chinese Agent Harness manual in this repository from fixed-source evidence. Use when work targets docs/harness-survey, approved plans or H2 order, chapter ledgers, the seven Harness systems, citations, links, synthesis, or tightly scoped review fixes.
---

# Harness Survey Source Chapter

Use this skill as the primary workflow for this repository. It owns scope,
evidence handling, prose boundaries, and final validation. External research or
writing guidance never replaces the repository's plans and source evidence.

## Select the task mode

- **Source chapter or case study:** trace one or more Harness implementations and
  write the approved chapter plus its evidence ledger.
- **Index or navigation:** update only the requested index span, links, progress
  statement, or reader route.
- **Review fix:** apply only the named findings and necessary sentence-level
  repairs; preserve the existing chapter structure unless explicitly changed.
- **Synthesis, design principles, or research agenda:** derive claims from closed
  chapter ledgers first. Use external literature or writing guidance only when
  the user requests it, and keep it subordinate to source evidence.

## Establish authority and scope

1. Read the user's requested file boundary and Git-operation boundary first.
2. Read the relevant sections of `docs/harness-survey/WRITING_PLAN.md` and
   `docs/harness-survey/IMPLEMENTATION_PLAN.md`.
3. Read `00_index.md`, chapter 04 terminology, the target file, relevant adjacent
   chapters, and the current `.superpowers/sdd/chapter-<nn>-ledger.md` when it
   exists.
4. Record the allowed files, approved H1/H2 sequence, word budget, citation keys,
   required links, and expected evidence status before investigating sources.
5. Treat fixed commits as evidence anchors, not current-state guarantees. Recheck
   each required source checkout, full commit, and worktree cleanliness before
   relying on it.

Do not modify the seven upstream source trees. Do not stage, commit, push, or
perform broad cleanup unless the user explicitly authorizes it.

## Build the evidence chain

For implementation claims, trace in this order:

`entrance -> configuration -> core state -> loop or scheduler -> boundary -> error and recovery`

Use `rg --files` before guessing paths. Record the question, Harness and commit,
entry or symbol, call chain, evidence status, confidence, and uncovered paths in
the chapter ledger.

Use the evidence labels precisely:

- `Documented`: stated by maintained project documentation.
- `Implemented`: present in source or tests.
- `Default`: selected by the actual default configuration or control path.
- `Verified`: observed through an appropriate current runtime check.
- `Inferred`: reasoned from evidence but not directly established.

Static source or test reading is not runtime verification. Keep comparison claims
narrow: authorization is not execution success, cancellation is not rollback,
correlation is not idempotency, and an independent Context is not necessarily an
independent Workspace.

## Write for readers, keep evidence internal

- Write Chinese-first, mechanism-oriented continuous prose.
- Keep paths, commits, raw fields, symbol names, call-chain details, and confidence
  assessments in the ledger rather than the reader body.
- Use paragraphs, tables, Mermaid, and the approved semantic boxes. Follow the
  target chapter's rules for code blocks, formulas, and examples.
- Explain an English term in Chinese at its first use and reuse the established
  terminology afterward.
- Add contentful links to earlier concepts or the introductory teaching case, and
  verify the target heading fragments.
- Explain mechanism, boundary, tradeoff, and consequence instead of reproducing a
  feature table in prose.

## Use optional supporting skills by name

- For external literature search or bibliography verification, use
  `academic-research-suite` when that skill is available.
- For a bounded systems-argument structure review, use `systems-paper-writing`
  when that skill is available.
- If either skill is unavailable, skip it and continue with this workflow. Do not
  resolve skills through filesystem paths or treat an optional skill as a
  prerequisite.
- Supporting-skill output is advisory. This skill remains responsible for scope,
  evidence classification, edits, and validation.

## Validate before completion

- The target is nonempty with exactly one H1 and the approved H2 count and order.
- No unintended H4, trailing whitespace, placeholders, or disallowed fenced blocks.
- Relative links and heading fragments resolve.
- Every citation key exists in `docs/harness-survey/references.bib`; newly added
  bibliographic facts have a verifiable source.
- Tracked files pass `git diff --check`; new untracked files also pass
  `git diff --no-index --check /dev/null <file>`.
- Modified files stay within the authorized scope, including ledgers and index
  updates that ordinary tracked-only diff commands may omit.
- The completion report names the changed files, chapter structure, ledger, checks
  run, and every remaining `Inferred`, unverified, or uncovered boundary.

Stop source investigation once each requested claim has a closed evidence chain
or is explicitly recorded as uncovered. Do not broaden the chapter to compensate
for missing evidence.
