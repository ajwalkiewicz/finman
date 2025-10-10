# Use Python 3.10 slim image as base
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create directory for database and ensure proper permissions
RUN mkdir -p /app/data \
    && chmod 755 /app/data

# Create a non-root user for security
# RUN adduser --disabled-password --gecos '' --shell /bin/bash appuser \
#     && chown -R appuser:appuser /app
# USER appuser

# Expose the port the app runs on
EXPOSE 8010

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=10s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8010/docs')" || exit 1

# Command to run the application
CMD ["python", "run.py"]