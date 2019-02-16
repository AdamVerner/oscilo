FILENAME := Obhajoba2
CC := pdflatex -synctex=1 -interaction=nonstopmode
DEPS := beamerthemeBlacko.sty beamercolorthemeBlacko.sty

$(FILENAME).pdf : $(DEPS) $(FILENAME).tex 
	$(CC) $(FILENAME).tex

show: $(FILENAME).pdf
	xdg-open $(FILENAME).pdf

.PHONY: regen

regen:
	rm -f $(FILENAME).pdf
	make

.PHONY: clean

clean:
	rm -f *.aux *.log *.out *.pdf *.synctex.gz *.dvi *.toc *.run.xml  *.bcf *.blg *.bbl *.lot *.lof *.nav *.snm

