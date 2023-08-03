# Use an official Python runtime as a parent image - for a list of others see https://hub.docker.com/_/python/
FROM python:3.10.6

# Set the working directory to /app/text_analyser - this is a directory that gets created in the image
WORKDIR /app/text_analyser

# Copy the current host directory contents into the container at /app/text_analyser
COPY . /app/text_analyser

# Upgrade pip to the latest version
RUN pip install --no-cache-dir --upgrade pip

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --use-feature=fast-deps -r requirements.txt

# Install prometheus for monitoring
RUN pip install prometheus_client

# Make port 50001 available to the world outside this container
EXPOSE 50001

# Run text_analyser.py when the container launches
CMD ["python", "text_analyser.py"]
