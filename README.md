# Alertmanager webhook for Telegram using Flask 

## INSTALL

* pip install -r requirements.txt

Change on flaskAlert.py
=======================
* botToken
* chatID (without -)
  
Running
=======
* python flaskAlert.py

Running on docker
=================
* docker container run -d -e bottoken="telegramBotToken" -e chatid="telegramChatID" alertmanager-webhook-telegram:latest
