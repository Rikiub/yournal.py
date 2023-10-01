<div align="center">

# yournal.py
Fast (y)ournal script to make daily notes from your terminal.

![Python](https://img.shields.io/badge/python-default?logo=python)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

![intro](https://github.com/Rikiub/yournal.py/blob/6fe4c41afa54eff7008a6852f240261d59f16b3b/intro.gif)

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

Or if you [installed](#installation) it...

```shel
yournal
```

> By default, the daily note will be opened with your `EDITOR` variable. If this fails, the default text editor of your system will be used. 

### 📅 Open/create daily note by date
```shell
yournal [yesterday|today|tomorrow]
```

### 🔧📄 Configuration and templates
```shell
yournal -d <path/to/dir> -t <path/to/template>
```
> For persistent configuration see [this](#configuration).

## Installation

> Minium **Python** version: 3.8

First you need to have **Python** installed on your system, then clone this repository:

```shell
git clone https://github.com/Rikiub/yournal.py.git
```

Or instead, download the lastest [release](https://github.com/Rikiub/yournal.py/releases).

You can use this script directly with `python yournal.py`, but for a better integration, read on.

---

Add the `yournal.py` file to your system **PATH**.

For example, a common **Linux** user **PATH** is: `~/.local/bin`. 
<br>
For other systems, please investigate.

> Rename `yournal.py` to `yournal` if you want a shorter command.

## Configuration

By default, `yournal` will create the daily notes in the current working directory, along with other settings To change this behavior, you need to set these environment variables on your system:

- `YOURNAL_EXTENSION` for daily note file extension
- `YOURNAL_DIRECTORY` for the directory where the daily notes will be saved.
- `YOURNAL_TEMPLATE` for the template file to use.

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
