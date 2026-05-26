import pytest
from app.alerts import build_message


FIRING_ALERT = {
    "status": "firing",
    "labels": {
        "alertname": "instance_down",
        "instance": "i-abc123",
        "name": "prod-server",
    },
    "annotations": {
        "summary": "Server is down",
        "description": "Has been down for 2 minutes.",
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
    "annotations": {
        "summary": "Server is back",
    },
    "startsAt": "2024-01-01T12:00:00Z",
    "endsAt": "2024-01-01T12:10:00Z",
}


def test_firing_status_uppercased():
    msg = build_message(FIRING_ALERT)
    assert "*Status:* FIRING" in msg


def test_instance_with_name():
    msg = build_message(FIRING_ALERT)
    assert "*Instance:* i-abc123 (prod-server)" in msg


def test_instance_without_name():
    alert = {**FIRING_ALERT, "labels": {"instance": "i-abc123"}}
    msg = build_message(alert)
    assert "*Instance:* i-abc123" in msg
    assert "(" not in msg


def test_firing_includes_started_at():
    msg = build_message(FIRING_ALERT)
    assert "*Started at:* 2024-01-01 12:00:00" in msg


def test_firing_includes_summary_and_description():
    msg = build_message(FIRING_ALERT)
    assert "*Summary:* Server is down" in msg
    assert "*Description:* Has been down for 2 minutes." in msg


def test_resolved_status_uppercased():
    msg = build_message(RESOLVED_ALERT)
    assert "*Status:* RESOLVED" in msg


def test_resolved_includes_resolved_at():
    msg = build_message(RESOLVED_ALERT)
    assert "*Resolved at:* 2024-01-01 12:10:00" in msg


def test_resolved_has_no_started_at():
    msg = build_message(RESOLVED_ALERT)
    assert "Started at" not in msg


def test_info_annotation_included():
    alert = {**FIRING_ALERT, "annotations": {"info": "some info"}}
    msg = build_message(alert)
    assert "*Info:* some info" in msg


def test_empty_annotations_omitted():
    alert = {**FIRING_ALERT, "annotations": {}}
    msg = build_message(alert)
    assert "Summary" not in msg
    assert "Description" not in msg
    assert "Info" not in msg


def test_missing_instance_omitted():
    alert = {**FIRING_ALERT, "labels": {"alertname": "instance_down"}}
    msg = build_message(alert)
    assert "Instance" not in msg
