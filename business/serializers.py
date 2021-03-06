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
	class Meta:
		model = Schedule
'''
class ScheduleSimpleSerializer(serializers.ModelSerializer):
	class Meta:
		model = Schedule
'''


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
