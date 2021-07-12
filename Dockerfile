ARG PYTHON_VERSION=3.9.6
FROM python:${PYTHON_VERSION}-slim-buster as builder
WORKDIR /pypahe
RUN pip install --no-cache-dir poetry==1.1.7
COPY ./pyproject.toml ./poetry.lock ./
RUN poetry config virtualenvs.in-project true --local \
    && poetry install --no-dev \
    && poetry cache clear pypi --all --no-interaction

FROM python:${PYTHON_VERSION}-slim-buster
RUN useradd --create-home pypahe
WORKDIR /home/pypahe
USER pypahe
COPY --from=builder /pypahe/.venv/ /home/pypahe/.local/
COPY ./pypahe ./pypahe
COPY ./pypahe.py ./pypahe.py
ENTRYPOINT ["./pypahe.py"]
