all:    mk_harmony mk_charm

mk_harmony:
	(cd src/harmony; sh gen.scr) > harmony.py
	(cat src/harmony/harmony.preamble harmony.py; echo ++++++) > harmony


mk_charm:
	(cd src/charm; sh gen.scr) > charm.c
	gcc -g -O3 -DNDEBUG -DHARMONY_COMBINE charm.c -o charm
