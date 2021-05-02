Harmony is a programming language designed for testing and experimenting with
concurrent code.

More information: https://harmony.cs.cornell.edu

Installing command-line harmony:
    - requires Python 3 and a 64-bit C compiler
    - to install, execute the following steps:
        1: run
                    python3 install.py
        2: add the current directory to the search path
    - to test harmony, run
                harmony --help

Some installation hints:
    Setting the search path under Linux and MacOSX:
        - see http://www.linux-migration.org/ch02s06.html
        - if you run harmony in the harmony directory, you may have to
          run "./harmony [args ...]" instead of just "harmony [args ...]"

    Installing 64-bit gcc under Windows:
        - follow instructions at http://mingw-w64.org/doku.php).
        - at the Settings window, make sure you select the x86-64
          architecture (instead of the default i686) during installation!
        - at the next window, make sure you copy the Destination folder;
          you'll need it later
        - after installation is complete, add the Destination folder
          you copied in the previous step extended with \mingw64\bin to
          your Path environment variable
          (search "Edit environment variables" in the search bar.  You
           can add it either to the Path associated with your account
           or the system Path)
        - make sure you can run gcc from a cmd prompt (you can start
          'cmd' from the search bar)

    Checking for upgrades and upgrading
        - run
            python3 install.py --version
          to see if you have the most up-to-date version
        - run
            python3 install.py --update
          to upgrade to the latest version
