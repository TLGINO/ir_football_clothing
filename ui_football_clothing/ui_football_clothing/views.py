import json
import random

from django.http import HttpResponse
from django.shortcuts import render

from .index import Indexer
from .models import Item


def main(request):
    if request.method == "GET":
        return handle_get(request)
    return HttpResponse("Hello, world.")


def handle_get(request, data=None, number_results=25):
    if not data:
        data = list(Item.objects.all().values())

    context = {"data": json.dumps(data), "number_results": number_results}
    return render(request, "index.html", context)


def search(request):
    q = request.GET.get("search", "")
    q_item = request.GET.get("search_item", "")
    q_brand = request.GET.get("search_brand", "")
    price_params = request.GET.get("search_price", None)
    number_results = int(request.GET.get("number_results", 25))

    q_total = f"{q} {q_item} {q_brand}".strip()

    print("Q PRE _" + q_total + "_")
    if not q_total and not price_params:
        return handle_get(request, number_results=number_results)

    gte, lte = None, None
    if price_params:
        gte, lte = [int(p) if p.isdigit() else None for p in price_params.split("-")]

    indexer = Indexer()
    data = indexer.query_document_search(q=q_total, gte=gte, lte=lte)

    return handle_get(request, data=data, number_results=number_results)


def item(request):
    item_id = int(request.GET.get("id", 0))

    item = Item.objects.values().filter(id=item_id).first()

    data = Item.objects.values().filter(data=item["data"]).exclude(id=item_id).values()

    # Shuffle data and only take first x
    data = list(data)
    random.shuffle(data)
    data = data[:10]

    context = {"item": item, "data": data}
    return render(request, "item_info.html", context)
