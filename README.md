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
        - install gcc (http://mingw-w64.org/doku.php)
		- make sure you can run gcc from a command prompt by add
		  the mingw-w64/bin directory to the PATH environment variable
        - to run a harmony program, do the following:
            python3 harmony.py [args ...]
