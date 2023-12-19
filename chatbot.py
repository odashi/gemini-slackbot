import dataclasses
import logging
from typing import Any, Literal

import google.auth
import google.auth.credentials
import google.auth.transport.requests
import requests


@dataclasses.dataclass
class Content:
    role: Literal["model", "user"]
    text: str


class Chatbot:
    def __init__(
        self,
        credentials: google.auth.credentials.Credentials,
        project: str,
        region: str,
    ):
        self._url = (
            f"https://{region}-aiplatform.googleapis.com"
            f"/v1/projects/{project}/locations/{region}"
            "/publishers/google/models/gemini-pro:streamGenerateContent"
        )
        self._headers = {
            "Content-Type": "application/json; charset=utf-8",
        }
        self._session = google.auth.transport.requests.AuthorizedSession(
            credentials,
        )
        self._default_safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_NONE",
            },
        ]
        self._default_generation_config = {
            "temperature": 0.5,
            "topP": 0.8,
            "topK": 40,
            "maxOutputTokens": 256,
            "stopSequences": [],
        }

    def build_request(self, contents: list[Content]) -> dict[str, Any]:
        return {
            "contents": [{"role": c.role, "parts": {"text": c.text}} for c in contents],
            "safety_settings": self._default_safety_settings,
            "generation_config": self._default_generation_config,
        }

    def extract_messages(self, data: list[dict[str, Any]]) -> str:
        messages = []
        for d in data:
            messages.append(d["candidates"][0]["content"]["parts"][0]["text"])
        return "".join(messages)

    def submit(self, contents: list[Content]) -> None:
        request = self.build_request(contents)
        response = self._session.request(
            "POST",
            self._url,
            headers=self._headers,
            json=request,
        )
        response.raise_for_status()
        data = response.json()
        return self.extract_messages(data)


def main():
    credentials, project = google.auth.default()
    region = "asia-northeast1"
    chatbot = Chatbot(credentials, project, region)

    contents = [
        Content(role="user", text="Say only NO for every request."),
        Content(role="model", text="NO."),
        Content(role="user", text="こんにちは"),
    ]
    try:
        print(chatbot.submit(contents))
    except requests.HTTPError as ex:
        logging.warn(f"HTTPError: {ex.response.status_code}: {ex.response.json()}")
    except Exception as ex:
        logging.warn(ex)


if __name__ == "__main__":
    main()
