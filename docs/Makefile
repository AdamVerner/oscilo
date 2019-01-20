FILENAME := Main
CC := pdflatex -synctex=1 -interaction=nonstopmode

example-show: $(FILENAME).pdf
	xdg-open $(FILENAME).pdf

$(FILENAME).pdf : template/SPSTemplate.cls $(FILENAME).tex 
	$(CC) $(FILENAME).tex
	# biber $(FILENAME)
	$(CC) $(FILENAME).tex
	$(CC) $(FILENAME).tex

.PHONY: regen

regen:
	rm -f $(FILENAME).pdf
	make example-show

.PHONY: clean

clean:
	# idgaf delete everything
	rm -f *.aux *.log *.out *.pdf *.synctex.gz *.dvi *.toc *.run.xml  *.bcf *.blg *.bbl *.lot *.lof

