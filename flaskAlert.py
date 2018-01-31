from flask import Flask
from flask import request
import telegram
import logging

app = Flask(__name__)
app.secret_key = 'aYT>.L$kk2h>!'

@app.route('/alert', methods = ['POST'])
def postAlertmanager():

    content = request.get_json()

    try:

        for alert in content['alerts']:

            message = """
Status """+alert['status']+"""
    
Alertname: """+alert['labels']['alertname']+"""

Instance: """+alert['labels']['instance']+"""("""+alert['labels']['name']+""")
    
"""+alert['annotations']['description']+"""
"""
            bot = telegram.Bot(token=botToken)
            bot.sendMessage(chat_id="-chatID",text=message)
    except:

        logger = logging.getLogger(__name__)
        logger.info(content)
        bot = telegram.Bot(token=botToken)
        bot.sendMessage(chat_id="-chatID",text="Falhou o envio via Flask para o Telegram")

    return ""

if __name__ == '__main__':
    logging.basicConfig(filename='flaskAlert.log',level=logging.INFO)
    app.run(host='0.0.0.0', port= 8090)
