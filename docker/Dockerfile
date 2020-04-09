FROM alpine:3.7

LABEL maintainer "Carlos Augusto Malucelli <malucellicarlos@gmail.com>"

RUN apk update \
		&& apk add py-pip bash gcc python-dev musl-dev libffi-dev openssl-dev \
		&& rm -rf /var/cache/apk/* \
		&& wget https://github.com/nopp/alertmanager-webhook-telegram/archive/master.zip \
		&& unzip master.zip \
		&& pip install -r alertmanager-webhook-telegram-master/requirements.txt 

WORKDIR alertmanager-webhook-telegram-master

RUN mv docker/run.sh run.sh \
	&& chmod +x run.sh

EXPOSE 9119

ENTRYPOINT ["./run.sh"]
