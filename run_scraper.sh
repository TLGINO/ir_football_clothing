#!/bin/bash

echo "Scraping data for Adidas"
scrapy crawl adidas -o data/adidas.json
echo "Done"

echo "Scraping data for Decathlon"
scrapy crawl decathlon -o data/decathlon.json
echo "Done"