# Use Python 3.12 slim image as base
FROM python:3.12-slim

# Install system dependencies required for swisseph and other packages
# libsqlite3 is needed by swisseph for ephemeris calculations
# Other packages support various dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libsqlite3-0 \
    libsqlite3-dev \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Expose port (Railway will override this)
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health').read()" || exit 1

# Run the deployment script
CMD ["python", "deploy_production.py"]
