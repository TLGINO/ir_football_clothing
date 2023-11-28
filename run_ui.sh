#!/bin/bash

cd ui_football_clothing

# Index the data before running the server
python3 ui_football_clothing/index.py

# DB wipe
python3 manage.py makemigrations ui_football_clothing
python3 manage.py migrate ui_football_clothing

# Create fixtures (populate DB with data)
python3 fixture.py
python3 manage.py loaddata data.json

# Run the server
python3 manage.py runserver 8080