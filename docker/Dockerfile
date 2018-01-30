FROM alpine:3.7

LABEL maintainer "Carlos Augusto Malucelli <malucellicarlos@gmail.com>"

RUN apk update \
		&& apk add git py-pip bash \
		&& git clone https://github.com/nopp/alertmanager-webhook-telegram.git \
		&& pip install -r alertmanager-webhook-telegram/requirements.txt

WORKDIR /alertmanager-webhook-telegram

COPY run.sh /alertmanager-webhook-telegram

RUN chmod +x /alertmanager-webhook-telegram/run.sh

EXPOSE 9119

ENTRYPOINT ["./run.sh"]
