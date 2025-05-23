# Use Python 3.9 as base image
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy application files
COPY requirements.txt .
COPY app.py .
COPY House_price_prediction.pkl .
COPY templates ./templates  

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Flask application port
EXPOSE 5001

# Run the application
CMD ["python", "app.py"]
