from django.shortcuts import render

from django.http import HttpResponse

import json

# Create your views here.

from wikipydia.exceptions import PageDoesNotExists

from . import wikilinks

from collections import Counter

def home_index(request):

    if 'page' in request.GET:
        try:
            #links_scores = wikilinks.get_links_score(request.GET['page'], True)
            links_scores = Counter()

            article, _ = wikilinks.get_or_create_article_by_url(request.GET['page'])

            #Populate links scores
            for art_link in article.links.all():
                art_link_url = art_link.link.url
                links_scores[art_link_url] = art_link.score
                #page_links.append([article.title, art_link_url])

            #page_links = [[request.GET['page'], link_text] for link_text, _ in links_scores][:10]
            page_links = [[article.title, link_text] for link_text, _ in links_scores.most_common(10)]

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
