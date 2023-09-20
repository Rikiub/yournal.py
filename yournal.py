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

# set the name of the environment variables. change it if you want to use other variables.
ENV_DIR_NAME = "YOURNAL_DIR"
ENV_TEMPLATE_NAME = "YOURNAL_TEMPLATE"


def parse_vars(text_to_parse: str) -> str:
    """Parse title and dates. Requires "arrow" package."""
    import arrow

    system_locale = locale.getlocale()[0]
    system_locale = system_locale.split("_", 1)[0]
    regex_pattern = "{{(\w+)(?::([^}]+))?}}"

    def replace_match(match):
        key = match.group(1)
        value = match.group(2)

        if key == "title":
            return arrow.now().format("YYYY-MM-DD", locale=system_locale)
        elif key == "date":
            if value is None:
                return arrow.now().format("YYYY-MM-DD", locale=system_locale)
            else:
                return arrow.now().format(value, locale=system_locale)
        elif key == "time":
            if value is None:
                return arrow.now().format("HH:mm", locale=system_locale)
            else:
                return arrow.now().format(value, locale=system_locale)

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

    if platform.system() in ("Windows", "Linux", "Darwin"):
        EDITOR = os.getenv("EDITOR")

        try:
            if EDITOR:
                subprocess.call([EDITOR, file])
            elif (
                subprocess.call(["open", file]),
                subprocess.call(["xdg-open", file]),
                subprocess.call([file]),
            ):
                pass
        except:
            raise OSError("Failed to open system editor.")
    else:
        raise OSError(
            "Failed to determine your system. Valid systems: Windows, Linux, Darwin."
        )


def daily_note(directory: Path, template: Path = None) -> None:
    """Main function."""

    # open/create daily_note
    directory.mkdir(parents=True, exist_ok=True)
    daily_note = directory / f"{date.today()}.md"

    # open
    if daily_note.exists():
        open_file_with_editor(daily_note)

    # create
    else:
        # parse template if exist
        if isinstance(template, Path) and template.is_file():
            if check_dynamic_templates_support():
                text = extract_text(template)
                template = parse_vars(text)
            else:
                template = extract_text(template)

            with daily_note.open("w") as note:
                note.write(template)
        else:
            print(f'The template "{template}" not exist.')
            raise SystemExit(1)

        open_file_with_editor(daily_note)


def parseArguments() -> Namespace:
    """CLI interface."""

    parser = ArgumentParser(
        formatter_class=RawDescriptionHelpFormatter,
        prog="yournal",
        description="Fast (y)ournal script to make Daily Notes on your terminal.",
        epilog=f"""By default, yournal uses these environment variables when no arguments are provided:
    {ENV_DIR_NAME} for DIRECTORY
    {ENV_TEMPLATE_NAME} for TEMPLATE

To parse "dynamic variables" in templates you need to have the Python "arrow" package installed. You can install it with pip:
    pip install arrow

    The "Obsidian Templates" syntax is supported for now.
""",
    )
    parser.add_argument(
        "-d",
        "--directory",
        help="Directory where save your Daily Notes.",
        default=os.getenv(ENV_DIR_NAME) or Path.cwd(),
        type=Path,
    )
    parser.add_argument(
        "-t",
        "--template",
        help="Template file to parse. Recommended use a markdown file.",
        default=os.getenv(ENV_TEMPLATE_NAME) or None,
        type=Path,
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parseArguments()
    daily_note(directory=args.directory, template=args.template)
