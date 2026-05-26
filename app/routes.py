import json
import logging

from flask import Blueprint, current_app, request

from .alerts import build_message

logger = logging.getLogger(__name__)

bp = Blueprint("alerts", __name__)


@bp.route("/alert", methods=["POST"])
def post_alertmanager():
    try:
        payload = json.loads(request.get_data())
    except json.JSONDecodeError as exc:
        logger.error("Invalid JSON payload: %s", exc)
        return "Bad Request", 400

    alerts = payload.get("alerts", [])
    if not alerts:
        return "No alerts", 200

    telegram = current_app.telegram
    errors = []

    for alert in alerts:
        alert_name = alert.get("labels", {}).get("alertname", "unknown")
        try:
            message = build_message(alert)
            telegram.send(message)
            logger.info("Sent alert: %s", alert_name)
        except Exception as exc:
            logger.exception("Failed to send alert '%s': %s", alert_name, exc)
            errors.append(f"{alert_name}: {exc}")

    if errors:
        try:
            telegram.send(f"⚠️ Failed to forward {len(errors)} alert(s):\n" + "\n".join(errors))
        except Exception:
            pass
        return "Partial failure", 207

    return "OK", 200
