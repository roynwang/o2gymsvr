# -*- coding: utf-8 -*-
import json
import requests
import time
import pprint
from pyquery import PyQuery as pq
from lxml import etree
import pprint
import re
import codecs
import datetime



if __name__ == "__main__":
    for i in range(1,3000):
        file_object = open('./workout/'+ str(i))
        try:
            all_the_text = file_object.read( )
            j = json.loads(all_the_text)
            if not 'id' in j:
                continue
            sql = "insert into GymVideo (id,gym,uploader,coach,title,pic,summary,attachment,`update`,datestr) values (" + \
                 j['id'] + ',' + \
                 str(31) + ',' + \
                 '"crawler"' + ',' + \
                 '"crawler"' + ',' + \
                 '"'+j['name'] + '",' + \
                 '"'+j['pic'] + '",' + \
                 '"'+j['description'] + '",' + \
                 '"'+j['video_url'] + '",' + \
                 '"'+ str(datetime.datetime.now()) + '",' + \
                 '"2017-06-06")' 
            print sql
        finally:
            file_object.close( )


