all:
	(cd src/harmony; sh gen.scr) > harmony.py
	(cd src/charm; sh gen.scr) > charm.c
	gcc -g -std=c99 charm.c -m64 -o charm.exe -lpthread
	chmod +x harmony

behavior: behavior.py charm.dump
	: ./harmony y.hny
	: ./harmony -mqueue=queueconc code/qtestconc4.hny
	: ./harmony code/qtestconc4.hny
	python3 behavior.py -Tdot -M charm.dump > x.gv
	dot -Tpdf x.gv > x.pdf
	open x.pdf

iface: iface.py iface.json
	./harmony -i 'countLabel(cs)' code/csonebit.hny
	: ./harmony -i 'countLabel(cs)' code/Peterson.hny
	: ./harmony -i '(flags,turn)' code/Peterson.hny
	: ./harmony -i rw code/RWtest.hny
	python3 iface.py iface.json > x.gv
	dot -Tpdf x.gv > x.pdf
	open x.pdf
