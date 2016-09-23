source:
	mkdir -p bin
	scalac -d bin -cp "lib/*" `find src -name "*.scala"`

report:
	cd report; \
	pdflatex report.tex; \
	mv report.pdf ./..

clean:
	rm -rf bin/*

all: 	clean source
