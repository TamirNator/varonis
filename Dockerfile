FROM python:3.9-slim

WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app

# Define build-time variable
ARG DATABASE_URL

# Set environment variable
ENV DATABASE_URL=${DATABASE_URL}

EXPOSE 5000

CMD ["python", "app.py"]