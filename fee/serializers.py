from rest_framework import serializers
from .models import *
from usr.models import *

class CoachSalarySettingSerializer(serializers.ModelSerializer):
	coachname = serializers.SerializerMethodField()
	class Meta:
		model = CoachSalarySetting
	def get_coachname(self, obj):
		return User.objects.get(id=obj.coach).displayname 

class GymFeeSerializer(serializers.ModelSerializer):
	coach_salary_setting = CoachSalarySettingSerializer(read_only = True, many = True)
	class Meta:
		model = CoachSalarySetting

	
class SalaryReceiptSerializer(serializers.ModelSerializer):
	displayname = serializers.SerializerMethodField()
	avatar = serializers.SerializerMethodField()

	class Meta:
            model = SalaryReceipt 

	def get_coachname(self, obj):
            return User.objects.get(name=obj.name).displayname 

	def get_avatar(self, obj):
            return User.objects.get(name=obj.name).avatar

