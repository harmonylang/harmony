# Harmony

Harmony is a programming language designed for testing and experimenting with concurrent code.

- [Harmony](#harmony)
  - [Preliminary Requirements](#preliminary-requirements)
    - [Installing Python3](#installing-python3)
    - [Installing GCC](#installing-gcc)
  - [Harmony on VSCode](#harmony-on-vscode)
  - [Command-Line Harmony Installation Guide](#command-line-harmony-installation-guide)
    - [Install using pip](#install-using-pip)
    - [Install from Source](#install-from-source)
  - [Checking for Updates on Harmony](#checking-for-updates-on-harmony)
    - [VSCode Extension](#vscode-extension)
    - [Command Line Harmony](#command-line-harmony)
  - [Modifying your PATH variable](#modifying-your-path-variable)

For more information, please visit the official page https://harmony.cs.cornell.edu

## Preliminary Requirements

1. Python (version 3.6 or higher)
2. GCC compiler

### Installing Python3

If you do not have Python3 already installed, download and install Python depending on your OS (Windows, Mac, Linux, etc) on the official [Python site](https://www.python.org/downloads/). Be sure to install version `3.6` or higher.

For WSL(2) users, you can run the following command instead:
```sh
sudo apt update
sudo apt install python3
```

On the command line, you can check if Python has been successfully installed by running `python3 --version`.

### Installing GCC

`gcc` is a compiler for the C programming language and is needed for the model checker component of Harmony. Here are the steps to installing `gcc` depending on your OS.

**Windows**:

Installing **64-bit** `gcc` under Windows:
  - Follow the instructions at https://www.mingw-w64.org/downloads/#mingw-builds to download the `mingw-w64` installer. Run the installer once it is downloaded.
  - At the Settings window, make sure you **select the x86-64
    architecture** (instead of the default i686) during installation!
  - At the next window, make sure you copy name of the Destination folder; you'll need it later.
  - After installation is complete, add the name of the Destination folder you copied in the previous step extended with `\mingw64\bin` to your `Path` environment variable
    (search for **Edit environment variables** in the search bar. You can add it either to the `Path` associated with your account or the system `Path`).
  - Make sure you can run gcc from a cmd prompt (you can start
    `cmd` from the search bar and run the command `gcc`)

**MacOS**:

You will need to install a package manager to use `gcc`, either [Homebrew](https://brew.sh/) or [MacPorts](https://www.macports.org/install.php). You can check if you have one or the other by running `brew` (for Homebrew) and `port` (for MacPorts). Otherwise, install one of the two package managers. Be sure **not to install both** as they don't behave well together.

Open the Terminal application.

If you are using Homebrew, run the following commands:

```sh
brew update
brew install gcc
```

If you are using MacPorts, run this command:

```sh
sudo port install gcc
```

**Linux**:

Follow the instructions for installing packages based on your distribution. [This article](https://www.ubuntupit.com/how-to-install-and-use-gcc-compiler-on-linux-system/) has a good list of installation steps for common Linux distribution.

## Harmony on VSCode

We have Harmony as an extension you can use on VSCode! By installing this extension, you are equipped with the Harmony compiler and the model checker out of the box without extra configurations. If you would like to use Harmony via this, then you are done!

Please see [here](#) for a quick guide on the basic usage of the VSCode extension.

## Command-Line Harmony Installation Guide

The other way of using Harmony is via the command line, e.g. PowerShell, Bash, ZSH, etc. There are two options for installing Harmony for the command line: 1) install via `pip` and 2) building Harmony directly from source.

- [Install using pip](#install-using-pip)
- [Install from Source](#install-from-source)

### Install using pip

The Harmony CLI can be installed using the `pip` via the command below.

```sh
# install the latest version of Harmony.
pip install harmony-model-checker
```
---

When installing via pip, you may see a message on the terminal something like the following:

```sh
WARNING: The script harmony is installed in '/path/with/harmony/' which is not on PATH.
  Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
```
If you do, add that path displayed in the message to your `PATH` variable. Otherwise, you continue.

---

Run the following command, and you are ready.

```sh
harmony --build-model-checker
```

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


## Modifying your PATH variable

**Windows**:

Search for **Edit environment variables** in the search bar. You can add it either to the `Path` associated with your account or the system `Path`.

![A pane with sections](doc-images/first-pane.png "First pane").

Select the variable `Path` in the user variables section and then click "Edit", which opens a new pane.

![A pane with sections](doc-images/hover-new.png "First pane").

Click "New" to add a new path, for example, the path to `gcc`.

![A pane with sections](doc-images/adding-new-path.png "First pane").


**MacOS / Linux**:

Open the Terminal application. Check which shell is running on the Terminal. You check which one you have by running `echo "$SHELL"`.

The following instructions are for `bash` and `zsh`, where `/path/to/add` is to be substituted:

```sh
# for bash
echo "export PATH=$PATH:/path/to/add" >> ~/.bash_profile

# for zsh
echo "export PATH=$PATH:/path/to/add" >> ~/.zsh_profile
```
