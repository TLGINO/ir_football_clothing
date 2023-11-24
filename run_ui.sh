#!/bin/bash

docker run -d -p 9200:9200 -p 9600:9600 -e "discovery.type=single-node" opensearchproject/opensearch:latest

cd ui_football_clothing


python3 ui_football_clothing/index.py
python3 manage.py runserver 8080