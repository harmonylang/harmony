# Harmony

Harmony is a programming language designed for testing and experimenting with concurrent code.

- [Harmony](#harmony)
  - [Installing Python3](#installing-python3)
  - [Installing Graphviz](#installing-graphviz)
  - [Install Harmony via Pip](#install-harmony-via-pip)
    - [For Windows Users](#for-windows-users)
    - [For CS Deparment Linux Machine Users](#for-cs-deparment-linux-machine-users)
  - [Adding Scripts to PATH](#adding-scripts-to-path)
  - [Command-Line Harmony](#command-line-harmony)
  - [Harmony on VSCode](#harmony-on-vscode)
  - [Updating Harmony](#updating-harmony)
  - [Troubleshooting](#troubleshooting)
    - [Modifying your PATH variable](#modifying-your-path-variable)

For more information, please visit the official page https://harmony.cs.cornell.edu.

Harmony requires the following to be installed:

1. Python (version 3.6 or higher)
2. Graphviz
3. C Compiler (potentially potential)

In the following instructions, Windows users using WSL should follows instructions for Linux.

For users of a Cornell CS Department Linux machine, e.g. `<netid>@ugclinux.cs.cornell.edu`, you likely do not need to install `Python3` or `Graphviz` because they may be available already. However, you can verify that they are available by running `python3 --version` and `dot -V` respectively.

## Installing Python3

Harmony requires Python (version 3.6 or higher) to be installed. If you do not have Python3 already installed, download and install Python depending on your OS (Windows, Mac, Linux, etc) on the official [Python site](https://www.python.org/downloads/). Be sure to download the installer for Python version `3.6` or higher.

In the installer, the default installation settings will also add `pip`. If you choose to run the installer with custom settings, be sure that `pip` gets installed.

On the command line, you can check if Python has been successfully installed by running the following:

```sh
python --version

## If python does not work or if python gives version 2.X
python3 --version
```

## Installing Graphviz

Harmony uses [Graphviz](https://graphviz.org/) to visualize the state changes in a program. For example, the following Harmony program can produce the subsequent graph.

```py
# Filename: example.hny
def a():
    print "A"

def b():
    print "B"

spawn a()
spwan b()

# Run with [harmony -o example.png example.hny]
```

![Dot output using example.hny](https://harmony.cs.cornell.edu/docs/textbook/figures/simple-graph-example.png "Dot output")

Instructions for installing the latest version of Graphviz can be found [here](https://graphviz.org/download/).

For **Windows** users, when running the installer, make sure to select the option **Add Graphviz to the system PATH for current user** so that the command `dot` is available to produce the graphs.

## Install Harmony via Pip

After installing `python`, you should also be able to use the command `pip`. Run the following command to get the latest version of Harmony:

```sh
pip install --user harmony

## If pip fails try pip3
pip3 install --user harmony
```

### For Windows Users

For **Windows** users: you may encounter the error message along the lines of the following when installing `harmony`:

```sh
error: Microsoft Visual C++ 14.0 or greater is required. Get it with
"Microsoft C++ Build Tools": <link to visual studio - cpp build tools>
```

This is to be expected if you had not installed the "Microsoft C++ Build Tools" before. Navigate to the outputted link and press `Download Build Tools` to download the installer. When you run the installer, you will encounter a selection screen such as the following:

![Workload installation selection screen](https://harmony.cs.cornell.edu/docs/textbook/figures/find-c%2B%2B-build-tools.png "Worload installation selection screen")

Select `Desktop development with C++` in the `Desktop & Mobile` section and then install.

![Select the workload and install](https://harmony.cs.cornell.edu/docs/textbook/figures/press-install-c%2B%2B-build-tools.png "Select the workload and install")

Note that this will likely take a while. When it finishes installing, run `pip install harmony` again.


### For CS Deparment Linux Machine Users

It may be possible that `pip` is not available on your Linux machine. In that case, you will need to download and build the source code directly.

Go to [https://pypi.org/project/harmony/#files](https://pypi.org/project/harmony/#files). There, you should find a `harmony-1.2.x.tar.gz` for the latest version of Harmony. Download the file onto your local machine and then send it to the Linux machine via `scp`.

Alternatively, you can download the file directly from the Linux machine via `wget`. Right click on the download link to the file and copy the link address. Then on the Linux machine, run the following:

```sh
wget <link copied from pypi.org>
```

Once you have the `tar.gz` file on your Linux machine, run the following commands:

```sh
# Change the version number accordingly if necessary
gzip -d harmony-1.2.2767.tar.gz
tar -xf harmony-1.2.2767.tar
cd harmony-1.2.2767
python3 setup.py install --user
```

You can find the latest releases [here](https://pypi.org/project/harmony/#files).


Afterward, you will likely need to add the directory with the `harmony` command to your environment `PATH`. You can get the directory with the script by running `python3 -m site --user-base`, which will output something like `/home/<net-id>/.local`. Add this directory to your `PATH` (See [here](#modifying-your-path-variable) for more information on how to do so).

## Adding Scripts to PATH

When installing Harmony, you may encounter a warning on the command line of something like the following:

```sh
WARNING: The script harmony is installed in '/path/with/harmony/' which is not on PATH.
  Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
```

If you do not see this warning, then you can continue.

Otherwise, add that path displayed in the message to your `PATH` variable. See [here](#modifying-your-path-variable) for extra information on editing the `PATH` variable.

## Command-Line Harmony

Once you have installed `harmony`, you should be able to use the `harmony` command on your command line.

You check which version you have by running `harmony --version`.

## Harmony on VSCode

Harmony is available as an extension on VSCode, which includes syntax highlighting and basic parser checks.

Please see [here](https://marketplace.visualstudio.com/items?itemName=kevinsun-dev-cornell.harmonylang) for a guide on the basic usage of the VSCode extension.

## Updating Harmony

Harmony can be updated by running the following `pip` command on the command line:

```sh
pip install --upgrade harmony
```

In Harmony versions `1.2.0` and higher, the compiler will output a warning if the currently installed version of Harmony is outdated and an updated one can be installed.

## Troubleshooting

The following section provides some guide for how to resolve common issues.

### Modifying your PATH variable

**Windows**:

Search for **Edit environment variables** in the search bar. You can add it either to the `Path` associated with your account or the system `Path`.

![A pane with sections](https://harmony.cs.cornell.edu/docs/textbook/figures/first-pane.png "First pane")

Select the variable `Path` in the user variables section and then click "Edit", which opens a new pane.

![Hover over the new button](https://harmony.cs.cornell.edu/docs/textbook/figures/hover-new.png "Hovering over the new button")

Click "New" to add a new path, for example, the directory containing `gcc` or the `pip` scripts.

![Add new path](https://harmony.cs.cornell.edu/docs/textbook/figures/adding-new-path.png "Adding new path")

Complete your changes by pressing "Ok".

You will have to restart your command line (and VSCode if you are using the extension) to have the changes take effect.

**MacOS / Linux**:

Open the Terminal application. Check which shell is running on the Terminal. You check which one you have by running `echo "$SHELL"`.

The following instructions are for `bash` and `zsh`. Open the `~/.bash_profile` file (for bash users) or the `~/.zsh_profile` file (for zsh users) using your favorite text editor, such as `vim`, `nano`, `emacs`, or `TextEdit`. Then, add the following command to the end of the file, where `/path/to/add` is to be substituted:

```sh
export PATH=$PATH:/path/to/add/
```

Save the file.

You will have to restart Terminal (and VSCode if you are using the extension) to have the changes take effect.
