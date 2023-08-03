# Use an official Python runtime as a parent image - for a list of others see https://hub.docker.com/_/python/
FROM python:3.10.6

# Set the working directory to /app/web_display - this is a directory that gets created in the image
WORKDIR /app/web_display

# Copy the current host directory contents into the container at /app/web_display
COPY . /app/web_display

# Upgrade pip to the latest version
RUN pip install --no-cache-dir --upgrade pip

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --use-feature=fast-deps -r requirements.txt

# Make port 50003 available to the world outside this container
EXPOSE 50003

# Run web_display.py when the container launches
CMD ["python", "web_display.py"]
