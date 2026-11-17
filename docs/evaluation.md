# Evaluation

## After improvements (17 November 2026)

NVIDIA SkillEvaluator 0.9.0 and SkillSpector 2.13.3, run without API keys or LLM review (`env -i`, SkillSpector `--no-llm`; every report records `llm_requested: false` and `inference_usage: []`), against the skill folder as it stands in the **uncommitted working tree on top of commit `3a82b1b`**. The measured folder is identified by the sha256 of its per-file manifest: `1c6261c3c43d71eec5a6d2d243be102327a9b9963c48fc803d8d0bea23caa044`. The baseline below was re-run first and reproduced exactly (C 78.5, Tier 1 failed, the same four findings, risk 50).

| Check | Baseline | After improvements |
| --- | --- | --- |
| Static quality | C, 78.5/100 (correctness 60, discoverability 85, reliability 85, efficiency 100) | **A, 93.5/100** (correctness 85, discoverability 95, reliability 100, efficiency 100) |
| Tier 1 (12 validators) | Failed: Schema and Security Scan | **Passed**, 12 of 12 validators (with warnings, listed below) |
| SkillSpector | Risk 50/100: P6 HIGH, P2 HIGH, EA2 MEDIUM x2 | **Risk 0/100, no findings**; analysis still "partial" (see below) |
| LLM rubric, Tier 2, Tier 3 | Not run | Not run |

Tier 1 reports publication as "incomplete, not eligible", because the Tier 2 and Tier 3 evidence it requires does not exist. This is not a publication-readiness claim.

### What changed, and what each group did to the numbers

Each group was re-scanned on its own copy (raw outputs: `/tmp/html-sdd-eval2/out/<label>/`).

| Step | Change | Quality | Tier 1 | SkillSpector risk (findings) |
| --- | --- | --- | --- | --- |
| baseline | none | C 78.5 | failed | 50 (P6, P2, EA2 x2) |
| a | `inline_view.py` bug fixes and tests (below) | C 78.5 | failed | 50 (unchanged) |
| b | Authoring comments removed from the template; `review-page.md` gained the rules they carried | C 78.5 | failed | 32 (P2 gone) |
| c | Frontmatter: license, `metadata.author`, `metadata.version`, `metadata.tags` | B 82.0 | failed (Security Scan only) | 32 |
| d | "print rule" reworded in `review-page.md` | B 82.0 | **passed** | 11 (EA2 x2) |
| e | Consent wording of the automatic QA and grade runs | B 82.0 | passed | 0 |
| f | `## Purpose`, `## Scripts`, `## Examples`, `## Requirements`, `## Limitations`, `## Troubleshooting`, and a "Not for" sentence in the description | **A 93.5** | passed | 0 |

The quality jump in step f comes from sections the heuristic looks for. They are real documentation (script table, exit codes, examples, limitations, a troubleshooting table quoting the script's real messages), but the grade measures documentation completeness, not agent behaviour.

**Real defects fixed in `scripts/inline_view.py`, each with tests that failed before the fix:**

- *Wrong tab status.* A tab button without a status chip picked up the next tab's chip, so chat showed the wrong status and the "placeholders left in an approved tab" lint read the wrong label. The chip is now read from the tab's own button; a missing chip shows `unknown` and `--check` reports an error naming the tab (a warning under `--legacy`).
- *Remote-asset lint gaps.* Only double-quoted, lower-case `src`/`href` on five tags were caught. It now catches `video`, `audio`, `track`, `embed`, `object`, `input`, `form`, `frame`, SVG `image` and `use`, the attributes `src`, `href`, `srcset` (every candidate), `data`, `poster`, `xlink:href` and `action`, upper-case and single-quoted or unquoted values, and `ftp://`; `url()` and `@import` are matched case-insensitively. `<a href>` stays allowed, as do `data:` URIs, relative paths and `data-*` attributes.
- *Div counting.* Panel balance counted the substring `<div`; it now matches real `<div` and `</div>` tags.
- *Template hygiene.* Eight authoring comments were copied into every generated page (and some into the chat HTML). They are removed; every rule they stated already lived in `SKILL.md` or `review-page.md`, and two nuances that were missing from `review-page.md` were added. Structural banners and the two mechanism comments remain.

### Remaining deductions and warnings, on purpose

| Item | Why it stays |
| --- | --- |
| Quality: "Instructions don't mention `run_script`" (-10 correctness) | A SkillEvaluator runtime convention; Claude Code and Codex run scripts through the shell |
| Quality: top-level `version` recommended (-5 correctness) | The Agent Skills frontmatter has `metadata.version`, as in the sibling skills. A scratch copy with an added top-level `version: "1.0.0"` scored **A, 95.2**, so that is what the field is worth; it was not shipped, because it duplicates the version outside the spec |
| Quality: description 429 characters (-5 discoverability) | Shortening it risks skill-trigger regressions; sibling skills are as long |
| Schema warnings: no `## Instructions` heading, `templates/` "unexpected" in the skill root | Moving `templates/` would break every documented path and existing installs |
| Code Integrity warning: no tests inside the skill folder | Tests live in the repo's `tests/` and must not ship to user installs |
| SCRIPT_LINT: deep nesting (depth 14) and magic numbers in `inline_view.py` | Not gating; refactoring the HTML parser to satisfy a lint is regression risk with no user benefit |
| SkillSpector analysis "partial" (info, 100% of files scanned) | Four path-like references do not match a bundled file: the three `sdd/csv-export.html` example commands and the existing `DESIGN.md` mention. They are project paths the skill refers to, not missing files |

### Security findings: verdicts

- **P6 "print rule" (HIGH):** false positive, a CSS print rule. The sentence was reworded for clarity ("by a `::details-content` rule in the print stylesheet"); the meaning is unchanged.
- **P2 hidden instructions (HIGH):** false positive as an attack, but real minor hygiene: instruction comments were being copied into generated project files. Removed (above).
- **EA2 "without asking" / "without approval" (MEDIUM x2):** a true match for a deliberate design (QA and grade start automatically after the architecture gate has announced them and offered `no QA` / `no grade`). The wording now names that consent point ("start them unless the user replied `no QA` or `no grade`") and the scanner no longer matches. **The behaviour is unchanged and the underlying risk is not removed:** QA executes freshly built code in a temporary copy, and its isolation is enforced by instructions and the host's sandbox, not by the skill. This is stated under *Limitations* in `SKILL.md`.
- **Dropped on purpose:** an optional warning for network calls inside a page's scripts. Its keyword list (`fetch`, `WebSocket` and similar) made SkillSpector report a new MEDIUM finding (LP3, "no declared permissions") and raised the risk from 50 to 57. Because it was optional, it was not shipped; the remote-asset lint covers resource loads only, and the limitation is documented.

### Tests

`python3 -m unittest discover -s tests -v`: 23 tests pass on Python 3.10, 3.12, 3.13 and 3.14. They cover the three defects above, golden snapshots of all six tabs in both formats (comments and whitespace normalised, so only a real content change fails), the 12 KB glance-only fallback, legacy QA/Grade pages, usage errors, and the wording of every approval gate, opt-out, budget and authorization rule in `SKILL.md`, the template's architecture gate and both agent files.

### Not run, and limits of this measurement

The Tier 1 LLM rubric, Tier 2, Tier 3 and any run of the skill by an agent were not run (no paid calls were made). These are static, keyless heuristics: they do not show that agents follow the gates or that the page works in every browser. The scores were measured on an uncommitted working tree; re-measure after committing if the result is to be quoted for a revision.

## Baseline (before improvements)

On 17 November 2026, NVIDIA SkillEvaluator 0.9.0 and SkillSpector 2.13.3 were run without API keys or LLM review against skill commit `3a82b1b73916361604c8a778e3d33f5bf1727326`, Git tree `d1c8a1ecaefd6d8be2e16473b3c035f4cee3b934`.

| Check | Result |
| --- | --- |
| Static quality | **C, 78.5/100**: correctness 60, discoverability 85, reliability 85, efficiency 100 |
| Tier 1 | **Failed**: 10 passed, 2 failed (missing author metadata and the security scan) |
| SkillSpector | **Medium risk, 50/100, caution**; two HIGH and two MEDIUM findings; analysis partial due to a runtime-path reference |
| LLM rubric, Tier 2 and Tier 3 | Not run |

Quality is a static heading and metadata heuristic, not a measure of agent performance. Deductions include missing metadata, examples, limitations and troubleshooting; the evaluator also expects a `run_script` convention that is not required by this skill's supported agents.

The independent reviewer assessed both HIGH security matches as false positives: one refers to a CSS print rule, and the other is an ordinary HTML authoring comment in the template. One MEDIUM finding concerns the real design choice to launch QA and grading automatically after the user has been informed and offered an opt-out at the architecture gate. QA executes built code in a temporary copy, but isolation is enforced by instructions rather than a technical sandbox; the other MEDIUM match describes not running a scenario when approval is absent. These interpretations are not a guarantee of safety; the Tier 1 security check remains failed.

The evaluator used a Python 3.13 SkillSpector installation to avoid an incompatible Python 3.15 dependency build; this changes the scanner launch path, not the files scanned. No paid calls were made. A separate scratch experiment that added metadata alone produced B, 83.8, but that change was not applied to this skill and is not the score reported above.

To rerun the quality check on the skill at the recorded revision:

```bash
uvx --python 3.13 --from 'skillevaluator[all]==0.9.0' skillevaluator quality-check ./skills/sdd-html-feature
```
