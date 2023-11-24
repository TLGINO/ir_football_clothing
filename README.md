### Useful links:

[Scrapy Tutorial](https://docs.scrapy.org/en/latest/intro/tutorial.html)



### How to use:
Create a python virtual env, here I am using pyenv:

```sh
pyenv virtualenv ir_football_clothing
```

Make sure it is activated, it should return something similar to this:

```sh
pip -V
pip 23.2.1 from /home/martin/.pyenv/versions/ir_football_clothing/lib/python3.10/site-packages/pip (python 3.10)
```

Install python dependencies:
```sh
pip install -r requirements.txt
```

Run the scraper:
```sh
sh run_scraper.sh
```

The resulting .json data will be store in /data/[site_name].json

### How to contribute:

For code quality / formatting run:
```sh
black .
isort --profile black .
```