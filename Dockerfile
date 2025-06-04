# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages (if your app had external dependencies, you'd list them in a requirements.txt)
# In this simple case, there are no external Python dependencies beyond what's in the standard library.
# If you had a requirements.txt, you would uncomment the following line:
# RUN pip install -r requirements.txt

# Command to run the application
CMD ["python", "original_coffee.py"]
