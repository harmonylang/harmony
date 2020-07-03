paper.pdf: paper.tex
	pdflatex paper

all:
	(cd sources; make)
	pdflatex paper
	bibtex paper
	makeindex paper
	makeglossaries paper
	pdflatex paper
	pdflatex paper
