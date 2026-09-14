#!/usr/bin/env python3
"""Build model and content preparation for the Agent Harness web edition."""

from __future__ import annotations

import argparse
import html
import json
import os
import posixpath
import re
import shutil
import subprocess
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Chapter:
    index: int
    prefix: str
    source_path: Path
    title: str
    slug: str
    part: str
    previous_slug: str | None
    next_slug: str | None


@dataclass(frozen=True)
class PreparedChapter:
    markdown: str
    figure_count: int
    table_count: int
    authored_table_count: int
    rewritten_link_count: int


@dataclass(frozen=True)
class SiteBuildReport:
    pages: int
    figures: int
    tables: int
    authored_table_captions: int
    rewritten_links: int


def load_manifest(path: Path) -> dict[str, Any]:
    """Load and validate the shared chapter-order manifest."""
    data = json.loads(path.read_text(encoding="utf-8"))
    order = data.get("order")
    parts = data.get("parts")
    if not isinstance(order, list) or not order or not all(
        isinstance(prefix, str) and re.fullmatch(r"\d{2}_", prefix)
        for prefix in order
    ):
        raise ValueError(f"invalid chapter order in {path}")
    if len(order) != len(set(order)):
        raise ValueError(f"duplicate chapter prefix in {path}")
    if not isinstance(parts, dict) or not all(
        prefix in order and isinstance(title, str) and title
        for prefix, title in parts.items()
    ):
        raise ValueError(f"invalid part mapping in {path}")
    if order[0] not in parts:
        raise ValueError(f"first chapter must start a part in {path}")
    return {"order": order, "parts": parts}


def chapter_slug(path: Path) -> str:
    """Return the stable URL slug derived from a numbered source filename."""
    return path.stem.replace("_", "-")


def _chapter_title(path: Path) -> str:
    headings = re.findall(r"^# (.+)$", path.read_text(encoding="utf-8"), re.M)
    if len(headings) != 1:
        raise ValueError(f"expected exactly one H1 in {path}, got {len(headings)}")
    return headings[0].strip()


def discover_chapters(
    survey_dir: Path, manifest: dict[str, Any]
) -> list[Chapter]:
    """Discover every numbered chapter in manifest order."""
    source_rows: list[tuple[str, Path, str, str, str]] = []
    current_part = ""
    for prefix in manifest["order"]:
        matches = sorted(survey_dir.glob(f"{prefix}*.md"))
        if len(matches) != 1:
            raise ValueError(
                f"expected exactly one chapter for prefix {prefix}, got {len(matches)}"
            )
        if prefix in manifest["parts"]:
            current_part = manifest["parts"][prefix]
        path = matches[0]
        source_rows.append(
            (prefix, path, _chapter_title(path), chapter_slug(path), current_part)
        )

    titles = [row[2] for row in source_rows]
    slugs = [row[3] for row in source_rows]
    if len(titles) != len(set(titles)):
        raise ValueError("chapter H1 titles must be unique")
    if len(slugs) != len(set(slugs)):
        raise ValueError("chapter URL slugs must be unique")

    chapters = []
    for index, (prefix, path, title, slug, part) in enumerate(source_rows):
        chapters.append(
            Chapter(
                index=index,
                prefix=prefix,
                source_path=path,
                title=title,
                slug=slug,
                part=part,
                previous_slug=slugs[index - 1] if index else None,
                next_slug=slugs[index + 1] if index + 1 < len(slugs) else None,
            )
        )
    return chapters


def normalize_fragment(fragment: str | None) -> str | None:
    """Normalize GitHub fragments to Pandoc's adjacent-separator behavior."""
    if fragment is None:
        return None
    return "#" + re.sub(r"-{2,}", "-", fragment[1:])


def _outside_fenced_blocks(text: str, transform) -> str:
    output = []
    chunk = []
    fence = None
    for line in text.splitlines(keepends=True):
        match = re.match(r"^\s*(`{3,}|~{3,})", line)
        if match and fence is None:
            if chunk:
                output.append(transform("".join(chunk)))
                chunk = []
            fence = match.group(1)[0]
            output.append(line)
        elif match and fence == match.group(1)[0]:
            output.append(line)
            fence = None
        elif fence is None:
            chunk.append(line)
        else:
            output.append(line)
    if chunk:
        output.append(transform("".join(chunk)))
    return "".join(output)


def _output_directory(chapter: Chapter) -> str:
    return "." if chapter.prefix == "00_" else f"chapters/{chapter.slug}"


def rewrite_chapter_links(
    text: str, chapters: list[Chapter], current: Chapter
) -> tuple[str, int]:
    """Rewrite source Markdown chapter links to relative clean web URLs."""
    by_name = {chapter.source_path.name: chapter for chapter in chapters}
    rewritten_count = 0

    def transform(chunk: str) -> str:
        def replace(match: re.Match[str]) -> str:
            nonlocal rewritten_count
            target = match.group(1)
            if target.startswith("#"):
                normalized = normalize_fragment(target)
                if normalized != target:
                    rewritten_count += 1
                return f"]({normalized})"

            parsed = re.fullmatch(r"([^/#?]+\.md)(#.*)?", target)
            if parsed is None or parsed.group(1) not in by_name:
                return match.group(0)

            destination = by_name[parsed.group(1)]
            fragment = normalize_fragment(parsed.group(2)) or ""
            if destination.slug == current.slug:
                href = fragment or "./"
            else:
                relative = posixpath.relpath(
                    _output_directory(destination), _output_directory(current)
                )
                href = relative.rstrip("/") + "/" + fragment
            rewritten_count += 1
            return f"]({href})"

        return re.sub(r"\]\(([^)]+)\)", replace, chunk)

    return _outside_fenced_blocks(text, transform), rewritten_count


def linkify_cross_references(text: str) -> str:
    """Link prose references such as 图 5-1 and 表 5-2 to stable IDs."""
    def transform(chunk: str) -> str:
        def replace(match: re.Match[str]) -> str:
            kind = match.group(1)
            number = match.group(2)
            prefix = "fig" if kind == "图" else "tab"
            return f"[{kind} {number}](#{prefix}-{number})"

        return re.sub(r"(?<![\[*`])(图|表)[ \t]*([0-9]+-[0-9]+)", replace, chunk)

    return _outside_fenced_blocks(text, transform)


def wrap_tables(
    text: str, path: Path, chapter_number: str, chapter_title: str
) -> tuple[str, int, int]:
    """Wrap Markdown tables with stable IDs and source-authored captions."""
    lines = text.splitlines()
    output: list[str] = []
    table_index = 0
    authored = 0
    index = 0

    while index < len(lines):
        is_table = (
            index + 1 < len(lines)
            and lines[index].startswith("|")
            and re.match(r"^\|(?:\s*:?-+:?\s*\|)+\s*$", lines[index + 1])
        )
        if not is_table:
            output.append(lines[index])
            index += 1
            continue

        table_end = index
        while table_end < len(lines) and lines[table_end].startswith("|"):
            table_end += 1

        table_index += 1
        number = f"{chapter_number}-{table_index}"
        label = f"tab-{number}"
        caption_index = table_end
        while caption_index < len(lines) and lines[caption_index] == "":
            caption_index += 1
        caption_match = (
            re.match(r"^\*表[ \t]*([0-9]+-[0-9]+)[^\n]*\*$", lines[caption_index])
            if caption_index < len(lines)
            else None
        )
        if caption_match is not None:
            if caption_match.group(1) != number:
                raise ValueError(
                    f"table number mismatch in {path.name}: "
                    f"expected {number}, found {caption_match.group(1)}"
                )
            caption = lines[caption_index]
            authored += 1
            next_index = caption_index + 1
        else:
            caption = f"*表 {number}　{chapter_title}：对照表（{table_index}）。*"
            next_index = table_end

        output.extend(
            [
                f"::: {{#{label} .book-table}}",
                caption,
                "",
                *lines[index:table_end],
                ":::",
            ]
        )
        index = next_index

    suffix = "\n" if text.endswith("\n") else ""
    return "\n".join(output) + suffix, table_index, authored


def figure_number(caption: str) -> str:
    """Extract a chapter-local figure number from the source caption."""
    match = re.match(r"^\*图[ \t]*([0-9]+-[0-9]+)[^\n]*\*$", caption)
    if match is None:
        raise ValueError(f"invalid Mermaid source caption: {caption}")
    return match.group(1)


def mermaid_svg_id(svg_path: Path) -> str:
    """Return a unique SVG identifier that is also a valid CSS ID selector."""
    return "diagram-" + re.sub(r"[^A-Za-z0-9_-]", "-", svg_path.stem)


def web_mermaid_config(source: str, base_config_path: Path) -> dict[str, Any]:
    """Derive Web-only SVG layout settings from the shared Mermaid theme."""
    config = json.loads(base_config_path.read_text(encoding="utf-8"))
    web_font_family = (
        "Noto Sans SC, Source Han Sans SC VF, Source Han Sans SC, sans-serif"
    )
    config["fontFamily"] = web_font_family
    config.setdefault("themeVariables", {})["fontFamily"] = web_font_family
    config["themeCSS"] = config.get("themeCSS", "").replace(
        "'Source Han Sans SC VF', 'Source Han Sans SC'",
        "'Noto Sans SC', 'Source Han Sans SC VF', 'Source Han Sans SC'",
    )
    diagram_type = source.lstrip().split(None, 1)[0] if source.strip() else ""
    if diagram_type in {"flowchart", "graph"}:
        config["htmlLabels"] = False
        config.setdefault("flowchart", {})["wrappingWidth"] = 120
        config["themeCSS"] = (
            config.get("themeCSS", "")
            + " .edgeLabel { font-size: 22px !important; "
            "font-weight: 600 !important; }"
        )
    elif diagram_type in {"stateDiagram", "stateDiagram-v2"}:
        config["htmlLabels"] = False
    return config


def _display_columns(text: str) -> int:
    return sum(
        2 if unicodedata.east_asian_width(character) in {"W", "F"} else 1
        for character in text
    )


def _balanced_edge_label(label: str) -> str:
    if "<br" in label or _display_columns(label) <= 18:
        return label
    total = _display_columns(label)
    target = total / 2
    separators = set(" 、，,/；;：:后与或")
    candidates = [
        index
        for index in range(1, len(label))
        if label[index - 1] in separators
    ]
    if not candidates:
        candidates = list(range(1, len(label)))
    split_at = min(
        candidates,
        key=lambda index: abs(_display_columns(label[:index].rstrip()) - target),
    )
    left = label[:split_at].rstrip()
    right = label[split_at:].lstrip()
    if not left or not right:
        return label
    return f"{left}<br/>{right}"


def wrap_mermaid_edge_labels(source: str) -> str:
    """Add balanced Web-only line breaks to long Mermaid edge labels."""
    flow_pattern = re.compile(r"((?:-->|-\.->|==>)\|)([^|\n]+)(\|)")
    wrapped = flow_pattern.sub(
        lambda match: (
            match.group(1) + _balanced_edge_label(match.group(2)) + match.group(3)
        ),
        source,
    )
    if source.lstrip().startswith(("stateDiagram-v2", "stateDiagram")):
        state_pattern = re.compile(
            r"(?m)^(\s*.+?\s*-->\s*.+?\s*:\s*)([^\n]+)$"
        )
        wrapped = state_pattern.sub(
            lambda match: match.group(1) + _balanced_edge_label(match.group(2)),
            wrapped,
        )
    return wrapped


def render_mermaid_svg(source: str, svg_path: Path) -> None:
    """Render one Mermaid diagram as SVG with the shared book theme."""
    web_dir = Path(__file__).resolve().parent
    book_dir = web_dir.parent / "book"
    base_config_path = book_dir / "mermaid-config.json"
    mermaid_path = svg_path.with_suffix(".mmd")
    svg_path.parent.mkdir(parents=True, exist_ok=True)
    web_source = wrap_mermaid_edge_labels(source)
    mermaid_path.write_text(web_source, encoding="utf-8")
    config = web_mermaid_config(web_source, base_config_path)
    if config.get("htmlLabels") is False:
        config_path = svg_path.parent / "mermaid-web-config.json"
        config_path.write_text(
            json.dumps(config, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    else:
        config_path = base_config_path
    command = [
        "mmdc",
        "-i",
        str(mermaid_path),
        "-o",
        str(svg_path),
        "--svgId",
        mermaid_svg_id(svg_path),
        "-c",
        str(config_path),
        "-w",
        "2400",
        "-s",
        "2",
    ]
    puppeteer_config = os.environ.get("HARNESS_WEB_PUPPETEER_CONFIG")
    if puppeteer_config:
        puppeteer_config_path = Path(puppeteer_config).expanduser().resolve()
        if not puppeteer_config_path.is_file():
            raise RuntimeError(
                f"Puppeteer config does not exist: {puppeteer_config_path}"
            )
        command.extend(
            ["--puppeteerConfigFile", str(puppeteer_config_path)]
        )
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip()
        raise RuntimeError(f"Mermaid render failed for {svg_path.name}: {detail}")

    postprocess_command = [
        "node",
        str(web_dir / "postprocess-svg.mjs"),
        str(svg_path),
    ]
    if puppeteer_config:
        postprocess_command.append(str(puppeteer_config_path))
    postprocess_result = subprocess.run(
        postprocess_command, capture_output=True, text=True
    )
    if postprocess_result.returncode != 0:
        detail = (postprocess_result.stderr or postprocess_result.stdout).strip()
        raise RuntimeError(
            f"SVG postprocessing failed for {svg_path.name}: {detail}"
        )


def prepare_chapter_markdown(
    chapter: Chapter,
    chapters: list[Chapter],
    assets_dir: Path,
    renderer=render_mermaid_svg,
) -> PreparedChapter:
    """Prepare one source chapter for Pandoc's HTML writer."""
    text = chapter.source_path.read_text(encoding="utf-8")
    h1 = f"# {chapter.title}"
    if h1 not in text:
        raise ValueError(f"missing expected H1 in {chapter.source_path}")
    figure_count = 0

    def replace_mermaid(match: re.Match[str]) -> str:
        nonlocal figure_count
        figure_count += 1
        source = match.group(1).strip() + "\n"
        caption = match.group(2)
        number = figure_number(caption)
        svg_path = assets_dir / f"{chapter.slug}-figure-{figure_count:02d}.svg"
        renderer(source, svg_path)
        return (
            f'::: {{#fig-{number} .book-figure image="{svg_path.resolve()}"}}\n'
            f"{caption}\n"
            ":::"
        )

    text, rendered = re.subn(
        r"(?m)^```mermaid\n(.*?)```\n\n(\*图[^\n]+\*)",
        replace_mermaid,
        text,
        flags=re.S,
    )
    remaining = len(re.findall(r"(?m)^```mermaid\n", text))
    if remaining:
        raise ValueError(
            f"unpaired Mermaid source caption in {chapter.source_path.name}: "
            f"{remaining} block(s) remain"
        )
    if rendered != figure_count:
        raise ValueError(f"Mermaid render count mismatch in {chapter.source_path.name}")

    chapter_number = str(int(chapter.prefix[:2]))
    text, table_count, authored = wrap_tables(
        text, chapter.source_path, chapter_number, chapter.title
    )
    text = linkify_cross_references(text)
    text, rewritten = rewrite_chapter_links(text, chapters, chapter)
    if re.search(r"\[@[^\]]+\]", text) and "{#refs}" not in text:
        text = text.rstrip() + "\n\n## 参考文献 {.unnumbered}\n\n::: {#refs}\n:::\n"
    return PreparedChapter(
        markdown=text,
        figure_count=figure_count,
        table_count=table_count,
        authored_table_count=authored,
        rewritten_link_count=rewritten,
    )


def run_pandoc_fragment(markdown_path: Path) -> str:
    """Render a Markdown fragment through the web edition Lua filter."""
    filter_path = Path(__file__).resolve().parent / "book-filter.lua"
    command = [
        "pandoc",
        str(markdown_path),
        "--from=markdown+smart+pipe_tables+fenced_code_blocks+raw_html+link_attributes+header_attributes+auto_identifiers+fenced_divs",
        "--to=html5",
        f"--lua-filter={filter_path}",
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Pandoc HTML fragment failed: {result.stderr.strip()}")
    return result.stdout


def chapter_href(current: Chapter, destination: Chapter) -> str:
    """Return a relative clean URL from one chapter page to another."""
    if current.slug == destination.slug:
        return "./"
    relative = posixpath.relpath(
        _output_directory(destination), _output_directory(current)
    )
    return relative.rstrip("/") + "/"


def build_book_navigation(chapters: list[Chapter], current: Chapter) -> str:
    """Build the grouped full-book navigation for one page."""
    groups: list[tuple[str, list[Chapter]]] = []
    for chapter in chapters:
        if not groups or groups[-1][0] != chapter.part:
            groups.append((chapter.part, []))
        groups[-1][1].append(chapter)

    sections = []
    for part, group in groups:
        links = []
        for chapter in group:
            current_attr = ' aria-current="page"' if chapter.slug == current.slug else ""
            links.append(
                '<li><a class="book-nav-link" href="{}"{}>'
                '<span class="book-nav-number">{}</span>'
                '<span>{}</span></a></li>'.format(
                    html.escape(chapter_href(current, chapter), quote=True),
                    current_attr,
                    html.escape(chapter.prefix[:2]),
                    html.escape(chapter.title),
                )
            )
        sections.append(
            '<section class="book-part">'
            f'<h2 class="book-part-title">{html.escape(part)}</h2>'
            f'<ol>{"".join(links)}</ol>'
            "</section>"
        )
    return "".join(sections)


def render_chapter_page(
    chapter: Chapter,
    chapters: list[Chapter],
    markdown_path: Path,
    output_path: Path,
    repository_url: str,
    pdf_href: str | None,
) -> None:
    """Render one fully templated chapter page with Pandoc."""
    web_dir = Path(__file__).resolve().parent
    survey_dir = web_dir.parent / "harness-survey"
    template = web_dir / "template" / "page.html"
    asset_root = "./" if chapter.prefix == "00_" else "../../"
    first = chapters[0]
    previous = chapters[chapter.index - 1] if chapter.index else None
    next_chapter = (
        chapters[chapter.index + 1] if chapter.index + 1 < len(chapters) else None
    )
    metadata = {
        "page_title": chapter.title,
        "page_description": f"Agent Harness 比较研究：{chapter.title}",
        "page_slug": chapter.slug,
        "page_number": chapter.prefix[:2],
        "part_title": chapter.part,
        "asset_root": asset_root,
        "home_href": chapter_href(chapter, first),
        "repository_url": repository_url,
    }
    if previous is not None:
        metadata["previous_href"] = chapter_href(chapter, previous)
        metadata["previous_title"] = previous.title
    if next_chapter is not None:
        metadata["next_href"] = chapter_href(chapter, next_chapter)
        metadata["next_title"] = next_chapter.title
    if pdf_href:
        metadata["pdf_href"] = pdf_href

    output_path.parent.mkdir(parents=True, exist_ok=True)
    metadata_path = markdown_path.with_suffix(".metadata.json")
    metadata_path.write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    command = [
        "pandoc",
        str(markdown_path),
        "--from=markdown+smart+pipe_tables+fenced_code_blocks+raw_html+link_attributes+header_attributes+auto_identifiers+fenced_divs",
        "--to=html5",
        "--standalone",
        "--section-divs",
        "--toc",
        "--toc-depth=3",
        "--citeproc",
        f"--bibliography={survey_dir / 'references.bib'}",
        f"--template={template}",
        f"--lua-filter={web_dir / 'book-filter.lua'}",
        f"--metadata-file={metadata_path}",
        "--metadata=link-citations:true",
        "--metadata=reference-section-title:参考文献",
        f"--resource-path={markdown_path.parent}:{survey_dir}",
        "--output",
        str(output_path),
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(
            f"Pandoc HTML page failed for {chapter.source_path.name}: "
            f"{result.stderr.strip()}"
        )
    rendered = output_path.read_text(encoding="utf-8")
    marker = "<!--BOOK_NAV-->"
    if marker not in rendered:
        raise RuntimeError(f"book navigation marker missing in {output_path}")
    rendered = rendered.replace(marker, build_book_navigation(chapters, chapter), 1)
    output_path.write_text(rendered, encoding="utf-8")


def build_site(
    repo_root: Path,
    site_root: Path,
    work_root: Path,
    repository_url: str,
    pdf_source: Path | None,
    renderer=render_mermaid_svg,
) -> SiteBuildReport:
    """Generate every static page and asset before search indexing."""
    repo_root = repo_root.resolve()
    site_root = site_root.resolve()
    work_root = work_root.resolve()
    web_dir = repo_root / "docs" / "web"
    manifest = load_manifest(repo_root / "docs" / "book" / "book-manifest.json")
    chapters = discover_chapters(repo_root / "docs" / "harness-survey", manifest)
    if len(chapters) != 36:
        raise ValueError(f"expected 36 chapters, found {len(chapters)}")

    site_root.mkdir(parents=True, exist_ok=True)
    work_root.mkdir(parents=True, exist_ok=True)
    shutil.copytree(web_dir / "assets", site_root / "assets", dirs_exist_ok=True)
    (site_root / ".nojekyll").write_text("", encoding="utf-8")

    copied_pdf = None
    if pdf_source is not None and pdf_source.is_file():
        destination = site_root / "downloads" / pdf_source.name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(pdf_source, destination)
        copied_pdf = destination

    figures = 0
    tables = 0
    authored_captions = 0
    rewritten_links = 0
    diagram_dir = work_root / "diagrams"
    markdown_dir = work_root / "markdown"
    for chapter in chapters:
        prepared = prepare_chapter_markdown(
            chapter, chapters, diagram_dir, renderer=renderer
        )
        figures += prepared.figure_count
        tables += prepared.table_count
        authored_captions += prepared.authored_table_count
        rewritten_links += prepared.rewritten_link_count

        markdown_path = markdown_dir / f"{chapter.slug}.md"
        markdown_path.parent.mkdir(parents=True, exist_ok=True)
        markdown_path.write_text(prepared.markdown, encoding="utf-8")
        if chapter.prefix == "00_":
            output_path = site_root / "index.html"
        else:
            output_path = site_root / "chapters" / chapter.slug / "index.html"
        pdf_href = None
        if copied_pdf is not None:
            prefix = "" if chapter.prefix == "00_" else "../../"
            pdf_href = f"{prefix}downloads/{copied_pdf.name}"
        render_chapter_page(
            chapter,
            chapters,
            markdown_path,
            output_path,
            repository_url,
            pdf_href,
        )

    return SiteBuildReport(
        pages=len(chapters),
        figures=figures,
        tables=tables,
        authored_table_captions=authored_captions,
        rewritten_links=rewritten_links,
    )


def main() -> None:
    web_dir = Path(__file__).resolve().parent
    default_repo = web_dir.parents[1]
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=default_repo)
    parser.add_argument("--site-root", type=Path, required=True)
    parser.add_argument("--work-root", type=Path, required=True)
    parser.add_argument(
        "--repository-url",
        default="https://github.com/specialpointcentral/harness",
    )
    parser.add_argument("--pdf-source", type=Path)
    args = parser.parse_args()
    report = build_site(
        args.repo_root,
        args.site_root,
        args.work_root,
        args.repository_url,
        args.pdf_source,
    )
    print(
        f"prepared web site: pages={report.pages}, figures={report.figures}, "
        f"tables={report.tables}, authored table captions="
        f"{report.authored_table_captions}, rewritten links={report.rewritten_links}"
    )


if __name__ == "__main__":
    main()
