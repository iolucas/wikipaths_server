from wikipydia import wikipedia, wikidb
from collections import Counter, defaultdict
import re

#from wikidb import WikiDb

#wiki_db = wikidb.WikiDb()

from .models import WikiArticle as WA, WikiUrl, ArticleLink

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
    try:
        art = wikipedia.get_article_by_href(url)
    except:
        return None, False

    #Try to get the article with pageId, if not found, create it 
    try:
        article = WA.objects.get(pageid=art.page_id())
    except WA.DoesNotExist:
        article_created_flag = True
        article = WA(title=art.title(), pageid=art.page_id())

        #Save new article before adding new stuff to it
        article.save()

        #Get links scores
        links_scores = get_art_links_score(art, normalize=True)

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

    if normalize:
        #Get the higher score value and divide everything by it
        #Normalizing by the higher score instead of sum everything to on
        #Avoid diferent number of links per page to get higher scores than other pages
        higher_score = sorted_links_scores[0][1]
        sorted_links_scores = [(links_case_dict[link], score/higher_score) for link, score in sorted_links_scores]

    return sorted_links_scores
