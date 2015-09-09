from rest_framework import serializers
from business.models import *
from usr.serializers import *
from rest_framework_bulk import BulkListSerializer, BulkSerializerMixin


class CourseSerializer(serializers.ModelSerializer):
	class Meta:
		model = Course

class GymSerializer(serializers.ModelSerializer):
	coaches_set = CoachSimpleSerializer(source="coaches", many=True, read_only=True)
	class Meta:
		model = Gym


class ScheduleSerializer(BulkSerializerMixin, serializers.ModelSerializer):
	customerprofile = SimpleUserSerilaizer(source='custom', read_only=True)
	coachprofile = CoachSerializer(source='coach', read_only=True)
	class Meta:
		model = Schedule
