.PHONY: all
all: clean build

.PHONY: all
build:
	mkdir -p build
	pdflatex --output-dir=build paper.tex
	pdflatex --output-dir=build paper.tex

.PHONY: clean
clean:
	rm -rf build