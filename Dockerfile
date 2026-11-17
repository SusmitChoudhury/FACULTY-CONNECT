FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code and pre-compiled frontend assets
COPY . .

# Grant write permissions for SQLite database across all cloud platforms (HF Spaces / Render / Railway)
RUN chmod -R 777 /app

# Default port (Hugging Face Spaces uses 7860, Render uses dynamic $PORT)
ENV PORT=7860
ENV PYTHONUNBUFFERED=1

EXPOSE 7860
EXPOSE 5000

# Start production gunicorn server with multiple threads for high speed
CMD ["sh", "-c", "gunicorn --chdir backend app:app --bind 0.0.0.0:${PORT:-7860} --workers 2 --threads 4"]
