from rest_framework import serializers
from recommend.models import *
from weibo.serializers import *
from business.serializers import *
from usr.serializers import *


class RecommendSerializer(serializers.ModelSerializer):
	article_display = WeiboSerializer(source="article", read_only=True)
	person_display = UserSerializer(source="person", read_only=True)
	gym_display = GymSerializer(source="gyms", read_only=True)
	course_display = CourseSerializer(source="course", read_only=True)

	class Meta:
		model = Recommend
