from rest_framework import serializers
from .models import *

class WorkoutCategeorySerializer(serializers.ModelSerializer):
	class Meta:
		model = WorkoutCategeory

class WorkoutActionSerializer(serializers.ModelSerializer):
	class Meta:
		model = WorkoutAction
