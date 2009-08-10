all: debug

PYJAMAS = ./pyjamas-trunk
PYJSFLAGS_DEBUG = --print-statements --strict --line-tracking --source-tracking --store-source --bound-methods
PYJSFLAGS_RELEASE = --no-print-statements --bound-methods
COPY_FILES = figures.png huppa.html ../hazmana.jpg ../hazmana2.jpg excanvas/excanvas.js

huppa.html: huppa.txt
	rst2html huppa.txt huppa.html

debug: huppa.html
	${PYJAMAS}/bin/pyjsbuild ${PYJSFLAGS_DEBUG} huppa
	cp ${COPY_FILES} output/

release: clean huppa.html
	${PYJAMAS}/bin/pyjsbuild ${PYJSFLAGS_RELEASE} huppa
	cp ${COPY_FILES} output/

upload:
	rsync --progress --compress --delete -r output/ cben@web.sf.net:public_html/huppoid      

clean:
	rm -rf huppa.html output
