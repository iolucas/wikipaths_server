from django.shortcuts import render

from django.http import HttpResponse

import json

# Create your views here.

from wikipydia.exceptions import PageDoesNotExists

from . import wikilinks


def home_index(request):

    if 'page' in request.GET:
        try:
            links_scores = wikilinks.get_links_score(request.GET['page'], True)

            page_links = [[request.GET['page'], link_text] for link_text, _ in links_scores][:10]

            return render(request, "pages.html", {
                'links_scores': links_scores,
                'page_links': json.dumps(page_links),
                'links_score_dict_json': json.dumps(dict(links_scores))
            })
        except PageDoesNotExists:
            return render(request, "pages.html", {
                'links_scores': [("PAGE NOT FOUND", "")]
            })

    return render(request, "home.html")
