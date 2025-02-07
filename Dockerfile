# Use the official Python image from the Docker Hub
FROM python:3

# Set the working directory in the container to /app
WORKDIR /app

# Copy the requirements.txt file from the local machine to the container
COPY requirements.txt .

# Install the Python dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code from the local machine to the container
COPY . .

# Expose port 8000 to allow traffic to the container
EXPOSE 8000

# Run the application using uvicorn
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]
