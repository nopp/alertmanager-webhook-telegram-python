FROM alpine:3.7

LABEL maintainer "Carlos Augusto Malucelli <malucellicarlos@gmail.com>"

RUN apk update \
		&& apk add py-pip bash gcc python-dev musl-dev libffi-dev openssl-dev \
		&& rm -rf /var/cache/apk/* \
		&& wget https://github.com/nopp/alertmanager-webhook-telegram/archive/master.zip \
		&& unzip master.zip \
		&& pip install -r alertmanager-webhook-telegram-master/requirements.txt

WORKDIR /alertmanager-webhook-telegram

COPY run.sh /alertmanager-webhook-telegram

COPY flaskAlert.py /alertmanager-webhook-telegram

RUN chmod +x /alertmanager-webhook-telegram/run.sh

RUN chmod +x /alertmanager-webhook-telegram/flaskAlert.py

EXPOSE 9119

ENTRYPOINT ["./run.sh"]
