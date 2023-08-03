# Use an official Python runtime as a parent image - for a list of others see https://hub.docker.com/_/python/
FROM python:3.10.6

# Set the working directory to /app/text_reader - this is a directory that gets created in the image
WORKDIR /app/text_reader

# Copy the current host directory contents into the container at /app/text_reader
COPY . /app/text_reader

# Upgrade pip to the latest version
RUN pip install --no-cache-dir --upgrade pip

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --use-feature=fast-deps -r requirements.txt

# Run text_reader.py when the container launches
CMD ["python", "text_reader.py"]