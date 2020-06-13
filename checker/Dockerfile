FROM python:3.8-slim-buster

RUN adduser --disabled-password --gecos "" --home /home/worker worker
USER worker
WORKDIR /home/worker

RUN pip install Flask requests jsondiff requests
ENV \
  FLASK_ENV=development \
  FLASK_DEBUG=0
COPY ./clouddriver-check.py .
EXPOSE 5000
ENTRYPOINT ["python", "/home/worker/clouddriver-check.py"]
