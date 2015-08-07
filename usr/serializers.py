from rest_framework import serializers
from usr.models import *
from weibo.models import *


class FakeWeiboSerializer(serializers.ModelSerializer):
	class Meta:
		model = Weibo

class UserCourseSerializer(serializers.ModelSerializer):
	studying = serializers.StringRelatedField(many=True)
	class Meta:
		model = User

class SimpleUserSerilaizer(serializers.ModelSerializer):
	class Meta:
		model = User
		exclude = ("upped","fwded","commented")

class CoachSerializer(serializers.ModelSerializer):
	class Meta:
		model = User

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

class FeedSerializer(serializers.ModelSerializer):
	feed = serializers.StringRelatedField(many=True)
	#feed = FakeWeiboSerializer(many=True)
	class Meta:
		model = TimeLine
		fields = ('feed',)


class UserSerializer(serializers.ModelSerializer):
	upped_person = serializers.StringRelatedField(many=True)
	class Meta:
		model = User
		#exclude = ("upped","fwded","commented")

class CoachSerializer(serializers.ModelSerializer):
	class Meta:
		model = User

class AlbumSerializer(serializers.ModelSerializer):
	album = serializers.StringRelatedField(many=True)
	class Meta:
		model = User

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
