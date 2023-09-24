#!/usr/bin/env python3
"""
Author: Rikiub
Repository: https://github.com/Rikiub/yournal.py

Fast (y)ournal script to make Daily Notes on your terminal.

-h or --help to see usage help.
"""

from argparse import ArgumentParser, Namespace, RawDescriptionHelpFormatter
from datetime import date, timedelta
from pathlib import Path
import subprocess
import platform
import os


# constants
ENV_EXTENSION_NAME = "YOURNAL_EXTENSION"
ENV_DIRECTORY_NAME = "YOURNAL_DIRECTORY"
ENV_TEMPLATE_NAME = "YOURNAL_TEMPLATE"
DATE_NOW = date.today()
WEEKLY_DATES = {
    "yesterday": DATE_NOW - timedelta(days=1),
    "today": DATE_NOW,
    "tomorrow": DATE_NOW + timedelta(days=1),
}


def open_file_with_editor(file: Path) -> None:
    """Open file with default system editor."""
    system = platform.system()

    try:
        if editor := EDITOR:
            editor_env = [editor]
        elif system == "Windows":
            editor_env = ["cmd", "/c", "start"]
        elif system == "Linux":
            editor_env = ["xdg-open"]
        elif system == "Darwin":
            editor_env = ["open"]
        subprocess.run([*editor_env, file])
    except FileNotFoundError as e:
        print(
            f'ERROR: Failed to open "{e.filename}" editor, check your EDITOR variable/argument. \nSupported OS: Windows, Linux, Darwin.'
        )
        raise SystemExit(1)


def daily_note(
    file_date: str, directory: Path, template: Path = None, file_extension: str = "md"
) -> None:
    """open/create Daily Note."""

    message_create = f'Creating "{file_date}" daily note.'
    message_open = f'Opening "{file_date}" daily note.'

    directory.mkdir(parents=True, exist_ok=True)
    daily_note = directory / str(f"{file_date}.{file_extension}")

    # open
    if daily_note.exists():
        print(message_open)
        open_file_with_editor(daily_note)

    # create
    else:
        print(message_create)

        if template:
            try:
                text = template.read_text()
                daily_note.write_text(text)
            except FileNotFoundError:
                print(
                    f'ERROR: template "{template}" not exist or not is a plain text file.'
                )
                raise SystemExit(1)
        else:
            daily_note.touch()

        print(message_open)
        open_file_with_editor(daily_note)


def parseArguments() -> Namespace:
    """CLI interface."""

    parser = ArgumentParser(
        formatter_class=RawDescriptionHelpFormatter,
        add_help=False,
        prog="yournal",
        description="Fast (y)ournal script to make Daily Notes on your terminal.",
        epilog=f"""By default, yournal uses these environment variables when no arguments are provided:
    {ENV_DIRECTORY_NAME} for DIRECTORY
    {ENV_TEMPLATE_NAME} for TEMPLATE
    {ENV_EXTENSION_NAME} for daily note file extension
""",
    )

    dates = parser.add_argument_group("dates")
    dates.add_argument(
        "dates",
        help="open daily note by date. DEFAULT: today",
        choices=[*WEEKLY_DATES.keys()],
        default="today",
        nargs="?",
        type=str,
    )

    paths = parser.add_argument_group("paths")
    paths.add_argument(
        "-x",
        "--extension",
        help='set daily note file extension. DEFAULT: "md" (markdown)',
        default=os.getenv(ENV_EXTENSION_NAME) or "md",
        type=str,
    )
    paths.add_argument(
        "-d",
        "--directory",
        help="directory where save your daily notes. DEFAULT: cwd (current working directory)",
        default=os.getenv(ENV_DIRECTORY_NAME) or Path.cwd(),
        type=Path,
    )
    paths.add_argument(
        "-t",
        "--template",
        help="template file to use",
        default=os.getenv(ENV_TEMPLATE_NAME) or None,
        type=Path,
    )

    options = parser.add_argument_group("options")
    options.add_argument(
        "-h", "--help", action="help", help="show this help message and exit"
    )
    options.add_argument(
        "-i",
        "--ignore",
        help="ignore EDITOR environment variable and use system editor",
        action="store_true",
    )
    options.add_argument(
        "-e",
        "--editor",
        help="use a custom editor command",
        default=os.getenv("EDITOR") or None,
        type=str,
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parseArguments()

    # set global vars
    if args.ignore:
        EDITOR = None
    else:
        EDITOR = args.editor

    # start
    daily_note(
        file_date=WEEKLY_DATES[args.dates],
        directory=args.directory,
        template=args.template,
        file_extension=args.extension,
    )
