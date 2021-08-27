from alpine:latest

RUN apk add --no-cache python3-dev
RUN apk add py3-pip
RUN pip3 install --upgrade pip

RUN apk --update add build-base libxslt-dev

RUN apk add --virtual .build-deps \
        --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing \
        --repository http://dl-cdn.alpinelinux.org/alpine/edge/main \
        gcc libc-dev geos-dev geos && \
    runDeps="$(scanelf --needed --nobanner --recursive /usr/local \
    | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
    | xargs -r apk info --installed \
    | sort -u)" && \
    apk add --virtual .rundeps $runDeps

RUN geos-config --cflags


WORKDIR /app

COPY . /app

RUN pip install --disable-pip-version-check -r requirements.txt
RUN apk del build-base python3-dev && \
    rm -rf /var/cache/apk/*

EXPOSE 5000

ENTRYPOINT ["python3"]
CMD ["app.py"]

     
