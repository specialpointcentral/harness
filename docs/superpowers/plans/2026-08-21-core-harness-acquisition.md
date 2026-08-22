# Core Harness Acquisition Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Acquire the seven selected upstream harness repositories reproducibly and identify publicly documented Claude Code-derived or reverse-engineered projects without importing questionable proprietary-source mirrors.

**Architecture:** Initialize the containing directory as a Git repository and keep each upstream as a shallow top-level Git submodule pinned by the outer repository. Record `shallow = true` in `.gitmodules` so subsequent initialization recommends depth-one clones; use public metadata, licensing, acknowledgements, and source-level provenance markers for Claude Code lineage analysis.

**Tech Stack:** Git shallow submodules, GitHub public repositories, shell verification, Markdown research notes.

## Global Constraints

- Core harnesses are Codex, OpenCode, Pi, Gemini CLI, DeepSeek Harness, Goose, and Aider.
- Initialize the outer directory as a Git repository on branch `main`, as explicitly approved by the user.
- Place the seven submodules directly at the repository root, not under an `upstreams/` directory.
- Use depth-one shallow submodules and record `shallow = true` for reproducible future initialization.
- Do not mirror or commit suspected leaked proprietary Claude Code source.
- Distinguish official distributed/minified packages, reverse-engineering artifacts, behavioral reimplementations, wrappers, and genuine source forks.
- Treat stars and downloads as dated adoption proxies, not unique-user counts.

---

### Task 1: Initialize the research repository and acquire seven submodules

**Files:**
- Create: `.git/`
- Create: `.gitmodules`
- Create: `codex/`
- Create: `opencode/`
- Create: `pi/`
- Create: `gemini-cli/`
- Create: `deepseek-harness/`
- Create: `goose/`
- Create: `aider/`

**Interfaces:**
- Consumes: Public upstream Git URLs.
- Produces: One outer Git repository with seven pinned, depth-one submodules.

- [x] Initialize the outer repository with `git init -b main`.
- [x] Add each repository with `git submodule add --depth 1`.
- [x] Set `submodule.<name>.shallow = true` in `.gitmodules` for all seven entries.
- [x] Verify every checkout is shallow and has the expected `origin`.
- [x] Record each default branch, `HEAD`, commit date, license, and worktree cleanliness.
- [x] Confirm no clone failed or silently resolved to an unexpected renamed repository.

### Task 2: Investigate Claude Code lineage candidates

**Files:**
- No workspace source files are created from candidate repositories.

**Interfaces:**
- Consumes: Public repository metadata, documentation, commit history, package metadata, acknowledgements, and code-search evidence.
- Produces: A provenance-calibrated classification of candidate projects.

- [x] Identify repositories that explicitly claim to reconstruct, deobfuscate, reimplement, wrap, or emulate Claude Code.
- [x] Separate code lineage from product/API compatibility and UI similarity.
- [x] Check licenses and provenance disclosures before treating a candidate as an open-source derivative.
- [x] Do not clone suspected proprietary-source mirrors into the workspace.

### Task 3: Verify and report

**Files:**
- Inspect: `.gitmodules`
- Inspect: `<submodule>/.git`
- Inspect: `<submodule>/LICENSE*`

**Interfaces:**
- Consumes: Task 1 checkouts and Task 2 evidence.
- Produces: A concise acquisition manifest and a recommended Claude Code-derived comparison set.

- [x] Run a uniform Git verification pass over all seven repositories.
- [x] Report exact checked-out commits and any source or scope caveats.
- [x] Explain which Claude-like projects are true source derivatives, reverse-engineered reconstructions, clean-room reimplementations, or wrappers.
