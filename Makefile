all: build

build:
	rm -rf output
	pyjamas-trunk/bin/pyjsbuild --strict huppa
	cp figures.png output/
