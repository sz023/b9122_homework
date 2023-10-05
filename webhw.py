import requests
from bs4 import BeautifulSoup
import urllib.request


#####Q1
def press_release(webpage):
    press_release_tag = webpage.find('a', href="/en/press-release")
    return bool(press_release_tag)

def find_crisis(seed_url, limit=10):
    urls = [seed_url]    #queue of urls to crawl
    seen = [seed_url]    #stack of urls seen so far
    opened = []          #we keep track of seen urls so that we don't revisit them
    press = []
    print("Starting with url="+str(urls))
    while len(urls) > 0 and len(press) <= limit:
        # DEQUEUE A URL FROM urls AND TRY TO OPEN AND READ IT
        try:
            curr_url=urls.pop(0)
            print("num. of URLs in stack: %d " % len(urls))
            print("Trying to access= "+curr_url)
            req = urllib.request.Request(curr_url)
            webpage = urllib.request.urlopen(req).read()
            opened.append(curr_url)

        except Exception as ex:
            print("Unable to access= "+curr_url)
            print(ex)
            continue    #skip code below

        # IF URL OPENS, CHECK WHICH URLS THE PAGE CONTAINS
        # ADD THE URLS FOUND TO THE QUEUE url AND seen
        soup = BeautifulSoup(webpage)  #creates object soup
        if press_release(soup) == True:
            if "crisis" in soup.get_text().lower():
                press.append(curr_url)
        # Put child URLs into the stack
        for tag in soup.find_all('a', href = True): #find tags with links
            childUrl = tag['href'] #extract just the link
            o_childurl = childUrl
            childUrl = urllib.parse.urljoin(seed_url, childUrl)
#             print("seed_url=" + seed_url)
#             print("original childurl=" + o_childurl)
#             print("childurl=" + childUrl)
#             print("seed_url in childUrl=" + str(seed_url in childUrl))
#             print("Have we seen this childUrl=" + str(childUrl in seen))
            if seed_url in childUrl and childUrl not in seen:
#                 print("***urls.append and seen.append***")
                urls.append(childUrl)
                seen.append(childUrl)
            else:
#                 print("######")
                continue
    return press



# Extract and print the press release links
seed_url = "https://press.un.org/en"
press_releases = find_crisis(seed_url)
for pr in press_releases:
    print(pr)


###Q2
import requests
from bs4 import BeautifulSoup
import urllib.request


def get_plenary_status(soup1):
    """
    Determine if a plenary session exists in the given webpage.

    Args:
    - webpage: the parsed webpage object

    Returns:
    - 1 if "plenary session" is found in the webpage
    - 2 if "plenary session" is not found but the span exists
    - 3 if the span with class "ep_name" doesn't exist
    """
    try:
        session_tag = soup1.find_all("span", class_="ep_name")

        # Check if the tag contains the text "plenary session"
        if "plenary session" in str(soup1.find_all("span", class_="ep_name")).lower() and "filter" not in str(
                soup1.find_all("span", class_="ep_name")).lower():
            return 1
        else:
            return 2
    except AttributeError:  # This handles if session_tag is None or doesn't have the method get_text()
        print("Can't find any span with class 'ep_name'")
        return 3


def find_crisis2(seed_url, limit=10):
    urls = [seed_url]  # queue of urls to crawl
    seen = [seed_url]  # stack of urls seen so far
    opened = []  # we keep track of seen urls so that we don't revisit them
    press2 = []
    print("Starting with url=" + str(urls))
    while (len(urls) > 0) and (len(press2) < limit):
        # DEQUEUE A URL FROM urls AND TRY TO OPEN AND READ IT
        try:
            curr_url = urls.pop(0)
            print("num. of URLs in stack: %d " % len(urls))
            print("Trying to access= " + curr_url)
            req = urllib.request.Request(curr_url)
            webpage = urllib.request.urlopen(req).read()
            opened.append(curr_url)

        except Exception as ex:
            print("Unable to access= " + curr_url)
            print(ex)
            continue  # skip code below

        # IF URL OPENS, CHECK WHICH URLS THE PAGE CONTAINS
        # ADD THE URLS FOUND TO THE QUEUE url AND seen
        soup = BeautifulSoup(webpage)  # creates object soup

        if get_plenary_status(soup) == 1:
            if "crisis" in soup.get_text().lower():
                press2.append(curr_url)

        # Put child URLs into the stack
        for tag in soup.find_all('a', href=True):  # find tags with links
            childUrl = tag['href']  # extract just the link
            o_childurl = childUrl
            childUrl = urllib.parse.urljoin(seed_url, childUrl)
            #             print("seed_url=" + seed_url)
            #             print("original childurl=" + o_childurl)
            #             print("childurl=" + childUrl)
            #             print("seed_url in childUrl=" + str(seed_url in childUrl))
            #             print("Have we seen this childUrl=" + str(childUrl in seen))
            if seed_url in childUrl and childUrl not in seen:
                #                 print("***urls.append and seen.append***")
                urls.append(childUrl)
                seen.append(childUrl)
            else:
                #                 print("######")
                continue
    return press2


# Extract and print the press release links
seed_url = "https://www.europarl.europa.eu/news/en/press-room"
press_releases = find_crisis2(seed_url)
for pr in press_releases:
    print(pr)