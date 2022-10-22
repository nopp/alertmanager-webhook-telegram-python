import telegram, json, logging
from dateutil import parser
from flask import Flask
from flask import request
from flask_basicauth import BasicAuth

app = Flask(__name__)
app.secret_key = 'changeKeyHeere'
basic_auth = BasicAuth(app)

# Yes need to have -, change it!
chatID = "-xchatIDx"

# Authentication conf, change it!
app.config['BASIC_AUTH_FORCE'] = True
app.config['BASIC_AUTH_USERNAME'] = 'XXXUSERNAME'
app.config['BASIC_AUTH_PASSWORD'] = 'XXXPASSWORD'

# Bot token, change it!
bot = telegram.Bot(token="botToken")

@app.route('/alert', methods = ['POST'])
def postAlertmanager():

    try:
        content = json.loads(request.get_data())
        for alert in content['alerts']:
            message = "Status: "+alert['status']+"\n"
            if 'name' in alert['labels']:
                message += "Instance: "+alert['labels']['instance']+"("+alert['labels']['name']+")\n"
            else:
                message += "Instance: "+alert['labels']['instance']+"\n"
            if 'info' in alert['annotations']:
                message += "Info: "+alert['annotations']['info']+"\n"
            if 'summary' in alert['annotations']:
                message += "Summary: "+alert['annotations']['summary']+"\n"                
            if 'description' in alert['annotations']:
                message += "Description: "+alert['annotations']['description']+"\n"
            if alert['status'] == "resolved":
                correctDate = parser.parse(alert['endsAt']).strftime('%Y-%m-%d %H:%M:%S')
                message += "Resolved: "+correctDate
            elif alert['status'] == "firing":
                correctDate = parser.parse(alert['startsAt']).strftime('%Y-%m-%d %H:%M:%S')
                message += "Started: "+correctDate
            bot.sendMessage(chat_id=chatID, text=message)
            return "Alert OK", 200
    except RetryAfter:
        sleep(30)
        bot.sendMessage(chat_id=chatID, text=message)
        return "Alert OK", 200
    except TimedOut as e:
        sleep(60)
        bot.sendMessage(chat_id=chatID, text=message)
        return "Alert OK", 200
    except NetworkError as e:
        sleep(60)
        bot.sendMessage(chat_id=chatID, text=message)
        return "Alert OK", 200
    except Exception as error:       
        bot.sendMessage(chat_id=chatID, text="Error: "+str(error))
        app.logger.info("\t%s",error)
        return "Alert fail", 200

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run(host='0.0.0.0', port=9119)
