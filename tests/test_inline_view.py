"""Offline checks for the SDD HTML page checker and report extractor (stdlib unittest only)."""
import importlib.util
import pathlib
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills' / 'sdd-html-feature'
SCRIPT = SKILL / 'scripts' / 'inline_view.py'
TEMPLATE = SKILL / 'templates' / 'feature.html'
GOLDEN = Path(__file__).resolve().parent / 'golden'
TABS = ('design', 'spec', 'arch', 'build', 'verify', 'appr')

DESIGN_CHIP = '<span class="st wait">awaiting approval</span>'
DESIGN_BUTTON = re.compile(r'(<button [^>]*data-p="design">Design )<span class="st[^"]*">[^<]*</span>(</button>)')
DESIGN_REP = '<h2 class="rep">'


def load_module():
    spec = importlib.util.spec_from_file_location('inline_view', SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    # Read source directly: tests must not read or write bytecode in the installable skill.
    exec(compile(SCRIPT.read_text(encoding="utf-8"), str(SCRIPT), "exec"), mod.__dict__)
    return mod


def normalize(text):
    """Strip HTML comments, collapse whitespace and drop spaces before closing tags, so only real content differences count."""
    text = re.sub(r'<!--.*?-->', '', text, flags=re.S)
    text = re.sub(r'\s+', ' ', text)
    return re.sub(r' (?=</)', '', text).strip() + '\n'


def mask_numbers(text):
    return re.sub(r'\d+', 'N', text)


class Base(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.dir = Path(self._tmp.name)
        self.template = TEMPLATE.read_text(encoding='utf-8')

    def run_view(self, *args, cwd=None):
        return subprocess.run([sys.executable, '-I', str(SCRIPT), *map(str, args)],
                              capture_output=True, text=True, cwd=cwd)

    def page(self, html, name='feature.html'):
        path = self.dir / name
        path.write_text(html, encoding='utf-8')
        return path

    def edited(self, old, new, count=1):
        """The shipped template with `old` replaced by `new` (the old text must exist)."""
        self.assertIn(old, self.template, 'fixture anchor missing from the template')
        return self.template.replace(old, new, count)

    def inject_in_design(self, fragment):
        return self.edited(DESIGN_REP, fragment + DESIGN_REP)

    def check_html(self, html, *flags):
        return self.run_view('--check', *flags, self.page(html))


class TemplateAndFormatTests(Base):
    def test_shipped_template_passes_lint(self):
        result = self.run_view('--check', TEMPLATE)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('0 error(s), 0 warning(s)', result.stdout)

    def test_extracts_design_glance(self):
        result = self.run_view(TEMPLATE, 'design', '--format', 'md')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('At a glance', result.stdout)
        self.assertIn('design', result.stdout.lower())

    def test_rejects_page_missing_required_structure(self):
        result = self.check_html('<!doctype html><html><body>Incomplete</body></html>')
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_md_output_ends_with_the_gate_line(self):
        result = self.run_view(TEMPLATE, 'design', '--format', 'md')
        last = result.stdout.rstrip('\n').split('\n\n')[-1]
        self.assertTrue(last.startswith('**Next gate:**'), last)
        self.assertIn('design approved', last)

    def test_usage_and_argument_errors(self):
        self.assertEqual(self.run_view().returncode, 2)
        self.assertEqual(self.run_view(TEMPLATE).returncode, 2)
        self.assertEqual(self.run_view(TEMPLATE, 'nope').returncode, 1)
        self.assertEqual(self.run_view(TEMPLATE, 'design', '--format', 'xml').returncode, 1)
        self.assertEqual(self.run_view(self.dir / 'missing.html', 'design').returncode, 1)

    def test_tmp_and_out_write_the_full_html_to_a_file_and_print_its_path(self):
        page = self.page(self.template)
        stdout = self.run_view(page, 'design').stdout
        tmp = self.run_view(page, 'design', '--tmp')
        self.assertEqual(tmp.returncode, 0, tmp.stderr)
        path = pathlib.Path(tmp.stdout.strip())
        self.assertTrue(path.is_absolute() and path.name.endswith('-design.html'))
        self.assertGreaterEqual(len(path.read_text(encoding='utf-8')), len(stdout))
        self.assertNotIn('emitted the glance only', tmp.stderr)
        target = self.dir / 'out.html'
        out = self.run_view(page, 'design', '--out', str(target))
        self.assertEqual(out.stdout.strip(), str(target))
        self.assertEqual(target.read_text(encoding='utf-8'), path.read_text(encoding='utf-8'))
        self.assertEqual(self.run_view(page, 'design', '--tmp', '--format', 'md').returncode, 1)
        self.assertEqual(self.run_view(page, 'design', '--tmp', '--out', str(target)).returncode, 1)

    def test_glance_only_fallback_above_the_size_limit(self):
        result = self.run_view(self.page(self.template), 'design')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('emitted the glance only', result.stderr)
        self.assertIn('too large to show here', result.stdout)
        self.assertIn('Source: ', result.stdout)
        self.assertLessEqual(len(result.stdout.encode('utf-8')), 12000)

    def test_small_tab_keeps_its_detailed_report(self):
        result = self.run_view(self.page(self.template), 'appr')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn('too large to show here', result.stdout)

    def test_unbalanced_div_in_a_panel_refuses_to_render(self):
        html = self.inject_in_design('<div>')
        result = self.run_view(self.page(html), 'design')
        self.assertEqual(result.returncode, 1)
        self.assertIn('refusing to emit a truncated copy', result.stderr)

    def test_div_lookalike_tags_are_not_counted_as_divs(self):
        html = self.inject_in_design('<p>a <divider>b</divider></p>')
        result = self.run_view(self.page(html), 'design')
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_legacy_qa_grade_page(self):
        button = re.search(r'<button [^>]*data-p="verify">.*?</button>', self.template).group(0)
        start = self.template.index('<div role="tabpanel" id="p-verify"')
        end = self.template.index('<!-- ============ APPROVALS', start)
        panel = self.template[start:end]

        def legacy(text, tab, label):
            return text.replace('verify', tab).replace('Verify', label)

        html = self.template.replace(button, legacy(button, 'qa', 'QA') + legacy(button, 'grade', 'Grade'), 1)
        html = html.replace(panel, legacy(panel, 'qa', 'QA') + legacy(panel, 'grade', 'Grade'), 1)
        page = self.page(html)
        render = self.run_view(page, 'verify')
        self.assertEqual(render.returncode, 0, render.stderr)
        self.assertIn('qa tab:', render.stdout)
        self.assertIn('grade tab:', render.stdout)
        check = self.run_view('--check', page)
        self.assertEqual(check.returncode, 0, check.stdout)
        self.assertIn('legacy page', check.stdout)


class GoldenSnapshotTests(Base):
    """Output of the shipped template, with comments and whitespace normalised, must not drift."""

    def render_template(self, tab, fmt):
        (self.dir / 'feature.html').write_text(self.template, encoding='utf-8')
        return self.run_view('feature.html', tab, '--format', fmt, cwd=self.dir)

    def test_golden_outputs(self):
        for tab in TABS:
            for fmt in ('md', 'html'):
                with self.subTest(tab=tab, fmt=fmt):
                    result = self.render_template(tab, fmt)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertEqual(normalize(result.stdout), normalize((GOLDEN / f'{tab}.{fmt}').read_text(encoding='utf-8')))
                    # The glance-only note quotes a byte count, which legitimately changes with the template.
                    expected = (GOLDEN / f'{tab}.{fmt}.stderr').read_text(encoding='utf-8')
                    self.assertEqual(mask_numbers(normalize(result.stderr)), mask_numbers(expected))


class StatusChipTests(Base):
    """D1: a tab button without a status chip must not borrow the next tab's chip."""

    def without_design_chip(self):
        html, n = DESIGN_BUTTON.subn(r'\1\2', self.template)
        self.assertEqual(n, 1)
        return html

    def test_render_shows_unknown_not_the_next_tabs_status(self):
        page = self.page(self.without_design_chip())
        md = self.run_view(page, 'design', '--format', 'md')
        self.assertIn('design tab: unknown', md.stdout)
        self.assertNotIn('design tab: not started', md.stdout)
        out = self.run_view(page, 'design')
        self.assertIn('design tab: unknown', out.stdout)

    def test_check_errors_and_names_the_tab(self):
        result = self.check_html(self.without_design_chip())
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertRegex(result.stdout, r'error: tab design: .*status chip')

    def test_legacy_flag_downgrades_to_a_warning(self):
        result = self.check_html(self.without_design_chip(), '--legacy')
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertRegex(result.stdout, r'warning: tab design: .*status chip')

    def test_approved_tab_with_placeholders_still_errors(self):
        html = self.edited(DESIGN_CHIP, '<span class="st ok">approved</span>')
        result = self.check_html(html)
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn('template placeholders (class tpl)', result.stdout)
        self.assertIn('<script data-sample>', result.stdout)

    def test_bad_vocabulary_is_still_reported(self):
        html = self.edited(DESIGN_CHIP, '<span class="st wait">maybe</span>')
        result = self.check_html(html)
        self.assertEqual(result.returncode, 1)
        self.assertIn('not in the allowed vocabulary', result.stdout)


class RemoteAssetTests(Base):
    """D2: anything that loads from the network is an error; links and local assets stay allowed."""

    REMOTE = {
        'video src': '<video src=https://example.com/a.mp4></video>',
        'audio src': '<audio src="https://example.com/a.mp3"></audio>',
        'img srcset': '<img alt="" srcset="https://example.com/a.png 1x, local.png 2x">',
        'img srcset second candidate': '<img alt="" srcset="local.png 1x, https://example.com/a.png 2x">',
        'source srcset': '<picture><source srcset="//example.com/a.webp"></picture>',
        'object data': '<object data="https://example.com/a.svg"></object>',
        'embed protocol-relative': '<embed src="//example.com/a.swf">',
        'single quotes': "<img alt='' src='https://example.com/a.png'>",
        'upper case': '<IMG ALT="" SRC="HTTPS://example.com/a.png">',
        'svg image': '<svg><image href="https://example.com/a.png"/></svg>',
        'svg use xlink': '<svg><use xlink:href="https://example.com/s.svg#a"/></svg>',
        'form action': '<form action="https://example.com/collect"></form>',
        'input src': '<input type="image" src="https://example.com/a.png" alt="">',
        'link stylesheet': '<link rel="stylesheet" href="https://example.com/a.css">',
        'script src': '<script src="https://example.com/a.js"></script>',
        'track src': '<video><track src="https://example.com/a.vtt"></video>',
        'poster': '<video poster="https://example.com/a.png"></video>',
        'newline between attributes': '<img\n  alt=""\n  src="https://example.com/a.png">',
        'ftp': '<img alt="" src="ftp://example.com/a.png">',
        'css url upper case': '<style>.x{background:URL(HTTPS://example.com/a.png)}</style>',
        'css import upper case': '<style>@IMPORT "https://example.com/a.css";</style>',
    }

    ALLOWED = {
        'anchor to docs': '<a href="https://example.com">doc</a>',
        'data uri image': '<img alt="" src="data:image/png;base64,iVBORw0KGgo=">',
        'relative image': '<img alt="" src="img/local.png">',
        'fragment link': '<a href="#p-spec">spec</a>',
        'data-label url': '<table><tr><td data-label="https://x">x</td></tr></table>',
        'data-p url': '<span data-p="https://x">x</span>',
        'text mentioning a url': '<p>See https://example.com/docs, or src="https://x" in prose.</p>',
        'srcset data uri with slashes': '<img alt="" srcset="data:image/png;base64,//AAAA 1x">',
        'srcset local then data uri': '<img alt="" srcset="local.png 1x, data:image/png;base64,//AA 2x">',
        'object relative data': '<object data="local.svg"></object>',
        'form relative action': '<form action="/local"></form>',
        'css local url': '<style>.x{background:url(#ar1)}</style>',
    }

    def test_remote_loads_are_errors(self):
        for name, fragment in self.REMOTE.items():
            with self.subTest(name):
                result = self.check_html(self.inject_in_design(fragment))
                self.assertEqual(result.returncode, 1, result.stdout)
                self.assertRegex(result.stdout, r'error: remote (asset|@import)')

    def test_local_and_link_content_is_allowed(self):
        for name, fragment in self.ALLOWED.items():
            with self.subTest(name):
                result = self.check_html(self.inject_in_design(fragment))
                self.assertEqual(result.returncode, 0, result.stdout)
                self.assertNotIn('remote', result.stdout)


class TemplateHygieneTests(Base):
    """D3: authoring instructions live in the skill's references, not in every generated page."""

    def test_no_comments_inside_panels(self):
        mod = load_module()
        for tab in TABS:
            with self.subTest(tab=tab):
                self.assertNotIn('<!--', mod.panel_body(self.template, tab))

    def test_only_structural_comments_remain(self):
        comments = [c.strip() for c in re.findall(r'<!--(.*?)-->', self.template, flags=re.S)]
        banners = [c for c in comments if re.fullmatch(r'=+ [A-Z]+ =+', c)]
        others = [c for c in comments if c not in banners]
        self.assertEqual(len(banners), 6)
        self.assertEqual(len(others), 2, others)
        self.assertTrue(any('Inert in the page' in c for c in others), others)
        self.assertTrue(any('Sample simulation' in c for c in others), others)


class GatePreservationTests(unittest.TestCase):
    """The approval gates, opt-outs and budgets must survive any rewording of the skill text."""

    @staticmethod
    def flat(path):
        return re.sub(r'\s+', ' ', path.read_text(encoding='utf-8'))

    def test_skill_keeps_every_gate_phrase(self):
        text = self.flat(SKILL / 'SKILL.md')
        phrases = [
            'design approval', 'spec approval', 'architecture approval',
            'Never infer approval',
            'clicking a control never constitutes approval',
            '`no QA`', '`no grade`',
            'Reply `no QA` or `no grade` to skip either',
            'At most two fix rounds',
            'At most 3 spawns',
            'never re-spawn just to get a PASS',
            'Publishing, deployment, installation and commits are separate actions requiring their own authorization',
            'Spawned agents never spawn agents',
            'Do not write the spec in the same turn',
        ]
        for phrase in phrases:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_template_architecture_gate_keeps_the_opt_out(self):
        text = self.flat(TEMPLATE)
        self.assertIn('reply <code>no QA</code> or <code>no grade</code> to skip either', text)
        self.assertIn('up to 3 subagent runs per approved revision', text)

    def test_agents_keep_their_read_only_rules(self):
        self.assertIn('Never edit the real source', self.flat(SKILL / 'agents' / 'qa-tester.md'))
        self.assertIn('Never edit, create or delete project files', self.flat(SKILL / 'agents' / 'code-grader.md'))


if __name__ == '__main__':
    unittest.main()
