all:
	(cd src/harmony; sh gen.scr) > harmony.py
	(cat src/harmony/harmony.preamble harmony.py; echo ++++++) > harmony
	chmod +x harmony
	rm -f charm
