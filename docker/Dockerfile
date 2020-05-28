FROM alpine:3.7

LABEL maintainer="Carlos Augusto Malucelli <camalucelli@gmail.com>"

WORKDIR /alertmanager-webhook-telegram

RUN apk update \
                && apk add git py3-pip bash gcc python3-dev musl-dev libffi-dev openssl-dev unzip tzdata \
                && rm -rf /var/cache/apk/* \
                && git clone https://github.com/qq516249940/alertmanager-webhook-telegram-python.git . \
                && git checkout dev  \
                && pip3 install -r requirements.txt \
                && chmod +x docker/run.sh 
             

EXPOSE 9119

ENTRYPOINT ["./docker/run.sh"]
