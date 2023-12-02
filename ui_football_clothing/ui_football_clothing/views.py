import random

from django.http import HttpResponse
from django.shortcuts import render

from .index import Indexer
from .models import Item


def main(request):
    if request.method == "GET":
        return handle_get(request)
    return HttpResponse("Hello, world.")


def handle_get(request, data=None):
    if not data:
        data_pre = list(Item.objects.all().values())
        data = list(data_pre)
        random.shuffle(data)

    context = {"data": data}
    return render(request, "index.html", context)


def search(request):
    q = request.POST.get("search", "")
    q_item = request.POST.get("search_item", "")
    q_brand = request.POST.get("search_brand", "")
    price_params = request.POST.get("search_price", None)

    q_total = f"{q} {q_item} {q_brand}".strip()

    print("Q PRE _" + q_total + "_")
    if not q_total and not price_params:
        return handle_get(request)

    gte, lte = None, None
    if price_params:
        gte, lte = [int(p) if p.isdigit() else None for p in price_params.split("-")]

    indexer = Indexer()
    data = indexer.query_document_search(q=q_total, gte=gte, lte=lte)

    return handle_get(request, data)
