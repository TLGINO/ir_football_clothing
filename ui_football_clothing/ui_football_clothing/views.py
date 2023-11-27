import random

from django.http import HttpResponse
from django.shortcuts import render

from .index import Indexer
from .models import Item


def main(request):
    if request.method == "GET":
        return handle_get(request)
    elif request.method == "POST":
        return handle_post(request)

    return HttpResponse("Hello, world. You're at the main index.")


def handle_get(request, data=None):
    if not data:
        data_pre = list(Item.objects.all().values())
        data = list(data_pre)
        random.shuffle(data)

    context = {"data": data}
    return render(request, "index.html", context)


def search(request):
    q = request.POST.get("search", None)
    price_params = request.POST.get("price", None)

    if not q and not price_params:
        return handle_get(request)

    gte, lte = None, None
    if price_params:
        gte, lte = [int(p) if p.isdigit() else None for p in price_params.split("-")]
    indexer = Indexer()
    data = indexer.query_document_search(q=q, gte=gte, lte=lte)

    return handle_get(request, data)


def handle_post(request):
    return handle_get(request)
