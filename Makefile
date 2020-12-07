all:	harmony

harmony:    harmony.preamble harmony.py
	(cat harmony.preamble harmony.py; echo ++++++) > harmony

charmony: charmony.c json.c map.c global.c ops.c value.c queue.c global.h
	gcc charmony.c json.c map.c global.c ops.c value.c queue.c -o charmony
