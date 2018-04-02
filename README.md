# Alertmanager webhook for Telegram using Flask 

## INSTALL

* pip install -r requirements.txt

Change on flaskAlert.py
=======================
* botToken
* chatID (without -)
  
Alertmanager configuration example
==================================

		receivers:
		- name: 'telegram-webhook'
		  webhook_configs:
		  - url: http://ipFlaskAlert:9119/alert
		    send_resolved: true
		    
One way to get the chat ID
==========================
1) Add bot on channel
2) Send message on this channel with @botname
3) Access access the link https://api.telegram.org/botXXX:YYYY/getUpdates (xxx:yyyy botID)

Running
=======
* python flaskAlert.py

Running on docker
=================
* docker container run -d -e bottoken="telegramBotToken" -e chatid="telegramChatID" -p 9119:9119 nopp/alertmanager-webhook-telegram:latest
