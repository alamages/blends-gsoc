## ----------------------------------------------------------------------
## Makefile : makefile for docbook-xml
## ----------------------------------------------------------------------

## ----------------------------------------------------------------------
## Document definitions
doc_lang	:= en
doc_name	:= debian-blends
doc_xml	:= $(shell for l in $(doc_lang); do echo $(doc_name).$$l.xml; done)
sources := $(shell find . -name "*.xml")
doc_pdf	:= $(shell for l in $(doc_lang); do echo $$l/pdf/$(doc_name).$$l.pdf; done)
doc_ps	:= $(shell for l in $(doc_lang); do echo $$l/ps/$(doc_name).$$l.ps; done)
doc_dvi	:= $(shell for l in $(doc_lang); do echo $$l/dvi/$(doc_name).$$l.dvi; done)

doc_txt	:= $(shell for l in $(doc_lang); do echo $$l/txt/$(doc_name).$$l.txt; done)
#this needed cause xmlto txt does not include section numbering by default
doc_txt_params := --stringparam section.autolabel=1 --stringparam section.label.includes.component.label=1

doc_html := $(shell for l in $(doc_lang); do echo $$l/html/index.html; done)
pkg             := blends-doc

## ----------------------------------------------------------------------
## General definitions
LN		:= /bin/ln -sf
RMR		:= /bin/rm -fr
LOCALE          := unset LC_ALL; unset LANG; unset LANGUAGE; 

## ----------------------------------------------------------------------
# this can and will be overriden by a higher level makefile
PUBLISHDIR := alioth.debian.org:/srv/alioth.debian.org/chroot/home/groups/blends/htdocs/blends

# There is no difference between letter and a4, but a2 for instance works
PAPERSIZE  := a4

## ----------------------------------------------------------------------
## Targets
all:		html

validate: $(doc_xml)
	for f in $(doc_xml); do \
	  xmllint --valid --noout $$f; \
	done

html: $(doc_html)

$(doc_html): $(doc_xml) $(sources)
	for l in $(doc_lang); do \
	  f=$(doc_name).$$l.xml; d=$$l/html; \
	  mkdir -p $$d; \
	  $(LOCALE) xmlto -o $$d -x $(doc_name).xsl html $$f; \
	done

txt $(doc_txt): $(doc_xml)
	for l in $(doc_lang); do \
	  f=$(doc_name).$$l.xml; d=$$l/txt; \
	  mkdir -p $$d; \
	  $(LOCALE) xmlto $(doc_txt_params) -o $$d txt $$f; \
	done

ps $(doc_ps): 	$(doc_xml)
	for l in $(doc_lang); do \
	  f=$(doc_name).$$l.xml; d=$$l/ps; \
	  mkdir -p $$d; \
	  $(LOCALE) xmlto -o $$d --with-dblatex ps $$f; \
	done


pdf $(doc_pdf): $(doc_xml)
	for l in $(doc_lang); do \
	  f=$(doc_name).$$l.xml; d=$$l/pdf; \
	  mkdir -p $$d; \
	  $(LOCALE) xmlto -o $$d --with-dblatex pdf $$f; \
	done


dvi $(doc_dvi): $(doc_xml)
	for l in $(doc_lang); do \
	  f=$(doc_name).$$l.xml; d=$$l/dvi; \
	  mkdir -p $$d; \
	  $(LOCALE) xmlto -o $$d --with-dblatex dvi $$f; \
	done


#publish: 	html pdf
#		rsync -azult --delete $(doc_html)/* $(PUBLISHDIR)
#		[ -s debian-blends.en.pdf ] && rsync -azult $(doc_pdf) $(PUBLISHDIR)

clean:
	for l in $(doc_lang); do \
	  for d in html pdf txt ps dvi info; do \
	    $(RMR) $$l/$$d; \
	  done; \
	done
	find . -name "*~" -exec $(RMR) {} \;

distclean:
		make clean

.PHONY: all publish clean distclean validate
