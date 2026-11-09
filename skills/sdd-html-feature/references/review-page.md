# Feature page requirements

One UTF-8 HTML file per feature, `sdd/<feature>.html` by default (use the project's own convention if it has one). It is the single source of truth for every phase. Start from [../templates/feature.html](../templates/feature.html) and replace the example content.

## Tabs and the summary-first format

Tabs: **Design, Spec, Architecture, Build, QA, Grade, Approvals**. Add tabs as phases are reached; keep earlier ones. Each tab status chip says approved, awaiting approval, not started, done, n/a, skipped or unavailable (the Approvals chip counts gates, for example "0 of 3 gates") (with the reason in the panel). The header badge states the current gate.

Every tab except Approvals (a plain record table) has the same shape:

1. **At a glance** (first): a screenful with everything the reader must decide or know: what changes, the failure paths, decisions to settle, what is not verified, and the exact chat reply needed for the next gate.
2. **Detailed report** (`<h2 class="rep">`): all the detail, containing everything in the glance and more, never different content. Spec tab: full Given/When/Then for every scenario (in `<details class="gwt">`), the contracts, and the traceability table.

Tabs use ARIA `tablist`, `tab` and `tabpanel`, arrow keys, Home and End, and `#hash` links. Without JavaScript all panels are visible. Print shows every panel; `details` are opened by the `beforeprint` script and by a `::details-content` print rule where the browser supports it.

## Content by feature type

Pick what resolves a decision; mark a view "N/A — reason" when it does not apply.

- **Backend or API:** sequence diagram with real actors and F-frames; request/response examples; status and error codes; state after each failure; data model or lifecycle if it resolves a decision.
- **CLI:** transcripts of success and each failure, exit codes, help text, flags and defaults.
- **Library:** usage snippet, public interface and errors, dependency direction.
- **Jobs and services:** trigger, schedule, retry and idempotence, lifecycle (states and transitions), side effects.
- **Frontend:** realistic copy; every state (empty, loading, error, success) as a gallery; a narrow layout; map each screen state to the response or event causing it.
- **Docs or guidance only:** show before and after text, what changes in behavior, and how it will be checked.

## Diagrams

Inline SVG only, 3–7 named nodes per diagram, with `<title>`, `<desc>`, `aria-labelledby` and a text equivalent under it. A diagram answers one question (for example "where is input validated?"). Use stable IDs (F1, S1). Colour is never the only signal: nodes carry a text tag (NEW, CHANGED, EXISTING, DEFERRED; sequence-diagram headers may use "· added" or "· existing" instead) and a distinct line style (thick = changed, dashed = deferred or failure). Diagrams shown in the template: sequence with failure frames, dependency graph with legend. Others to use when helpful: lifecycle/state, data model, contract/seam. Markers use `fill="context-stroke"` so they follow the line colour.

Do not use Mermaid in a page that would need a CDN. If the project mandates Mermaid source, keep it in the project's design file and reproduce a simplified diagram here.

## Theme and accessibility

Define colours as `:root` tokens; override them in `@media screen and (prefers-color-scheme:dark)`. Use `color-mix` for tints. Keep text contrast adequate in both themes, visible focus outlines, and a narrow layout that needs no horizontal scrolling at 320 px (tables scroll locally in a focusable region). Tables with five or more prose columns (QA runs, failures) use `<table class="cards">` with a `data-label` on each `<td>`; the template CSS turns each row into a labelled card below 600 px (the inline chat frame included), so nothing scrolls sideways and no column has to be dropped. Wrap each SVG in a focusable `.scroll` region with a minimum width on narrow screens so labels stay legible. Do not disable zoom. Announce changed summaries with a small polite live region. Data-driven labels use `textContent`, never `innerHTML`.

Reviewer notes say "Review only"; mock content says "Simulation". No "Approve" button that implies workflow authorization.

## Inline render in chat

At the end of each phase, when the host can render interactive HTML inline, show a compact version: the **At a glance** content open, and the detailed report inside one collapsible `<details class="big">`. Generate it from the page, do not retype it (drift): `python3 <skill-dir>/scripts/inline_view.py sdd/<feature>.html <tab>`, where `<skill-dir>` is the skill's folder, and pass that HTML straight to the host's renderer (do not save it in the project). Mark elements to omit from the inline copy with class `skip-inline` on a `<p>` or `<nav>`. Each panel must open exactly as `<div role="tabpanel" id="p-<tab>" …>` (that attribute order) and may not contain `<div` or `</main>` inside a comment; the script refuses to emit a panel whose `<div>` tags do not balance. The inline version uses transparent body and the host's theme variables with fallbacks. If the host cannot render inline, give the file path and say how to open it. Never claim an inline preview that did not happen.

## Approvals tab

Record only approvals actually received in chat: gate, date, approved content (a short hash of the tab content is optional, but note it identifies what was approved, not what the page shows today), and the user's words. Later edits to status labels and traceability are not re-approvals; a behaviour, scope or contract change reopens the gate that owns it.

## Before requesting approval

1. Open the saved file with networking disabled when browser tools exist. Exercise tabs, selectors, disclosures, links, keyboard use, a narrow viewport, dark mode and print; check the console.
2. Check every relative link. Check each diagram has a text equivalent. Check every failure ID appears in the failure inventory and in the traceability table.
3. Confirm there are no remote assets, live calls, secrets or untrusted HTML.
4. Without browser tooling, inspect statically and say which visual and interaction checks did not run.
5. Link the saved file in the conversation.

No validator can establish design completeness. Report mechanical checks separately from human review and actual browser checks.
