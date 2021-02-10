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
        - to run a harmony program from the cmd window, first change
          to the harmony-1.0 folder and then run:
                python3 harmony.py [args ...]
