#!/usr/bin/env python3
"""
Author: Rikiub
Repository: https://github.com/Rikiub/yournal.py

Fast (y)ournal script to make Daily Notes on your terminal.

-h or --help to see usage help.
"""

from argparse import ArgumentParser, Namespace, RawDescriptionHelpFormatter
from datetime import date
from pathlib import Path
import subprocess
import platform
import os

# modules for templating support
import locale
import re

# environment variables.
ENV_DIR_NAME = "YOURNAL_DIR"
ENV_TEMPLATE_NAME = "YOURNAL_TEMPLATE"


def parse_vars(text_to_parse: str) -> str:
    """Parse title and dates. Requires "arrow" package."""
    import arrow

    regex_pattern = "{{(\w+)(?::([^}]+))?}}"

    def replace_match(match):
        key = match.group(1)
        value = match.group(2)

        # Obsidian Templates
        if key == "title":
            return arrow.now().format("YYYY-MM-DD")
        elif key == "date":
            if value is None:
                return arrow.now().format("YYYY-MM-DD")
            else:
                return arrow.now().format(value)
        elif key == "time":
            if value is None:
                return arrow.now().format("HH:mm")
            else:
                return arrow.now().format(value)

    parsed_template = re.sub(regex_pattern, replace_match, text_to_parse)
    return parsed_template


def check_dynamic_templates_support() -> bool:
    """Check if dependences are installed."""
    try:
        import arrow

        return True
    except:
        return False


def extract_text(file: Path) -> str:
    """Extract text from file."""
    with file.open("r") as file:
        text = file.read()
        return text


def open_file_with_editor(file: Path) -> None:
    """Open file with default system editor."""
    global IGNORE_ENV, CUSTOM_EDITOR

    system = platform.system()
    EDITOR = os.getenv("EDITOR")

    if CUSTOM_EDITOR:
        editor_env = [CUSTOM_EDITOR]
    elif not IGNORE_ENV and EDITOR:
        editor_env = [EDITOR]
    elif system == "Windows":
        editor_env = ["cmd", "/c", "start"]
    elif system == "Linux":
        editor_env = ["xdg-open"]
    elif system == "Darwin":
        editor_env = ["open"]
    else:
        raise OSError(
            "Failed to open system editor. Supported OS: Windows, Linux, Darwin."
        )
    subprocess.run([*editor_env, file])


def daily_note(directory: Path, template: Path = None) -> None:
    """open/create Daily Note."""
    global SKIP_TEMPLATE_PARSE

    directory.mkdir(parents=True, exist_ok=True)
    daily_note = directory / f"{date.today()}.md"

    # open
    if daily_note.exists():
        open_file_with_editor(daily_note)

    # create
    else:
        # parse template if exist
        if isinstance(template, Path):
            if template.is_file():
                if not SKIP_TEMPLATE_PARSE and check_dynamic_templates_support():
                    text = extract_text(template)
                    template = parse_vars(text)
                else:
                    template = extract_text(template)

                with daily_note.open("w") as note:
                    note.write(template)
            else:
                raise FileNotFoundError(
                    f'The template "{template}" not exist or not is a file.'
                )
        else:
            daily_note.touch()

        open_file_with_editor(daily_note)


def parseArguments() -> Namespace:
    """CLI interface."""

    parser = ArgumentParser(
        formatter_class=RawDescriptionHelpFormatter,
        add_help=False,
        prog="yournal",
        description="Fast (y)ournal script to make Daily Notes on your terminal.",
        epilog=f"""By default, yournal uses these environment variables when no arguments are provided:
    {ENV_DIR_NAME} for DIRECTORY
    {ENV_TEMPLATE_NAME} for TEMPLATE

Dynamic templates supported: {check_dynamic_templates_support()}

To parse "dynamic variables" in templates you need to have the Python "arrow" package installed. You can install it with pip:
    pip install arrow

    The "Obsidian Templates" syntax is supported for now.
""",
    )

    paths = parser.add_argument_group("paths")
    paths.add_argument(
        "-d",
        "--directory",
        help="directory where save your daily notes",
        default=os.getenv(ENV_DIR_NAME) or Path.cwd(),
        type=Path,
    )
    paths.add_argument(
        "-t",
        "--template",
        help="template file to parse",
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
        help="ignore environment variables",
        action="store_true",
    )
    options.add_argument(
        "-s",
        "--skip",
        help="skip dynamic templates parse",
        action="store_true",
    )
    options.add_argument(
        "-e",
        "--editor",
        help="use a custom editor command",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parseArguments()

    CUSTOM_EDITOR = args.editor
    IGNORE_ENV = args.ignore
    SKIP_TEMPLATE_PARSE = args.skip

    daily_note(directory=args.directory, template=args.template)
