all:
	(cd src/harmony; sh gen.scr) > harmony.py
	(cd src/charm; sh gen.scr) > charm.c
	gcc -O3 -std=c99 -DNDEBUG charm.c -m64 -o charm.exe
	chmod +x harmony
