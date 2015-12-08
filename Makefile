all: html

# Prerequisites needed to build
# =============================
RST2HTML = $(shell which rst2html || which rst2html.py || echo rst2html-NOT-FOUND)
${RST2HTML}:
	@echo "Get Docutils from http://docutils.sf.net"
	@false

hibidi.py:
	curl -O -L http://cben-hacks.sf.net/bidi/hibidi.py

html: huppa.html

huppa.html: huppa.rst my.css docutils.conf ${RST2HTML} hibidi.py
	${RST2HTML} huppa.rst | python ./hibidi.py > huppa.html

clean:
	-rm huppa.html
