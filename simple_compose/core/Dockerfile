# syntax=docker/dockerfile:1

FROM python:3.11-slim

# Prevent .pyc files and ensure logs show immediately
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies (curl handy for health checks)
RUN apt-get update && apt-get install -y --no-install-recommends curl \
 && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your entrypoint script
COPY deploy_core.py .

# Expose Control Plane port (default = 8000)
EXPOSE 8000

# Run deploy_core
CMD ["python", "-u", "deploy_core.py"]
