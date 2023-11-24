from django.http import HttpResponse
from django.shortcuts import render

from .index import Indexer


def main(request):
    if request.method == "GET":
        return handle_get(request)
    elif request.method == "POST":
        return handle_post(request)

    return HttpResponse("Hello, world. You're at the main index.")


def handle_get(request):
    context = {}
    return render(request, "index.html", context)


def handle_post(request):
    indexer = Indexer()
    response = indexer.query_document_search("adidas")
    # [TODO] handle search bar thing here
    return handle_get(request)
