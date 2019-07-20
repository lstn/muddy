FROM python:3.7-alpine

COPY . /muddy
WORKDIR /muddy

RUN pip install .

ENTRYPOINT ["/usr/local/bin/muddy"]
CMD ["--help"]