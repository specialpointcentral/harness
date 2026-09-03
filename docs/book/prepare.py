#!/usr/bin/env python3
"""Assemble the survey book and render Mermaid from the chapter sources."""

import json
import os
import re
import subprocess
import sys
from pathlib import Path


BOOK_DIR = Path(__file__).resolve().parent
REPO_ROOT = Path(os.environ.get("HARNESS_REPO_ROOT", BOOK_DIR.parents[1])).resolve()
SURVEY_DIR = REPO_ROOT / "docs" / "harness-survey"
BUILD_DIR = Path(
    os.environ.get("HARNESS_BOOK_BUILD_DIR", "/tmp/harness-book-build")
).resolve()
ASSETS_DIR = BUILD_DIR / "assets"
MERMAID_CONFIG = BOOK_DIR / "mermaid-config.json"

ORDER = [f"{number:02d}_" for number in range(33)] + ["90_", "91_", "93_"]
PARTS = {
    "00_": "序章与总览",
    "05_": "核心机制",
    "15_": "工程治理与执行",
    "23_": "七个系统个案",
    "30_": "综合与研究议程",
    "90_": "附录",
}
MERMAID_MAX_EFFECTIVE_FONT_PT = 9.5


def chapter_path(prefix: str) -> Path:
    matches = sorted(SURVEY_DIR.glob(f"{prefix}*.md"))
    if len(matches) != 1:
        raise SystemExit(
            f"expected exactly one chapter for prefix {prefix}, got {len(matches)}"
        )
    return matches[0]


def mermaid_max_scale() -> float:
    config = json.loads(MERMAID_CONFIG.read_text(encoding="utf-8"))
    font_size = config.get("themeVariables", {}).get("fontSize", "")
    match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)px", font_size)
    if match is None:
        raise SystemExit(f"invalid Mermaid theme fontSize: {font_size!r}")
    source_font_size = float(match.group(1))
    return min(1.0, MERMAID_MAX_EFFECTIVE_FONT_PT / source_font_size)


def normalize_pandoc_fragment(fragment: str | None) -> str | None:
    """Match Pandoc's punctuation removal, which collapses adjacent separators."""
    if fragment is None:
        return None
    return "#" + re.sub(r"-{2,}", "-", fragment[1:])


def rewrite_internal_links(
    text: str, h1_slugs: dict[str, str]
) -> tuple[str, int]:
    normalized = 0

    def replace(match: re.Match[str]) -> str:
        nonlocal normalized
        target = match.group(1)

        if target.startswith("#"):
            rewritten = normalize_pandoc_fragment(target)
            if rewritten != target:
                normalized += 1
            return f"]({rewritten})"

        parsed = re.fullmatch(r"([0-9a-z_]+\.md)(#.*)?", target)
        if not parsed or parsed.group(1) not in h1_slugs:
            return match.group(0)

        original_fragment = parsed.group(2)
        fragment = normalize_pandoc_fragment(original_fragment)
        if fragment != original_fragment:
            normalized += 1
        return f"]({fragment or '#' + h1_slugs[parsed.group(1)]})"

    return re.sub(r"\]\(([^)]+)\)", replace, text), normalized


def linkify_cross_references(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        kind = match.group(1)
        number = match.group(2)
        prefix = "fig" if kind == "图" else "tab"
        return rf"\hyperlink{{{prefix}-{number}}}{{{kind} {number}}}"

    return re.sub(
        r"(?<![\[*`])(图|表)[ \t]*([0-9]+-[0-9]+)", replace, text
    )


def wrap_tables(
    text: str, path: Path, chapter_number: str, chapter_title: str
) -> tuple[str, int, int]:
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
                raise SystemExit(
                    f"table number mismatch in {path.name}: "
                    f"expected {number}, found {caption_match.group(1)}"
                )
            caption = lines[caption_index]
            authored += 1
            next_index = caption_index + 1
        else:
            caption = f"*表 {number}　{chapter_title}：对照表（{table_index}）。*"
            next_index = table_end

        output.extend([
            f'::: {{.book-table label="{label}"}}',
            caption,
            "",
            *lines[index:table_end],
            ":::",
        ])
        index = next_index

    return (
        "\n".join(output) + ("\n" if text.endswith("\n") else ""),
        table_index,
        authored,
    )


def run() -> None:
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    figure_scale = f"{mermaid_max_scale():.4f}"

    paths = [(prefix, chapter_path(prefix)) for prefix in ORDER]
    if len(paths) != 36:
        raise SystemExit(f"expected 36 chapters, got {len(paths)}")

    h1_slugs: dict[str, str] = {}
    chapter_titles: dict[str, str] = {}
    for prefix, path in paths:
        h1 = next(
            (
                line[2:].strip()
                for line in path.read_text(encoding="utf-8").splitlines()
                if line.startswith("# ")
            ),
            None,
        )
        if h1 is None:
            raise SystemExit(f"missing H1 in {path.name}")
        chapter_titles[path.name] = h1
        h1_slugs[path.name] = f"ch{prefix[:2]}"

    mermaid_count = 0
    table_count = 0
    authored_table_count = 0
    normalized_links = 0
    output_parts: list[str] = []
    manifest: list[dict[str, object]] = []

    for prefix, path in paths:
        text = path.read_text(encoding="utf-8")
        chapter_title = chapter_titles[path.name]
        local_diagram_count = 0

        if prefix in PARTS:
            output_parts.append(f"\\part{{{PARTS[prefix]}}}\n")

        original_h1 = f"# {chapter_title}"
        display_h1 = f"# {prefix[:2]}｜{chapter_title}"
        text = text.replace(original_h1, display_h1, 1)
        text = re.sub(
            r"^#\s+(.+)$",
            lambda match: f"# {match.group(1)} {{#{h1_slugs[path.name]}}}",
            text,
            count=1,
            flags=re.M,
        )

        def render_mermaid(match: re.Match[str]) -> str:
            nonlocal mermaid_count, local_diagram_count
            mermaid_count += 1
            local_diagram_count += 1
            stem = f"diagram-{mermaid_count:03d}"
            mermaid_path = ASSETS_DIR / f"{stem}.mmd"
            image_path = ASSETS_DIR / f"{stem}.pdf"
            source = match.group(1).strip() + "\n"
            mermaid_path.write_text(source, encoding="utf-8")

            command = [
                "mmdc",
                "-i",
                str(mermaid_path),
                "-o",
                str(image_path),
                "-c",
                str(MERMAID_CONFIG),
                "-w",
                "2400",
                "-s",
                "2",
                "--pdfFit",
            ]
            result = subprocess.run(command, capture_output=True, text=True)
            if result.returncode != 0:
                print(result.stdout, file=sys.stderr)
                print(result.stderr, file=sys.stderr)
                raise SystemExit(f"Mermaid render failed: {stem} in {path.name}")

            caption = f"{chapter_title}：架构与流程（{local_diagram_count}）"
            source_caption = match.group(2)
            image_tex_path = image_path.as_posix()
            figure_number = re.match(r"\*图[ \t]*([0-9]+-[0-9]+)", source_caption)
            if figure_number is None:
                raise SystemExit(f"invalid Mermaid source caption in {path.name}")
            number = figure_number.group(1)
            figure_label = f"fig-{number}"
            manifest.append(
                {
                    "diagram": mermaid_count,
                    "chapter": path.name,
                    "caption": caption,
                    "source": f"assets/{stem}.mmd",
                    "image": f"assets/{stem}.pdf",
                }
            )
            figure_block = (
                f'::: {{.book-figure image="{image_tex_path}" label="{figure_label}" '
                f'scale="{figure_scale}"}}\n'
                f"{source_caption}\n"
                ":::"
            )
            return figure_block

        text, rendered_count = re.subn(
            r"(?m)^```mermaid\n(.*?)```\n\n(\*图[^\n]+\*)",
            render_mermaid,
            text,
            flags=re.S,
        )
        source_mermaid_count = len(re.findall(r"```mermaid\n", text))
        if source_mermaid_count != 0:
            raise SystemExit(
                f"unpaired Mermaid source caption in {path.name}: "
                f"{source_mermaid_count} block(s) remain"
            )
        if rendered_count != local_diagram_count:
            raise SystemExit(
                f"Mermaid render count mismatch in {path.name}: "
                f"rendered {rendered_count}, counted {local_diagram_count}"
            )
        text, chapter_tables, chapter_authored_tables = wrap_tables(
            text, path, str(int(prefix[:2])), chapter_title
        )
        table_count += chapter_tables
        authored_table_count += chapter_authored_tables
        text = linkify_cross_references(text)
        text, chapter_normalized = rewrite_internal_links(text, h1_slugs)
        normalized_links += chapter_normalized
        output_parts.append(text.rstrip() + "\n")

    assembled = "\n\n".join(output_parts) + "\n"
    known_pandoc_slug = "#事件溯源-session-与-surface-日志分离"
    known_github_slug = "#事件溯源-session-与-surface--日志分离"
    if known_github_slug in assembled or known_pandoc_slug not in assembled:
        raise SystemExit("known GitHub/Pandoc slug normalization did not take effect")
    if mermaid_count == 0:
        raise SystemExit("no Mermaid diagrams found")

    (BUILD_DIR / "book.md").write_text(assembled, encoding="utf-8")
    (BUILD_DIR / "diagram-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(
        f"chapters: {len(paths)}, Mermaid diagrams: {mermaid_count}, "
        f"tables: {table_count}, "
        f"authored table captions: {authored_table_count}, "
        f"normalized fragment links: {normalized_links}"
    )


if __name__ == "__main__":
    run()
