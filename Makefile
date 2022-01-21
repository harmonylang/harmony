all: parser
	python3 setup.py build_ext -i

setup: gen
	python3 setup.py install

parser: gen
	java -jar antlr-4.9.3-complete.jar -Dlanguage=Python3 -visitor Harmony.g4 -o harmony_model_checker/parser -no-listener

gen:
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

upload-test: dist
	twine upload -r testpypi dist/*

upload: dist
	twine upload dist/*

clean:
	rm -f code/*.htm code/*.hvm code/*.hco code/*.png code/*.hfa code/*.tla code/*.gv *.html
	rm -f harmony_model_checker/modules/*.htm harmony_model_checker/modules/*.hvm harmony_model_checker/modules/*.hco
	rm -rf compiler_integration_results/
