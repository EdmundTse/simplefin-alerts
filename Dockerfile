FROM python:3.12-slim

WORKDIR /app

# Copy project files for installation
COPY pyproject.toml .
COPY src/ src/

# Install the package
RUN pip install --no-cache-dir .

# Create volume mount point for persistent data
VOLUME /data

# Set environment variable for data file location
ENV SIMPLEFIN_DATA_PATH=/data/simplefin-data.pickle

# Run as module
CMD ["python", "-m", "simplefin_alerts"]
