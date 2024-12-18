# Base image
FROM python:3.9-slim

# Set work directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the port your app runs on
EXPOSE 8501

# # Set default command to run the app
# CMD ["streamlit", "run", "scripts/dashboard.py"]