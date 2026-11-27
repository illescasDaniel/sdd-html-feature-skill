# Resolving reviewer findings

Use this for R# proposal findings and Q#/G# verification findings. Preserve the reviewer's original text, severity and implementation/requirement classification. Add an author response separately; do not rewrite the review to make it pass.

For each finding, record one disposition and its reason:

- **Fix:** evidence supports it; propose the smallest correction. Before approval, correct the draft. If approved behavior, scope, contracts, migration, trust boundaries or UI change, reopen the owning gate and obtain approval before dependent work.
- **Contest:** cite checkable evidence in the page or source demonstrating the error. "This was intentional" or the author's recollection is insufficient. Keep it contested until the reviewer confirms the correction or the user explicitly resolves it. Do not convert a contest into a PASS, lower the severity or relabel the finding yourself.
- **Escalate:** resolution depends on a fact or decision not in the available artifacts. State what is missing and propose a question for the owning tab. Stop dependent work on material uncertainty; the existing gate handles the decision.
- **Decline:** record the reason and residual consequence. A low-severity suggestion may be declined without a code change. An unmet requirement or material risk needs the user's explicit acceptance; it never becomes "verified" merely because it was declined.

A misunderstood paraphrase can reveal a real comprehension gap. Clarify what the page fails to explain rather than contesting it using private conversation context. When the paraphrase itself contradicts explicit text, cite that text and preserve both versions.

Apply the existing fix/review budgets. A documented contest needs no extra run unless confirmation is necessary; a re-check consumes the appropriate slot. If the budget is exhausted, record unresolved findings and hand over, rather than retrying for a preferred verdict. Requirement findings continue to follow the SKILL.md gate-reopening rule; an author response never overrides their label or silently closes them.

Store R# dispositions in Architecture (and the owning tab for a proposed change); Q#/G# dispositions in Verify. Keep unresolved items visible in the relevant glance. No separate report files or extra approval gate are required.
