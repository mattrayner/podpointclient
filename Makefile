.PHONY: clean package publish

test:
	pytest

clean:
	rm -r dist/*

package:
	python3 setup.py sdist

publish: clean package
	twine upload dist/* --verbose