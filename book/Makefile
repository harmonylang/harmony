paper.pdf: pp.tex
	pdflatex pp
	mv pp.pdf paper.pdf

pp.tex: paper.tex sources/preproc.py
	python3 sources/preproc.py paper.tex > pp.tex

all: paper.tex sources/preproc.py
	python3 sources/preproc.py paper.tex > pp.tex
	pdflatex pp
	bibtex pp
	makeindex pp
	makeglossaries pp
	pdflatex pp
	pdflatex pp
	mv pp.pdf paper.pdf
