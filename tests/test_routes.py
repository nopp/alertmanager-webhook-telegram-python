import json
import pytest


FIRING_ALERT = {
    "status": "firing",
    "labels": {
        "alertname": "instance_down",
        "instance": "i-abc123",
    },
    "annotations": {
        "summary": "Server is down",
    },
    "startsAt": "2024-01-01T12:00:00Z",
    "endsAt": "0001-01-01T00:00:00Z",
}

RESOLVED_ALERT = {
    "status": "resolved",
    "labels": {
        "alertname": "instance_down",
        "instance": "i-abc123",
    },
    "annotations": {},
    "startsAt": "2024-01-01T12:00:00Z",
    "endsAt": "2024-01-01T12:10:00Z",
}


def post(client, data):
    return client.post("/alert", data=json.dumps(data), content_type="application/json")


def test_valid_alert_returns_200(client, mock_telegram):
    resp = post(client, {"alerts": [FIRING_ALERT]})
    assert resp.status_code == 200


def test_valid_alert_calls_telegram_send(client, mock_telegram):
    post(client, {"alerts": [FIRING_ALERT]})
    mock_telegram.send.assert_called_once()


def test_multiple_alerts_all_sent(client, mock_telegram):
    post(client, {"alerts": [FIRING_ALERT, RESOLVED_ALERT]})
    assert mock_telegram.send.call_count == 2


def test_resolved_alert_returns_200(client, mock_telegram):
    resp = post(client, {"alerts": [RESOLVED_ALERT]})
    assert resp.status_code == 200


def test_empty_alerts_returns_200_without_sending(client, mock_telegram):
    resp = post(client, {"alerts": []})
    assert resp.status_code == 200
    mock_telegram.send.assert_not_called()


def test_invalid_json_returns_400(client):
    resp = client.post("/alert", data="not-json", content_type="application/json")
    assert resp.status_code == 400


def test_telegram_failure_returns_207(client, mock_telegram):
    mock_telegram.send.side_effect = RuntimeError("Telegram down")
    resp = post(client, {"alerts": [FIRING_ALERT]})
    assert resp.status_code == 207


def test_partial_failure_second_alert_fails(client, mock_telegram):
    mock_telegram.send.side_effect = [None, RuntimeError("fail")]
    resp = post(client, {"alerts": [FIRING_ALERT, RESOLVED_ALERT]})
    assert resp.status_code == 207


def test_message_contains_alert_status(client, mock_telegram):
    post(client, {"alerts": [FIRING_ALERT]})
    sent_text = mock_telegram.send.call_args[0][0]
    assert "FIRING" in sent_text


def test_message_contains_instance(client, mock_telegram):
    post(client, {"alerts": [FIRING_ALERT]})
    sent_text = mock_telegram.send.call_args[0][0]
    assert "i-abc123" in sent_text
