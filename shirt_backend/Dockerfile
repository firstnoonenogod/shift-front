# Use Alpine-based Python image which is extremely lightweight
FROM python:3.9-alpine

# Set working directory
WORKDIR /app

# Reduce Docker image size by preventing Python from writing .pyc files and disabling pip cache
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on

# Install build dependencies needed for certain Python packages, then clean up
RUN apk add --no-cache --virtual .build-deps gcc musl-dev && \
    apk add --no-cache libffi-dev

# Copy requirements file first for better cache utilization
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt && \
    apk del .build-deps && pip install pydantic[email]

# Copy application code
COPY . .

# Expose the port the app will run on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
