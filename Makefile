all:
	(cd src/harmony; sh gen.scr) > harmony.py
	(cd src/charm; sh gen.scr) > charm.c
	gcc -g -std=c99 -DNDEBUG charm.c -m64 -o charm.exe -lpthread
	chmod +x harmony
