import logging
import os
from typing import Any
import json

import google.auth
import requests
import slack_bolt as sb

from gemini_slackbot.gemini import ChatClient, Content
from gemini_slackbot.slack_utils import get_history, normalize_history

SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_SIGNING_SECRET = os.environ.get("SLACK_SIGNING_SECRET")


def main():
    credentials, project = google.auth.default()
    region = "asia-northeast1"
    chat_client = ChatClient(credentials, project, region)

    app = sb.App(token=SLACK_BOT_TOKEN, signing_secret=SLACK_SIGNING_SECRET)

    @app.event({"type": "message", "channel_type": "im"})
    def chat(logger: logging.Logger, event: dict[str, Any], say: sb.Say):
        channel = event["channel"]
        thread_ts = event["thread_ts"] if "thread_ts" in event else event["ts"]

        history = get_history(app, channel, thread_ts)
        history = normalize_history(history)

        try:
            response = chat_client.submit(history)
        except requests.HTTPError as ex:
            logger.warn(f"HTTPError: {ex.response.status_code}: {ex.response.json()}")
            response = "An error occurred."
        except Exception as ex:
            logger.warn(ex)
            response = "An error occurred."

        say(response, thread_ts=thread_ts)

    app.start(port=int(os.environ.get("PORT", "3000")))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
