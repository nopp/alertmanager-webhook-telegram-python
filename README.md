# Alertmanager webhook for Telegram using Flask

## INSTALL

* pip install -r requirements.txt

Change on flaskAlert.py
=======================
* botToken
* chatID

If you'll use with authentication, change too

* BASIC_AUTH_USERNAME
* BASIC_AUTH_PASSWORD

Disabling authentication
========================
On flaskAlert.py change app.config['BASIC_AUTH_FORCE'] = True to app.config['BASIC_AUTH_FORCE'] = False

Alertmanager configuration example
==================================

	receivers:
	- name: 'telegram-webhook'
	  webhook_configs:
	  - url: http://ipFlaskAlert:9119/alert
	    send_resolved: true
	    http_config:
	      basic_auth:
		username: 'admin'
		password: 'password'

One way to get the chat ID
==========================
1) Access https://web.telegram.org/
2) Click to specific chat to the left
3) At the url, you can get the chat ID(Ex: https://web.telegram.org/#/im?p=g1234567, so the chatID is 1234567)

Running
=======
* python flaskAlert.py

Running on docker
=================
    git clone https://github.com/nopp/alertmanager-webhook-telegram.git
    cd alertmanager-webhook-telegram/docker/
    docker build -t alertmanager-webhook-telegram:1.0 .

    docker run -d --name telegram-bot \
    	-e "bottoken=telegramBotToken" \
    	-e "chatid=telegramChatID" \
    	-e "username=<username>" \
    	-e "password=<password>" \
    	-p 9119:9119 alertmanager-webhook-telegram:1.0

Example to test
===============
	curl -XPOST --data '{"status":"resolved","groupLabels":{"alertname":"instance_down"},"commonAnnotations":{"description":"i-0d7188fkl90bac100 of job ec2-sp-node_exporter has been down for more than 2 minutes.","summary":"Instance i-0d7188fkl90bac100 down"},"alerts":[{"status":"resolved","labels":{"name":"olokinho01-prod","instance":"i-0d7188fkl90bac100","job":"ec2-sp-node_exporter","alertname":"instance_down","os":"linux","severity":"page"},"endsAt":"2019-07-01T16:16:19.376244942-03:00","generatorURL":"http://pmts.io:9090","startsAt":"2019-07-01T16:02:19.376245319-03:00","annotations":{"description":"i-0d7188fkl90bac100 of job ec2-sp-node_exporter has been down for more than 2 minutes.","summary":"Instance i-0d7188fkl90bac100 down"}}],"version":"4","receiver":"infra-alert","externalURL":"http://alm.io:9093","commonLabels":{"name":"olokinho01-prod","instance":"i-0d7188fkl90bac100","job":"ec2-sp-node_exporter","alertname":"instance_down","os":"linux","severity":"page"}}' http://username:password@flaskAlert:9119/alert
