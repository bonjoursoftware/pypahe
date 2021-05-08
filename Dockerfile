FROM python:3.9.4-slim-buster as builder
RUN useradd --create-home pypahe
WORKDIR /home/pypahe
USER pypahe
RUN pip install "pipenv==2020.11.15"
ENV PATH="/home/pypahe/.local/bin:$PATH"
COPY ./Pipfile.lock ./
RUN PIPENV_VENV_IN_PROJECT=1 pipenv sync

FROM python:3.9.4-slim-buster
RUN useradd --create-home pypahe
WORKDIR /home/pypahe
USER pypahe
COPY --from=builder /home/pypahe/.venv/lib/python3.9/site-packages/ /home/pypahe/.local/lib/python3.9/site-packages/
COPY ./pypahe ./pypahe
COPY ./pypahe.py ./pypahe.py
ENTRYPOINT ["./pypahe.py"]
