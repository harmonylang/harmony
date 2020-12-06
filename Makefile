all:	harmony

harmony:    harmony.preamble harmony.py
	(cat harmony.preamble harmony.py; echo ++++++) > harmony

jparse: jparse.c json.c map.c global.c ops.c value.c queue.c global.h
	gcc jparse.c json.c map.c global.c ops.c value.c queue.c -o jparse
