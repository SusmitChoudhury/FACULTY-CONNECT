FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code and pre-compiled frontend assets
COPY . .

# Default port
ENV PORT=5000
ENV PYTHONUNBUFFERED=1

EXPOSE 5000

# Start production gunicorn server with multiple threads for high speed
CMD ["sh", "-c", "gunicorn --chdir backend app:app --bind 0.0.0.0:${PORT:-5000} --workers 2 --threads 4"]
