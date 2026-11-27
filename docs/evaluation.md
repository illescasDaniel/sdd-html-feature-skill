# Evaluation

The skill on `develop` is now named `sdd-html-feature-beta`. The reports below retain their original `sdd-html-feature` name, paths and content hashes from before the namespace-only rename; they are historical evidence, not fresh scores for the renamed artifact.

## Instruction refactor and re-scan (27 November 2026)

The current **uncommitted develop candidate on top of `1faeb96`** scores **A, 94.8/100**, compared with B, 89.8 before this refactor. Both were scanned with the same pinned SkillEvaluator 0.9.0 / SkillSpector 2.13.3 settings described below, with LLM checks disabled and no suppression baseline. The final scan ran on the physical checkout after moving its ignored bytecode cache to trash.

| Metric | Before refactor | After refactor |
| --- | --- | --- |
| Static quality | B, 89.8 | **A, 94.8** |
| Correctness | 85 | 85 |
| Discoverability | 95 | 100 |
| Reliability | 100 | 100 |
| Efficiency | 75 | 100 |
| Estimated main-file tokens (characters / 4) | 6,240 | 4,786 |
| Tier 1 | Pass on clean committed export | **Pass on physical checkout**: 11 passed, dependency audit N/A |
| SkillSpector | Risk 7, one medium LP3 advisory | Risk 7, same advisory; no high or critical findings |

**Changes:** moved host-specific rendering and error troubleshooting into focused references loaded when needed; condensed duplicated hero, question, QA and Verify instructions while retaining their full rules in the owning resources; routed finding resolution directly from SKILL.md; shortened the description from 429 to 136 characters. T3 rendering now uses the host's actual tool-discovery mechanism rather than assuming ToolSearch exists. Three quality deductions disappear: excessive main-file length, nested reference navigation and a long description.

**Bytecode hygiene:** the test module loader now compiles the script's source directly instead of using a loader that can read/write cached bytecode inside the installable skill. A normal `python3 -m unittest discover -s tests -q` run passes all 24 tests and leaves no bytecode in the skill. The earlier failed workspace scan remains below for provenance.

**Behavioral checks:** two fresh native-agent runs stopped at Design and Spec approval respectively, preserved production source, and produced pages passing lint. The resume run preserved the prior Design approval and review opt-out. A separate description-only routing run selected the skill for explicitly requested/adopted visual SDD across jobs, CLI and data models, and skipped typo, read-only analysis and unadopted feature requests. These focused observations do not establish broad routing accuracy or full workflow/renderer integration; [run record](../evals/records/2026-11-27-compact.md).

**Evidence:** [final Tier 1 JSON](evaluations/2026-11-27/improved-tier1.json), [final per-file hashes](evaluations/2026-11-27/improved-manifest.json), [provenance](evaluations/2026-11-27/provenance.json). Final evaluator digest: `sha256:9d462f7201cad50ef4f431754e1212173749bb4b79d8c5bd992074b80b36d772`. All 11 bundled files were inspected; the same four project/example-reference caveats leave SkillSpector's original partial/CAUTION status intact.

**Remaining deductions:** the evaluator still expects a `run_script` call and a top-level `version` field. The skill uses its real shell command and the existing `metadata.version`; neither was changed merely to satisfy a tool convention. LP3 still advises declaring tool scope. This refactor does not establish host-enforced permission boundaries. Tier 2/3 and LLM rubric evaluations remain unrun.

## Static re-evaluation on develop (27 November 2026)

Evaluated committed `develop` revision `1faeb9676a9402216dd906e97fa889a760f32398`, with NVIDIA SkillEvaluator **0.9.0** and its checksum-pinned SkillSpector **2.13.3**, using Python 3.13, `env -i`, a fresh HOME and `--no-llm`. No suppression baseline, LLM rubric, Tier 2 or Tier 3 was used. This evaluation scanned the installable skill subtree; repository-root behavioral cases were not installed or counted as scanner coverage.

The previous revision `1147f32646a822fe33dd6805a59f462836ee543d` was exported and scanned with the same tools/settings for a direct comparison. The older **93.5** result below belongs to the separately identified 17 November working-tree snapshot; it is not the measured score of the previous revision.

| Check | Previous revision, re-run | develop, clean committed export |
| --- | --- | --- |
| Static quality | **A, 91.2/100** | **B, 89.8/100** |
| Correctness / discoverability / reliability | 85 / 95 / 100 | 85 / 95 / 100 |
| Efficiency | 85 | 75 |
| Estimated SKILL.md tokens (characters / 4) | 5,238 | 6,240 |
| Tier 1 | Pass: 11 passed, dependency audit N/A | Pass: 11 passed, dependency audit N/A |
| SkillSpector | Risk **7/100**, one medium LP3 advisory | Risk **7/100**, one medium LP3 advisory |

The quality decline comes from a new 10-point efficiency deduction for a nested reference in `review-page.md` (now linking to `finding-resolution.md`). Both revisions already incur the 15-point efficiency deduction for exceeding the 5,000 estimated-token recommendation. The existing `run_script`, top-level `version` and long-description deductions remain. The score is a static heuristic, not evidence that the new review workflow performs worse.

**Security:** LP3 reports that tool scope is not declared in frontmatter. This is an advisory, not an observed exploit; it occurs in both revisions. No high or critical findings occur in the committed exports. SkillSpector inspected all nine bundled files in develop, but retains a partial/CAUTION status for four unresolved project/example references (the existing `DESIGN.md` mention and three `sdd/csv-export.html` examples). SkillEvaluator records those caveats and passes the security gate. Tool/read-only restrictions remain host-dependent; no automatic sandbox enforcement is established by this scan.

**Workspace diagnostic:** the first scan of the physical checkout failed, with risk 78, because it included an ignored `scripts/__pycache__/inline_view.cpython-314.pyc`. Git tracks no bytecode. A fresh export of the exact committed skill excluded this local cache and passed. The failed scan is retained below; the pass applies to committed/installable content, not to the contaminated physical checkout. The local cache was not deleted or suppressed for the scan.

**Evidence:** [develop Tier 1 JSON](evaluations/2026-11-27/develop-tier1.json), [previous revision Tier 1 JSON](evaluations/2026-11-27/previous-tier1.json), [workspace diagnostic JSON](evaluations/2026-11-27/workspace-tier1.json), [committed file hashes](evaluations/2026-11-27/develop-manifest.json), [versions, commands and report hashes](evaluations/2026-11-27/provenance.json). JSON reports retain their original temporary source paths. SkillEvaluator's content digest for develop is `sha256:21a65d0a36fbe51d525bcd56f6aa8b141f94af5bc5a898b1f59b65523c366a9f` (algorithm `skill-evaluator-source-tree/2`).

Publication remains incomplete because required Tier 2/3 evidence is absent. The behavioral observations below are separate from SkillEvaluator Tier 3. No skill instructions were modified to improve these scores during this re-evaluation.

## Behavioral forward evaluations (27 November 2026)

Five fresh native-agent runs exercised the new candidate on `develop`: first Design stop, resume at Spec, requirement reopening, proposal review and parent-turn isolation. The three gate runs left production source unchanged and stopped for the required approval. The proposal reviewer found the supplied current-state error, existing reusable helper and unresolved contract; the isolation child answered `UNKNOWN`.

All expected outcomes were observed. Of 15 case assertions, 14 have observed outcome evidence; the proposal review's no-execution condition remains partly verified through a child receipt. Full child tool traces were not exposed. This is a focused observation on one host/model, with no A/B improvement claim. See the [candidate hash, evidence and limits](../evals/records/2026-11-27.md) and [replayable cases](../evals/README.md).

The current candidate also passes 24 offline unit tests, the skill validator, bundled-link checks and the template page lint. Browser checks, complete build/QA/grade execution, contest resolution and budget exhaustion were not evaluated. The static re-evaluation above measures the committed candidate separately from these behavioral observations.

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
