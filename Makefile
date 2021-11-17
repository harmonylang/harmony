all:
	(cd src/harmony; sh gen.scr) > harmony.py
	(cd src/charm; sh gen.scr) > charm.c
	gcc -O3 -std=c99 -DNDEBUG charm.c -m64 -o charm.exe -lpthread
	chmod +x harmony

iface: iface.py iface.json
	: ./harmony -i 'flags' code/csonebit.hny
	./harmony -i '(flags,turn)' code/Peterson.hny
	python3 iface.py iface.json > x.gv
	dot -Tpdf x.gv > x.pdf
	open x.pdf
    
