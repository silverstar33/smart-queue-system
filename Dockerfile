# Use official Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app


# Copy source files
COPY backend/ /app/

# Copy requirements and install
COPY backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose FastAPI default port
EXPOSE 8000

# Run FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
