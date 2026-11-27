<p align="center"><img src="assets/icon.svg" alt="sdd-html-feature-beta icon" width="96"></p>

# sdd-html-feature-beta

This `develop` branch provides the beta skill alongside the stable `sdd-html-feature`; install it as `sdd-html-feature-beta` without replacing the stable install.

Visual spec-driven development in a single, self-contained HTML page per feature. Review the design, specification and architecture through separate approval gates, challenge the proposal with a fresh reviewer before architecture approval, then build, test and independently verify the result.

## How it works

<img alt="HTML SDD workflow: design, specification, architecture, build and verification" src="assets/infographic.png" height="350">

| Phase | Reviewable result |
| --- | --- |
| Design | Visual proposal, flows, alternatives, reuse, decisions and open questions |
| Spec | Contracts, scenarios and traceability |
| Architecture | Interfaces, dependencies, file-change plan and independent proposal review |
| Build and verify | Tests, implementation, QA and independent grade |
| Approvals | The approvals received in chat |

The page is saved as `sdd/<feature>.html`, works offline and retains readable content without JavaScript. Approval happens in chat. [See the full guide and screenshots](docs/guide.md).

## Quick start

```bash
npx skills add https://github.com/illescasDaniel/sdd-html-feature-skill/tree/develop/skills/sdd-html-feature-beta
```

Ask your agent to use `sdd-html-feature-beta` for a feature. Review the HTML page and approve each gate in chat. See the [manual installation instructions](docs/guide.md#use).

## Requirements and limits

Python 3 runs the page checker and report extractor. Your agent host may not support inline interactive HTML; the saved page remains available locally. QA and grading use independent agents when available, with documented limits and opt-outs. A page interaction is a simulation, not an approval.

## Evaluation

[![NVIDIA SkillEvaluator quality A, 94.8 out of 100; Tier 1 passed; SkillSpector risk 7, one medium advisory](assets/evaluation.svg)](docs/evaluation.md)

The refactored develop candidate gives **A, 94.8/100**, up from B, 89.8 with the same SkillEvaluator 0.9.0 settings. Shorter core instructions, focused references and a concise description improve discoverability and efficiency. Tier 1 passes on the physical checkout; SkillSpector 2.13.3 reports risk **7/100**, one medium tool-scope advisory and no high or critical findings. These keyless static checks do not establish agent performance. The result identifies an uncommitted working tree on `1faeb96`; [evaluation details and raw reports](docs/evaluation.md) include its file hashes and limits.

## Tests

Run `python3 -m unittest discover -s tests -v` for offline checks of the page checker and report extractor. These script tests do not evaluate whether an agent follows the skill or whether the page works across browsers. [Behavioral cases](evals/README.md) cover approval stops, resume, requirement reopening, proposal review and parent-context isolation; see the [run record](docs/evaluation.md#behavioral-forward-evaluations-27-november-2026) for results and limits.

## License

[MIT](LICENSE).
