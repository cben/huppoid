all: debug

# Prerequisites needed to build
# =============================
pyjamas-trunk:
	svn co https://pyjamas.svn.sourceforge.net/svnroot/pyjamas/trunk pyjamas-trunk

export PYTHONPATH = ${HOME}/Working/docutils/docutils
RST2HTML = ~/Working/docutils/docutils/tools/rst2html.py
#RST2HTML = $(shell which rst2html || echo rst2html-NOT-FOUND)
${RST2HTML}:
	@echo "Get Docutils from http://docutils.sf.net"
	@false

hibidi.py:
	curl -O http://cben-hacks.sf.net/bidi/hibidi.py

# Config
# ======
PYJAMAS = ./pyjamas-trunk
PYJSFLAGS_DEBUG = --print-statements --strict --line-tracking --source-tracking --store-source
# -O worked for some time, now doesn't ("Script error. at line number 0. Please inform webmaster").
PYJSFLAGS_RELEASE = --no-print-statements
COPY_FILES = figures.png huppa.html ../hazmana.jpg ../hazmana2.jpg excanvas/excanvas.js

html: huppa.html

huppa.html: huppa.txt ru-he.css docutils.conf ${RST2HTML} hibidi.py
	${RST2HTML} huppa.txt | python ./hibidi.py > huppa.html
	-cp huppa.html output/

debug: html ${PYJAMAS}
	${PYJAMAS}/bin/pyjsbuild ${PYJSFLAGS_DEBUG} huppa
	cp ${COPY_FILES} output/

release: clean html ${PYJAMAS}
	${PYJAMAS}/bin/pyjsbuild ${PYJSFLAGS_RELEASE} huppa
	cp ${COPY_FILES} output/

upload:
	rsync --progress --compress --delete -r output/ cben@web.sf.net:public_html/huppoid

clean:
	rm -rf huppa.html output
