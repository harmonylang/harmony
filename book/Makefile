paper.pdf: paper.tex
	pdflatex paper

all:
	pdflatex paper
	bibtex paper
	makeindex paper
	makeglossaries paper
	pdflatex paper
	pdflatex paper
