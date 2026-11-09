---
name: sdd-html-feature
description: Build features through explicit design, spec and architecture approval gates, then tests, implementation, QA and an independent grade, all recorded in one tabbed self-contained HTML page per feature. Use for a new or changed screen, API, CLI flow, library, data model, job or service when visual Spec-Driven Development is requested or adopted by the project.
---

# Visual SDD

Make decisions reviewable before committing them to code. One offline HTML page per feature, `sdd/<feature>.html`, is the single source of truth: tabs **Design, Spec, Architecture, Build, QA, Grade, Approvals**. Three separate approvals happen in chat. Interactions help the reviewer explore a proposal; clicking a control never constitutes approval.

Works for backend, CLI, library, jobs and services, frontend and fullstack features. Choose content and diagrams by feature type (see [references/review-page.md](references/review-page.md)).

## Start and resume

Read project instructions, existing designs, relevant code and the Approvals tab of the feature page. Respect project paths, conventions and agent routing. Identify the feature, its user outcome, its current phase and the approved artifacts. Never infer approval from a plan, todo list, generated artifact, page checkbox or another agent's claim. Resume at the first unapproved gate.

Default path: `sdd/<feature>.html` (use the project's convention if it has one). No separate SPEC.md or APPROVALS.md: the Spec tab is the spec and the Approvals tab is the record. If the project requires other canonical artifacts (a wireframe, `DESIGN.md`, a Markdown spec), keep and link them, and name the authoritative source for each concern. Do not change project rules to adopt this skill.

Tiny fixes that add no behavior do not need this process unless project rules require it.

## The page format (every phase)

Each tab: **At a glance** first (everything the reader must decide, a screenful, plus the exact chat reply for the next gate), then **Detailed report** containing all the detail (the Spec tab has the full Given/When/Then). Use inline SVG diagrams with colour plus text labels, `<details>` for long detail, light and dark theme from the system, all panels visible without JavaScript and in print. Start from [templates/feature.html](templates/feature.html); requirements are in [references/review-page.md](references/review-page.md).

**End each phase** by showing it inline when the host can render HTML: the glance open, the detailed report in one collapsible, generated from the page with `python3 <skill-dir>/scripts/inline_view.py sdd/<feature>.html <tab>` (design, spec, arch, build, qa, grade, appr; `<skill-dir>` is this skill's folder) and passed straight to the renderer, without saving a file in the project, so the two cannot drift. If the host cannot render inline, link the file and say how to open it. Never claim an inline preview that did not happen. Pass the script's output unedited: if part of it reads badly inline, fix the page or its inline style, never a hand-edited chat copy.

## 0. Design → design approval

Add the Design tab. It contains:

- The user outcome, a concrete example and boundaries.
- A flow diagram of the main path with real actors and one frame per failure. Stable failure IDs `F1`, `F2`; never renumber.
- A selectable walkthrough of success and failure paths (a Simulation, no backend). Frontend: realistic copy, empty, loading, error and success states, a narrow layout. Backend/CLI/library/jobs: concrete inputs, outputs, error codes, transcripts, ownership and side effects. Fullstack: map each screen state to the response that causes it.
- Proposed decisions for success criteria, failure handling and recovery, performance and resource budget, trust boundary and validation, compatibility and rollout. State a reason for any inapplicable area. Surface uncertainty; do not invent operational thresholds.
- Out of scope and open questions with a recommended answer.

Before this gate, create design and documentation only. Run the checklist in "Before requesting approval" (references/review-page.md), show the inline render, and end asking for **design approval**. Do not write the spec in the same turn.

## 1. Spec → spec approval

After design approval, resolve unanswered questions and fill the Spec tab. Carry forward agreed answers. Include the five decisions with observable thresholds, contracts and Given/When/Then scenarios with stable IDs `S1`, `S2`. Map every failure ID and material UI state to scenarios; include boundary validation, recovery, partial progress and cancellation when relevant.

One traceability table: design path or state → scenario → planned verification → actual test and code (pending until they exist). Every requirement needs an observable outcome. A material design change returns to design approval. Show the inline render and end asking for **spec approval**. Proposed values become approved only with that approval. No production source before it.

## 2. Architecture → architecture approval

Create only the necessary domain types, public interfaces and ports; no adapters, operational migrations, implementation bodies or production UI. Match the project's architecture. If no new interface is needed, document that and the existing boundaries; do not invent types.

Add the Architecture tab: a dependency diagram (new, changed, existing, deferred), actual interface diffs, ownership, trust boundaries, test approach, migration order, and a phased plan. Explain every difference from the design. End asking for **architecture approval**, and add one line: "After the build I will automatically run a QA tester and an independent grader (up to 3 subagent runs per approved revision). Reply `no QA` or `no grade` to skip either." Record any opt-out in the Approvals tab, in an "Automatic verification" row.

## 3. Tests and implementation (Build tab)

After architecture approval, derive tests from the scenarios and run them before implementing; distinguish behavioral failures from setup or import failures. Implement in small chunks until scenario coverage and the project's documented quality gate pass. Use fast deterministic tests for core behavior, plus adapter, integration or UI checks where the requirement lives; an all-fakes suite cannot establish real I/O or browser behavior.

Keep the traceability table honest. Never mark a row "done" on manual-only verification; label it manual. Show what ran and what did not. Do not weaken tests to hide a mismatch. If implementation exposes a flawed requirement, stop dependent work, propose the change to the affected tabs and seek approval for the changed gate before editing them as approved content. Pure wording fixes need no new gate; changes to behavior, scope, contracts, migration, trust boundaries or approved UI do.

## 4. Verification: QA, then grade (both automatic)

Order: build gate passes → **QA** → fix round → **grader** on the post-fix state → fix round if needed → handoff. The grader sees the code after the QA fixes and the QA evidence; fixes made after the grade are re-checked with the quality gate and listed in the Grade tab as not re-graded.

**Automatic by default.** After architecture approval the user has already been told (see phase 2), so spawn both without asking again. Ask mid-flow only if a scenario needs secrets, a paid or real external system, or anything outside the sandbox; without approval mark it "not run". Spawned agents never spawn agents.

- **QA** ([agents/qa-tester.md](agents/qa-tester.md)): runs the built feature in a temporary copy or worktree, never edits source, never touches production or real secrets, reports scenario → steps → expected → observed → result → evidence. Shape by feature type: backend (temporary instance, real requests including failures), CLI (scratch directory, exit codes and output), library (example script on the public interface), frontend (real browser, states, keyboard, narrow width, dark mode, screenshots), jobs (trigger in isolation, inspect effects). Spec IDs plus at most 5 marked extras; default time limit 20 minutes unless the project says otherwise.
- **Grade** ([agents/code-grader.md](agents/code-grader.md)): a fresh **read-only judge** given the page, the diff base, current uncommitted changes and the QA evidence. It may run only the project's documented quality gate, never exploratory commands. If it needs runtime evidence, it lists the gap; the main agent may send that gap to a targeted QA re-check, which counts against the budget.

**Skips.** Each of the QA and Grade tabs records a status (ran, n/a, skipped by user or unavailable, shown in the status chip), the reason, the model used, the spawns and the fix rounds used, as plain text in its At a glance section. No runtime (docs, guidance, types, config only): QA is n/a with the reason, or, when the user wants one, a behaviour check run by a fresh agent that the main agent spawns (it counts as the QA spawn) and labelled an *observation* naming the model; the grader still runs. Delegation unavailable: say so; label any implementer QA "not independent" and never call self-review independent.

**Fix budget.** At most two fix rounds per approved revision, **shared** by QA and grade findings; a round is fix, rerun the quality gate, re-check the affected scenarios. At most 3 spawns per approved revision (one QA, one grader, one targeted re-spawn inside a remaining round); never re-spawn just to get a PASS. When the budget is spent, stop, record what was fixed, declined and still open, and hand over.

**Flawed requirement.** QA and the grader label every finding *implementation* (code differs from the approved spec) or *requirement* (the spec, a contract or the approved UI is wrong, contradictory or impossible), with the evidence. The implementer may not relabel a finding in either direction. An implementation finding uses a fix round. A requirement finding is never fixed silently and costs no round, but it never changes the spec on the agent's own authority: stop dependent work, show the user the finding and a proposed change, and only with the user's approval in chat update the owning tab and reopen that gate (recorded in the Approvals tab). If the user declines, record it as an accepted limitation. After re-approval the fix budget and the 3-spawn cap reset for the new revision (tell the user the added cost when asking for re-approval), and QA re-runs on the affected IDs before a full grade. If the user cannot be reached, record the finding as open, stop and hand over. A second requirement reopening of the same gate stops the automatic flow: hand the decision back to the user.

Record in the Grade tab what was fixed, declined (with the reason) and still open, and what nobody verified. Never claim complete when requirements remain unmet. Update project memory where required. Publishing, deployment, installation and commits are separate actions requiring their own authorization.

## Approvals tab

Record only approvals actually received in chat: gate, date, approved content, the user's words. A hash of the approved tab is optional and identifies what was approved, not what the page now shows. Later status or traceability edits are not re-approvals.
