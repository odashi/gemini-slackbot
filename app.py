import json
import logging
import os
from typing import Any

import google.auth
import google.auth.transport.requests
import slack_bolt as sb


class Chatbot:
    def __init__(self, region: str):
        creds, project = google.auth.default()
        self._url = (
            f"https://{region}-aiplatform.googleapis.com"
            f"/v1/projects/{project}/locations/{region}"
            "/publishers/google/models/gemini-pro:streamGenerateContent"
        )
        self._headers = {
            "Content-Type": "application/json; charset=utf-8",
        }
        self._session = google.auth.transport.requests.AuthorizedSession(creds)

    def submit(self, request: dict[str, Any]) -> None:
        response = self._session.request(
            "POST",
            self._url,
            headers=self._headers,
            json=request,
        )
        if response.status_code != 200:
            raise RuntimeError(f"{response.status_code}: {response.json()}")
        return response.json()


def main():
    logging.basicConfig(level=logging.INFO)
    region = "asia-northeast1"
    chatbot = Chatbot(region)

    request = {
        "contents": {
            "role": "user",
            "parts": {
                "text": "Give me a recipe for banana bread.",
            },
        },
        "safety_settings": {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_LOW_AND_ABOVE",
        },
        "generation_config": {
            "temperature": 0.2,
            "topP": 0.8,
            "topK": 40,
            "maxOutputTokens": 200,
            "stopSequences": [".", "?", "!"],
        },
    }

    print(json.dumps(chatbot.submit(request), indent=2))

    return

    print(creds.token)
    return
    genai.configure(credentials=creds)
    # logging.info(list(genai.))

    app = sb.App(
        token=os.environ.get("SLACK_BOT_TOKEN"),
        signing_secret=os.environ.get("SLACK_SIGNING_SECRET"),
    )

    @app.event({"type": "message", "channel_type": "im"})
    def chat(logger: logging.Logger, event: dict[str, Any], say: sb.Say):
        logger.info(json.dumps(event, indent=2))
        result = app.client.conversations_replies(
            channel=event["channel"], ts=event["thread_ts"]
        )
        messages = result["messages"]
        for m in messages:
            logger.info(("BOT" if "app_id" in m else "USER") + " " + m["text"])
        say(f"Hello, {event['user']}!", thread_ts=event["ts"])

    app.start(port=int(os.environ.get("PORT", "3000")))


if __name__ == "__main__":
    main()
