SHELL := /bin/bash
PY_VERSION := 2.7

export PYTHONUNBUFFERED := 1

BASE := $(shell /bin/pwd)
VENV_DIR := $(BASE)/.venv
LIB_DIR := $(BASE)/lib
export PATH := var:$(PATH):$(VENV_DIR)/bin

PYTHON := $(shell /usr/bin/which python$(PY_VERSION))
VIRTUALENV := $(PYTHON) -m virtualenv
ZIP_FILE := $(BASE)/hashlambda.zip

.DEFAULT_GOAL := build
.PHONY: build clean bundle test


build:
	$(VIRTUALENV) "$(VENV_DIR)"
	"$(VENV_DIR)/bin/pip$(PY_VERSION)" \
		--isolated \
		--disable-pip-version-check \
		install -Ur requirements.txt
		
bundle:
	zip -r -9 "$(ZIP_FILE)" *.py
	cd "$(VENV_DIR)/lib/python$(PY_VERSION)/site-packages" \
		&& zip -r9 "$(ZIP_FILE)" .

clean:
	rm -rf "$(VENV_DIR)" "$(BASE)/var" "$(BASE)/__pycache__" "$(ZIP_FILE)"
