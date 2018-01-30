#
# Alertmanager webhook for Telegram using Flask
#
import telegram
from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/alert', methods = ['POST'])
def postAlertmanager():

    content = request.get_json()

    message = """
Status """+content['status']+"""
    
Alertname: """+content['commonLabels']['alertname']+"""

Instance: """+content['commonLabels']['instance']+"""("""+content['commonLabels']['name']+""")
    
"""+content['commonAnnotations']['description']+"""
"""

    bot = telegram.Bot(token='botToken')
    bot.sendMessage(chat_id="-chatID",text=message)
        
    return message
 
app.run(host='0.0.0.0', port= 9119)

