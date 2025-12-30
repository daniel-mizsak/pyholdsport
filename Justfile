@_:
    just --list --unsorted

[group("lifecycle")]
clean:
    rm -rf \
        .DS_Store \
        .artifacts \
        .cache \
        .coverage \
        .mypy_cache \
        .nox \
        .pytest_cache \
        .ruff_cache \
        coverage.xml \
        htmlcov \
        .venv
    find . -type d -name "__pycache__" -exec rm -r {} +

[group("lifecycle")]
install:
    uv sync --all-groups

[group("lifecycle")]
upgrade:
    uv sync --upgrade

[group("lifecycle")]
fresh: clean install

[group("qa")]
lint:
    uv run ruff check
    uv run ruff format --diff

[group("qa")]
type:
    uv run mypy .

[group("qa")]
test *args:
    uv run pytest {{ args }}

[group("qa")]
test-all-python:
    uv run nox

[group("qa")]
coverage:
    uv run pytest \
        --cov=tests \
        --cov-fail-under=100 \
        --cov-report=term-missing

    uv run pytest \
        --cov=pyholdsport \
        --cov-report=term-missing \
        --cov-report=xml:.artifacts/coverage.xml \
        --cov-report=html:.artifacts/htmlcov

[group("qa")]
check-all: lint type test-all-python coverage

[group("build")]
build-documentation:
    uv run zensical build --clean --strict

[group("build")]
build-package:
    uv build --out-dir .artifacts/dist

[group("build")]
build-all: build-documentation build-package
