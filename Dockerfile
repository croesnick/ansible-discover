FROM python:3.7-alpine

LABEL maintainer="Carsten Rösnick-Neugebauer <croesnick@gmail.com>"

ENV USER ansiblediscover
ENV HOME /home/${USER}

RUN adduser ${USER} -h "${HOME}" -D
WORKDIR /ansiblediscover
COPY . /ansiblediscover

RUN apk add --no-cache --virtual .build-deps \
       gcc \
       libffi-dev \
       linux-headers \
       make \
       musl-dev \
    && pip install -e . \
    && apk del .build-deps \
    && rm -rf ~/.cache/

USER ${USER}
CMD ["ansible-discover", "--help"]
