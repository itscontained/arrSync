FROM amd64/python:3.7.4-alpine

LABEL maintainers="dirtycajunrice"

WORKDIR /app

COPY /requirements.txt /arrSync.py /app/

RUN pip install --no-cache-dir -r /app/requirements.txt

CMD entrypoint.py