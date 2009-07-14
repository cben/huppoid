all: build

build:
	pyjamas-trunk/bin/pyjsbuild --strict huppa
	cp figures.png output/

clean:
	rm -rf output

