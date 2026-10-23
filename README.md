
# Automated File Organizer & Cleanup Utility

A Python command-line tool that organizes files into category folders based on their file extensions.

## Features

- Organizes files into Documents, Images, Videos, Archives, and Code.
- Prevents filename overwrites by adding numbers to duplicate filenames.
- Handles permission and filesystem errors.
- Records operations in the terminal and `organizer.log`.
- Provides a dry-run mode to preview file movements.
- Does not delete files.
- Uses Python's built-in libraries; no third-party packages are required.

## Technologies Used

- Python
- os
- shutil
- pathlib
- logging
- argparse

## Requirements

- Python 3.9 or newer
- No additional packages required

## Project Structure

```text
automated-file-organizer/
├── organizer.py
├── README.md
└── .gitignore
```

## How to Run on Windows

Open PowerShell in the project folder.

### 1. Preview file movements

```powershell
python organizer.py "$HOME\Downloads" --dry-run
```

### 2. Organize files

After checking the preview, run:

```powershell
python organizer.py "$HOME\Downloads"
```

### 3. Organize a test folder

```powershell
python organizer.py "C:\Users\YourName\Desktop\TestFiles" --dry-run
```

Replace `YourName` with your Windows username and use a test folder containing sample files.

## File Categories

| Category | Examples |
|---|---|
| Documents | PDF, DOCX, TXT, XLSX |
| Images | JPG, PNG, GIF, SVG |
| Videos | MP4, MKV, AVI |
| Archives | ZIP, RAR, 7Z |
| Code | PY, JAVA, CPP, HTML, CSS, SQL |

Files with unsupported extensions are left unchanged.

## Safety Notes

- Always use `--dry-run` before moving files.
- Test the program on sample files first.
- The program moves files but does not delete them.
- Only files in the selected folder's top level are processed.
- Files that cannot be accessed are reported in the log.

## Learning Outcomes

This project demonstrates file handling, directory management, exception handling, logging, command-line arguments, and basic automation in Python.

## License

You may add a license if you decide how you want others to reuse this project.
