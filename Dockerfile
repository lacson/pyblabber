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
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy other files
COPY . .

# Run script
CMD [ "python", "./pyblabber.py" ]

