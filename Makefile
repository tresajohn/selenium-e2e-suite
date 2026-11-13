.PHONY: install test test-headless report clean

install:
	pip install -e ".[dev]"

test:
	mkdir -p reports
	behave features/ -f behave_html_formatter:HTMLFormatter -o reports/report.html
	$(MAKE) _fix-report-colors

test-headless:
	mkdir -p reports
	HEADLESS=true behave features/ -f behave_html_formatter:HTMLFormatter -o reports/report.html
	$(MAKE) _fix-report-colors

_fix-report-colors:
	python3 -c "\
	import re, pathlib; \
	p = pathlib.Path('reports/report.html'); \
	t = p.read_text(); \
	t = t.replace('#65c400', '#4a8e56').replace('#dbffb4', '#ddeee2').replace('#3d7700', '#2e6338'); \
	p.write_text(t)"

report:
	open reports/report.html

clean:
	rm -rf reports/ logs/screenshots/*.png
