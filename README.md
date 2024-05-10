### IR Football Clothing Project

Project developed during the Information Retrival Course.
Objective of the project was to scrape 3 different websites for football clothing and then display the scraped data on our own website, implementing search functions / indexing on said data.

### Useful links:

[Scrapy Tutorial](https://docs.scrapy.org/en/latest/intro/tutorial.html)



### How to use:
Create a python virtual env, here I am using pyenv:

```sh
pyenv virtualenv ir_football_clothing

```

Make sure it is activated, it should return something similar to this:

```sh
pip3 -V
pip 23.2.1 from /home/martin/.pyenv/versions/ir_football_clothing/lib/python3.10/site-packages/pip (python 3.10)
```

Install python dependencies:
```sh
pip3 install -r requirements.txt
```

Run the scraper:
```sh
sh run_scraper.sh
```

The resulting .json data will be stored in /data/[site_name].json

Run the site:
```sh
sh run_ui.sh
```


### How to contribute:

For code quality / formatting run:
```sh
black .
isort --profile black .
```
