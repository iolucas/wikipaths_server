from django.shortcuts import render

from django.http import HttpResponse

import json

import requests as httpRequests
from urllib.parse import quote

# Create your views here.

from wikipydia.exceptions import PageDoesNotExists

from . import wikilinks

from collections import Counter

def home_index(request):

    if 'debug' in request.GET:
        debug_url = request.GET['debug']

        links, nodes_score = wikilinks.get_article_nb_links_and_scores_norm(debug_url)

        return HttpResponse(json.dumps(links)+ "\n\n\n" + json.dumps(nodes_score))

    if 'page' in request.GET:
        try:

            links, nodes_score = wikilinks.get_article_nb_links_and_scores_norm(request.GET['page'], 1, 25)

            #links_scores = wikilinks.get_links_score(request.GET['page'], True)
            links_scores = Counter()

            return render(request, "pages.html", {
                'page': request.GET['page'],
                'links_scores': links_scores,
                'page_links': json.dumps(links),
                'links_score_dict_json': json.dumps(nodes_score)
            })
        except PageDoesNotExists:
            return render(request, "pages.html", {
                'links_scores': [("PAGE NOT FOUND", "")]
            })

    return render(request, "home3.html")

def search_article(request):

    if 'q' not in request.GET:
        return HttpResponse("[]")

    # "http://en.wikipedia.org/w/api.php?action=opensearch&namespace=0&format=json&redirects=resolve&limit=10&search=C%2b%2b"
    # https://www.mediawiki.org/wiki/API:Opensearch

    lang = "en"
    quoted_query = quote(request.GET['q'])

    req_params = [
        'action=opensearch',
        'namespace=0',
        'format=json',
        'redirects=resolve',
        'limit=10',
        'search=' + quoted_query
    ]

    wikipedia_api_url = "https://" + lang + ".wikipedia.org/w/api.php?" + "&".join(req_params)

    jsonResult = httpRequests.get(wikipedia_api_url, timeout=60).json()

    #Zip results to a better format
    zippedJson = json.dumps(list(zip(jsonResult[1], jsonResult[2], jsonResult[3])))

    return HttpResponse(zippedJson)