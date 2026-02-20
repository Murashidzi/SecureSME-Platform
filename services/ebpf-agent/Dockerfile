# We use a standard Debian base because it plays nice with BCC tools
FROM debian:bookworm-slim

# 1. Install Dependencies
# we need bpfcc-tools' and 'python3-bpfcc' for the magic
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    bpfcc-tools \
    linux-headers-generic \
    kmod \
    && rm -rf /var/lib/apt/lists/*

# 2. Set working directory
WORKDIR /app

# 3. Copy files
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt --break-system-packages

COPY app /app

# 4. Run the monitor
# We use unbuffered output so we see logs instantly
CMD ["python3", "-u", "monitor.py"]
