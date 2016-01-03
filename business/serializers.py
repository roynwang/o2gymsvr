from rest_framework import serializers
from business.models import *
from usr.serializers import *


class CourseSerializer(serializers.ModelSerializer):
	class Meta:
		model = Course

class GymSerializer(serializers.ModelSerializer):
	coaches_set= CoachSimpleSerializer(source="coaches", many=True, read_only=True)
	class Meta:
		model = Gym

'''
class GymWithDisSerializer(serializers.ModelSerializer):
	class Meta:
		model = Gym
'''


class ScheduleSerializer(serializers.ModelSerializer):
	customerprofile = SimpleUserSerilaizer(source='custom', read_only=True)
	coachprofile = CoachSerializer(source='coach', read_only=True)
	complete_status = serializers.SerializerMethodField()
	class Meta:
		model = Schedule
	def get_complete_status(self, obj):
		completed = Schedule.objects.filter(order=obj.order,deleted = False, done = True).count()
		sum_amount = obj.order.product.amount
		return str(completed) + "/" + str(sum_amount)

class ScheduleSimpleSerializer(serializers.ModelSerializer):
	customerprofile = SimpleUserSerilaizer(source='custom', read_only=True)
	coachprofile = CoachSerializer(source='coach', read_only=True)
	class Meta:
		model = Schedule


class BodyEvalSerializer(serializers.ModelSerializer):
	class Meta:
		model = BodyEval

class BodyEvalDateSerializer(serializers.ModelSerializer):
	class Meta:
		model = BodyEval
		fields = ["date"]

class TrainSerializer(serializers.ModelSerializer):
	class Meta:
		model = Train

class BodyEvalOptionsSerializer(serializers.ModelSerializer):
	class Meta:
		model = BodyEvalOptions

class TrainDateSerializer(serializers.ModelSerializer):
	class Meta:
		model = BodyEval
		fields = ["date"]
