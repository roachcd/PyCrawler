#Chase Roach
#A simple open source web crawler for python

from email import header
from turtle import delay
from urllib import request
from bs4 import BeautifulSoup
import urllib3 as urllib
import time

#Init
finalData = []
pagesSearched = []
subpagesFound = []

####################
### FOR CRAWLING ###
####################

#begin your crawl
#rootPages = pages to being crawl at
#depth = number of subpages to crawl through
#verbose = print data about search to terminal
#delay = time delay between each page load
def crawl(rootPages = [], depth = 3, verbose = True, delay = .5):
    for page in rootPages:
        begin([[], [page], page, 0], depth, verbose, delay)                                   
    return finalData

#recursivly goes to each subpage until depth is reached
#adds [tokens, page] to final data, returns nothing
def begin(crawlData, toDepth, verbose, delay):
    depth = crawlData[3]
    
    if(verbose):
        print("Subpages Found: " + str(len(crawlData[1])))

    for subpage in crawlData[1]:

        if(verbose):
            print(str(len(pagesSearched)) + "/" + str(len(subpagesFound)) + " pages indexed")
            print("Current Page: " + subpage)
            print("Current Depth: " + str(depth))

        time.sleep(delay) #courteous sleep, set with delay perameter
        if(subpage not in pagesSearched):
            crawlData = loadPage(subpage, depth, toDepth)
            if crawlData == -1: #if page not loadable, pass to next page
                if(verbose):
                    print("  ERR:  " + subpage + " is not a valid URL")
                pass
            else:
                finalData.append([crawlData[0], crawlData[2]]) #append [tokens, page] to final data
                if(depth < toDepth): #if depth is not reached, run next set of subpages
                    begin(crawlData, toDepth, verbose, delay)
        else:
            print("  " + subpage + " already indexed")
            pass

#loads page html
#returns [tokens, subpages, rootpage, depth+1]
def loadPage(page, depth, toDepth):
    #Headers
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
    #get soup of page
    try:
        req = urllib.request("GET", page, headers=hdr)
    except:
        return -1
    soup = BeautifulSoup(req.data, features="html.parser")
    pagesSearched.append(page);
    data = indexPage(soup, page, depth, toDepth) #[tokens, subpages]
    return [data[0],  data[1],   page,   (depth+1)]
           #tokens  | subpages | rootpage | depth + 1

#creates tokens and subpages of given page
#returns [tokens, subpages]
def indexPage(soup, page, depth, toDepth):
    #get only text from web page
    for script in soup(["script", "style"]): #remove script and style tags
        script.extract()
    text = soup.get_text() #get only text
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk) #remove line breaks
    text.lower()

    #tokenize web page text
    tokens = text.split()
    #print(tokens)

    #find subpages
    links = soup.find_all("a", href=True) #get all a tags
    subpages = []
    for link in links:
        href = link["href"] #get link in a tag
        if href.startswith("/") or not href.startswith("http"): #if relative make absolute
            href = page + href

        if "#" not in href: #remove links that contain anchors
            subpages.append(href)
            if(depth < toDepth):
                subpagesFound.append(href)
    return [tokens, subpages]

#####################
### FOR SEARCHING ###
#####################

#Searches for tokens from searchString
#in given crawlData
#returns sorted [[similarity, link]]
#where data[0] is best match
def search(searchString, crawlData):
    searchData = []
    searchString.lower()
    searchTokens = searchString.split()
    for page in crawlData:
        similarity = 0
        for searchToken in searchTokens:
            for crawlToken in page[0]:
                if searchToken == crawlToken:
                    similarity = similarity + 1
        searchData.append([similarity, page[1]])
    searchData.sort(reverse=True)
    return searchData