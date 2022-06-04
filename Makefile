.PHONY: spec test lint clean package publish

test: spec

spec:
	python3 -m pytest \
		-vv \
		-qq \
		--timeout=9 \
		--durations=10 \
		--cov podpointclient \
		--cov-report term \
		--cov-report html \
		-o console_output_style=count \
		-p no:sugar \
		tests

lint:
	pylint ./podpointclient

clean:
	rm -r dist/*

package:
	python3 setup.py sdist

publish: clean package
	twine upload dist/* --verbose