FROM python:3.10.14-slim-bookworm

WORKDIR /app

RUN apt-get update && apt-get install build-essential -y
COPY ./other/requirements.txt requirements.txt
RUN pip install --upgrade pip && \
	pip install -r requirements.txt
RUN python -c "import nltk; nltk.download('punkt')"