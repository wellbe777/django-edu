# Pull official base Python Docker image
FROM python:3.12.6

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libmemcached-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*
    
# Install setuptools
RUN pip install --upgrade pip setuptools

# Set environment variables to prevent .pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Install Python dependencies
RUN pip install --upgrade pip
COPY requirements_edu-r.txt .
RUN pip install -r requirements_edu-r.txt

# Copy Django project files into the container
COPY . .
