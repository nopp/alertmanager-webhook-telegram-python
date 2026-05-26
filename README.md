# Alertmanager webhook for Telegram (Python version)

![Docker Image CI](https://github.com/nopp/alertmanager-webhook-telegram-python/workflows/Docker%20Image%20CI/badge.svg)
![Code scanning - action](https://github.com/nopp/alertmanager-webhook-telegram-python/workflows/Code%20scanning%20-%20action/badge.svg)

GO version: https://github.com/nopp/alertmanager-webhook-telegram-go

## Project structure

```
├── app/
│   ├── __init__.py     # app factory (create_app)
│   ├── config.py       # config from env vars
│   ├── alerts.py       # alert message builder
│   ├── telegram.py     # Telegram HTTP client
│   └── routes.py       # Flask blueprint (/alert)
├── wsgi.py             # gunicorn / dev entrypoint
├── requirements.txt
└── docker/
    ├── Dockerfile
    └── run.sh
```

## Requirements

- Python 3.11+
- pip packages: see `requirements.txt`

## Configuration

All config via environment variables — no hardcoded secrets.

| Variable | Required | Default | Description |
|---|---|---|---|
| `TELEGRAM_BOT_TOKEN` | ✅ | — | Bot token from @BotFather |
| `TELEGRAM_CHAT_ID` | ✅ | — | Target chat/group ID |
| `BASIC_AUTH_USERNAME` | ❌ | `""` | HTTP basic auth username |
| `BASIC_AUTH_PASSWORD` | ❌ | `""` | HTTP basic auth password |
| `BASIC_AUTH_FORCE` | ❌ | `true` | Set `false` to disable auth |
| `SECRET_KEY` | ❌ | random | Flask secret key |
| `MAX_RETRIES` | ❌ | `3` | Telegram send retries |

## Install & run locally

```bash
pip install -r requirements.txt

export TELEGRAM_BOT_TOKEN=your_token
export TELEGRAM_CHAT_ID=your_chat_id
export BASIC_AUTH_USERNAME=admin
export BASIC_AUTH_PASSWORD=secret

# dev
python wsgi.py

# production
gunicorn -w 4 -b 0.0.0.0:9119 wsgi:app
```

## Docker

```bash
cd docker/
docker build -t alertmanager-webhook-telegram .

docker run -d --name telegram-webhook \
  -e TELEGRAM_BOT_TOKEN=your_token \
  -e TELEGRAM_CHAT_ID=your_chat_id \
  -e BASIC_AUTH_USERNAME=admin \
  -e BASIC_AUTH_PASSWORD=secret \
  -p 9119:9119 \
  alertmanager-webhook-telegram
```

## Alertmanager config example

```yaml
receivers:
  - name: telegram-webhook
    webhook_configs:
      - url: http://your-host:9119/alert
        send_resolved: true
        http_config:
          basic_auth:
            username: admin
            password: secret
```

## Get your Telegram chat ID

1. Go to https://web.telegram.org/
2. Open the target chat
3. Copy the numeric ID from the URL (e.g. `https://web.telegram.org/#/im?p=g1234567` → ID is `-1234567` for groups)

## Test

```bash
curl -XPOST \
  -u admin:secret \
  -H 'Content-Type: application/json' \
  --data '{
    "status": "resolved",
    "alerts": [{
      "status": "resolved",
      "labels": {
        "alertname": "instance_down",
        "instance": "i-0d7188fkl90bac100",
        "name": "prod-server"
      },
      "annotations": {
        "summary": "Instance i-0d7188fkl90bac100 down",
        "description": "Host has been down for more than 2 minutes."
      },
      "endsAt": "2024-01-01T16:16:19Z",
      "startsAt": "2024-01-01T16:02:19Z"
    }]
  }' \
  http://localhost:9119/alert
```
