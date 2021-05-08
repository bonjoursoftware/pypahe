FROM python:3.9.4-slim-buster
WORKDIR /pypahe
RUN pip install "pipenv==2020.11.15"
COPY ./Pipfile.lock ./
RUN pipenv sync --dev
COPY ./ ./
ENTRYPOINT ["pipenv", "run"]
