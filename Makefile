PYTHON_VERSION = $(shell head -1 .python-version)

DEV_TAG = bonjoursoftware/pypahe:dev
LATEST_TAG = bonjoursoftware/pypahe:latest

SRC_DIR = pypahe

PIPENV_RUN = docker run --interactive --rm $(DEV_TAG)

.PHONY: all
all: fmt-check test static-analysis md-check package

.PHONY: docker-build
docker-build:
	@docker build \
		--build-arg PYTHON_VERSION=$(PYTHON_VERSION) \
		--tag $(DEV_TAG) \
		--file dev.Dockerfile \
		. > /dev/null

.PHONY: fmt-check
fmt-check: docker-build
	@$(PIPENV_RUN) black --line-length 120 --check .

.PHONY: test
test: docker-build
	@$(PIPENV_RUN) pytest \
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
	@$(PIPENV_RUN) flake8 --max-line-length 120

.PHONY: mypy
mypy: docker-build
	@$(PIPENV_RUN) mypy --strict ./**/*.py

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
