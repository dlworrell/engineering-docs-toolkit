.PHONY: build check test edt-build edt-check edt-clean

EDT_SMOKE_DIR ?= .edt-smoke

build:
	edt build

check:
	edt check

test:
	python -m pytest

edt-clean:
	rm -rf $(EDT_SMOKE_DIR)

edt-build: edt-clean
	mkdir -p $(EDT_SMOKE_DIR)
	cd $(EDT_SMOKE_DIR) && python -m edt.cli init
	cd $(EDT_SMOKE_DIR) && python -m edt.cli import
	cd $(EDT_SMOKE_DIR) && python -m edt.cli build

edt-check: edt-build
	cd $(EDT_SMOKE_DIR) && python -m edt.cli check
