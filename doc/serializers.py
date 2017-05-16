from rest_framework import serializers
from doc.models import *
from usr.models import *
import datetime



class GymDocSerializer(serializers.ModelSerializer):
	class Meta:
		model =	GymDoc

class GymVideoSerializer(serializers.ModelSerializer):
        keywords = serializers.SerializerMethodField()
	class Meta:
		model =	GymVideo
        def get_keywords(self,obj):
            keywords = ""
            cursor = GymVideoKeyword.objects.filter(videoid=obj.id)
            for row in cursor:
                keywords += row.keyword
                keywords += ' '
            return keywords[0:-1]




class GymVideoKeywordSerializer(serializers.ModelSerializer):
	class Meta:
		model =	GymVideoKeyword
