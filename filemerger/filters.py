import os
from .gitignore import is_ignored


def is_allowed_file(
    path: str,
    *,
    output_file: str | None = None,
    gitignore_spec=None,
    root: str | None = None,
    max_file_size_bytes: int,
    excluded_dirs: set[str],
    excluded_files: set[str],
    allowed_extensions: set[str],
) -> bool:

    if not os.path.isfile(path):
        return False

    if output_file and os.path.abspath(path) == os.path.abspath(output_file):
        return False

    if gitignore_spec and root and is_ignored(path, root=root, spec=gitignore_spec):
        return False

    if os.path.basename(path) in excluded_files:
        return False

    if os.path.splitext(path)[1].lower() not in allowed_extensions:
        return False

    parts = path.split(os.sep)
    if any(part in excluded_dirs for part in parts):
        return False

    try:
        if os.path.getsize(path) > max_file_size_bytes:
            return False
    except OSError:
        return False

    return True