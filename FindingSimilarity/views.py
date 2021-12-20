from django.shortcuts import render
from .handle import *


def index(request):
    context = dict()
    query = request.POST.get('query', None)

    if query:
        finding = FindingSimilarity(query)
        results = finding.get_results()

        context['results'] = results
        context['query'] = query

    return render(request, 'home/index.html', context)
