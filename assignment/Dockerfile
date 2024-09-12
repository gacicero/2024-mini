# Use the official Python image as a base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose port 8080 to match Cloud Run's expected port
EXPOSE 8080

# Command to run the Flask app
CMD ["gunicorn", "-b", ":8080", "app:app"]
