.PHONY: build check test

build:
	edt build

check:
	edt check

test:
	python -m pytest
