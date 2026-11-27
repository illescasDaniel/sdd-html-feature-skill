# Behavioral evaluations

These cases exercise an agent following the skill; they are separate from the offline parser tests. They live at the repository root so normal skill installs do not carry test fixtures. Each case has a user prompt, input files where needed, expected outcomes and trace-based assertions. They are observations on a named host/model, not proof of universal reliability.

## Run with native agents

1. Create a unique scratch directory outside the repository for each case. Copy its `files/` contents there (the optional `place-files.sh` does this in the current directory). Keep an untouched copy or hashes for side-effect comparisons.
2. Launch a fresh native agent with parent history disabled and the installed skill's absolute path. Give it the prompt, scratch directory and input paths. For `proposal-review`, use `agents/design-reviewer.md` and the page/source paths instead of the full feature workflow. Do not supply expected outcomes, grader files or the author's interpretation to the agent. Let it work until the first required user stop; do not simulate an approval.
3. Keep writes inside that scratch directory and skill resources read-only. Disable external services and nested delegation in these focused cases. The three gate cases may use generated Markdown gate reports; that evaluates decisions and artifacts, not a host's HTML renderer.
4. Save the actual result, dispatch arguments, native trace evidence when exposed, and the before/after file comparison. Check each assertion in `graders/` against the artifacts and actual trace. Distinguish direct observations from the child's own command/read receipt. Missing evidence stays unverified; never invent traces.
5. Record tested skill revision or working-tree hash, host/model, case, assertion results and limitations. Keep private raw traces outside the repository; publish only sanitized evidence. For an A/B comparison, repeat in separate scratch directories with the previous skill version and the same inputs. The initial forward runs do not establish an improvement over baseline.

The `parent-context-isolation` case is a two-context probe: establish a random private marker only in the parent conversation before launching the child, then give the child only that case's question with history inheritance disabled. Inspect its actual answer. Never place the marker in the prompt, a file, an input path or the grader. Run this case using the native orchestration tool, not as a standalone single-agent CLI task. It tests parent-turn isolation only; shared filesystem access and injected host instructions remain outside its scope.

## What the cases cover

- `approval-boundary`: first stop is Design; no production implementation; alternatives and reuse are investigated.
- `resume-at-spec`: saved approval and review opt-out survive conversation loss; work resumes at Spec.
- `reopen-requirement`: a QA requirement finding cannot silently change an approved contract or production code.
- `proposal-review`: independent paraphrase, false current-state claims, reuse, unresolved contracts and expected absence of proposed files.
- `description-routing`: description-only selection across feature types, read-only analysis and tiny fixes.
- `parent-context-isolation`: actual fresh-child response and dispatch evidence.

The fixture pages are compact saved-artifact inputs, not visual template examples. These runs do not exercise a full implementation/QA/grade cycle, paid services, browser behavior, host tool enforcement, review-budget exhaustion or resolution of contested findings. Report those gaps explicitly.
