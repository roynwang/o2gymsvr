from rest_framework import serializers
from coupon.models import *
from usr.serializers import *


class FreeCourseSerializer(serializers.ModelSerializer):
	coachdetail = serializers.SerializerMethodField()
	#customerdetail = serializers.SerializerMethodField()
	def get_coachdetail(self,obj):
		c = User.objects.get(id=obj.coach)
		s = CoachSerializer(c)
		return s.data
	'''
	def get_customerdetail(self,obj):
		if obj.customer == None or obj.customer == '':
			return False
		c = User.objects.get(id=obj.customer)
		s = CoachSerializer(c)
		return s.data
	'''

	class Meta:
		model = FreeCourse

class CouponSerializer(serializers.ModelSerializer):
	class Meta:
		model = Coupon 


