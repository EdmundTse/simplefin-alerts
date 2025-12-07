#!/bin/sh

# Set up cron schedule
echo "Setting up cron schedule: $SCHEDULE"

# Create cron job with environment variables
{
    echo "SIMPLEFIN_DATA_PATH=$SIMPLEFIN_DATA_PATH"
    echo "SIMPLEFIN_SETUP_TOKEN=$SIMPLEFIN_SETUP_TOKEN"
    echo "APPRISE_URL=$APPRISE_URL"
    echo "APPRISE_TAG=$APPRISE_TAG"
    echo ""
    echo "$SCHEDULE root cd /app && python -m simplefin_alerts >> /proc/1/fd/1 2>&1"
} > /etc/cron.d/simplefin-alerts

chmod 0644 /etc/cron.d/simplefin-alerts

# Start cron in foreground
echo "Starting cron daemon..."
cron -f
