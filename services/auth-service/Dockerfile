# Use an official lightweight Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Set environment variables (Prevents Python from writing pyc files to disc)
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONNUNBUFFERED 2

#Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#Copy project
COPY . .

#Run the application
CMD ["python", "run.py"]
