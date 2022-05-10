import urllib.request as urlreq
import bs4 as bs
import re

def getResponse(url):
    request = urlreq.Request(url, headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36 Edg/101.0.1210.39"
    })
    with urlreq.urlopen(request) as response:
        data = response.read().decode("utf-8")

    root = bs.BeautifulSoup(data, "html.parser")
    return root

# https://www.ptt.cc/man/marvel/D7B0/D450/D47A/index.html
# target:
# 		<div class="m-ent">
#			<div class="title">
#				<a href="/man/marvel/D7B0/D450/D47A/D249/index.html">◆ 子不語-第一卷</a>
#		    </div>
#	    </div>
def getVolumes(data):
    address = data.find_all("a", string=re.compile(u".*子不語.*"))
    volumes = []
    for i in address:
        # i["href"] is relative path
        volumes.append("https://www.ptt.cc" + i["href"])
    return volumes

def getArticles(data):
    address = data.find_all("a", string=re.compile(u"^◇ \[分享\] ")) # u = unicode
    articles = []
    for i in address:
        # i["href"] is relative path
        articles.append("https://www.ptt.cc" + i["href"])
    return articles

def getOriginals(data):
    return data.find("div", id="main-content")

def main():
    web_url = "https://www.ptt.cc/man/marvel/D7B0/D450/D47A/index.html"
    web_response = getResponse(web_url) # get web_url reply
    volumes = getVolumes(web_response) # get all volume url
    Results = {}
    for volumes_ind, volume in enumerate(volumes):
        volume_response = getResponse(volume) # get one volume reply
        articles = getArticles(volume_response) # get all article url of one volume
        article_ind = 1
        for article in articles:
            article_response = getResponse(article)
            originals = getOriginals(article_response)
    
def test():
    web_url = "https://www.ptt.cc/man/marvel/D7B0/D450/D47A/index.html"
    web_response = getResponse(web_url) # get web_url reply
    volumes = getVolumes(web_response) # get all volume url
    Results = {}
    volume_response = getResponse(volumes[0])
    articles = getArticles(volume_response)
    article_response = getResponse(articles[0])
    original = getOriginals(article_response)
    txt = original.text
    print(re.search(u"\n\d{1,2}-\d{1,2}(.*\n.*)*--(?!.*--)",txt,re.MULTILINE))
        