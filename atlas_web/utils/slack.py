import json
import os

import requests
from django.conf import settings


def push_to_slack(text, channel="#mps-atlas-web"):

    if settings.DEBUG:
        return

    if "test" in os.environ["DJANGO_SETTINGS_MODULE"]:
        return

    payload = {
        "text": text,
        "channel": channel.lower(),
    }

    headers = {"content-type": "application/json"}
    r = requests.post(
        settings.SLACK_WEBHOOK_URL, data=json.dumps(payload), headers=headers
    )
    r.raise_for_status()
