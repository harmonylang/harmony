# Harmony

Harmony is a programming language designed for testing and experimenting with concurrent code.

- [Harmony](#harmony)
  - [Preliminary Requirements](#preliminary-requirements)
    - [Install Python3](#install-python3)
    - [Install GCC](#install-gcc)
  - [Harmony on VSCode](#harmony-on-vscode)
  - [Command-Line Harmony Installation Guide](#command-line-harmony-installation-guide)
    - [Install using pip](#install-using-pip)
    - [Install from Source](#install-from-source)
  - [Checking for Updates on Harmony](#checking-for-updates-on-harmony)
    - [VSCode Extension](#vscode-extension)
    - [Command Line Harmony](#command-line-harmony)

For more information, please visit https://harmony.cs.cornell.edu

## Preliminary Requirements

1. Python (version 3.6 or higher)
2. GCC compiler

### Install Python3

If you do not have Python3 already installed, download and install Python depending on your OS (Windows, Mac, Linux, etc) [here](https://www.python.org/downloads/). Be sure to install version `3.6` or higher.

On the command line, you can check if Python has been successfully installed by running `python3 --version`.

### Install GCC

`gcc` is a compiler for the C programming language and is needed for the model checker component of Harmony. Here are the steps to installing `gcc` depending on your OS.

**Windows**:

Installing **64-bit** `gcc` under Windows:
  - Follow the instructions at http://mingw-w64.org/doku.php to download the `mingw-w64` installer. Run the installer once it is downloaded.
  - At the Settings window, make sure you **select the x86-64
    architecture** (instead of the default i686) during installation!
  - At the next window, make sure you copy name of the Destination folder; you'll need it later.
  - After installation is complete, add the name of the Destination folder you copied in the previous step extended with `\mingw64\bin` to your `Path` environment variable
    (search for **Edit environment variables** in the search bar. You can add it either to the `Path` associated with your account or the system `Path`).
  - Make sure you can run gcc from a cmd prompt (you can start
    `cmd` from the search bar and run the command `gcc`)

**MacOS**:

If you are using Homebrew, run this command:

```sh
brew install gcc
```

If you are using MacPorts, run this command:

```sh
sudo port install gcc
```

**Linux**: Follow the instructions for installing packages based on your distribution. [This article](https://www.ubuntupit.com/how-to-install-and-use-gcc-compiler-on-linux-system/) has a good list of installation steps for common Linux distribution.

## Harmony on VSCode

We have Harmony as an extension you can use on VSCode! By installing this extension, you are equipped with the Harmony compiler and the model checker out of the box without extra configurations. If you would like to use Harmony via this, then you are done!

Please see [here](#) for a quick guide on the basic usage of the VSCode extension.

## Command-Line Harmony Installation Guide

The other way of using Harmony is via the command line, e.g. PowerShell, Bash, ZSH, etc. There are two options for installing Harmony for the command line: 1) install via `pip` and 2) building Harmony directly from source.

### Install using pip

The Harmony CLI can be installed using the `pip` via the command below.

```sh
# install the latest version of Harmony.
pip install harmony-model-checker
```

When installing via pip, you may see a message on the terminal something like the following:

```sh

```

If so, add the path displayed in the message to the PATH variable.

### Install from Source

Download the source code from the [GitHub repository](https://www.github.com) via **Download as ZIP**.

On a command line, navigate to the directory using `cd`. Once there, run the command `make setup` to build Harmony.

After successfully building Harmony, run `pwd` to out the path name of the directory with Harmony. Edit your PATH variable to include this path.

## Checking for Updates on Harmony

### VSCode Extension

Updates are handled and notified by VSCode. When opening VSCode, you may receive a popup notification that an update for the extension is available.

### Command Line Harmony

Running `harmony --update` checks if an update is available.

Running `harmony --upgrade` upgrades Harmony to the latest version.
