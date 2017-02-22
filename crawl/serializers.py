from rest_framework import serializers
from crawl.models import *


class CrawlShopCountSerializer(serializers.ModelSerializer):
        class Meta:
                model = CrawlShopCount

class CrawlGrouponCountSerializer(serializers.ModelSerializer):
        class Meta:
                model = CrawlGrouponCount

class CrawlTaskSerializer(serializers.ModelSerializer):
        class Meta:
                model = CrawlTask


