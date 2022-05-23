.PHONY: clean package publish

test:
	python3 -m pytest \
		-vv \
		-qq \
		--timeout=9 \
		--durations=10 \
		--cov custom_components.pod_point \
		--cov-report term \
		--cov-report html \
		-o console_output_style=count \
		-p no:sugar \
		tests

clean:
	rm -r dist/*

package:
	python3 setup.py sdist

publish: clean package
	twine upload dist/* --verbose