<div align="center">

# yournal.py
Fast (y)ournal script to make daily notes from your terminal.

![Python](https://img.shields.io/badge/python-default?logo=python)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

![intro](https://raw.githubusercontent.com/Rikiub/yournal.py/main/intro.gif)

</div>

## Features

- 🍃 Lighweight, fast and snappy. It is a pure Python script.
- 📅 `[yesterday | today | tomorrow ]` date navigation.
- 🔧 Enviroment variables based [configuration](#configuration).
- 📄 Simple template support.

## Usage

### 🍃 First open

In your shell, you can try one of these commands:

```shell
python yournal.py
```
```shell
./yournal.py
```

Or if you [installed](#installation) it..

```shell
yournal
```

### 📅 Open/create daily note by date
```shell
yournal [yesterday|today|tomorrow]
```
> By default, the daily note will be opened with your `EDITOR` variable. If this fails, the default text editor of your system will be used. 

### 🔧📄 Configuration and templates
```shell
yournal -d <path/to/dir> -t <path/to/template>
```
> For persistent configuration see [this](#configuration).

## Installation

> Minium **Python** version: 3.8

### Pipx (Recommended)

The easy way. If you have [Pipx](https://pypa.github.io/pipx/) installed simply type in your shell:

```shell
pipx install yournal
```

### Pip

The classic way. Type in your shell:

```shell
pip install yournal
```

### AUR (Arch Linux)

[![latest packaged version(s)](https://repology.org/badge/latest-versions/yournal.svg)](https://repology.org/project/yournal/versions)

Use an **AUR** helper such as:
```shell
paru -S yournal
```
```shell
yay -S yournal
```

### Manual

Download the lastest [release](https://github.com/Rikiub/yournal.py/releases/latest) and get the `yournal.py` file.

You can use this script directly with `python yournal.py`, but for a better integration, add the `yournal.py` file to your system **PATH**.

- For example, a common **Linux** user **PATH** is: `~/.local/bin`. 
- For other systems, please investigate.

> Rename `yournal.py` to `yournal` if you want a shorter command.

## Configuration

### Enviroment variables

By default, `yournal` will create the daily notes in the current working directory, along with other settings To change this behavior, you need to set these environment variables on your system:

- `YOURNAL_EXTENSION` for daily note file extension
- `YOURNAL_DIRECTORY` for the directory where the daily notes will be saved.
- `YOURNAL_TEMPLATE` for the template file to use.

### Shell aliases

You can create a shell `alias` for yournal with custom arguments.

In **Bash** you can do this by adding the following to your `.bashrc` file. For **Zsh**, in `.zshrc`.
```shell
alias yournal="yournal -d path/to/dir -t path/to/template"
```

## CLI (Command Line Interface)

```
usage: yournal [-x EXTENSION] [-d DIRECTORY] [-t TEMPLATE] [-h] [-i] [-e EDITOR] [{yesterday,today,tomorrow}]

Fast (y)ournal script to make daily notes on your terminal.

dates:
  {yesterday,today,tomorrow}
                        open daily note by date. DEFAULT: today

paths:
  -x EXTENSION, --extension EXTENSION
                        set daily note file extension. DEFAULT: "md" (markdown)
  -d DIRECTORY, --directory DIRECTORY
                        directory where save your daily notes. DEFAULT: cwd (current working directory)
  -t TEMPLATE, --template TEMPLATE
                        template file to use

options:
  -h, --help            show this help message and exit
  -i, --ignore          ignore EDITOR environment variable and use system editor
  -e EDITOR, --editor EDITOR
                        use a custom editor command

By default, yournal uses these environment variables when no arguments are provided:
    YOURNAL_EXTENSION for daily note file extension
    YOURNAL_DIRECTORY for DIRECTORY
    YOURNAL_TEMPLATE for TEMPLATE
```
