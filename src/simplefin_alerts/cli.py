"""Command-line interface for SimpleFin Alerts."""

import os

from simplefin_alerts.config import load_config
from simplefin_alerts.notifications import send_via_apprise
from simplefin_alerts.simplefin import get_account_errors


def list_to_string(lst):
    """Convert a list to a space-separated string, or return False if empty."""
    if not lst:
        return False
    return " ".join(map(str, lst))


def main():
    """Main entry point for the CLI."""
    data_path = os.environ.get("SIMPLEFIN_DATA_PATH", "simplefin-data.pickle")

    # Load configuration (pickle file first, then setup token)
    config = load_config(data_path)

    if not config or not config.get("access_url"):
        print("Error: No SimpleFin access URL configured.")
        print("Set SIMPLEFIN_SETUP_TOKEN environment variable to claim access.")
        return 1

    access_url = config["access_url"]
    apprise_url = config.get("apprise_url", "")
    apprise_tag = config.get("apprise_tag", "")

    # Query SimpleFin for errors
    try:
        errors = get_account_errors(access_url)
    except Exception as e:
        print(f"Error querying SimpleFin: {e}")
        return 1

    error_string = list_to_string(errors)

    if error_string:
        print(error_string)
        if apprise_url:
            send_via_apprise(apprise_url, apprise_tag, error_string)
    else:
        message = "No SimpleFin Accounts in Error State"
        print(message)
        if apprise_url:
            send_via_apprise(apprise_url, apprise_tag, message)

    return 0


if __name__ == "__main__":
    exit(main())
