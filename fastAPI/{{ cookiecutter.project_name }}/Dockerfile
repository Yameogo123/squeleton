# Use an official Python runtime as the base image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Install the package in editable mode
RUN pip install -e .

# Expose ports for FastAPI 
# FastAPI
EXPOSE 8000  

# Command to run the FastAPI backend
CMD ["python", "app/main.py"]