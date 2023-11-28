#!/bin/bash

# Removes all files in the /data dir except .gitkeep
find data -type f ! -name ".gitkeep" -exec rm -v {} \;


echo "Scraping data for Adidas"
scrapy crawl adidas -o data/adidas.json
echo "Done"

echo "Scraping data for Decathlon"
scrapy crawl decathlon -o data/decathlon.json
echo "Done"

echo "Scraping data for Sports Direct"
scrapy crawl sports_direct -o data/sports_direct.json
echo "Done"