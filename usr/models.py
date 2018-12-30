# coding=utf-8
from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import datetime
from business.models import *


# Create your models here.
class CurrentVersion(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=64)
	client = models.CharField(max_length=64)
        version = models.IntegerField()

class CoachKpi(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=64)
        startdate = models.DateField()
        enddate = models.DateField()
        dimension = models.CharField(max_length=64)
        cate = models.CharField(max_length=64)
        value = models.CharField(max_length=1024)
        gym = models.IntegerField()

        #private
        @classmethod
        def archieve_range(cls,name,startdate, enddate, dimension):
            usr = User.objects.get(name=name)
            gym = usr.gym.first().id
            #query courses
            courses = usr.sealed_time.filter(date__range=[startdate,enddate],\
                    done=True)

            ret = []
            ret.append({"option":"活跃客户数",\
                    "value":cls.count_customer(courses)})
            ret.append({"option":"体验课完成",\
                    "value":cls.count_trial(courses)})
            ret.append({"option":"课程完成",\
                    "value":cls.count_normal(courses)})
            ret.append({"option":"训练计划完成",\
                    "value":cls.count_planned(courses)})
            ret.append({"option":"计划客户阅读",\
                    "value":cls.count_plan_read(courses)})
            ret.append({"option":"期望数据记录人数",\
                    "value":cls.count_expected_eval(courses)})
            ret.append({"option":"完成数据记录人数",\
                    "value":cls.count_actual_eval(courses, startdate, enddate)})
            #query eval
            datestr = str(startdate)
            for item in ret:
                v = item['value']
                if not isinstance(v, str) or not isinstance(v, unicode):
                    v = str(item['value'])
                CoachKpi.objects.create(name=name,\
                        startdate=startdate,\
                        enddate=enddate,\
                        cate=item['option'],\
                        value=v,\
                        dimension=dimension,\
                        gym=gym)


        @classmethod
        def count_order(self, usr, startdate,enddate):
            enddate = enddate.datetime() + datetime.timedelta(days = 1)
            return usr.income_orders.filter(\
                    paidtime__range=[startdate.datetime(),enddate]).count()

        @classmethod
        def count_actual_eval(self, courses, startdate, enddate):
            ret = []
            cts = []
            for c in courses:
                if c.action_required == "数据测量" and c.coursetype != "trial" and not c.custom in cts:
                    cts.append(c.custom)
                    if BodyEval.objects.filter(date__range=[startdate,enddate], name = c.custom.name).count() > 0:
                        ret.append(c.custom.displayname)
            ret = str(len(ret)) + ":" + ",".join(ret)
            return ret

        @classmethod
        def count_customer(self,courses):
            cts = []
            for c in courses:
                if c.coursetype != "trial" and not c.custom in cts:
                    cts.append(c.custom)
            return len(cts)

        #private

        @classmethod
        def count_normal(self, courses=None):
            ret = 0
            for c in courses:
                if c.coursetype != "trial":
                    ret += 1
            return ret

        @classmethod
        def count_trial(self, courses=None):
            ret = 0
            for c in courses:
                if c.coursetype == "trial":
                    ret += 1
            return ret


        @classmethod
        def count_expected_eval(self, courses):
            cts = []
            ret = []
            for c in courses:
                if c.action_required == "数据测量" and c.coursetype != "trial" and not c.custom in cts:
                    cts.append(c.custom)
                    ret.append(c.custom.displayname)
            ret = str(len(cts)) + ":" + ",".join(ret)
            return ret



        @classmethod
        def count_planned(self, courses):
            ret = 0
            for c in courses:
                if not c.detail is None and len(c.detail)>5:
                    ret += 1
            return ret

        @classmethod
        def count_plan_read(self, courses):
            ret = 0
            for c in courses:
                if c.user_confirmed:
                    ret += 1
            return ret


class User(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=64, db_index=True, unique=True)
	displayname = models.CharField(max_length=128)
	iscoach = models.BooleanField(default=False)
	created = models.DateTimeField(default=datetime.datetime.now())
	avatar = models.CharField(max_length=256,default=settings.DEFAULT_AVATAR)

	upped = models.ManyToManyField("weibo.Weibo", related_name="up_by", null=True)
	fwded = models.ManyToManyField("weibo.Weibo", related_name="fwd_by", null=True)
	commented = models.ManyToManyField("weibo.Weibo", related_name="comment_by",null=True)

	upped_person = models.ManyToManyField("self", related_name="up_by",null=True)
	upnum = models.IntegerField(default=0)

	recommand_p = models.IntegerField(blank=True, null=True)

	#for coach
	tags = models.CharField(max_length=64, blank=True, default="")
	introduction = models.CharField(max_length=1024, blank=True, default="") 

	order_count = models.IntegerField(default=0)
	rate = models.IntegerField(default=0)
	course_count = models.BigIntegerField(default=0)
	
	sex = models.BooleanField(default=True)
	signature = models.CharField(max_length=64, blank=True)
	
	openid = models.CharField(max_length=64,unique=True,db_index=True, blank=True, default="")

	role = models.CharField(max_length=32, default="customer")
	corps = models.CharField(max_length=512, default="[]")

	age = models.IntegerField(blank=True, null=True)

	can_book = models.BooleanField(default=True)

	disable_complete = models.BooleanField(default=False)

	birthday = models.DateField(blank=True, null=True)

	flag = models.IntegerField(default=0)

	trial = models.IntegerField(blank=True, null=True)

	comments = models.CharField(max_length=64, blank=True, null=True)
	emergency_contact = models.CharField(max_length=64, blank=True)

        balance = models.IntegerField(default=0)

	trial_coach = models.CharField(max_length=64, blank=True, default="")

	owner = models.CharField(max_length=64,default="") 
	order_status = models.CharField(max_length=32,default=None,blank=True,null=True) 

	train_comments = models.CharField(max_length=512, default="",blank=True)

        custom_avatar = models.CharField(max_length=512, default="",blank=True)

        def get_coach_gym(self):
            return self.gym.all()[0]

        def get_frequency(self, days):
            startday = datetime.datetime.today().date() + datetime.timedelta(days=-days)
            return self.booked_time.filter(date__gt=startday, done=True).count()

        def save_owner(self, coach):
            self.owner = coach.name
            self.save()

        def find_owner(self):
            q = self.booked_time.order_by("-date")
            if q.count() > 0:
                if q[0].coursetype != 'trial':
                    self.save_owner(q[0].coach)

        def update_owner_status(self):
            q = self.orders.all()
            for o in q:
                donecount = o.schedule_set.filter(done=True).count()
                if donecount == o.product.amount:
                    o.status = "done"
                    o.save()
                self.order_status = o.status
                if o.status != 'done':
                    break
            self.save()

        def get_to_next_eval(self):
            evals = BodyEval.objects.filter(name=self.name).order_by("-date")
            if evals.count() == 0:
                return (0, 0)
            last_eval = evals[0]
            today = datetime.date.today()
            delta_day = 40 - (today - last_eval.date).days
            delta_train = 8 - self.booked_time.filter(date__gt=last_eval.date, done=True).count()
            if delta_day < 0:
                delta_day = 0
            if delta_train < 0:
                delta_train = 0
            return (delta_day, delta_train)

        def trySendEvalNotification(self, schedule):
            require_measure = False
            evals = BodyEval.objects.filter(name=self.name).order_by("-date")
            if schedule.coursetype != "trial" and evals.count() == 0:
                require_measure = True
            if not require_measure and not schedule.is_first_course():
                #1 should after 30 day after last eval
                if evals.count() == 0:
                    return
                last_eval = evals[0]
                delta = schedule.date - last_eval.date 
                if delta.days > 40:
                    require_measure = True
                '''
                else:
                    times = self.booked_time.filter(date__gt=last_eval.date).count()
                    if times < 8:
                        return
                    require_measure = True
                '''

            #3 send all in the gym
            order = self.booked_time.order_by("-date")[0].order
            if not order:
                gym = 31
            else:
                gym = order.gym.id

            if require_measure and gym in [19,31]:
                schedule.action_required = "数据测量"
                schedule.save()
                Todo.objects.create( \
                        content = schedule.custom.displayname + "需要测量",
                        gym = gym,\
                        by = "系统通知",\
                        schedule_date = schedule.date)
                #create todo
                message = Message.objects.create(name=schedule.coach.name, \
                        by=self.name, \
                        content= self.displayname +"需要进行数据测量", \
                        link="", \
                        dismiss_date=schedule.date)

            '''
            for coach in gym.coaches.all():
                if coach.role != 'admin' or coach.name == schedule.coach.name:
                    continue
                message = Message.objects.create(name=coach.name, \
                        by=self.name, \
                        content= self.displayname +"需要进行数据测量", \
                        link="", \
                        dismiss_date=schedule.date)
            '''


	def __unicode__(self):
		return self.name


        def get_trial_count(self,start,end):
            #try to get 
	    daterange = [startdate, enddate]
            #if empty try 
            count = self.booked_time.filter(done=True,coursetype="trial",date__range=daterange).count()
            #save
            return count
        

        def get_order_count(self,start,end):
            pass

        def get_course_completed(self,start,end):
            count = self.booked_time.filter(done=True,date__range=daterange).exclude(coursetype="trial")
            return count

        def get_active_customer(self,start,end):
            self.booked_time.filter(done=True,date__range=daterange).values_list('custom', flat=True)
            pass

        def get_unactive_customer(self,start,end):
            pass
        
        def get_30_train_times(self):
            mkey = self.name + "_30_train_times"
            mdetail = cache.get(mkey)
            if not mdetail:
                mdetail = self.booked_time.filter(done=True,\
                        date__gte=datetime.datetime.now() - datetime.timedelta(days=30)).count()
                cache.set(mkey, mdetail, 60*60*24)
            return mdetail



class Balance(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=64, db_index=True)
        gym = models.IntegerField()
        balance = models.IntegerField(default=0)
        gift = models.IntegerField(default=0)
        group_enddate = models.DateField(null=True, blank=True)
        groupcourse_count = models.IntegerField(default=0)

        def charge(self, amount, gift = 0):
            self.balance += int(amount)
            self.gift += gift
            self.save()

        def charge_groupcourse_count(self,groupcourse_count):
            self.groupcourse_count += groupcourse_count
            self.save()

        def add_months(self, sourcedate,months):
            month = sourcedate.month - 1 + months
            year = int(sourcedate.year + month / 12 )
    	    month = month % 12 + 1
	    day = min(sourcedate.day,calendar.monthrange(year,month)[1])
	    return datetime.date(year,month,day)


        def charge_date(self, price, duration):
            startdate = self.group_enddate
            if not startdate:
                startdate = datetime.date.today()
            enddate = self.add_months(startdate,duration)
            self.group_enddate = enddate
            self.consume(price)


        def consume(self, amount):
            self.balance -= int(amount)
            self.save()

        def consume_groupcourse(self):
            self.groupcourse_count -= 1
            self.save()

        def cancelconsume(self, amount):
            self.balance += int(amount)
            self.save()
        
        def cancelconsume_groupcourse(self, amount=1):
            self.groupcourse_count += amount
            self.save()

        def precheck(self, amount):
            if self.balance >= amount:
                return True
            return False

        def complete_order(self, balance_order):
            if balance_order.status == "completed":
                return
            balance_order.status="completed"
            balance_order.save()
            gift = balance_order.amount - balance_order.paid_amount
            if balance_order.groupcourse_count != 0:
                self.charge_groupcourse_count(balance_order.groupcourse_count)
            else:
                self.charge(balance_order.amount, gift)
        

class ChargeHistory(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=64, db_index=True)
	price = models.IntegerField(default=0)
	amount = models.IntegerField(default=0)
	gym = models.IntegerField(default=0)
	created = models.DateTimeField(default=datetime.datetime.now())


class TimeLine(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.OneToOneField(User, to_field="name", unique=True, related_name="timeline")
	feed = models.ManyToManyField('weibo.Weibo', related_name="feeder")
	followedby = models.ManyToManyField('TimeLine', related_name='follows')
	refresh = models.ManyToManyField('weibo.Weibo')

	def __unicode__(self):
		return self.name

class WorkingDays(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=64, db_index=True, unique=True)
	weekrest = models.CharField(max_length=32, default="")
	excep_rest = models.CharField(max_length=1024, default="")
	excep_work = models.CharField(max_length=1024, default="")
	out_hours = models.CharField(max_length=64, default="")
	noon_hours = models.CharField(max_length=32, default="")

class FeedBack(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=64, db_index=True)
	feedback = models.CharField(max_length=1024, default="")
	created = models.DateTimeField(default=datetime.datetime.now())


class TagIndex(models.Model):
	id = models.AutoField(primary_key=True)
	tag = models.CharField(max_length=64, db_index=True)
	name = models.CharField(max_length=64)
	gym = models.IntegerField()
	created = models.DateTimeField(default=datetime.datetime.now())









