from rest_framework import serializers
from order.models import *
from business.models import *
from business.serializers import *
from usr.serializers import *



class ProductSimpleSerializer(serializers.ModelSerializer):
	class Meta:
		model =	Product

class OrderDetailSerializer(serializers.ModelSerializer):
	coachdetail = SimpleUserSerilaizer(source="coach",read_only = True)
	customerdetail = SimpleUserSerilaizer(source="custom",read_only = True)
	booked = serializers.SerializerMethodField()
	endtime = serializers.SerializerMethodField()
	complete_status = serializers.SerializerMethodField()
	course_count = serializers.SerializerMethodField()

	class Meta:
		model =	Order 

	def get_complete_status(self, obj):
		completed = Schedule.objects.filter(order=obj,deleted = False, done = True).count()
		sum_amount = obj.product.amount
		return str(completed) + "/" + str(sum_amount)

	def get_booked(self, obj):
		bookedlist = Schedule.objects.filter(order=obj,deleted = False).order_by("-date","hour")
		sr = ScheduleSerializer(bookedlist, many=True)
		return sr.data
	def get_endtime(self, obj):
		return obj.cal_endtime()
	def get_course_count(self, obj):
		return obj.product.amount

class OrderSerializer(serializers.ModelSerializer):
	coachdetail = SimpleUserSerilaizer(source="coach", read_only = True)
	customerdetail = SimpleUserSerilaizer(source="custom", read_only = True)
	#booked = serializers.SerializerMethodField()
	complete_status = serializers.SerializerMethodField()
	all_booked = serializers.SerializerMethodField()
	endtime = serializers.SerializerMethodField()
	course_count = serializers.SerializerMethodField()

	class Meta:
		model =	Order 

	def get_course_count(self, obj):
		return obj.product.amount
	def get_complete_status(self, obj):
		completed = Schedule.objects.filter(order=obj,deleted = False, done = True).count()
		sum_amount = obj.product.amount
		return str(completed) + "/" + str(sum_amount)

	def get_all_booked(self, obj):
		completed = Schedule.objects.filter(order=obj,deleted = False).count()
		sum_amount = obj.product.amount
		return completed >= sum_amount

	def get_endtime(self, obj):
		return obj.cal_endtime()
		
		

class ProductSerializer(serializers.ModelSerializer):
	coachdetail = SimpleUserSerilaizer(source="coach", read_only=True)
	soldcount = serializers.SerializerMethodField()

	def get_soldcount(self, obj):
		return obj.sold.count()

	class Meta:
		model =	Product


