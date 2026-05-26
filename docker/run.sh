#!/bin/bash
set -euo pipefail

require_var() {
  local var="$1"
  if [ -z "${!var:-}" ]; then
    echo "ERROR: required env var '$var' is not set" >&2
    exit 1
  fi
}

warn_var() {
  local var="$1"
  if [ -z "${!var:-}" ]; then
    echo "WARNING: '$var' is not set — basic auth may be disabled or misconfigured"
  fi
}

require_var TELEGRAM_BOT_TOKEN
require_var TELEGRAM_CHAT_ID
warn_var BASIC_AUTH_USERNAME
warn_var BASIC_AUTH_PASSWORD

echo "Config OK. Starting gunicorn…"
exec gunicorn -w 4 -b 0.0.0.0:9119 wsgi:app
