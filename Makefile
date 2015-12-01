all: html copy

# Prerequisites needed to build
# =============================
RST2HTML = $(shell which rst2html || echo rst2html-NOT-FOUND)
${RST2HTML}:
	@echo "Get Docutils from http://docutils.sf.net"
	@false

hibidi.py:
	curl -O -L http://cben-hacks.sf.net/bidi/hibidi.py

html: output/huppa.html

output/:
	mkdir output

COPY_FILES = huppa.py figures.png hazmana.jpg hazmana2.jpg

copy: output/
	cp ${COPY_FILES} output/

output/huppa.html: output/ huppa.txt ru-he.css docutils.conf ${RST2HTML} hibidi.py
	${RST2HTML} huppa.txt | python ./hibidi.py > output/huppa.html

upload:
	rsync --progress --compress --delete -r output/ cben@web.sf.net:public_html/huppoid

clean:
	rm -rf output/
