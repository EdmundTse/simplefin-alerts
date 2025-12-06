"""Configuration management for SimpleFin Alerts."""

from __future__ import annotations

import base64
import os
import pickle

import requests


def load_config(data_path: str) -> dict | None:
    """
    Load configuration from pickle file, or claim new access using setup token.

    Priority:
    1. Pickle file from previous runs
    2. SIMPLEFIN_SETUP_TOKEN environment variable (claims new access URL)

    Returns:
        dict with access_url, apprise_url, apprise_tag or None if not configured
    """
    apprise_url = os.environ.get("APPRISE_URL", "")
    apprise_tag = os.environ.get("APPRISE_TAG", "")

    # Try to load from pickle file first
    try:
        with open(data_path, "rb") as file:
            data = pickle.load(file)
            access_url = data.get("access_url", "")
            if access_url:
                return {
                    "access_url": access_url,
                    "apprise_url": apprise_url or data.get("apprise_url", ""),
                    "apprise_tag": apprise_tag or data.get("apprise_tag", ""),
                }
    except (OSError, FileNotFoundError, pickle.UnpicklingError):
        pass

    # No saved config, check for setup token to claim access URL
    setup_token = os.environ.get("SIMPLEFIN_SETUP_TOKEN", "")
    if setup_token:
        access_url = claim_access_url(setup_token)
        if access_url:
            # Save to pickle for future runs
            save_config(data_path, access_url, apprise_url, apprise_tag)
            return {
                "access_url": access_url,
                "apprise_url": apprise_url,
                "apprise_tag": apprise_tag,
            }

    return None


def claim_access_url(setup_token: str) -> str | None:
    """
    Claim a SimpleFin access URL using a setup token.

    Args:
        setup_token: Base64-encoded setup token from SimpleFin

    Returns:
        Access URL string, or None if claim failed
    """
    try:
        claim_url = base64.b64decode(setup_token)
        response = requests.post(claim_url)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Failed to claim SimpleFin access URL: {e}")
        return None


def save_config(data_path: str, access_url: str, apprise_url: str, apprise_tag: str) -> None:
    """
    Save configuration to pickle file.

    Args:
        data_path: Path to the pickle file
        access_url: SimpleFin access URL
        apprise_url: Apprise API URL
        apprise_tag: Apprise notification tag
    """
    data = {
        "access_url": access_url,
        "apprise_url": apprise_url,
        "apprise_tag": apprise_tag,
    }

    # Ensure directory exists
    dir_name = os.path.dirname(data_path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)

    with open(data_path, "wb") as file:
        pickle.dump(data, file)
