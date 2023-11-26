from django.db import models


class Item(models.Model):
    url = models.CharField(max_length=300)
    title = models.CharField(max_length=300)
    data = models.CharField(max_length=300)
    price = models.FloatField(default=-1)
    image = models.CharField(max_length=300)
