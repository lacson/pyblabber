# Dockerfile for pyblabber
# Jonathan Lacson
# CS 2304 Spring 2019

# Python is love, Python is life.
FROM python:latest

# So people know who to yell at when it doesn't work
LABEL maintainer="lacson@vt.edu"

# Set workdir appropriately
WORKDIR /usr/src/app

# Install the packages we need
COPY src/requirements.txt ./
RUN pip install --no-cache-dir -r src/requirements.txt

# Declare the port to use (and pass it as an env var to python)
ARG port=5000
ENV FLASK_PORT=${port}

# Expose said port
EXPOSE ${port}:${port}

# Copy other files
COPY src/. .

# Run script
CMD [ "python", "./pyblabber.py" ]

