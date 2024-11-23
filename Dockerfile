# Use the official Python image
FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

EXPOSE 8080

# Set the working directory in the container
WORKDIR /app

# Copy the project files to the container
COPY pyproject.toml .
COPY src/ src/

RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install --no-cache-dir .

# Set the default command to use Bash for easy exploration
CMD ["bash"]
