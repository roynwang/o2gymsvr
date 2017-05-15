from rest_framework import serializers
from doc.models import *
from usr.models import *
import datetime



class GymDocSerializer(serializers.ModelSerializer):
	class Meta:
		model =	GymDoc

class GymVideoSerializer(serializers.ModelSerializer):
	class Meta:
		model =	GymVideo




