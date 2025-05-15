FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install dependencies early to leverage caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the script into the container
COPY src/read_secret.py .

# Run script
CMD ["python", "./read_secret.py"]
