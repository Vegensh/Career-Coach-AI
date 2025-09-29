# Use official Python base image
FROM python:3.10-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements.txt first (for caching dependencies)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files
COPY . .

# Expose Streamlit's default port
EXPOSE 8501

# Streamlit needs this to run properly inside Docker
ENV PYTHONUNBUFFERED=1 \
    STREAMLIT_PREFER_ENV=true \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ENABLECORS=false

# Run Streamlit app
CMD ["streamlit", "run", "app.py"]
