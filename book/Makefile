paper.pdf: pp.tex
	pdflatex pp
	mv pp.pdf paper.pdf

pp.tex: paper.tex preproc.py
	python3 preproc.py paper.tex > pp.tex

all: paper.tex preproc.py
	python3 preproc.py paper.tex > pp.tex
	pdflatex pp
	bibtex pp
	makeindex pp
	makeglossaries pp
	pdflatex pp
	pdflatex pp
	mv pp.pdf paper.pdf
