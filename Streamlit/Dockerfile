# Use the official Python base image
FROM python:3.12-slim

RUN apt-get update && apt-get install gcc -y

# Set the working directory in the container
WORKDIR /app

# Copy the entire current directory to the container
COPY . .

RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["streamlit", "run", "Lily.py"]
