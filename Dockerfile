# Use the official Python base image
FROM python:3.13-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the Python dependencies
RUN pip install -r requirements.txt

# Copy the application code to the working directory (for build time)
COPY ./src /app
COPY .env /app

# Expose the port on which the application will run
EXPOSE 8000

# Set PYTHONPATH to ensure modules can be found
ENV PYTHONPATH=/app

# Run the FastAPI application using uvicorn server (como en el ejemplo del profesor)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]