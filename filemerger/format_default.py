from typing import List
from .stats import MergeStats
from .user_config import load_user_config
from .config import DEFAULT_SEPARATOR_LENGTH


class DefaultFormatter:

    # FileMerger v0.3.2
    # ------------------------------------------------------------------
    # EXTENSIBLE METADATA
    # Runtime separator override
    # ------------------------------------------------------------------

    def __init__(self, separator_override: int | None = None):
        self.separator_override = separator_override

    def write(self, files: List[str], output_file: str) -> MergeStats:

        user_config = load_user_config()

        sep_len = (
            self.separator_override
            if self.separator_override is not None
            else user_config.get("output", {}).get(
                "separator_length", DEFAULT_SEPARATOR_LENGTH
            )
        )

        separator = "-" * int(sep_len)

        stats = MergeStats(files=len(files))

        with open(output_file, "w", encoding="utf-8") as out:

            header = "FILES INCLUDED\n" + separator + "\n"
            out.write(header)
            stats.lines += header.count("\n")
            stats.bytes += len(header.encode("utf-8"))

            for f in files:
                line = f"{f}\n"
                out.write(line)
                stats.lines += 1
                stats.bytes += len(line.encode("utf-8"))

            out.write("\n")
            stats.lines += 1
            stats.bytes += 1

            for file_path in files:

                block_header = (
                    f"{separator}\nFILE: {file_path}\n{separator}\n"
                )

                out.write(block_header)
                stats.lines += block_header.count("\n")
                stats.bytes += len(block_header.encode("utf-8"))

                try:

                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read().rstrip() + "\n"
                        out.write(content)

                        stats.lines += content.count("\n")
                        stats.bytes += len(content.encode("utf-8"))

                except UnicodeDecodeError:

                    skipped = "[Skipped: binary or non-UTF8 file]\n"

                    out.write(skipped)

                    stats.lines += 1
                    stats.bytes += len(skipped.encode("utf-8"))
                    stats.skipped_files += 1

        return stats