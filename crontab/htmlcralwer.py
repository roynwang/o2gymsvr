import json
import requests
import time


def get_task(s):
    url = "http://o2-fit.com/api/cwl/task/latest/"
    resp = s.get(url)
    return resp.json()

def crawl_html(s, url):
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.89 Safari/537.36'
    header = {"User-Agent": user_agent}
    print "crawling:" + url
    res = s.get(url, headers=header)
    print res.text
    return res

def send_back(task, html):
    print html
    url = "http://o2-fit.com/api/cwl/task/"+str(task['id'])+"/"
    data = {"html":html}
    #requests.patch(url,data)


if __name__ == "__main__":
    s = requests.Session()
    while(1):
        task = get_task(s)
        print task
        #send_back(task, crawl_html(s,task['url']))
        crawl_html(s,task['url'])
        time.sleep(60)


