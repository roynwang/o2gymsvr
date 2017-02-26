from pyquery import PyQuery as pq
from lxml import etree
import pprint
import re

class ListHandler:
    def __init__(self, task):
        self.task = task
        self.doc = pq(self.task.html)

    def extract_page_url(self):
        t = self.doc(".tg-paginator-link")
        ret = []
        baseurl = self.task.url.split("?")[0]
        for link in t:
            m = pq(link)
            url  = baseurl + m.attr("href")
            ret.append(url)
        return ret

    def is_first_page(self):
        pgn = self.get_current_page_num()
        return pgn == 1

    def get_current_page_num(self):
        t = self.doc(".tg-paginator-selected")
        return int(t.text())


    def get_groupon_list(self):
        ret = []
        l = self.doc(".tg-floor-item")
        for item in l:
            ret.append(self.build_groupon_item(item))
        return ret

    def build_groupon_item(self,g):
        d = pq(g)
        shopid =  0
        shopname =  d(".tg-floor-title h3").text()
        grouponhref = d(".tg-floor-img").attr("href")
        grouponid =  int(re.search('(\d+)',grouponhref).group(0))
        grouponname = d(".tg-floor-title h4").text()
        price = int(float(d(".tg-floor-price-new em").text()))
        soldhtml = d(".tg-floor-sold").text();
        soldtext = re.search('(\d+)',soldhtml)
        sold_until_now = 0
        if soldtext:
            sold_until_now = int(soldtext.group(0))

        ret = {\
                "shopid": shopid,\
                "grouponid": grouponid, \
                "shopname": shopname,\
                "grouponid": grouponid,\
                "grouponname": grouponname,\
                "price": price,\
                "sold_until_now": sold_until_now\
                }
        return ret
        
        

