PYTHON_VERSION = $(shell head -1 .python-version)

DEV_TAG = bonjoursoftware/pypahe:dev
LATEST_TAG = bonjoursoftware/pypahe:latest

SRC_DIR = pypahe

POETRY_RUN = docker run --interactive --rm $(DEV_TAG)

.PHONY: all
all: fmt-check test static-analysis md-check package

.PHONY: docker-build
docker-build:
	@curl -sL https://github.com/bonjoursoftware/python-dockerfiles/raw/main/poetry.Dockerfile | docker build \
		--build-arg PYTHON_VERSION=$(PYTHON_VERSION) \
		--tag $(DEV_TAG) \
		-f- . > /dev/null

.PHONY: fmt-check
fmt-check: docker-build
	@$(POETRY_RUN) black --line-length 120 --check .

.PHONY: test
test: docker-build
	@$(POETRY_RUN) pytest \
		-v \
		-p no:cacheprovider \
		--no-header \
		--cov=$(SRC_DIR) \
		--cov-fail-under=100 \
		--no-cov-on-fail

.PHONY: static-analysis
static-analysis: flake8 mypy

.PHONY: flake8
flake8: docker-build
	@$(POETRY_RUN) flake8 --max-line-length 120

.PHONY: mypy
mypy: docker-build
	@$(POETRY_RUN) mypy --strict ./**/*.py

.PHONY: fmt
fmt:
	@pipenv run black --line-length 120 .

.PHONY: md-check
md-check:
	@docker pull zemanlx/remark-lint:0.2.0 >/dev/null
	@docker run --rm -i -v $(PWD):/lint/input:ro zemanlx/remark-lint:0.2.0 --frail .

.PHONY: package
package:
	@docker build \
		--build-arg PYTHON_VERSION=$(PYTHON_VERSION) \
		--tag $(LATEST_TAG) \
		. > /dev/null
