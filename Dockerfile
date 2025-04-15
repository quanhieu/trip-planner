# Dockerfile
FROM python:3.11-slim

# Đặt thư mục làm việc
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
  build-essential \
  curl \
  && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create a non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Mở các cổng cần thiết (các cổng cho các agent và Streamlit)
EXPOSE 8000 8001 8002 8003 8004 8501

# Default command (can be overridden in docker-compose.yml)
CMD ["python", "-m", "agents.orchestrator_agent"]
