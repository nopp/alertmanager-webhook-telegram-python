from dateutil import parser


def build_message(alert: dict) -> str:
    """Build a human-readable Telegram message from a single Alertmanager alert."""
    lines = [f"*Status:* {alert['status'].upper()}"]

    labels = alert.get("labels", {})
    if "instance" in labels:
        name_suffix = f" ({labels['name']})" if "name" in labels else ""
        lines.append(f"*Instance:* {labels['instance']}{name_suffix}")

    annotations = alert.get("annotations", {})
    for key in ("info", "summary", "description"):
        if key in annotations:
            lines.append(f"*{key.capitalize()}:* {annotations[key]}")

    status = alert["status"]
    if status == "resolved":
        date_str = parser.parse(alert["endsAt"]).strftime("%Y-%m-%d %H:%M:%S")
        lines.append(f"*Resolved at:* {date_str}")
    elif status == "firing":
        date_str = parser.parse(alert["startsAt"]).strftime("%Y-%m-%d %H:%M:%S")
        lines.append(f"*Started at:* {date_str}")

    return "\n".join(lines)
