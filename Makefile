DOCKER_RUN = docker run  --interactive --rm bonjoursoftware/pypahe:local

.PHONY: all
all: fmt-check test static-analysis

.PHONY: docker-build
docker-build:
	@docker build -t bonjoursoftware/pypahe:local . > /dev/null

.PHONY: fmt-check
fmt-check: docker-build
	@$(DOCKER_RUN) black --line-length 120 --check .

.PHONY: test
test: docker-build
	@$(DOCKER_RUN) pytest \
		-v \
		-p no:cacheprovider \
		--no-header \
		--cov=pypahe \
		--cov-fail-under=100 \
		--no-cov-on-fail

.PHONY: static-analysis
static-analysis: flake8 mypy

.PHONY: flake8
flake8: docker-build
	@$(DOCKER_RUN) flake8 --max-line-length 120

.PHONY: mypy
mypy: docker-build
	@$(DOCKER_RUN) mypy --strict ./**/*.py

.PHONY: fmt
fmt:
	@pipenv run black --line-length 120 .
