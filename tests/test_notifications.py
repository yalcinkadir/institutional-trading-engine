from __future__ import annotations

from src.notifications import NotificationClient


class FakeResponse:
    def __init__(self, status_code: int, text: str = "") -> None:
        self.status_code = status_code
        self.text = text


def test_telegram_skips_when_config_missing(monkeypatch) -> None:
    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
    monkeypatch.delenv("TELEGRAM_CHAT_ID", raising=False)
    client = NotificationClient(telegram_bot_token="", telegram_chat_id="")

    result = client.send_telegram("hello")

    assert result.channel == "telegram"
    assert result.status == "skipped"
    assert not result.delivered


def test_telegram_dry_run_does_not_call_network() -> None:
    called = False

    def fake_post(*args, **kwargs):
        nonlocal called
        called = True
        return FakeResponse(200)

    client = NotificationClient(dry_run=True, post=fake_post)

    result = client.send_telegram("hello")

    assert result.status == "dry_run"
    assert called is False


def test_telegram_success_uses_expected_payload() -> None:
    calls = []

    def fake_post(url, data=None, timeout=None, **kwargs):
        calls.append({"url": url, "data": data, "timeout": timeout})
        return FakeResponse(200, "ok")

    client = NotificationClient(
        telegram_bot_token="dummy-token",
        telegram_chat_id="dummy-chat",
        post=fake_post,
    )

    result = client.send_telegram("hello")

    assert result.status == "delivered"
    assert result.delivered
    assert calls[0]["url"].endswith("/botdummy-token/sendMessage")
    assert calls[0]["data"] == {"chat_id": "dummy-chat", "text": "hello"}


def test_telegram_failure_returns_structured_result() -> None:
    def fake_post(*args, **kwargs):
        return FakeResponse(500, "server error")

    client = NotificationClient(
        telegram_bot_token="dummy-token",
        telegram_chat_id="dummy-chat",
        post=fake_post,
    )

    result = client.send_telegram("hello")

    assert result.status == "failed"
    assert result.status_code == 500
    assert result.error == "server error"


def test_webhook_skips_when_config_missing(monkeypatch) -> None:
    monkeypatch.delenv("REPORT_WEBHOOK_URL", raising=False)
    client = NotificationClient(webhook_url="")

    result = client.send_webhook({"text": "hello"})

    assert result.channel == "webhook"
    assert result.status == "skipped"


def test_webhook_success_uses_json_payload() -> None:
    calls = []

    def fake_post(url, json=None, timeout=None, **kwargs):
        calls.append({"url": url, "json": json, "timeout": timeout})
        return FakeResponse(204, "")

    client = NotificationClient(webhook_url="mock-webhook-url", post=fake_post)

    result = client.send_webhook({"text": "hello"})

    assert result.status == "delivered"
    assert calls[0]["url"] == "mock-webhook-url"
    assert calls[0]["json"] == {"text": "hello"}


def test_send_text_can_include_webhook() -> None:
    def fake_post(*args, **kwargs):
        return FakeResponse(200, "ok")

    client = NotificationClient(
        telegram_bot_token="dummy-token",
        telegram_chat_id="dummy-chat",
        webhook_url="mock-webhook-url",
        post=fake_post,
    )

    results = client.send_text("hello", include_webhook=True)

    assert [result.channel for result in results] == ["telegram", "webhook"]
    assert all(result.status == "delivered" for result in results)
