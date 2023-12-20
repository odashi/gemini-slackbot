# gemini-slackbot

Slack bot to chat with Google Gemini.

# Implementation notes

## Google credentials

This program uses ADC on Google Cloud to communicate with Gemini.
You have to run this bot using an appropriate service account
with `aiplatform.endpoints.predict` permission (or `roles/aiplatform.user` role).

If you need to use an API key instead, you have to update some code in
[gemini.py](https://github.com/odashi/gemini-slackbot/blob/main/src/gemini_slackbot/gemini.py).

## Slack integration

This Slack bot listens the following events:

- `message.im`

and requires the following permissions:

- `chat:write`
- `im:history`
- `im:read`
- `im:write`
