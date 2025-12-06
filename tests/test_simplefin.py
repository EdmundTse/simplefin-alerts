"""Tests for SimpleFin API client."""

from simplefin_alerts.simplefin import parse_access_url


class TestParseAccessUrl:
    """Tests for parse_access_url function."""

    def test_parse_standard_url(self):
        """Should correctly parse a standard access URL."""
        url = "https://username:password@api.simplefin.org/simplefin"

        base_url, username, password = parse_access_url(url)

        assert base_url == "https://api.simplefin.org/simplefin"
        assert username == "username"
        assert password == "password"

    def test_parse_url_with_special_chars_in_password(self):
        """Should handle special characters in password."""
        url = "https://user:p@ss:word@api.simplefin.org"

        base_url, username, password = parse_access_url(url)

        assert base_url == "https://api.simplefin.org"
        assert username == "user"
        assert password == "p@ss:word"
