PHONY: package publish

package:
	python setup.py sdist

publish: package
	twine upload dist/* --verbose