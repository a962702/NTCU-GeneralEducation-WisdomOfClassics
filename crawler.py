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
    problem_link = []
    ptn = ["………………………………………………………………………………………………………(?![\\s\\S\\u4e00-\\u9fff]*………………………………………………………………………………………………………)[\\s\\S\\u4e00-\\u9fff]*",
           "(?<=………………………………………………………………………………………………………)[\\s\\S\\u4e00-\\u9fff]*",
           "[\\s\\S\\u4e00-\\u9fff]*(?<=--)"]
    results = ''
    for volumes_ind, volume in enumerate(volumes):
        volume_response = getResponse(volume) # get one volume reply
        articles = getArticles(volume_response) # get all article url of one volume
        for articles_ind, article in enumerate(articles):
            article_response = getResponse(article)
            original = getOriginals(article_response)
            txt = original.text
            legal = True
            for i in ptn:
                match = re.search(i,txt,re.MULTILINE)
                if not match:
                    problem_link.append(article)
                    legal = False
                    break
                txt = match[0]
            if legal:
                results = results + '\n\n' + txt
                print('Done : ' + article)
    file_name = "raw.txt"
    with open(file_name,'w',encoding='UTF-8') as wfile:
        wfile.write(results)
    for i in problem_link:
        print("Not match link : " + i)
    

def test():
    web_url = "https://www.ptt.cc/man/marvel/D7B0/D450/D47A/index.html"
    web_response = getResponse(web_url) # get web_url reply
    volumes = getVolumes(web_response) # get all volume url
    volume_response = getResponse(volumes[0])
    articles = getArticles(volume_response)
    article_response = getResponse(articles[0])
    original = getOriginals(article_response)
    txt = original.text
    problem_link = []
    legal = True
    ptn = ["………………………………………………………………………………………………………(?![\\s\\S\\u4e00-\\u9fff]*………………………………………………………………………………………………………)[\\s\\S\\u4e00-\\u9fff]*",
           "(?<=………………………………………………………………………………………………………)[\\s\\S\\u4e00-\\u9fff]*",
           "[\\s\\S\\u4e00-\\u9fff]*(?<=--)"]
    for i in ptn:
        match = re.search(i,txt,re.MULTILINE)
        if not match:
            problem_link.append(articles[0])
            legal = False
            break
        txt = match[0]
    # txt = re.search(r"………………………………………………………………………………………………………(?![\s\S\u4e00-\u9fff]*………………………………………………………………………………………………………)[\s\S\u4e00-\u9fff]*",txt,re.MULTILINE)[0]
    # txt = re.search(r"(?<=………………………………………………………………………………………………………)[\s\S\u4e00-\u9fff]*",txt,re.MULTILINE)[0]
    # txt = re.search(r"[\s\S\u4e00-\u9fff]*(?<=--)",txt,re.MULTILINE)[0]
    # print(re.search(u"\n\d{1,2}-\d{1,2}(.*\n.*)*--(?!.*--)",txt,re.MULTILINE))
    print(txt)
        
main()