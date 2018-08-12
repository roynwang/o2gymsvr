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
	class Meta:
		model = SalaryReceipt 


