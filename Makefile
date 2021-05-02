all:
	(cd src/harmony; sh gen.scr) > harmony.py
	(cd src/charm; sh gen.scr) > charm.c
	chmod +x harmony
	rm -f charm.exe
