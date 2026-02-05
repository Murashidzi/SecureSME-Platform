# Use Alpine (The "Tiny & Secure" Linux)
FROM python:3.12-alpine

# Set working directory
WORKDIR /app

# Set environment variables (Prevents Python from writing pyc files to disc)
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONNUNBUFFERED 2

# ALPINE SECURITY & SETUP
# 1. Update the OS (Alpine uses 'apk' instead of 'apt')
# 2. Install build dependencies for Postgres (gcc, musl-dev, etc.)
RUN apk update && apk upgrade && \
    apk add --no-cache \
    postgresql-dev \
    gcc \
    python3-dev \
    musl-dev \
    libffi-dev

# 3. Upgrade pip to fix CVE-2025-8869 (Medium)
RUN pip install --upgrade pip

#Install dependencies (application setup)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#Copy project
COPY . .

#Run the application
CMD ["python", "run.py"]
