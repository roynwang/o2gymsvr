from rest_framework import serializers
from order.models import *
from business.models import *
from business.serializers import *
from usr.serializers import *





class OrderDetailSerializer(serializers.ModelSerializer):
	coachdetail = SimpleUserSerilaizer(source="coach",read_only = True)
	customerdetail = SimpleUserSerilaizer(source="custom",read_only = True)
	booked = serializers.SerializerMethodField()

	class Meta:
		model =	Order 

	def get_booked(self, obj):
		bookedlist = Schedule.objects.filter(order=obj,deleted = False)
		sr = ScheduleSerializer(bookedlist, many=True)
		return sr.data

class OrderSerializer(serializers.ModelSerializer):
	coachdetail = SimpleUserSerilaizer(source="coach", read_only = True)
	customerdetail = SimpleUserSerilaizer(source="custom", read_only = True)
	#booked = serializers.SerializerMethodField()

	class Meta:
		model =	Order 

class ProductSerializer(serializers.ModelSerializer):
	coachdetail = SimpleUserSerilaizer(source="coach", read_only=True)
	soldcount = serializers.SerializerMethodField()

	def get_soldcount(self, obj):
		return obj.sold.count()

	class Meta:
		model =	Product

	
