from django.shortcuts import render

from django.http import HttpResponse

# Create your views here.

from . import wikilinks


def home_index(request):

    if 'page' in request.GET:

        links_scores = wikilinks.get_links_score(request.GET['page'])

        return render(request, "pages.html", {
            'links_scores': links_scores
        })

    return render(request, "home.html") 


