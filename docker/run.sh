#!/bin/bash
sed -i s/botToken/"$bottoken"/ flaskAlert.py
sed -i s/chatID/"$chatid"/ flaskAlert.py

/usr/bin/gunicorn flaskAlert
