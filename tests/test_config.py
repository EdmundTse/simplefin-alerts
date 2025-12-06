"""Tests for configuration module."""

import os
import pickle
import tempfile
from unittest import mock

from simplefin_alerts.config import load_config


class TestLoadConfig:
    """Tests for load_config function."""

    def test_load_from_pickle_file(self):
        """Should load configuration from pickle file."""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pickle") as f:
            data = {
                "access_url": "https://file:user@api.example.com",
                "apprise_url": "https://file.apprise.com",
                "apprise_tag": "file-tag",
            }
            pickle.dump(data, f)
            temp_path = f.name

        try:
            with mock.patch.dict(os.environ, {}, clear=True):
                # Clear relevant env vars
                for key in [
                    "SIMPLEFIN_SETUP_TOKEN",
                    "APPRISE_URL",
                    "APPRISE_TAG",
                ]:
                    os.environ.pop(key, None)

                config = load_config(temp_path)

                assert config["access_url"] == "https://file:user@api.example.com"
                assert config["apprise_url"] == "https://file.apprise.com"
                assert config["apprise_tag"] == "file-tag"
        finally:
            os.unlink(temp_path)

    def test_env_apprise_overrides_pickle(self):
        """Should use env var Apprise settings over pickle file values."""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pickle") as f:
            data = {
                "access_url": "https://file:user@api.example.com",
                "apprise_url": "https://old.apprise.com",
                "apprise_tag": "old-tag",
            }
            pickle.dump(data, f)
            temp_path = f.name

        try:
            with mock.patch.dict(
                os.environ,
                {
                    "APPRISE_URL": "https://new.apprise.com",
                    "APPRISE_TAG": "new-tag",
                },
                clear=True,
            ):
                config = load_config(temp_path)

                assert config["access_url"] == "https://file:user@api.example.com"
                assert config["apprise_url"] == "https://new.apprise.com"
                assert config["apprise_tag"] == "new-tag"
        finally:
            os.unlink(temp_path)

    def test_returns_none_when_no_config(self):
        """Should return None when no configuration available."""
        with mock.patch.dict(os.environ, {}, clear=True):
            for key in [
                "SIMPLEFIN_SETUP_TOKEN",
                "APPRISE_URL",
                "APPRISE_TAG",
            ]:
                os.environ.pop(key, None)

            config = load_config("nonexistent.pickle")

            assert config is None
