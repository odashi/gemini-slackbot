import logging
from typing import Literal

import slack_bolt as sb

from gemini_slackbot.common_types import Content

_logger = logging.getLogger(__name__)


def get_history(app: sb.App, channel: str, ts: str) -> list[Content]:
    result = app.client.conversations_replies(channel=channel, ts=ts).validate()

    return [
        Content(
            role=("model" if "app_id" in m else "user"),
            text=m["text"],
        )
        for m in result["messages"]
    ]


def normalize_history(history: list[Content]) -> list[Content]:
    workspace: list[tuple[Literal["model", "user"], list[str]]] = [("user", [""])]

    for c in history:
        if c.role == workspace[-1][0]:
            workspace[-1][1].append(c.text.strip())
        else:
            workspace.append((c.role, [c.text]))

    return [
        Content(role=role, text="\n".join(texts).strip()) for role, texts in workspace
    ]
