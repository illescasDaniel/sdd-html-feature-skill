# Reviewer context and completion evidence

Read this before launching the design reviewer, QA tester or code grader. A fresh conversation helps expose assumptions; it does not create a filesystem sandbox.

## Dispatch

- Inspect the actual host tool schema. For native Codex tools, explicitly use `fork_turns: "none"`, or `fork_context: false` when that is the supported option. On other hosts use the documented equivalent. Do not inherit the parent conversation or impersonate another reviewer inside it.
- Give the child absolute paths to its persona, the feature page and the selected source/reference files, plus its task, scope, revision identifier and budget. Ask it to read those files itself. Do not supply the author's private reasoning, a desired verdict, a paraphrase to copy or answers the page is supposed to explain.
- Pass project instructions for permissions and conventions. Do not retrieve chat history or project memory to fill gaps in the proposal. Required host instructions may still be injected; report that boundary instead of claiming complete context isolation.
- QA additionally receives the sandbox/run instructions, approved scenario IDs and evidence location. The grader additionally receives the diff base, committed/staged/unstaged/relevant untracked changes and QA evidence. The design reviewer receives the existing-system reading list and the proposed file-change list.
- Tell every child not to spawn agents. Use actual read-only tool restrictions when the host provides them; otherwise disclose that the restriction is instruction-based. Fresh context does not restrict filesystem, network or credential access; keep QA's sandbox rules separate.

## Receipt and result

Record role, model, host, revision, dispatch settings, selected input paths, completion status and available native evidence in the owning tab's detailed report. Keep private host/account traces outside the page; link sanitized evidence when needed.

A launched child is not a completed review. Wait for its actual result. Where the host exposes tool traces, verify successful reads of the persona, page and required references; a requested read or a child's claim alone is not proof. Distinguish observed reads from self-reported reads, and record unavailable traces, failures and timeouts. Do not claim that an unavailable trace proves a failed read.

If fresh conversation context cannot be established, report the independent run as unavailable. A main-agent check may still be useful but must be labelled "not independent". Present the limitation at the existing gate or handoff; do not silently substitute a self-review or invent an additional approval gate.

## Isolation evaluation

For an opt-in host evaluation, put a random marker only in the parent conversation and ask a fresh child what it is, directing it to answer UNKNOWN when absent. Inspect the actual child answer and dispatch arguments. Do not put the marker in a filename, shared file, prompt or reading list. This probes parent-turn isolation only; exclusion of host instruction files needs separate evidence. Never treat a successful probe on one host/version as universal support.
