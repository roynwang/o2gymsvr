# coding=utf-8
from rest_framework import serializers
from business.models import *
from usr.serializers import *

class CourseReviewSerializer(serializers.ModelSerializer):
	class Meta:
		model = CourseReview

class RefundSerializer(serializers.ModelSerializer):
	class Meta:
		model = Refund

class LivenessSerializer(serializers.ModelSerializer):
        coach_detail = serializers.SerializerMethodField()
	class Meta:
		model = Liveness
        def get_coach_detail(self,obj):
            c = User.objects.get(name=obj.name)
	    serializer = SimpleUserSerilaizer(c)
            return serializer.data

class ChargePricingSerializer(serializers.ModelSerializer):
	class Meta:
		model = ChargePricing

class InvoiceSerializer(serializers.ModelSerializer):
	class Meta:
		model = Invoice


class FinanceSerializer(serializers.ModelSerializer):
	class Meta:
		model = Finance

class FlowSerializer(serializers.ModelSerializer):
	class Meta:
		model = Flow


class GroupCourseSerializer(serializers.ModelSerializer):
	class Meta:
		model = GroupCourse

class SelfTrainSerializer(serializers.ModelSerializer):
        customer_detail = serializers.SerializerMethodField()
	class Meta:
		model = SelfTrain

        def get_customer_detail(self,obj):
            c = User.objects.get(name=obj.name)
	    serializer = SimpleUserSerilaizer(c)
            return serializer.data



class GroupCourseInstanceBookSerializer(serializers.ModelSerializer):
        customer_detail = serializers.SerializerMethodField()

	class Meta:
		model = GroupCourseInstanceBook

        def get_customer_detail(self,obj):
            c = User.objects.get(name=obj.customer)
	    serializer = SimpleUserSerilaizer(c)
            return serializer.data

class GroupCourseInstanceBookDetailSerializer(serializers.ModelSerializer):
        #customer_detail = serializers.SerializerMethodField()
        course_detail = serializers.SerializerMethodField()

	class Meta:
		model = GroupCourseInstanceBook

        def get_customer_detail(self,obj):
            c = User.objects.get(name=obj.customer)
	    serializer = SimpleUserSerilaizer(c)
            return serializer.data
        def get_course_detail(self,obj):
            c = GroupCourseInstance.objects.get(id=obj.course)
	    serializer = GroupCourseInstanceSerializer(c)
            return serializer.data


class GroupCourseInstanceSerializer(serializers.ModelSerializer):
        course_detail = serializers.SerializerMethodField()
        coach_detail = serializers.SerializerMethodField()
        booked = serializers.SerializerMethodField()

	class Meta:
		model = GroupCourseInstance

        def get_course_detail(self, obj):
            c = GroupCourse.objects.get(id=obj.course)
	    serializer = GroupCourseSerializer(c)
            return serializer.data

        def get_coach_detail(self,obj):
            c = User.objects.get(name=obj.coach)
	    serializer = SimpleUserSerilaizer(c)
            return serializer.data

        def get_booked(self, obj):
            booked = GroupCourseInstanceBook.objects.filter(course=obj.id)
	    serializer = GroupCourseInstanceBookSerializer(booked, many=True)
            return serializer.data
                

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
	finalprice = serializers.SerializerMethodField()
	class Meta:
		model = Schedule
	def get_complete_status(self, obj):
                if obj.coursetype == "charge":
                        return "储值客户"
                if obj.order is None:
                        return "体验课"
		completed = obj.order.schedule_set.filter(deleted = False, done = True).count()
		sum_amount = obj.order.product.amount
		return str(completed) + "/" + str(sum_amount)
        def get_finalprice(self, obj):
		return obj.getprice()


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

class TodoSerializer(serializers.ModelSerializer):
	class Meta:
		model = Todo

class TrainDateSerializer(serializers.ModelSerializer):
	class Meta:
		model = BodyEval
		fields = ["date"]

class SurveySerializer(serializers.ModelSerializer):
	customerprofile = serializers.SerializerMethodField()
	coachprofile = serializers.SerializerMethodField() 
	class Meta:
		model = Survey
        def get_customerprofile(self,obj):
            c = User.objects.get(name=obj.customer)
            return {"name":c.name,"displayname":c.displayname}

        def get_coachprofile(self,obj):
            c = User.objects.get(name=obj.coach)
	    serializer = SimpleUserSerilaizer(c)
            return {"name":c.name,"displayname":c.displayname}


class HomeworkSerializer(serializers.ModelSerializer):
	class Meta:
	    model = Homework
	customerprofile = serializers.SerializerMethodField()
	coachprofile = serializers.SerializerMethodField() 
        def get_customerprofile(self,obj):
            c = User.objects.get(name=obj.customer)
            return {"name":c.name,"displayname":c.displayname,"avatar":c.avatar}

        def get_coachprofile(self,obj):
            c = User.objects.get(name=obj.coach)
	    serializer = SimpleUserSerilaizer(c)
            return {"name":c.name,"displayname":c.displayname, "avatar":c.avatar}

class CustomerWeeklyKPISerializer(serializers.ModelSerializer):
	class Meta:
            model = CustomerWeeklyKPI
	customerprofile = serializers.SerializerMethodField()

        def get_customerprofile(self,obj):
            c = User.objects.get(name=obj.customer)
            return {"name":c.name,"displayname":c.displayname,"avatar":c.avatar}
