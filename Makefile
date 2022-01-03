all: gen
	./harmony --build-model-checker

gen:
	java -jar antlr-4.9.3-complete.jar -Dlanguage=Python3 -visitor Harmony.g4 -o harmony_model_checker/parser -no-listener
	(cd src/harmony; sh gen.scr) > harmony_model_checker/harmony.py
	(cd src/charm; sh gen.scr) > harmony_model_checker/charm.c
	chmod +x harmony

behavior: x.hny
	./harmony -o x.hny
	: ./harmony -mqueue=queueconc code/qtestconc4.hny
	: ./harmony code/qtestconc4.hny
	: python3 behavior.py -Tdot -M x.hco
	open x.png

iface: iface.py iface.json
	./harmony -i 'countLabel(cs)' code/csonebit.hny
	: ./harmony -i 'countLabel(cs)' code/Peterson.hny
	: ./harmony -i '(flags,turn)' code/Peterson.hny
	: ./harmony -i rw code/RWtest.hny
	python3 iface.py iface.json > x.gv
	dot -Tpdf x.gv > x.pdf
	open x.pdf

dist: gen
	rm -rf dist/
	PACKAGE_DIR=harmony_model_checker
	rm -rf build/
	rm -rf harmony_model_checker.egg-info/
	python setup.py sdist

upload: dist
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*
