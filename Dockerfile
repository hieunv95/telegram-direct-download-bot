FROM python:3.10-slim

WORKDIR /app

# Install supervisor to manage both processes
RUN apt-get update && apt-get install -y supervisor

# Copy application files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create supervisor config file to run both services
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expose port
EXPOSE 8000

# Start supervisor to manage processes
CMD ["/usr/bin/supervisord"]
