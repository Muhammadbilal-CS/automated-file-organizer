"""
Automated File Organizer & Cleanup Utility
Sorts files into category folders based on their extensions.

Safety:
- Only scans the selected folder's top level.
- Does not delete files.
- Avoids overwriting files with the same name.
- Supports dry-run mode to preview file movements.
"""

import argparse
import logging
import os
import shutil
from pathlib import Path


EXTENSION_CATEGORIES = {
    # Documents
    ".pdf": "Documents", ".doc": "Documents", ".docx": "Documents",
    ".txt": "Documents", ".rtf": "Documents", ".odt": "Documents",
    ".xls": "Documents", ".xlsx": "Documents", ".csv": "Documents",
    ".ppt": "Documents", ".pptx": "Documents",

    # Images
    ".jpg": "Images", ".jpeg": "Images", ".png": "Images",
    ".gif": "Images", ".bmp": "Images", ".webp": "Images",
    ".tiff": "Images", ".svg": "Images", ".ico": "Images",

    # Videos
    ".mp4": "Videos", ".mkv": "Videos", ".mov": "Videos",
    ".avi": "Videos", ".wmv": "Videos", ".webm": "Videos",
    ".mpeg": "Videos", ".mpg": "Videos",

    # Archives
    ".zip": "Archives", ".rar": "Archives", ".7z": "Archives",
    ".tar": "Archives", ".gz": "Archives", ".bz2": "Archives",
    ".xz": "Archives",

    # Code
    ".py": "Code", ".java": "Code", ".cpp": "Code",
    ".c": "Code", ".h": "Code", ".hpp": "Code",
    ".js": "Code", ".ts": "Code", ".html": "Code",
    ".css": "Code", ".php": "Code", ".json": "Code",
    ".xml": "Code", ".sql": "Code", ".sh": "Code",
    ".bat": "Code", ".ps1": "Code",
}


def configure_logging(log_file: Path) -> None:
    """Show logs in the terminal and save them to a file."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )


def unique_destination(destination: Path) -> Path:
    """Add a number to a filename if it already exists."""
    if not destination.exists():
        return destination

    parent = destination.parent
    stem = destination.stem
    suffix = destination.suffix
    counter = 1

    while True:
        candidate = parent / f"{stem}_{counter}{suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


def organize_directory(folder: Path, dry_run: bool = False) -> dict:
    """Organize supported files in the selected folder."""
    folder = folder.expanduser().resolve()

    if not folder.exists():
        raise FileNotFoundError(f"Folder does not exist: {folder}")

    if not folder.is_dir():
        raise NotADirectoryError(f"Not a directory: {folder}")

    counts = {
        "moved": 0,
        "would_move": 0,
        "skipped": 0,
        "errors": 0,
    }

    try:
        entries = list(os.scandir(folder))
    except PermissionError:
        logging.exception("Permission denied while scanning: %s", folder)
        counts["errors"] += 1
        return counts
    except OSError:
        logging.exception("Could not scan folder: %s", folder)
        counts["errors"] += 1
        return counts

    for entry in entries:
        source = Path(entry.path)

        try:
            if entry.is_symlink() or not entry.is_file(
                follow_symlinks=False
            ):
                counts["skipped"] += 1
                continue

            category = EXTENSION_CATEGORIES.get(source.suffix.lower())

            if category is None:
                logging.info("SKIP (unknown extension): %s", source.name)
                counts["skipped"] += 1
                continue

            destination_dir = folder / category
            destination = unique_destination(
                destination_dir / source.name
            )

            if dry_run:
                logging.info("DRY RUN: %s -> %s", source, destination)
                counts["would_move"] += 1
                continue

            destination_dir.mkdir(parents=True, exist_ok=True)

            # Check again before moving to reduce collision risk.
            destination = unique_destination(
                destination_dir / source.name
            )

            shutil.move(str(source), str(destination))
            logging.info("MOVED: %s -> %s", source.name, destination)
            counts["moved"] += 1

        except PermissionError:
            logging.exception("PERMISSION DENIED: %s", source)
            counts["errors"] += 1
        except FileExistsError:
            logging.exception("DESTINATION ALREADY EXISTS: %s", source)
            counts["errors"] += 1
        except OSError:
            logging.exception("FILESYSTEM ERROR: %s", source)
            counts["errors"] += 1

    return counts


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Organize files into Documents, Images, Videos, "
            "Archives, and Code."
        )
    )

    parser.add_argument(
        "folder",
        nargs="?",
        default=str(Path.home() / "Downloads"),
        help="Folder to organize (default: Downloads)",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview movements without moving files",
    )

    args = parser.parse_args()
    folder = Path(args.folder).expanduser()

    log_file = Path(__file__).resolve().parent / "organizer.log"
    configure_logging(log_file)

    logging.info("Starting organizer for: %s", folder.resolve())

    if args.dry_run:
        logging.info("DRY-RUN MODE: no files will be moved.")

    try:
        counts = organize_directory(folder, dry_run=args.dry_run)
    except (FileNotFoundError, NotADirectoryError) as exc:
        logging.error("%s", exc)
        raise SystemExit(1)

    print("\n" + "=" * 42)
    print("       FILE ORGANIZER SUMMARY")
    print("=" * 42)
    print(f"Folder checked : {folder.resolve()}")
    print(f"Files moved    : {counts['moved']}")
    print(f"Previewed      : {counts['would_move']}")
    print(f"Skipped        : {counts['skipped']}")
    print(f"Errors         : {counts['errors']}")
    print(f"Log file       : {log_file}")
    print("=" * 42)


if __name__ == "__main__":
    main()