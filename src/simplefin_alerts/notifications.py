"""Notification services for SimpleFin Alerts."""

import requests


def send_via_apprise(apprise_url: str, tag: str, content: str) -> bool:
    """
    Send notification via Apprise API.

    Args:
        apprise_url: URL of the Apprise API endpoint
        tag: Apprise tag for routing the notification
        content: Message body to send

    Returns:
        True if notification was sent successfully, False otherwise
    """
    payload = f"body={content}&tag={tag}"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    try:
        response = requests.post(apprise_url, headers=headers, data=payload)
        response.raise_for_status()
        return True
    except requests.RequestException as e:
        print(f"Failed to send notification: {e}")
        return False
