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


def chapter_path(prefix: str) -> Path:
    matches = sorted(SURVEY_DIR.glob(f"{prefix}*.md"))
    if len(matches) != 1:
        raise SystemExit(
            f"expected exactly one chapter for prefix {prefix}, got {len(matches)}"
        )
    return matches[0]


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


def run() -> None:
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)

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
            manifest.append(
                {
                    "diagram": mermaid_count,
                    "chapter": path.name,
                    "caption": caption,
                    "source": f"assets/{stem}.mmd",
                    "image": f"assets/{stem}.pdf",
                }
            )
            return f"![{caption}](assets/{stem}.pdf){{#fig:{stem} width=92% height=78%}}"

        text = re.sub(r"```mermaid\n(.*?)```", render_mermaid, text, flags=re.S)
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
        f"normalized fragment links: {normalized_links}"
    )


if __name__ == "__main__":
    run()
