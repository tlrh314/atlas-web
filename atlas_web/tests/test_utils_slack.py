import json
import os
from unittest import mock

import pytest
from django.conf import settings
from django.test import override_settings

from atlas_web.utils.slack import push_to_slack

pytestmark = pytest.mark.django_db


@mock.patch("requests.post")
class TestPushToSlack:
    @override_settings(DEBUG=True)
    def test_push_to_slack_does_not_push_if_debug(self, mock_post):
        assert settings.DEBUG
        push_to_slack("test_push_to_slack_does_not_push_if_debug")
        mock_post.assert_not_called()

    @override_settings(DEBUG=True)
    def test_push_to_slack_does_not_push_from_test_suite(self, mock_post):
        push_to_slack("test_push_to_slack_does_not_push_from_test_suite")
        mock_post.assert_not_called()

    @override_settings(DEBUG=False)
    def test_push_to_slack_does_push_if_not_debug_and_not_test_settings_module(
        self, mock_post
    ):
        os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings.local"
        assert "test" not in os.environ["DJANGO_SETTINGS_MODULE"]

        text = "test_push_to_slack_does_push_if_not_debug_and_not_test_settings_module"
        channel = "#mps-atlas-web"
        push_to_slack(text, channel=channel)
        mock_post.assert_called_with(
            str(settings.SLACK_WEBHOOK_URL),
            data=json.dumps({"text": text, "channel": channel.lower()}),
            headers={"content-type": "application/json"},
        )
