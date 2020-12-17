all:    harmony charm

harmony:    harmony.preamble harmony.py
	(cat harmony.preamble harmony.py; echo ++++++) > harmony

charm: charm.c json.c map.c global.c ops.c value.c queue.c hashdict.c hashdict.h global.h
	gcc -O3 charm.c json.c map.c global.c ops.c value.c queue.c hashdict.c -o charm
