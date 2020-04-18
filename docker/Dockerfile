FROM alpine:3.7

LABEL maintainer="Carlos Augusto Malucelli <camalucelli@gmail.com>"

WORKDIR /alertmanager-webhook-telegram

RUN apk update \
                && apk add py-pip bash gcc python-dev musl-dev libffi-dev openssl-dev unzip \
                && rm -rf /var/cache/apk/* \
                && wget https://github.com/nopp/alertmanager-webhook-telegram/archive/master.zip \
                && unzip -j master.zip  \
                && pip install -r requirements.txt \
                && chmod +x run.sh

EXPOSE 9119

ENTRYPOINT ["./run.sh"]
