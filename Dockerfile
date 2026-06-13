FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project subfolders
COPY channel_service/ ./channel_service/
COPY crm_backend/ ./crm_backend/

# Expose both local ports to the network container
EXPOSE 8000
EXPOSE 8001

# Boot both services sequentially on startup
CMD python channel_service/channel_service.py & python crm_backend/main.py