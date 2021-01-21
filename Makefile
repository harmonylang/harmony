all:    harmony charm

harmony:
	(cd src/harmony; sh gen.scr) > harmony.py
	(cat src/harmony/harmony.preamble harmony.py; echo ++++++) > harmony


charm:
	(cd src/charm; sh gen.scr) > charm.c
	gcc -g charm.c -o charm
