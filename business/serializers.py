from rest_framework import serializers
from business.models import *


class CourseSerializer(serializers.ModelSerializer):
	class Meta:
		model = Course

class GymSerializer(serializers.ModelSerializer):
	class Meta:
		model = Gym
