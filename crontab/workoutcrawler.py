import json
import requests
import time
import pprint
from pyquery import PyQuery as pq
from lxml import etree
import pprint
import re
import codecs
import time


def crawl_html(s, url):
    print url.encode("utf-8")
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.89 Safari/537.36'
    header = {"User-Agent": user_agent}
    res = s.get(url, headers=header)
    return res.text

if __name__ == "__main__":
    s = requests.Session()
    '''
    f = codecs.open('./workout/test.txt','r','utf-8')
    p = f.readline()
    o = json.loads(p)
    print o['name']
    '''
    for i in range(0,3000):
        url = "http://www.hiyd.com/dongzuo/"+str(i)+"/"
        content = crawl_html(s, url)
        d = pq(content)
        content = d("script:last").text()
        data = re.search("e\.init\((.+})\);", content).group(1)
        fileHandle = codecs.open('./workout/'+str(i), 'w','utf-8') 
        fileHandle.write(data)
        fileHandle.close()
        time.sleep(50)

        






