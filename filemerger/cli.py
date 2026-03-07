import argparse
import sys
import os

from .core import collect_files, merge_files
from .utils import normalize_output_filename


def _parse_csv(value: str | None):
    """
    Parse comma-separated CLI values into a normalized list.
    Trims whitespace and removes empty entries.
    """
    if not value:
        return []

    items = [v.strip() for v in value.split(",") if v.strip()]
    return list(dict.fromkeys(items))  # deduplicate while preserving order


def main():
    parser = argparse.ArgumentParser(
        description="Consolidate project files into a single text output"
    )

    parser.add_argument(
        "paths",
        nargs="+",
        help="Files or directories to include"
    )

    parser.add_argument(
        "-o", "--output",
        help="Output file name (always saved as .txt)"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show files that would be included without writing output"
    )

    parser.add_argument(
        "--stats",
        action="store_true",
        help="Print merge statistics"
    )

    parser.add_argument(
        "--llm",
        action="store_true",
        help="Optimize output for LLM context ingestion"
    )

    parser.add_argument(
        "--llm-compact",
        action="store_true",
        help="More compact LLM output with fewer blank lines"
    )

    parser.add_argument(
        "--ai-markers",
        action="store_true",
        help="Use explicit AI-friendly file boundary markers"
    )

    # FileMerger v0.3.2
    # ------------------------------------------------------------------
    # EXTENSIBLE METADATA
    # Runtime configuration overrides
    # ------------------------------------------------------------------

    parser.add_argument(
        "--allow-dir",
        help=(
            "Allow specific directories that are normally excluded. "
            "Comma-separated names. Example: --allow-dir migrations,tests"
        ),
    )

    parser.add_argument(
        "--allow-file",
        help=(
            "Allow specific filenames normally excluded. "
            "Comma-separated names. Example: --allow-file .DS_Store"
        ),
    )

    parser.add_argument(
        "--allow-ext",
        help=(
            "Add extra allowed file extensions. "
            "Comma-separated values. Example: --allow-ext .yaml,.yml"
        ),
    )

    parser.add_argument(
        "--max-size",
        type=int,
        help="Override maximum file size in MB"
    )

    parser.add_argument(
        "--separator",
        type=int,
        help="Override output separator length"
    )

    args = parser.parse_args()

    if args.llm_compact:
        args.llm = True

    output_file = normalize_output_filename(args.output)
    output_file = os.path.join(os.getcwd(), output_file)

    allow_dirs = _parse_csv(args.allow_dir)
    allow_files = _parse_csv(args.allow_file)
    allow_ext = _parse_csv(args.allow_ext)

    files = collect_files(
        args.paths,
        output_file=output_file,
        allow_dirs=allow_dirs,
        allow_files=allow_files,
        allow_extensions=allow_ext,
        max_size_override=args.max_size,
    )

    if not files:
        print("No valid files found.")
        sys.exit(2)

    if args.dry_run:
        print("Files to be included:")
        for f in files:
            print(f" - {f}")

        if args.stats:
            print("\nStats:")
            print(f"  Files: {len(files)}")

        sys.exit(0)

    stats = merge_files(
        files,
        output_file,
        llm_mode=args.llm,
        llm_compact=args.llm_compact,
        ai_markers=args.ai_markers,
        separator_override=args.separator,
    )

    print(f"✔ Merged {stats.files} files into {output_file}")

    if args.stats:
        print("\nStats:")
        print(f"  Files: {stats.files}")
        print(f"  Lines: {stats.lines}")
        print(f"  Bytes: {stats.bytes}")
        print(f"  Skipped files: {stats.skipped_files}")


if __name__ == "__main__":
    main()