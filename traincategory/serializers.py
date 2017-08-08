from rest_framework import serializers
from .models import *
import pinyin

class WorkoutCategeorySerializer(serializers.ModelSerializer):
	class Meta:
		model = WorkoutCategeory

class WorkoutActionSerializer(serializers.ModelSerializer):
	pinyin = serializers.SerializerMethodField()
	class Meta:
		model = WorkoutAction
	def get_pinyin(self, obj):
		return pinyin.get_initial(obj.name)

class SimpleWorkoutActionSerializer(serializers.ModelSerializer):
	pinyin = serializers.SerializerMethodField()
	class Meta:
		model = SimpleWorkoutAction
	def get_pinyin(self, obj):
		return pinyin.get_initial(obj.name).replace(" ","")
