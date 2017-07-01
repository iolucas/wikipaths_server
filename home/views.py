from django.shortcuts import render

from django.http import HttpResponse

import json

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

            links, nodes_score = wikilinks.get_article_nb_links_and_scores_norm(request.GET['page'],2, 8)

            #links_scores = wikilinks.get_links_score(request.GET['page'], True)
            links_scores = Counter()

            # article, _ = wikilinks.get_or_create_article_by_url(request.GET['page'])

            # links_scores[article.title] = 1

            # #Populate links scores
            # for art_link in article.links.all():

            #     #Check if the url of the article url points to some article
            #     if art_link.link.article: #If so, get the article title
            #         link_title = art_link.link.article.title
            #     else: #If not, get the url only
            #         link_title = art_link.link.url
            #     links_scores[link_title] = art_link.score
            #     #page_links.append([article.title, art_link_url])

            # #page_links = [[request.GET['page'], link_text] for link_text, _ in links_scores][:10]
            # page_links = [[article.title, link_text] for link_text, _ in links_scores.most_common(15)]

            return render(request, "pages.html", {
                'links_scores': links_scores,
                'page_links': json.dumps(links),
                'links_score_dict_json': json.dumps(nodes_score)
            })
        except PageDoesNotExists:
            return render(request, "pages.html", {
                'links_scores': [("PAGE NOT FOUND", "")]
            })

    return render(request, "home.html")
