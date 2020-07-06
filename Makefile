all:	harmony

harmony:    harmony.preamble harmony.py
	(cat harmony.preamble harmony.py; echo ++++++) > harmony

