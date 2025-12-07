FROM python:3

WORKDIR /app

# Install cron
RUN apt-get update && apt-get install -y --no-install-recommends cron \
    && rm -rf /var/lib/apt/lists/*

# Copy project files for installation
COPY pyproject.toml .
COPY src/ src/

# Install the package
RUN pip install --no-cache-dir .

# Create volume mount point for persistent data
VOLUME /data

# Set environment variable for data file location
ENV SIMPLEFIN_DATA_PATH=/data/simplefin-data.pickle

# Default schedule: run at 8am daily (cron format)
ENV SCHEDULE="0 8 * * *"

# Copy entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
