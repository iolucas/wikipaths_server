from wikipydia import wikipedia
from collections import Counter, defaultdict
import re


def get_links_score(href, normalize=False):
    """Get wiki article links score."""
    
    art = wikipedia.get_article_by_href(href)
    html_links = art.links()
    html_text = re.sub(r"[\n]+", " ", art.text())

    links_text_counter = Counter() #Link text counter
    links_text_dict = defaultdict(list)

    for link, text in html_links:
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
        sorted_links_scores = [(link, score/higher_score) for link, score in sorted_links_scores]


    return sorted_links_scores
