from rest_framework import serializers
from usr.models import *
from business.models import *
from weibo.models import *
from django.contrib.auth import get_user_model
import json
import pinyin


class CurrentVersionSerializer(serializers.ModelSerializer):
        class Meta:
                model = CurrentVersion

class ChargeHistorySerializer(serializers.ModelSerializer):
        class Meta:
                model = ChargeHistory

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
	pinyin = serializers.SerializerMethodField()
	class Meta:
		model = User
		exclude = ("upped","fwded","commented","upped_person","created")
	def get_pinyin(self, obj):
		return pinyin.get_initial(obj.displayname)

class CoachSimpleSerializer(serializers.ModelSerializer):
	#gym_detail = GymSimpleSerializer(source="gym",many=True,read_only=True)
	all_order_count = serializers.SerializerMethodField()
	class Meta:
		model = User
		exclude = ("upped","fwded","commented","upped_person","created")

	def get_all_order_count(self, obj):
		return obj.income_orders.count()


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
	gym = serializers.StringRelatedField(many=True,read_only=True)
	gym_id = serializers.PrimaryKeyRelatedField(source="gym",many=True,read_only=True)
	upped_person = serializers.StringRelatedField(many=True, read_only=True)
	corps_list = serializers.SerializerMethodField()
	class Meta:
		model = User
		#exclude = ("upped","fwded","commented")
	def get_corps_list(self, obj):
		if obj.corps == None or obj.corps == "":
			return []
		corps = json.loads(obj.corps)
		ret = []
		print(obj.name)
		print corps
		for corp in corps:
			ret.append({"k":corp, "v":unicode(Gym.objects.get(id=corp))})
		return ret


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

class FeedBackSerializer(serializers.ModelSerializer):
	class Meta:
		model = FeedBack

class MessageSerializer(serializers.ModelSerializer):
	class Meta:
		model = Message 

class ThresholdMsgSerializer(serializers.ModelSerializer):
	class Meta:
		model = ThresholdMsg

