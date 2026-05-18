from __future__ import annotations


def share_intelligence(sender: str, receivers: list[str], payload: dict) -> dict:
    transmissions = []

    for receiver in receivers:
        transmissions.append(
            {
                "from": sender,
                "to": receiver,
                "payload_keys": list(payload.keys()),
            }
        )

    return {
        "transmission_count": len(transmissions),
        "transmissions": transmissions,
    }
