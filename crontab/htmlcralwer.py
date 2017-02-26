import json
import requests
import time
import pprint


def get_task(s):
    url = "http://o2-fit.com/api/cwl/task/latest/"
    resp = s.get(url)
    return resp.json()

def crawl_html(s, url):
    print url.encode("utf-8")
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.89 Safari/537.36'
    header = {"User-Agent": user_agent}
    res = s.get(url, headers=header)
    return res.text

def send_back(task, html):
    url = "http://o2-fit.com/api/cwl/task/"+str(task['id'])+"/"
    data = {"html":html.encode("utf-8")}
    res = requests.patch(url,data)



if __name__ == "__main__":
    s = requests.Session()
    while(1):
        task = get_task(s)
        if task['url'] != "":
            send_back(task, crawl_html(s,task['url']))
        time.sleep(60)


