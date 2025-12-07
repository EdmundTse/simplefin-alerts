# SimpleFin Alerts

This tool gives a quick check for SimpleFin accounts in Error Status, with optional Apprise notifications.

## Setup

* You will need to generate a SimpleFin Setup Token, and have that handy.

* If you want to use Apprise Notifications, you will need to have the [Apprise API](https://github.com/caronc/apprise-api) installed and running, and have the URL handy (typically in the form: https://example.com/notify/apprise ), as well as the Apprise Tag created and configured that you want to send it to.

* The status of the accounts is printed to terminal, where the program is run, so it can be used manually. If you decide to use Apprise API, then you can set a system cron and it will send the status of the accounts via the chosen Apprise tag.

## Docker Usage

### Quick Start with Docker Compose

1. Copy the example environment file and configure it:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your credentials:
   ```
   # Setup token for first run (will be exchanged for access URL and saved)
   SIMPLEFIN_SETUP_TOKEN=your-base64-setup-token
   
   # Optional: Apprise notifications (omit to disable)
   APPRISE_URL=https://example.com/notify/apprise
   APPRISE_TAG=alerts
   
   # Optional: Custom schedule (default: daily at 8am)
   SCHEDULE=0 8 * * *
   ```

3. Build and run:
   ```bash
   docker compose up --build -d
   ```

The container runs with a built-in cron scheduler (default: daily at 8am).

### Build Docker Image Manually

```bash
docker build -t simplefin-alerts .
```

### Run with Environment Variables

```bash
# Long-running container with built-in scheduler (default: 8am daily)
docker run -d \
  -e SIMPLEFIN_SETUP_TOKEN="your-setup-token" \
  -e SCHEDULE="0 8 * * *" \
  -v ./data:/data \
  simplefin-alerts

# Custom schedule: every 6 hours
docker run -d \
  -e SCHEDULE="0 */6 * * *" \
  -v ./data:/data \
  simplefin-alerts
```

## Local Usage (without Docker)

### Install from source

```bash
pip install -e .
```

### Run the application

```bash
# First run: set setup token to claim access URL
export SIMPLEFIN_SETUP_TOKEN="your-setup-token"

# Optional: enable Apprise notifications
export APPRISE_URL="https://example.com/notify/apprise"
export APPRISE_TAG="alerts"

# Run the application
simplefin-alerts

# Or as a Python module
python -m simplefin_alerts

# Subsequent runs: access URL is loaded from simplefin-data.pickle
# (no need to set SIMPLEFIN_SETUP_TOKEN again)
```

## Development

### Setup development environment

```bash
pip install -e ".[dev]"
```

### Run tests

```bash
pytest
```

### Run linter

```bash
ruff check src/ tests/
```

## Project Structure

```
simplefin-alerts/
├── src/
│   └── simplefin_alerts/
│       ├── __init__.py
│       ├── __main__.py      # Entry point for python -m
│       ├── cli.py           # Command-line interface
│       ├── config.py        # Configuration management
│       ├── notifications.py # Apprise integration
│       └── simplefin.py     # SimpleFin API client
├── tests/
│   ├── __init__.py
│   ├── test_config.py
│   └── test_simplefin.py
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
└── README.md
```
