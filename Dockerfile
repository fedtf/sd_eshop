FROM python:3.7.7-alpine

COPY requirements.txt /requirements.txt

RUN apk add --no-cache --virtual .build-deps build-base \
    && pip3 install pip --upgrade \
    && pip3 install -r /requirements.txt \
    && pip3 install gunicorn \
    && apk del .build-deps

EXPOSE 8080

WORKDIR /sd_eshop

ADD . /sd_eshop

VOLUME /sd_eshop

ENV AIOHTTP_SETTINGS_PATH='/sd_eshop/config/production.yaml'
CMD gunicorn -w 4 sd_eshop.wsgi:app --bind 0.0.0.0:8080 --worker-class aiohttp.GunicornWebWorker
