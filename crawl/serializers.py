from rest_framework import serializers
from crawl.models import *


class CrawlShopCountSerializer(serializers.ModelSerializer):
        class Meta:
                model = CrawlShopCount


