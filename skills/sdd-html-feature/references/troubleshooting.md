# Troubleshooting

| Symptom (script message) | Cause | Fix |
|---|---|---|
| `has unbalanced <div> tags; refusing to emit a truncated copy` | An unclosed element, or a stray `<div`, inside a panel | Fix the markup in that panel |
| `a comment contains <div or </main>` | An HTML comment that the panel extractor would misread | Reword or remove the comment |
| stderr: `emitted the glance only` | The full copy is over 12 KB (expected) | Pass the output to the renderer as is |
| stderr: `even the glance-only html is N bytes` | The glance itself is too large | Shorten the glance, or use `--format md` |
| `status chip '...' is not in the allowed vocabulary`, or `its tab button has no status chip` | A misspelled or missing chip on the tab button | Use one of the listed statuses (review-page.md) |
| `remote asset: <img src> loads from the network` or `remote @import or url()` | The page loads something from the web | Inline it as a data URI or SVG, or remove it |
| `still has template placeholders (class tpl)` | Example text left in an approved, done or passed tab | Replace every `class="tpl"` element, and delete the `<script data-sample>` block |
| `required tab ... is missing` | A tab was removed | Restore it with status `n/a` and the reason; never remove tabs |
