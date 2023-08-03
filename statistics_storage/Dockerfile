# Use an official Python runtime as a parent image - for a list of others see https://hub.docker.com/_/python/
FROM python:3.10.6

# Set the working directory to /app/statistics_storage - this is a directory that gets created in the image
WORKDIR /app/statistics_storage

# Copy the current host directory contents into the container at /app/statistics_storage
COPY . /app/statistics_storage

# Upgrade pip to the latest version
RUN pip install --no-cache-dir --upgrade pip

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --use-feature=fast-deps -r requirements.txt

# Make port 50002 available to the world outside this container
EXPOSE 50002

# Run statistics_storage.py when the container launches
CMD ["python", "statistics_storage.py"]
