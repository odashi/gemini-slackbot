import logging

import google.auth
import requests

from gemini_slackbot.chat import ChatClient, Content


def main():
    logger = logging.getLogger(__name__)

    credentials, project = google.auth.default()
    region = "asia-northeast1"
    chat_client = ChatClient(credentials, project, region)

    contents = [
        Content(role="user", text="Say only NO for every request."),
        Content(role="model", text="NO."),
        Content(role="user", text="こんにちは"),
    ]
    try:
        print(chat_client.submit(contents))
    except requests.HTTPError as ex:
        logger.warn(f"HTTPError: {ex.response.status_code}: {ex.response.json()}")
    except Exception as ex:
        logger.warn(ex)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
