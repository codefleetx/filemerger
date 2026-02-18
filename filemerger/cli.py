import argparse
import sys
import os

from .core import collect_files, merge_files
from .utils import normalize_output_filename


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

    args = parser.parse_args()

    if args.llm_compact:
        args.llm = True

    output_file = normalize_output_filename(args.output)
    output_file = os.path.join(os.getcwd(), output_file)

    files = collect_files(args.paths, output_file=output_file)

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
