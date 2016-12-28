# coding=utf-8
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


class ScheduleCustomerBriefSerializer(serializers.ModelSerializer):
        customername = serializers.SerializerMethodField()
	class Meta:
		model = Schedule
		fields = ["date","customername"]
        def get_customername(self, obj):
            return obj.custom.displayname


class ScheduleSerializer(serializers.ModelSerializer):
	customerprofile = SimpleUserSerilaizer(source='custom', read_only=True)
	coachprofile = CoachSerializer(source='coach', read_only=True)
	complete_status = serializers.SerializerMethodField()
	class Meta:
		model = Schedule
	def get_complete_status(self, obj):
                if obj.order is None:
                        return "体验课"
		completed = obj.order.schedule_set.filter(deleted = False, done = True).count()
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

class BodyEvalOptionsSerializer(serializers.ModelSerializer):
	class Meta:
		model = BodyEvalOptions

class HealthQuesSerializer(serializers.ModelSerializer):
	class Meta:
		model = HealthQues

class HealthQuesDateSerializer(serializers.ModelSerializer):
	class Meta:
		model = HealthQues 
		fields = ["date"]

class HealthQuesOptionsSerializer(serializers.ModelSerializer):
	class Meta:
		model = HealthQuesOptions

class TrainSerializer(serializers.ModelSerializer):
	class Meta:
		model = Train



class TrainDateSerializer(serializers.ModelSerializer):
	class Meta:
		model = BodyEval
		fields = ["date"]
