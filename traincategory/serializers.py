from rest_framework import serializers
from .models import *
import pinyin

class CustomerTargetSerializer(serializers.ModelSerializer):
	class Meta:
		model = CustomerTarget

class KanbanTaskSerializer(serializers.ModelSerializer):
	class Meta:
            model = KanbanTask

class WorkoutCategeorySerializer(serializers.ModelSerializer):
	class Meta:
		model = WorkoutCategeory

class WorkoutActionSerializer(serializers.ModelSerializer):
	pinyin = serializers.SerializerMethodField()
	class Meta:
		model = WorkoutAction
	def get_pinyin(self, obj):
		return pinyin.get_initial(obj.name)

class SimpleWorkoutActionWithCustomerValueSerializer(serializers.ModelSerializer):
	pinyin = serializers.SerializerMethodField()
        tag = serializers.SerializerMethodField()
	class Meta:
		model = CustomerWorkoutValue
	def get_pinyin(self, obj):
		return pinyin.get_initial(obj.name).replace(" ","").lower()
        def get_tag(self, obj):
                obj = get_object_or_404(SimpleWorkoutAction,pk=obj.workoutid) 
                return obj.tag


class SimpleWorkoutActionSerializer(serializers.ModelSerializer):
	pinyin = serializers.SerializerMethodField()
	class Meta:
		model = SimpleWorkoutAction
	def get_pinyin(self, obj):
		return pinyin.get_initial(obj.name).replace(" ","").lower()

class NewSimpleWorkoutActionSerializer(serializers.ModelSerializer):
	pinyin = serializers.SerializerMethodField()
	class Meta:
		model = NewSimpleWorkoutAction
	def get_pinyin(self, obj):
		return pinyin.get_initial(obj.name).replace(" ","")


class CustomerWorkoutValueSerializer(serializers.ModelSerializer):
	pinyin = serializers.SerializerMethodField()
	class Meta:
		model = SimpleWorkoutAction
	def get_pinyin(self, obj):
		return pinyin.get_initial(obj.name).replace(" ","").lower()
