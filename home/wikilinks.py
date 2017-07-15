from wikipydia import wikipedia, wikidb
from wikipydia.url import QuotedURL, UnquotedURL
import wikipydia.wikilinks as WL 
from collections import Counter, defaultdict
import re

from wikipydia.exceptions import PageDoesNotExists

import json

from urllib.parse import unquote

#from wikidb import WikiDb

#wiki_db = wikidb.WikiDb()

from .models import WikiArticle as WA, WikiUrl, ArticleLink, JsonCache, JsonCacheUrl, JsonCacheData

def unquote_and_remove_underlines(str):
    return str
    # return unquote(str).replace("_", " ").replace("'", "\\'")

def get_links_score_cache(url):

    urlObj = UnquotedURL(url)

    # art = wikipedia.get_article_by_href(urlObj)
    # links_scores = WL.get_article_links_score(art) #Already sorted
    # round_links_scores = [(link, round(score, 2)) for link, score in links_scores]
    # return json.dumps(dict(round_links_scores))

    #Return the cache json if found
    for cacheUrl in JsonCacheUrl.objects.filter(url=urlObj.quoted):
        return cacheUrl.cache.json

    #Download article if not found
    try:
        art = wikipedia.get_article_by_href(urlObj)
    except PageDoesNotExists:
        return None

    #Get or create the json cache from this article
    try:
        cache = JsonCacheData.objects.get(pageid=art.page_id())
    except JsonCacheData.DoesNotExist:
        links_scores = WL.get_article_links_score(art) #Already sorted
        #Normalize things
        round_links_scores = [(unquote_and_remove_underlines(link), round(score, 2)) for link, score in links_scores]
        links_scores_json = json.dumps(dict(round_links_scores[:100]))
        cache = JsonCacheData.objects.create(pageid=art.page_id(), json=links_scores_json)

    #Create cacheUrl for this cache
    newCacheUrl = JsonCacheUrl.objects.create(url=urlObj.quoted, cache=cache)

    return newCacheUrl.cache.json

def normalize_counter(counter_dict, method="higher_count"):
    if method == "higher_count":
        norm_value = counter_dict.most_common(1)[0][1]
    elif method == "sum_one":
        norm_value = sum(counter_dict.values())

    norm_counter_dict = Counter()
    for key, value in counter_dict.items():
        norm_counter_dict[key] = value / norm_value

    return norm_counter_dict

def get_article_nb_links_and_scores_norm(url, max_deep=1, top_n=1):
    """Function to normalize _get_article_nb_links_and_scores function."""
    links_dict, score_counter = _get_article_nb_links_and_scores(url, max_deep=max_deep, top_n=top_n)

    all_links = list()
    for links in links_dict.values():
        all_links += list(links)

    norm_score_counter = normalize_counter(score_counter)

    return all_links, norm_score_counter


def _get_article_nb_links_and_scores(url, links_dict=None, score_counter=None, base_score=1, current_deep=1, max_deep=1, top_n=10):
    """Function to accumulate article neighborhood scores recursively."""

    article, _ = get_or_create_article_by_url(url)
    
    # if article == None:
    #     return None, None

    #Starts the objects if this is the first iteration
    if score_counter == None:
        score_counter = Counter()
        score_counter[article.title] = 1

    if links_dict == None:
        links_dict = dict()


    #If this article has not already been proceced, init its link dict
    if article.title not in links_dict:
        links_dict[article.title] = set()
    else: #else, return and skip it
        return

    art_link_scores_counter = Counter()
    #Get article links scores
    for art_link in article.links.all():
        art_link_scores_counter[art_link] = art_link.score

    #Normalize links raw counts
    art_link_scores_counter = normalize_counter(art_link_scores_counter)

    #Iterate the top n article links
    for art_link, art_link_score in art_link_scores_counter.most_common(top_n):

        #If we haven't reached the max deep, keeps the recursion passing the new objects
        if current_deep < max_deep:
            art_link_url = art_link.link.url
            _get_article_nb_links_and_scores(art_link_url, links_dict, score_counter, art_link_score, current_deep+1, max_deep, top_n)
            #art_link_art, _ = get_or_create_article_by_url(art_link_url)

        #Get proper title and append link and score
        art_link_title = get_artlink_title(art_link)
        links_dict[article.title].add((article.title, art_link_title))
        score_counter[art_link_title] += art_link_score * base_score

    return links_dict, score_counter



def get_artlink_title(art_link):
    #Since the art_link is loaded at the begging
    #if any change occurrs on its derived objects, it must be reloaded
    #The only problem is that it do not find new articles on its wikiurl
    #It is not a major problem since the next time it loads, it fix it, so we will keep like this

    #Check if the url of the article url points to some article
    if art_link.link.article: #If so, get the article title
        return art_link.link.article.title

    return art_link.link.url



def get_or_create_article_by_url(url):
    """Return article that the passed url-lang points to. If it does not exists, create it."""

    #Get or create the current url
    wiki_url, url_created = getOrCreateWikiUrl(url)

    article_created_flag = False

    #If the url was not created and it points to an article, return the article
    #Checks the url_created flag first for performance matters
    if not url_created and wiki_url.article:
        return wiki_url.article, False

    #If the url does not point to anything, get page data
    #try:
    art = wikipedia.get_article_by_href(UnquotedURL(url))
    #except:
        #return None, False

    #Try to get the article with pageId, if not found, create it 
    try:
        article = WA.objects.get(pageid=art.page_id())
    except WA.DoesNotExist:
        article_created_flag = True
        article = WA(title=art.title(), pageid=art.page_id())

        #Save new article before adding new stuff to it
        article.save()

        #Get links scores
        links_scores = get_art_links_score(art, normalize=False)

        #Create article links
        for link, score in links_scores:
            link_wiki_url, _ = getOrCreateWikiUrl(link)
            article_link = ArticleLink(link=link_wiki_url, score=score)
            article_link.save()
            article.links.add(article_link)

        article.save()

        #Set the article to the current url and save
        wiki_url.article = article
        wiki_url.save()

    #return the article and the created flag
    return article, article_created_flag

def getOrCreateWikiUrl(url):
    """Return the passed arguments and if it not exists, try to create it."""

    createdFlag = False

    #Try to get the article wikiurl
    try:
        wikiUrl = WikiUrl.objects.get(url=url)
    #If it does not exists, create it and set created flag
    except WikiUrl.DoesNotExist:
        wikiUrl = WikiUrl(url=url)
        wikiUrl.save()
        createdFlag = True

    return wikiUrl, createdFlag




def get_links_score(href, normalize=False):
    art = wikipedia.get_article_by_href(href)
    return get_art_links_score(art, normalize)

def get_art_links_score(art, normalize=False):
    """Get wiki article links score."""
    
    #art = wikipedia.get_article_by_href(href)
    # art, downloaded = wiki_db.get_article_by_href(href)
    # if downloaded:
    #     wiki_db.save()


    html_links = art.links()
    html_text = re.sub(r"[\n]+", " ", art.text())

    links_text_counter = Counter() #Link text counter
    links_text_dict = defaultdict(list)
    links_case_dict = dict() #Dictionary to store the link original case

    for link, text in html_links:
        links_case_dict[link.lower()] = link
        links_text_dict[text.lower()].append(link.lower())

    for l_text in links_text_dict.keys():
        matches = re.findall('[^a-zA-Z0-9_]' + re.escape(l_text) + '[^a-zA-Z0-9_]', html_text, re.IGNORECASE)
        for _ in range(len(matches)):
            links_weight = 1.0 / len(links_text_dict[l_text])
            for link in links_text_dict[l_text]:
                links_text_counter[link] += links_weight

    #Sort and get tuple
    sorted_links_scores = links_text_counter.most_common()

    # if normalize:
    #     #Get the higher score value and divide everything by it
    #     #Normalizing by the higher score instead of sum everything to on
    #     #Avoid diferent number of links per page to get higher scores than other pages
    #     higher_score = sorted_links_scores[0][1]
    #     sorted_links_scores = [(links_case_dict[link], score/higher_score) for link, score in sorted_links_scores]

    sorted_links_scores = [(links_case_dict[link], score) for link, score in sorted_links_scores]

    return sorted_links_scores
