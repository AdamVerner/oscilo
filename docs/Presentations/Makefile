FILENAME := Obhajoba3
CC := pdflatex -synctex=1 -interaction=nonstopmode
DEPS := beamerthemeBlacko.sty beamercolorthemeBlacko.sty

example-show: $(FILENAME).pdf
	xdg-open $(FILENAME).pdf

$(FILENAME).pdf : $(DEPS) $(FILENAME).tex 
	$(CC) $(FILENAME).tex

.PHONY: regen

regen:
	rm -f $(FILENAME).pdf
	make example-show

.PHONY: clean

clean:
	rm -f *.aux *.log *.out *.pdf *.synctex.gz *.dvi *.toc *.run.xml  *.bcf *.blg *.bbl *.lot *.lof *.nav *.snm

