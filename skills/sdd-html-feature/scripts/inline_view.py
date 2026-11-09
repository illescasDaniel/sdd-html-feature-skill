#!/usr/bin/env python3
"""Derive a compact inline-chat version of one tab of a feature page.

Usage: inline_view.py PAGE.html TAB   (TAB: design, spec, arch, build, qa, grade, appr)
Prints HTML to stdout: the tab's "At a glance" section open, the rest inside one <details class="big">.
Uses the page's inert <style data-inline media="not all"> block, enabled here.
Elements to leave out of the inline copy: put class "skip-inline" on a <p> or <nav>. Stdlib only.
"""
import re
import sys


def fail(msg: str) -> int:
    print("inline_view: " + msg, file=sys.stderr)
    return 1


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__, file=sys.stderr)
        return 2
    page, tab = sys.argv[1], sys.argv[2]
    try:
        with open(page, encoding="utf-8") as fh:
            html = fh.read()
    except OSError as exc:
        return fail("cannot read %s: %s" % (page, exc.strerror))
    style = re.search(r'<style data-inline media="not all">(.*?)</style>', html, re.S)
    if not style:
        return fail('page has no <style data-inline media="not all"> block')
    start = re.search(r'<div role="tabpanel" id="p-%s"[^>]*>' % re.escape(tab), html)
    if not start:
        return fail("page has no panel p-%s" % tab)
    # The panel ends where the next panel or </main> begins; drop trailing comments and the panel's own </div>.
    end = re.search(r'<div role="tabpanel"|</main>', html[start.end():])
    chunk = html[start.end(): start.end() + end.start()] if end else html[start.end():]
    chunk = re.sub(r'(?:\s*<!--(?:(?!-->).)*-->)*\s*$', "", chunk, flags=re.S)
    if not chunk.endswith("</div>"):
        return fail("panel p-%s does not end with its closing </div>" % tab)
    body = chunk[: -len("</div>")]
    if body.count("<div") != body.count("</div>"):
        return fail("panel p-%s has unbalanced <div> tags; refusing to emit a truncated copy" % tab)
    body = re.sub(r"<(p|nav)\b[^>]*\bskip-inline\b[^>]*>.*?</\1>", "", body, flags=re.S)
    parts = re.split(r'<h2 class="rep">.*?</h2>', body, maxsplit=1, flags=re.S)
    glance = parts[0]
    detail = parts[1] if len(parts) > 1 else ""
    out = "<style>%s</style>\n%s\n" % (style.group(1), glance)
    if detail.strip():
        out += '<details class="big"><summary>Detailed report</summary>\n%s\n</details>\n' % detail
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stdout.write(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
