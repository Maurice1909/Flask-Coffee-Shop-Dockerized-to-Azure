# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app

# Expose port 8000 (Gunicorn's default)
EXPOSE 8000

# Command to run the application using Gunicorn
# 'app:app' refers to the 'app' Flask instance inside 'app.py'
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
