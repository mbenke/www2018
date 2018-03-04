MATHJAXURL='http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML'
MATH=--mathjax #=$(MATHJAXURL)
#MATH=--mathml
#PDOPTS=$(MATH) #--self-contained
PDOPTS=
#PANDOC=~/.cabal/bin/pandoc $(PDOPTS)
PANDOC=pandoc $(PDOPTS)
DESTDIR=.

%-slides.html: %.md Makefile $(wildcard ./pandoc/slidy/*)
	@test -f $<
	$(PANDOC) -s -t slidy -o $(DESTDIR)/$@ $<

all: lab1-slides.html lab2css-slides.html #dom-slides.html jquery-slides.html
