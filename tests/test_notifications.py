import unittest
from notifications import get_last_notifications, get_task_slug, send_message, message_new_tasks
import requests_mock
import os
import pandas as pd
import test_constants as tc

class TestGetLastNotifications(unittest.TestCase):
    @requests_mock.Mocker()
    def test_get_last_notifications(self, mocker):
        mock_response = tc.MOCK_NOTIFICATIONS_RESPONSE
        mocker.get("https://www.airtasker.com/api/client/v1/experiences/notification-feed/index?page_token=ChowMUo0UkMxRzQ4MUVLRUU1Mjg0R0FDVlJYQg%3D%3D", json=mock_response)
