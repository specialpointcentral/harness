#!/usr/bin/env python3
"""Materialize Simplified Chinese static OTFs from Source Han VF TTC files."""

import argparse
import hashlib
import json
from pathlib import Path

from fontTools.ttLib import TTCollection
from fontTools.varLib.instancer import instantiateVariableFont


def family_names(font) -> set[str]:
    names: set[str] = set()
    for record in font["name"].names:
        if record.nameID not in (1, 16):
            continue
        try:
            names.add(record.toUnicode())
        except UnicodeError:
            continue
    return names


def sc_face(path: Path, expected_family: str):
    collection = TTCollection(path, lazy=False)
    for font in collection.fonts:
        if expected_family in family_names(font):
            return font
    raise SystemExit(f"{path} does not contain family {expected_family!r}")


def save_instance(source, weight: int, destination: Path) -> None:
    instance = instantiateVariableFont(
        source,
        {"wght": weight},
        inplace=False,
        downgradeCFF2=True,
        static=True,
    )
    instance.save(destination)


def source_fingerprint(paths: list[Path]) -> dict[str, object]:
    digest = hashlib.sha256()
    files = []
    for path in paths:
        stat = path.stat()
        with path.open("rb") as stream:
            while chunk := stream.read(1024 * 1024):
                digest.update(chunk)
        files.append({"path": str(path.resolve()), "size": stat.st_size})
    return {"files": files, "sha256": digest.hexdigest()}


def run() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--serif", required=True, type=Path)
    parser.add_argument("--sans", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--metadata", required=True, type=Path)
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    outputs = [
        args.output_dir / "SourceHanSerifSC-Regular.otf",
        args.output_dir / "SourceHanSerifSC-Bold.otf",
        args.output_dir / "SourceHanSansSC-Regular.otf",
        args.output_dir / "SourceHanSansSC-Bold.otf",
    ]
    manifest_path = args.output_dir / "font-source.json"
    fingerprint = source_fingerprint([args.serif, args.sans])
    cached = False
    if manifest_path.is_file() and all(path.is_file() for path in outputs):
        cached = json.loads(manifest_path.read_text(encoding="utf-8")) == fingerprint

    if not cached:
        serif = sc_face(args.serif, "Source Han Serif SC VF")
        sans = sc_face(args.sans, "Source Han Sans SC VF")
        save_instance(serif, 400, outputs[0])
        save_instance(serif, 700, outputs[1])
        save_instance(sans, 400, outputs[2])
        save_instance(sans, 700, outputs[3])
        manifest_path.write_text(
            json.dumps(fingerprint, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    font_path = f"{args.output_dir.resolve()}/"
    metadata = {
        "mainfont": "SourceHanSerifSC-Regular",
        "sansfont": "SourceHanSansSC-Regular",
        "monofont": "Menlo",
        "CJKmainfont": "SourceHanSerifSC-Regular",
        "CJKsansfont": "SourceHanSansSC-Regular",
        "CJKmonofont": "SourceHanSansSC-Regular",
        "mainfontoptions": [
            f"Path={font_path}",
            "Extension=.otf",
            "BoldFont=SourceHanSerifSC-Bold",
        ],
        "sansfontoptions": [
            f"Path={font_path}",
            "Extension=.otf",
            "BoldFont=SourceHanSansSC-Bold",
        ],
        "CJKmainfontoptions": [
            f"Path={font_path}",
            "Extension=.otf",
            "BoldFont=SourceHanSerifSC-Bold",
        ],
        "CJKsansfontoptions": [
            f"Path={font_path}",
            "Extension=.otf",
            "BoldFont=SourceHanSansSC-Bold",
        ],
        "CJKmonofontoptions": [
            f"Path={font_path}",
            "Extension=.otf",
            "BoldFont=SourceHanSansSC-Bold",
        ],
    }
    args.metadata.write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    state = "reused" if cached else "prepared"
    print(f"{state} Source Han SC fonts in {args.output_dir}")


if __name__ == "__main__":
    run()
