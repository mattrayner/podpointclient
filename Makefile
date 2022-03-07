.PHONY: clean package publish

clean:
	rm -r dist/*

package:
	python setup.py sdist

publish: clean package
	twine upload dist/* --verbose