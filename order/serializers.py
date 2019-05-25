from rest_framework import serializers
from order.models import *
from business.models import *
from business.serializers import *
from usr.serializers import *
from usr.models import *
import datetime



class ProductSimpleSerializer(serializers.ModelSerializer):
	class Meta:
		model =	Product

class BalanceOrderSerializer(serializers.ModelSerializer):
        customerdetail = serializers.SerializerMethodField()
        paid_day = serializers.SerializerMethodField()

	class Meta:
		model =	BalanceOrder

        def get_customerdetail(self,obj):
                customer = get_object_or_404(User, name=obj.customer)
                s = SimpleUserSerilaizer(customer)
                return s.data

        def get_paid_day(self,obj):
                return (obj.updated + datetime.timedelta(hours=8)).date()



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

class TSerializer(serializers.ModelSerializer):
	coachdetail = serializers.SerializerMethodField()
	customerdetail = serializers.SerializerMethodField()
	left_course = serializers.SerializerMethodField()
	left_money = serializers.SerializerMethodField()
	endtime = serializers.SerializerMethodField()
	paid_day = serializers.SerializerMethodField()

	class Meta:
		model =	Order 

        def coachdetail(self,obj):
            return obj.custom.displayname

        def customerdetail(self,obj):
            return obj.custom.displayname

	def get_left_course(self, obj):
		completed = Schedule.objects.filter(order=obj,deleted = False, done = True).count()
		sum_amount = obj.product.amount
		return sum_amount - completed

	def get_left_money(self, obj):
	        left_course = self.get_left_course(obj)
                return left_course * obj.product.price / obj.product.amount

	def get_endtime(self, obj):
		return obj.cal_endtime()

        def get_paid_day(self, obj):
            d = obj.paidtime + datetime.timedelta(hours=8)
            return datetime.datetime.strftime(d,"%Y-%m-%d")
		


class OrderSerializer(serializers.ModelSerializer):
	coachdetail = SimpleUserSerilaizer(source="coach", read_only = True)
	customerdetail = SimpleUserSerilaizer(source="custom", read_only = True)
	#booked = serializers.SerializerMethodField()
	complete_status = serializers.SerializerMethodField()
	all_booked = serializers.SerializerMethodField()
	endtime = serializers.SerializerMethodField()
	course_count = serializers.SerializerMethodField()
	paid_day = serializers.SerializerMethodField()

	class Meta:
		model =	Order 

	def get_course_count(self, obj):
		return obj.product.amount
	def get_complete_status(self, obj):
		completed = Schedule.objects.filter(order=obj,deleted = False, done = True).count()
		sum_amount = obj.product.amount
                if obj.status != "done" and completed == sum_amount:
                    obj.status = "done"
                    obj.save()
		return str(completed) + "/" + str(sum_amount)

	def get_all_booked(self, obj):
		completed = Schedule.objects.filter(order=obj,deleted = False).count()
		sum_amount = obj.product.amount
		return completed >= sum_amount

	def get_endtime(self, obj):
		return obj.cal_endtime()

        def get_paid_day(self, obj):
            d = obj.paidtime + datetime.timedelta(hours=8)
            return datetime.datetime.strftime(d,"%Y-%m-%d")
		
		

class ProductSerializer(serializers.ModelSerializer):
	coachdetail = SimpleUserSerilaizer(source="coach", read_only=True)
	soldcount = serializers.SerializerMethodField()

	def get_soldcount(self, obj):
		return obj.sold.count()

	class Meta:
		model =	Product

class GymBackupSerilaizer(serializers.ModelSerializer):

	complete_count = serializers.SerializerMethodField()
	course_count = serializers.SerializerMethodField()
        customer_name = serializers.SerializerMethodField()
        paid_time = serializers.SerializerMethodField()
        class Meta:
            model = Order
            fields = ['customer_name', 'custom', 'paid_time','amount', 'course_count','complete_count']
        def get_paid_time(self, obj):
            d = obj.paidtime + datetime.timedelta(hours=8)
            return datetime.datetime.strftime(d,"%Y-%m-%d %H:%M:%S")

	def get_complete_count(self, obj):
		return obj.schedule_set.filter(deleted = False, done = True).count()

	def get_course_count(self, obj):
                return obj.product.amount

	def get_customer_name(self, obj):
                return obj.custom.displayname

