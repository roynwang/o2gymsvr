from rest_framework import serializers
from usr.models import *
from business.models import *
from weibo.models import *
from django.contrib.auth import get_user_model

class FakeWeiboSerializer(serializers.ModelSerializer):
	class Meta:
		model = Weibo

class UserCourseSerializer(serializers.ModelSerializer):
	studying = serializers.StringRelatedField(many=True)
	class Meta:
		model = User

class UserRegisterationSerializer(serializers.ModelSerializer):
	class Meta:
		model = get_user_model()
		exclude = ("user_permissions","groups")

class SimpleUserSerilaizer(serializers.ModelSerializer):
	class Meta:
		model = User
		exclude = ("upped","fwded","commented","upped_person","created")

class CoachSimpleSerializer(serializers.ModelSerializer):
	#gym_detail = GymSimpleSerializer(source="gym",many=True,read_only=True)
	class Meta:
		model = User
		exclude = ("upped","fwded","commented","upped_person","created")


class CoachSerializer(serializers.ModelSerializer):
	gym = serializers.StringRelatedField(many=True)
	class Meta:
		model = User
		exclude = ("upped","fwded","commented","upped_person","created")


class AlbumSerializer(serializers.ModelSerializer):
	album = serializers.StringRelatedField(many=True)
	class Meta:
		model = User

class FollowsSerializer(serializers.ModelSerializer):
	class Meta:
		model = TimeLine

class TimeLineSerializer(serializers.ModelSerializer):
	follows = FollowsSerializer(many=True)
	class Meta:
		model = TimeLine


class UserSerializer(serializers.ModelSerializer):
	gym = serializers.StringRelatedField(many=True)
	gym_id = serializers.PrimaryKeyRelatedField(source="gym",many=True,read_only=True)
	upped_person = serializers.StringRelatedField(many=True)
	class Meta:
		model = User
		#exclude = ("upped","fwded","commented")


class FeedSerializer(serializers.ModelSerializer):
	feed = serializers.StringRelatedField(many=True)
	#feed = FakeWeiboSerializer(many=True)
	class Meta:
		model = TimeLine
		fields = ('feed',)

class HistorySerializer(serializers.ModelSerializer):
	history = serializers.StringRelatedField(many=True)
	class Meta:
		model = TimeLine
		fields = ('name','history') 

class WorkingDaysSerializer(serializers.ModelSerializer):
	class Meta:
		model = WorkingDays

