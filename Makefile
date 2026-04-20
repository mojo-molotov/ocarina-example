MAKEFLAGS += --silent

PY_CMD ?= python
VENV_BIN ?= .venv/bin
VENV_PYTHON ?= $(VENV_BIN)/python
VENV_PIP ?= $(VENV_BIN)/pip

.PHONY: all
all:
	$(error This Makefile is not for compilation)

.PHONY: ruff-check
ruff-check:
	ruff check .

.PHONY: mypy-check
mypy-check:
	mypy src/

.PHONY: install-on-ci
install-on-ci:
	@test -d .venv || $(PY_CMD) -m venv .venv
	$(VENV_PYTHON) -m pip install --upgrade pip
	$(VENV_PIP) install -e . --group dev

.PHONY: check-coding-style
check-coding-style: mypy-check ruff-check

.PHONY: create-venv
create-venv:
	$(PY_CMD) -m venv .venv

.PHONY: install
install:
ifeq ($(OS),Windows_NT)
	@if not exist .venv $(MAKE) create-venv
	.venv\Scripts\python.exe -m pip install --upgrade pip
	.venv\Scripts\pip.exe install -e . --group dev
	.venv\Scripts\pre-commit.exe install
else
	@test -d .venv || $(MAKE) create-venv
	.venv/bin/python -m pip install --upgrade pip
	.venv/bin/pip install -e . --group dev
	.venv/bin/pre-commit install
endif

.PHONY: ruff-format
ruff-format:
	ruff format .

.PHONY: clean
clean:
	@echo "Cleaning all artifacts..."
ifeq ($(OS),Windows_NT)
	if exist __pycache__ rmdir /s /q __pycache__
	if exist .mypy_cache rmdir /s /q .mypy_cache
	if exist .ruff_cache rmdir /s /q .ruff_cache
	for /d /r . %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d"
	for /d /r . %%d in (*.egg-info) do @if exist "%%d" rmdir /s /q "%%d"
	if exist .venv rmdir /s /q .venv
else
	rm -rf .venv __pycache__ .mypy_cache .ruff_cache *.egg-info
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
endif
