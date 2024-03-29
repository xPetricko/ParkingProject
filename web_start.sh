#!/bin/bash

# Create local data folder
echo "Create local data folder for netmodel"
mkdir -p ./data/netmodel


echo "Installing dependencies"
pip3 install -r ./requirements.txt

# Collect static files
echo "Collect static files"
python3 manage.py collectstatic --noinput


# Get database migrations
echo "Get database migrations"
python3 manage.py makemigrations

# Apply database migrations
echo "Apply database migrations"
python3 manage.py migrate

# Start server
echo "Starting server"
python3 manage.py runserver 0.0.0.0:8000


