import time
import urllib

import requests
import bs4

start_url = "https://en.wikipedia.org/wiki/Special:Random"
target_url = "https://en.wikipedia.org/wiki/Philosophy"

def find_first_link(url):
    response = requests.get(url)
    html = response.text
    soup = bs4.BeautifulSoup(html,"html.parser")
    content_div = soup.find(id="mw-content-text").find(class_="mw-parser-output")
    aricle_link = None
    
    for element in content_div.find_all("p", recursive=False):
        if element.find("a", recursive=False):
            article_link = element.find("a", recursive=False).get('href')
            break
    if not article_link:
        return
    
    first_link = urllib.parse.urljoin('https://en.wikipedia.org/', article_link)
    return first_link

def continue_crawl(search_history, target_url, max_steps =25):
    
    if search_history[-1] == target_url:
        print("We have reached the target article")
        return False
    
    elif len(search_history) >max_steps:
        print("The search is exceeding the limit, abandoning search")
        return False
    
    elif search_history[-1] in search_history[:-1]:
        print("This page has already been visited, abandoning search")
        return False
    
    else:
        return True


article_chain = [start_url]

while continue_crawl(article_chain,target_url,25):
    print(article_chain[-1])

    first_link = find_first_link(article_chain[-1])
    if not first_link:
        print("We've arrived at an article with no links, aborting search!")
        break

    article_chain.append(first_link)

    time.sleep(1)
