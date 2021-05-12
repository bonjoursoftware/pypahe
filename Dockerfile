ARG PYTHON_VERSION=3.9.4
FROM python:${PYTHON_VERSION}-slim-buster as builder
WORKDIR /pypahe
RUN pip install --no-cache-dir pipenv==2020.11.15
COPY ./Pipfile.lock ./
RUN PIPENV_VENV_IN_PROJECT=1 pipenv sync

FROM python:${PYTHON_VERSION}-slim-buster
RUN useradd --create-home pypahe
WORKDIR /home/pypahe
USER pypahe
COPY --from=builder /pypahe/.venv/ /home/pypahe/.local/
COPY ./pypahe ./pypahe
COPY ./pypahe.py ./pypahe.py
ENTRYPOINT ["./pypahe.py"]
