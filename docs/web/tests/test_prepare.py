import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
PREPARE_PATH = REPO_ROOT / "docs" / "web" / "prepare.py"
MANIFEST_PATH = REPO_ROOT / "docs" / "book" / "book-manifest.json"
SURVEY_DIR = REPO_ROOT / "docs" / "harness-survey"


def load_prepare_module():
    spec = importlib.util.spec_from_file_location("harness_web_prepare", PREPARE_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class ChapterModelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.prepare = load_prepare_module()

    def test_manifest_discovers_the_complete_ordered_book(self):
        manifest = self.prepare.load_manifest(MANIFEST_PATH)
        chapters = self.prepare.discover_chapters(SURVEY_DIR, manifest)

        self.assertEqual(36, len(chapters))
        self.assertEqual("00_index.md", chapters[0].source_path.name)
        self.assertEqual("Agent Harness：架构、工程与安全", chapters[0].title)
        self.assertEqual("05-harness-loop", chapters[5].slug)
        self.assertIsNone(chapters[0].previous_slug)
        self.assertEqual(chapters[1].slug, chapters[0].next_slug)
        self.assertEqual(chapters[-2].slug, chapters[-1].previous_slug)
        self.assertIsNone(chapters[-1].next_slug)
        self.assertEqual(36, len({chapter.title for chapter in chapters}))

    def test_invalid_chapter_sets_are_rejected(self):
        cases = {
            "missing": ({}, "expected exactly one chapter"),
            "duplicate": (
                {"00_first.md": "# One\n", "00_second.md": "# Two\n"},
                "expected exactly one chapter",
            ),
            "multiple_h1": ({"00_first.md": "# One\n\n# Two\n"}, "exactly one H1"),
        }
        for name, (files, message) in cases.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory() as temp_dir:
                root = Path(temp_dir)
                for filename, content in files.items():
                    (root / filename).write_text(content, encoding="utf-8")
                manifest_path = root / "manifest.json"
                manifest_path.write_text(
                    json.dumps({"order": ["00_"], "parts": {"00_": "序章"}}),
                    encoding="utf-8",
                )
                manifest = self.prepare.load_manifest(manifest_path)
                with self.assertRaisesRegex(ValueError, message):
                    self.prepare.discover_chapters(root, manifest)


class MarkdownPipelineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.prepare = load_prepare_module()
        manifest = cls.prepare.load_manifest(MANIFEST_PATH)
        cls.chapters = cls.prepare.discover_chapters(SURVEY_DIR, manifest)

    def chapter(self, prefix):
        return next(chapter for chapter in self.chapters if chapter.prefix == prefix)

    def test_links_and_cross_references_preserve_fenced_examples(self):
        source = (
            "[第一章](01_introducing_agent_harness.md#agent-harness-的工作定义) "
            "[序章](00_index.md) [本页](#a--b) 图 5-1 与表 5-2。\n"
            "[外部](https://example.com/01_introducing_agent_harness.md)\n\n"
            "```markdown\n[示例](01_introducing_agent_harness.md) 图 5-1\n```\n"
        )
        rewritten, count = self.prepare.rewrite_chapter_links(
            source, self.chapters, self.chapter("05_")
        )
        rewritten = self.prepare.linkify_cross_references(rewritten)

        self.assertEqual(3, count)
        self.assertIn("../01-introducing-agent-harness/#agent-harness-的工作定义", rewritten)
        self.assertIn("(../../)", rewritten)
        self.assertIn("(#a-b)", rewritten)
        self.assertIn("[图 5-1](#fig-5-1)", rewritten)
        self.assertIn("[表 5-2](#tab-5-2)", rewritten)
        self.assertIn("```markdown\n[示例](01_introducing_agent_harness.md) 图 5-1", rewritten)

    def test_tables_keep_authored_captions_and_stable_ids(self):
        source = "正文。\n\n| A | B |\n|---|---|\n| 1 | 2 |\n\n*表 5-1　测试表。*\n"
        rewritten, count, authored = self.prepare.wrap_tables(
            source, Path("05_harness_loop.md"), "5", "Harness Loop"
        )

        self.assertEqual((1, 1), (count, authored))
        self.assertIn('::: {#tab-5-1 .book-table}', rewritten)
        self.assertIn("*表 5-1　测试表。*", rewritten)

    def test_web_svg_rules_are_generic_and_css_safe(self):
        base_path = REPO_ROOT / "docs" / "book" / "mermaid-config.json"
        flowchart = self.prepare.web_mermaid_config("flowchart LR\nA --> B\n", base_path)
        sequence = self.prepare.web_mermaid_config(
            "sequenceDiagram\nA->>B: message\n", base_path
        )
        state = self.prepare.web_mermaid_config(
            "stateDiagram-v2\nA --> B: 需要确认目录、权限或未知副作用\n",
            base_path,
        )
        wrapped = self.prepare.wrap_mermaid_edge_labels(
            "flowchart LR\nM -->|行动提议经执行后形成新观察| O\n"
            "C -->|Token 压力或 Provider overflow| D\n"
            "A -->|第一行<br/>第二行| B\n"
        )
        wrapped_state = self.prepare.wrap_mermaid_edge_labels(
            "stateDiagram-v2\nA --> B: 需要确认目录、权限或未知副作用\n"
        )

        self.assertEqual(
            "diagram-02-horizontal-capability-map-figure-01",
            self.prepare.mermaid_svg_id(
                Path("02-horizontal-capability-map-figure-01.svg")
            ),
        )
        self.assertFalse(flowchart["htmlLabels"])
        self.assertEqual(120, flowchart["flowchart"]["wrappingWidth"])
        self.assertIn("font-size: 22px", flowchart["themeCSS"])
        self.assertFalse(state["htmlLabels"])
        self.assertNotIn("htmlLabels", sequence)
        self.assertIn("行动提议经执行后<br/>形成新观察", wrapped)
        self.assertIn("Token 压力或<br/>Provider overflow", wrapped)
        self.assertIn("第一行<br/>第二行", wrapped)
        self.assertIn("需要确认目录、<br/>权限或未知副作用", wrapped_state)

    def test_chapter_preparation_generates_figures_tables_links_and_references(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "05_example.md"
            source.write_text(
                "# 示例章节\n\n参见图 5-1 和表 5-1 [@example2026]。\n\n"
                "```mermaid\nflowchart LR\nA --> B\n```\n\n"
                "*图 5-1　示例图。*\n\n"
                "| A | B |\n|---|---|\n| 1 | 2 |\n\n*表 5-1　示例表。*\n",
                encoding="utf-8",
            )
            chapter = self.prepare.Chapter(
                0, "05_", source, "示例章节", "05-example", "核心机制", None, None
            )

            def fake_renderer(mermaid_source, svg_path):
                svg_path.parent.mkdir(parents=True, exist_ok=True)
                svg_path.write_text(
                    '<svg xmlns="http://www.w3.org/2000/svg"><text>图</text></svg>',
                    encoding="utf-8",
                )

            prepared = self.prepare.prepare_chapter_markdown(
                chapter, [chapter], root / "assets", fake_renderer
            )

            self.assertEqual((1, 1), (prepared.figure_count, prepared.table_count))
            self.assertIn("[图 5-1](#fig-5-1)", prepared.markdown)
            self.assertIn("[表 5-1](#tab-5-1)", prepared.markdown)
            self.assertIn("#fig-5-1", prepared.markdown)
            self.assertIn("#tab-5-1", prepared.markdown)
            self.assertIn("## 参考文献 {.unnumbered}", prepared.markdown)

    def test_pandoc_filter_emits_semantic_callout_figure_and_table(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            svg = root / "figure.svg"
            svg.write_text(
                '<svg xmlns="http://www.w3.org/2000/svg"><text>图</text></svg>',
                encoding="utf-8",
            )
            markdown = root / "page.md"
            markdown.write_text(
                "# 页面\n\n> **安全提示｜测试边界**\n>\n> 正文。\n\n"
                f'::: {{#fig-1-1 .book-figure image="{svg}"}}\n'
                "*图 1-1　测试图。*\n:::\n\n"
                "::: {#tab-1-1 .book-table}\n*表 1-1　测试表。*\n\n"
                "| A | B |\n|---|---|\n| 1 | 2 |\n:::\n",
                encoding="utf-8",
            )
            result = self.prepare.run_pandoc_fragment(markdown)

            self.assertIn('class="callout callout-security"', result)
            self.assertIn('<figure id="fig-1-1"', result)
            self.assertIn('id="tab-1-1"', result)
            self.assertIn('class="table-scroll"', result)


class PageGenerationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.prepare = load_prepare_module()
        manifest = cls.prepare.load_manifest(MANIFEST_PATH)
        cls.chapters = cls.prepare.discover_chapters(SURVEY_DIR, manifest)

    def test_navigation_and_templates_use_relative_clean_urls(self):
        current = self.chapters[5]
        navigation = self.prepare.build_book_navigation(self.chapters, current)
        self.assertEqual(36, navigation.count('class="book-nav-link"'))
        self.assertEqual(6, navigation.count('class="book-part"'))
        self.assertIn('aria-current="page"', navigation)

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            markdown = root / "page.md"
            markdown.write_text("# 页面\n\n## 小节\n\n正文。\n", encoding="utf-8")
            nested = root / "nested" / "index.html"
            self.prepare.render_chapter_page(
                current,
                self.chapters,
                markdown,
                nested,
                "https://github.com/specialpointcentral/harness",
                None,
            )
            nested_html = nested.read_text(encoding="utf-8")
            self.assertIn('../../assets/book.css', nested_html)
            self.assertIn('href="#小节"', nested_html)
            self.assertIn('../04-reference-architecture/', nested_html)

            root_page = root / "root" / "index.html"
            self.prepare.render_chapter_page(
                self.chapters[0],
                self.chapters,
                markdown,
                root_page,
                "https://github.com/specialpointcentral/harness",
                None,
            )
            root_html = root_page.read_text(encoding="utf-8")
            self.assertIn('data-pagefind-root="./pagefind/"', root_html)
            self.assertIn('href="./assets/book.css"', root_html)

    def test_full_build_generates_expected_pages_figures_and_tables(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)

            def fake_renderer(source, svg_path):
                svg_path.parent.mkdir(parents=True, exist_ok=True)
                svg_path.write_text(
                    '<svg xmlns="http://www.w3.org/2000/svg"><text>图</text></svg>',
                    encoding="utf-8",
                )

            report = self.prepare.build_site(
                REPO_ROOT,
                root / "site",
                root / "work",
                "https://github.com/specialpointcentral/harness",
                None,
                fake_renderer,
            )

            self.assertEqual((36, 35, 75), (report.pages, report.figures, report.tables))
            self.assertTrue((root / "site" / "index.html").is_file())
            self.assertTrue(
                (root / "site" / "chapters" / "05-harness-loop" / "index.html").is_file()
            )


if __name__ == "__main__":
    unittest.main()
