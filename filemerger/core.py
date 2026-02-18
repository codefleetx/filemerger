import os
from typing import List, Set
from .filters import is_allowed_file
from .gitignore import load_gitignore
from .user_config import load_user_config
from .config import EXCLUDED_DIRECTORIES, MAX_FILE_SIZE_MB
from .format_default import DefaultFormatter
from .format_llm import LLMFormatter
from .format_ai import AIMarkerFormatter
from .stats import MergeStats

def collect_files(
    paths: List[str],
    *,
    output_file: str | None = None,
) -> List[str]:
    collected: Set[str] = set()
    root = os.getcwd()

    gitignore_spec = load_gitignore(root)
    user_config = load_user_config()

    max_mb = user_config.get("filters", {}).get("max_file_size_mb", MAX_FILE_SIZE_MB)
    excluded_dirs = set(EXCLUDED_DIRECTORIES)
    excluded_dirs.update(
        user_config.get("filters", {}).get("exclude_dirs", [])
    )

    max_file_size_bytes = int(max_mb * 1024 * 1024)

    for path in paths:
        if os.path.isfile(path) and is_allowed_file(
            path,
            output_file=output_file,
            gitignore_spec=gitignore_spec,
            root=root,
            max_file_size_bytes=max_file_size_bytes,
            excluded_dirs=excluded_dirs,
        ):
            collected.add(os.path.abspath(path))

        elif os.path.isdir(path):
            for current_root, _, files in os.walk(path):
                for name in sorted(files):
                    full_path = os.path.join(current_root, name)
                    if is_allowed_file(
                        full_path,
                        output_file=output_file,
                        gitignore_spec=gitignore_spec,
                        root=root,
                        max_file_size_bytes=max_file_size_bytes,
                        excluded_dirs=excluded_dirs,
                    ):
                        collected.add(os.path.abspath(full_path))

    return sorted(collected)


def merge_files(
    files: List[str],
    output_file: str,
    *,
    llm_mode: bool = False,
    llm_compact: bool = False,
    ai_markers: bool = False,
) -> MergeStats:

    if ai_markers:
        formatter = AIMarkerFormatter()
    elif llm_mode or llm_compact:
        formatter = LLMFormatter(compact=llm_compact)
    else:
        formatter = DefaultFormatter()

    return formatter.write(files, output_file)
