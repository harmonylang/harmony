all:    harmony charm

harmony:    harmony.preamble harmony.py
	(cat harmony.preamble harmony.py; echo ++++++) > harmony

charm: charm.c json.c map.c global.c ops.c value.c queue.c global.h
	gcc -g charm.c json.c map.c global.c ops.c value.c queue.c -o charm
