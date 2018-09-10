# coding=utf-8
from django.db import models
from django.conf import settings
from django.utils import timezone
from usr.models import *
from business.models import *
from django.db.models import Sum

# Create your models here.
def last_day_of_month(date):
    if date.month == 12:
        return date.replace(day=31)
    return date.replace(month=date.month+1, day=1) - datetime.timedelta(days=1)


class GymFee(models.Model):
	id = models.AutoField(primary_key=True)
	gym = models.IntegerField(unique=True, db_index=True)
	balance =  models.IntegerField(default=0)
	coaches = models.TextField(default="[]")
	coach_count = models.IntegerField(default=0)

class CoachSalarySetting(models.Model):
	id = models.AutoField(primary_key=True)
	coach = models.IntegerField()
	gymfee = models.ForeignKey(GymFee, related_name="coach_salary_setting")
	base_salary = models.FloatField(default=0)
	yanglao = models.FloatField(default=0)
	yiliao = models.FloatField(default=0)
	shiye = models.FloatField(default=0)
	gongjijin = models.FloatField(default=0)
	xiaoshou = models.FloatField(default=0)
	xuke = models.FloatField(default=0)
	shangke = models.FloatField(default=0)
	fixed_shangke = models.FloatField(default=0)
	group_person = models.FloatField(default=0)


class SalaryReceipt(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=64)
	gym = models.IntegerField(default=0)
	year = models.IntegerField(default=0)
	month = models.IntegerField(default=0)
        kpi = models.DecimalField(default=0, max_digits=5, decimal_places=2)
        base = models.IntegerField(default=0)
        course_count = models.IntegerField(default=0)
        course_fee = models.IntegerField(default=0)
        shebao = models.DecimalField(default=0, max_digits=5, decimal_places=2)
        adjustment = models.IntegerField(default=0)
        adjustment_reason = models.CharField(max_length=512, default="")
        archived = models.BooleanField(default=False)
        final = models.DecimalField(default=0, max_digits=10, decimal_places=2)

        def getkpi(self):
            startday = datetime.date(self.year, self.month, 1)
            average = []
            range_end = last_day_of_month(startday)
            range_start = startday - datetime.timedelta(30)
            date_range =[range_start, range_end]
            queryset = Schedule.objects.filter(coach__name=self.name, \
                    date__range=date_range, \
                    coursetype__in=["normal","charge"]) \
                    .order_by("date","hour")

            enddate = range_end

            for i in range(0,30):
                customers = []
                customercount = 0
                coursecount = 0
                floor = enddate - datetime.timedelta(days=30)
                ceil = enddate
                
                for item in queryset:
                    if item.date > ceil or item.date <= floor:
                        continue
                    coursecount += 1
                    if not item.custom in customers:
                        customers.append(item.custom)
                daterange = [floor, ceil]
                allcourses = Schedule.objects.filter(custom__in=customers,\
                        date__range=daterange,coursetype__in=["normal","charge"], done=True)
                coursecount = allcourses.count()

                ##############
                enddate = enddate - datetime.timedelta(days=1)
                if len(customers) != 0 :
                    average.append(float(coursecount)/len(customers))
                
            if len(average) == 0:
                return 0
            return sorted(average)[-1] * 0.95

        def fix_default(self):
            if self.archived == True:
                return
            usr = get_object_or_404(User, name=self.name)
            setting = get_object_or_404(CoachSalarySetting, coach = usr.id, gymfee__gym=self.gym)
            self.base = setting.base_salary

            self.shebao = 383

            #count course
            courses = Schedule.objects.filter(date__year=self.year,
                    date__month=self.month,
                    coach__name = self.name,
                    coursetype__in=["normal","charge"], 
                    done=True)
            self.course_count = courses.count()
            

            self.kpi = self.getkpi()
            #caculate full
            if setting.shangke > 0:
                self.base += courses.aggregate(Sum('price'))['price__sum'] * setting.shangke / 100

            self.course_fee = setting.fixed_shangke
            if self.kpi >= 6:
                self.course_fee *= 1.2

            '''
            if self.adjustment == 0:
                pass
            '''
            groupcoures = GroupCourseInstanceBook.objects.filter(date__year=self.year,
                    date__month=self.month,
                    coach = self.name)
            self.adjustment = (groupcoures.count() * setting.group_person)
            self.adjustment_reason = "团课: " + str(groupcoures.count()) + "人次*" + str(setting.group_person)
            #adjustment = models.IntegerField(default=0)
            #adjustment_reason = models.CharField(max_length=512, default="")
            self.save()


        def to_finance(self):
            usr = get_object_or_404(User, name=self.name)
            memo = usr.displayname + "  " + str(self.year) + "/" + str(self.month) + "  " + str(self.final)
            Finance.objects.create(gym=self.gym, \
                    date = datetime.datetime.today(),
                    brief = memo,
                    by = 'system',
                    op = 'system',
                    cate = '工资支出',
                    amount = int(self.final),
                    channel = '现金',
                    memo = 'auto archieve')
