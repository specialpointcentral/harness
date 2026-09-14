import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
VERIFY_PATH = REPO_ROOT / "docs" / "web" / "verify.py"


def load_verify_module():
    spec = importlib.util.spec_from_file_location("harness_web_verify", VERIFY_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def write_valid_site(root: Path):
    (root / "chapters" / "one").mkdir(parents=True)
    (root / "assets").mkdir()
    (root / "pagefind").mkdir()
    (root / "assets" / "book.css").write_text("body {}\n", encoding="utf-8")
    (root / "pagefind" / "pagefind.js").write_text("export {};\n", encoding="utf-8")
    (root / "index.html").write_text(
        "<!doctype html><html><head>"
        '<link rel="stylesheet" href="assets/book.css">'
        "</head><body><main>"
        '<h1 id="home">首页</h1>'
        '<a href="chapters/one/#section">第一章</a>'
        '<figure id="fig-1-1" class="book-figure"></figure>'
        "</main></body></html>",
        encoding="utf-8",
    )
    (root / "chapters" / "one" / "index.html").write_text(
        "<!doctype html><html><head>"
        '<link rel="stylesheet" href="../../assets/book.css">'
        "</head><body><main>"
        '<h1 id="chapter">第一章</h1><h2 id="section">小节</h2>'
        '<a href="../../#home">首页</a>'
        '<div id="tab-1-1" class="book-table"></div>'
        "</main></body></html>",
        encoding="utf-8",
    )


class SiteVerifierTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.verify = load_verify_module()

    def test_valid_site_returns_counts(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            write_valid_site(root)

            report = self.verify.verify_site(
                root,
                expected_pages=2,
                expected_figures=1,
                expected_tables=1,
                require_search=True,
            )

            self.assertEqual((2, 1, 1), (report.pages, report.figures, report.tables))

    def test_rejects_wrong_page_count(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            write_valid_site(root)
            with self.assertRaisesRegex(ValueError, "expected 3 HTML pages"):
                self.verify.verify_site(root, 3, 1, 1, True)

    def test_rejects_broken_file_link(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            write_valid_site(root)
            page = root / "index.html"
            page.write_text(
                page.read_text(encoding="utf-8").replace(
                    "chapters/one/#section", "chapters/missing/"
                ),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "broken local target"):
                self.verify.verify_site(root, 2, 1, 1, True)

    def test_rejects_broken_fragment(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            write_valid_site(root)
            page = root / "index.html"
            page.write_text(
                page.read_text(encoding="utf-8").replace("#section", "#missing"),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "missing fragment"):
                self.verify.verify_site(root, 2, 1, 1, True)

    def test_rejects_local_absolute_path(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            write_valid_site(root)
            page = root / "index.html"
            page.write_text(
                page.read_text(encoding="utf-8").replace(
                    "assets/book.css", "/Users/example/book.css"
                ),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "absolute local path"):
                self.verify.verify_site(root, 2, 1, 1, True)

    def test_rejects_external_runtime_asset(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            write_valid_site(root)
            page = root / "index.html"
            page.write_text(
                page.read_text(encoding="utf-8").replace(
                    "assets/book.css", "https://cdn.example.com/book.css"
                ),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "external runtime asset"):
                self.verify.verify_site(root, 2, 1, 1, True)

    def test_allows_google_fonts_stylesheet(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            write_valid_site(root)
            page = root / "index.html"
            page.write_text(
                page.read_text(encoding="utf-8").replace(
                    "assets/book.css",
                    "https://fonts.googleapis.com/css2?family=Noto+Sans+SC",
                ),
                encoding="utf-8",
            )

            report = self.verify.verify_site(root, 2, 1, 1, True)

            self.assertEqual(2, report.pages)

    def test_rejects_missing_search_bundle(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            write_valid_site(root)
            (root / "pagefind" / "pagefind.js").unlink()
            with self.assertRaisesRegex(ValueError, "missing Pagefind index"):
                self.verify.verify_site(root, 2, 1, 1, True)

    def test_allows_local_svg_fragment_reference(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            write_valid_site(root)
            (root / "assets" / "icons.svg").write_text(
                '<svg xmlns="http://www.w3.org/2000/svg">'
                '<symbol id="icon-menu" viewBox="0 0 24 24"></symbol></svg>',
                encoding="utf-8",
            )
            page = root / "index.html"
            page.write_text(
                page.read_text(encoding="utf-8").replace(
                    "</main>",
                    '<svg><use href="assets/icons.svg#icon-menu"></use></svg></main>',
                ),
                encoding="utf-8",
            )

            report = self.verify.verify_site(root, 2, 1, 1, True)

            self.assertEqual(2, report.pages)

    def test_rejects_foreign_object_inside_flowchart_svg(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            write_valid_site(root)
            page = root / "index.html"
            page.write_text(
                page.read_text(encoding="utf-8").replace(
                    "</main>",
                    '<svg class="flowchart"><foreignObject><div>label</div>'
                    "</foreignObject></svg></main>",
                ),
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "flowchart contains foreignObject"):
                self.verify.verify_site(root, 2, 1, 1, True)


if __name__ == "__main__":
    unittest.main()
