#!/usr/bin/env python3
"""Structural verification for the generated Agent Harness static site."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


@dataclass(frozen=True)
class VerifyReport:
    pages: int
    figures: int
    tables: int
    links: int


class DocumentParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: set[str] = set()
        self.duplicate_ids: set[str] = set()
        self.references: list[tuple[str, str, str]] = []
        self.figures = 0
        self.tables = 0
        self.h1_count = 0
        self.main_count = 0
        self.mermaid_foreign_objects = 0
        self.invalid_mermaid_svg_layouts = 0
        self._diagram_div_stack: list[bool] = []
        self._mermaid_svg_stack: list[bool] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        values = dict(attrs)
        identifier = values.get("id")
        if identifier:
            if identifier in self.ids:
                self.duplicate_ids.add(identifier)
            self.ids.add(identifier)

        classes = set(values.get("class", "").split())
        if tag == "div":
            inside_diagram = any(self._diagram_div_stack) or "diagram" in classes
            self._diagram_div_stack.append(inside_diagram)
        if tag == "svg":
            is_mermaid = any(self._diagram_div_stack)
            self._mermaid_svg_stack.append(is_mermaid)
            if is_mermaid:
                try:
                    width = float(values.get("width", ""))
                    height = float(values.get("height", ""))
                    view_box = [
                        float(value)
                        for value in values.get("viewbox", "").replace(",", " ").split()
                    ]
                except ValueError:
                    width = height = 0
                    view_box = []
                if (
                    values.get("data-layout-collisions") != "0"
                    or width <= 0
                    or height <= 0
                    or len(view_box) != 4
                    or view_box[2] <= 0
                    or view_box[3] <= 0
                ):
                    self.invalid_mermaid_svg_layouts += 1
        elif tag == "foreignobject" and any(self._mermaid_svg_stack):
            self.mermaid_foreign_objects += 1
        if "book-figure" in classes:
            self.figures += 1
        if "book-table" in classes:
            self.tables += 1
        if tag == "h1":
            self.h1_count += 1
        if tag == "main":
            self.main_count += 1

        if tag == "a" and values.get("href"):
            self.references.append((tag, "href", values["href"]))
        elif tag in {"link", "use"} and values.get("href"):
            self.references.append((tag, "href", values["href"]))
        elif tag in {"script", "img", "source"} and values.get("src"):
            self.references.append((tag, "src", values["src"]))

    def handle_endtag(self, tag: str) -> None:
        if tag == "svg" and self._mermaid_svg_stack:
            self._mermaid_svg_stack.pop()
        if tag == "div" and self._diagram_div_stack:
            self._diagram_div_stack.pop()


def _parse_document(path: Path) -> DocumentParser:
    parser = DocumentParser()
    parser.feed(path.read_text(encoding="utf-8"))
    parser.close()
    if parser.duplicate_ids:
        raise ValueError(
            f"duplicate IDs in {path}: {', '.join(sorted(parser.duplicate_ids))}"
        )
    if parser.mermaid_foreign_objects:
        raise ValueError(
            f"Mermaid SVG contains foreignObject labels in {path}: "
            f"{parser.mermaid_foreign_objects}"
        )
    if parser.invalid_mermaid_svg_layouts:
        raise ValueError(
            f"invalid Mermaid SVG layout metadata in {path}: "
            f"{parser.invalid_mermaid_svg_layouts}"
        )
    return parser


def _is_runtime_asset(tag: str) -> bool:
    return tag in {"link", "script", "img", "source", "use"}


def _is_allowed_external_asset(tag: str, hostname: str | None) -> bool:
    return tag == "link" and hostname in {"fonts.googleapis.com", "fonts.gstatic.com"}


def _resolve_local_target(site_root: Path, page: Path, raw_url: str) -> tuple[Path, str]:
    parsed = urlsplit(raw_url)
    path_text = unquote(parsed.path)
    fragment = unquote(parsed.fragment)
    if path_text.startswith(("/Users/", "/private/", "/tmp/", "file:")):
        raise ValueError(f"absolute local path in {page}: {raw_url}")
    if path_text.startswith("/"):
        raise ValueError(f"root-relative path breaks Pages subpaths in {page}: {raw_url}")

    if not path_text:
        target = page
    else:
        target = (page.parent / path_text).resolve()
        if path_text.endswith("/") or target.is_dir():
            target = target / "index.html"
    try:
        target.relative_to(site_root)
    except ValueError as error:
        raise ValueError(f"local target escapes site root in {page}: {raw_url}") from error
    return target, fragment


def verify_site(
    site_root: Path,
    expected_pages: int,
    expected_figures: int,
    expected_tables: int,
    require_search: bool,
    require_pdf: bool = False,
) -> VerifyReport:
    """Validate pages, assets, links and stable fragments in a built site."""
    site_root = site_root.resolve()
    pages = sorted(site_root.rglob("*.html"))
    if len(pages) != expected_pages:
        raise ValueError(f"expected {expected_pages} HTML pages, found {len(pages)}")
    if require_search and not (site_root / "pagefind" / "pagefind.js").is_file():
        raise ValueError("missing Pagefind index: pagefind/pagefind.js")
    pdf_name = "Agent-Harness-架构工程与安全.pdf"
    pdf_path = site_root / "downloads" / pdf_name
    if require_pdf and (not pdf_path.is_file() or pdf_path.stat().st_size == 0):
        raise ValueError(f"missing required PDF: downloads/{pdf_name}")
    if require_pdf and not pdf_path.read_bytes().startswith(b"%PDF-"):
        raise ValueError(f"invalid required PDF: downloads/{pdf_name}")

    parsed_documents: dict[Path, DocumentParser] = {}
    figure_count = 0
    table_count = 0
    link_count = 0
    for page in pages:
        document = _parse_document(page)
        parsed_documents[page] = document
        figure_count += document.figures
        table_count += document.tables
        if document.h1_count != 1:
            raise ValueError(f"expected one H1 in {page}, found {document.h1_count}")
        if document.main_count != 1:
            raise ValueError(f"expected one main element in {page}, found {document.main_count}")

    pdf_reference_pages: set[Path] = set()
    for page, document in list(parsed_documents.items()):
        for tag, _, raw_url in document.references:
            if unquote(urlsplit(raw_url).path).endswith(f"downloads/{pdf_name}"):
                pdf_reference_pages.add(page)
            parsed = urlsplit(raw_url)
            if parsed.scheme in {"http", "https", "mailto", "tel"}:
                if _is_runtime_asset(tag) and not _is_allowed_external_asset(
                    tag, parsed.hostname
                ):
                    raise ValueError(f"external runtime asset in {page}: {raw_url}")
                continue
            if parsed.scheme or raw_url.startswith("//"):
                continue
            target, fragment = _resolve_local_target(site_root, page, raw_url)
            if not target.is_file():
                raise ValueError(f"broken local target in {page}: {raw_url}")
            link_count += 1
            if fragment:
                target_document = parsed_documents.get(target)
                if target_document is None:
                    target_document = _parse_document(target)
                    parsed_documents[target] = target_document
                if fragment not in target_document.ids:
                    raise ValueError(
                        f"missing fragment #{fragment} in {target} linked from {page}"
                    )

    if require_pdf and len(pdf_reference_pages) != len(pages):
        raise ValueError(
            f"missing required PDF download link on "
            f"{len(pages) - len(pdf_reference_pages)} page(s): downloads/{pdf_name}"
        )
    if figure_count != expected_figures:
        raise ValueError(
            f"expected {expected_figures} book figures, found {figure_count}"
        )
    if table_count != expected_tables:
        raise ValueError(f"expected {expected_tables} book tables, found {table_count}")
    return VerifyReport(
        pages=len(pages),
        figures=figure_count,
        tables=table_count,
        links=link_count,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("site_root", type=Path)
    parser.add_argument("--pages", type=int, default=36)
    parser.add_argument("--figures", type=int, default=35)
    parser.add_argument("--tables", type=int, default=75)
    parser.add_argument("--require-search", action="store_true")
    parser.add_argument("--require-pdf", action="store_true")
    args = parser.parse_args()
    report = verify_site(
        args.site_root,
        args.pages,
        args.figures,
        args.tables,
        args.require_search,
        require_pdf=args.require_pdf,
    )
    print(
        f"verified web site: pages={report.pages}, figures={report.figures}, "
        f"tables={report.tables}, local references={report.links}"
    )


if __name__ == "__main__":
    main()
