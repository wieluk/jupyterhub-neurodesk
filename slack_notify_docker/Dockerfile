FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy the Python script into the container
COPY notify_users.py .

# Install necessary Python packages
RUN pip install requests schedule

# Command to run the Python script
CMD ["python", "-u" ,"notify_users.py"]
