Harmony is a programming language for testing and experimenting with
concurrent code.

Website: harmony.www.cs.cornell.edu

Running harmony:

    Linux and MacOSX:
        - put harmony in your search path ($PATH)
            - see http://www.linux-migration.org/ch02s06.html
        - if you run harmony in the harmony directory, you may have to
          run "./harmony [args ...]" instead of just "harmony [args ...]"

    Windows:
        - install gcc (http://mingw-w64.org/doku.php).
        - at the Settings window, make sure you select the x86-64
          architecture (instead of the default i686) during installation!
        - at the next window, make sure you copy the Destination folder
        - after installation is complete, add the Destination folder
          plus \mingw\bin to your Path environment variable
		- make sure you can run gcc from a command prompt
        - to run a harmony program, do the following:
            python3 harmony.py [args ...]
