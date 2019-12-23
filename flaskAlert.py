import telegram
import logging
import json
from flask import Flask
from flask import request
from flask_basicauth import BasicAuth

app = Flask(__name__)
app.secret_key = 'aYT>.L$kk2h>!'
app.config['BASIC_AUTH_USERNAME'] = 'XXXUSERNAME'
app.config['BASIC_AUTH_PASSWORD'] = 'XXXPASSWORD'

basic_auth = BasicAuth(app)
app.config['BASIC_AUTH_FORCE'] = True
bot = telegram.Bot(token="botToken")
chatID = "xchatIDx"

@app.route('/alert', methods = ['POST'])
def postAlertmanager():

    content = json.loads(request.get_data())
    with open("Output.txt", "w") as text_file:
        text_file.write("{0}".format(content))
    try:
        for alert in content['alerts']:
            message = """Status: """+alert['status']+""" \n"""
            message += """Alertname: """+alert['labels']['alertname']+""" \n"""

            if alert['status'] == "firing":
                message += """Detected: """+alert['startsAt']+""" \n"""

            if alert['status'] == "resolved":
                message += """Resolved: """+alert['endsAt']+""" \n"""

            if 'name' in alert['labels']:
                message += """Instance: """+alert['labels']['instance']+"""("""+alert['labels']['name']+""") \n"""
            else:
                message += """Instance: """+alert['labels']['instance']+""" \n"""

            message += """\n\n"""+alert['annotations']['description']+""""""

            bot.sendMessage(chat_id=chatID, text=message)
            return "Alert OK", 200
    except:
        bot.sendMessage(chat_id=chatID, text="Error!")
        return "Alert nOK", 200


if __name__ == '__main__':
    logging.basicConfig(filename='flaskAlert.log', level=logging.INFO)
    app.run(host='0.0.0.0', port=9119)
