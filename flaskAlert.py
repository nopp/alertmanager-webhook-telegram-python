import telegram
import logging
from flask import Flask
from flask import request

app = Flask(__name__)
app.secret_key = 'aYT>.L$kk2h>!'

bot = telegram.Bot(token="botToken")
chatID = "-xchatIDx"

@app.route('/alert', methods = ['POST'])
def postAlertmanager():

    content = request.get_json()

    try:

        for alert in content['alerts']:

            if 'name' in alert['labels']:

                message = """
Status """+alert['status']+"""   
Alertname: """+alert['labels']['alertname']+"""
Instance: """+alert['labels']['instance']+"""("""+alert['labels']['name']+""")
"""+alert['annotations']['description']+"""
"""
            else:
                message = """
Status """+alert['status']+"""
Alertname: """+alert['labels']['alertname']+"""
Instance: """+alert['labels']['instance']+"""
"""+alert['annotations']['description']+"""
"""
            bot.sendMessage(chat_id=chatID,text=message)                
    except:

        logger = logging.getLogger(__name__)
        logger.info(content)
        bot.sendMessage(chat_id=chatID,text="Failed to send via Flask to Telegram!")

    return ""

if __name__ == '__main__':
    logging.basicConfig(filename='flaskAlert.log',level=logging.INFO)
    app.run(host='0.0.0.0', port=9119)
