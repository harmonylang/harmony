all: dependencies gen parser
	rm -rf build/  # Remove previous build files
	python3 setup.py build_ext -i

parser:
	java -jar antlr-4.9.3-complete.jar -Dlanguage=Python3 -visitor Harmony.g4 -o harmony_model_checker/parser -no-listener

dependencies:
	pip install -r requirements.txt

gen:
	printf "\n__package__ = \"harmony_model_checker\"\n" > harmony_model_checker/__init__.py
	printf "__version__ = \"1.2.%d\"\n" `git log --pretty=format:'' | wc -l | sed 's/[ \t]//g'` >> harmony_model_checker/__init__.py
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

dist: gen parser
	rm -rf build/ dist/ harmony_model_checker.egg-info/
	python3 setup.py sdist

upload-test: dist
	twine upload -r testpypi dist/*

upload: dist
	twine upload dist/*

clean:
	rm -f code/*.htm code/*.hvm code/*.hco code/*.png code/*.hfa code/*.tla code/*.gv *.html
	(cd harmony_model_checker/modules; rm -f *.htm *.hvm *.hco *.png *.hfa *.tla *.gv *.html)
	rm -rf compiler_integration_results.md compiler_integration_results/
	rm -rf build/ dist/ harmony_model_checker.egg-info/
