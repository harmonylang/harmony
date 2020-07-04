all:	cxl

cxl:    cxl.preamble cxl.py
	(cat cxl.preamble cxl.py; echo ++++++) > cxl

