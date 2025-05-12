# Use an official Python image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the full app, including cookies
COPY . .

# Expose the default Flask port
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]
