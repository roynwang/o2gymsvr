# coding=utf-8
from django.db import models
import datetime, calendar
from django.core.cache import cache

# Create your models here.

STATUS_TYPE = (("unpaid","Initialized"),
		("paid","Paid"),
		("booked","Booked"),
		("inprogress","Inprogress"),
		("done","Done"),
		("canceled","Cancelled"),
		("deleted","Deleted"))
def add_months(sourcedate,months):
	month = sourcedate.month - 1 + months
	year = int(sourcedate.year + month / 12 )
	month = month % 12 + 1
	day = min(sourcedate.day,calendar.monthrange(year,month)[1])
	return datetime.date(year,month,day)


class Order(models.Model):
	id = models.AutoField(primary_key=True)
	created = models.DateTimeField(auto_now_add=True)
	gym = models.ForeignKey("business.Gym", to_field="name", related_name="orders", null=True)
	custom = models.ForeignKey("usr.User", to_field="name", related_name="orders", null=True)
	coach = models.ForeignKey("usr.User", to_field="name", related_name="income_orders", null=True)
	billid = models.CharField(max_length=20, blank=True, db_index=True)
	paidtime = models.DateTimeField(blank=True, null=True)
	status = models.CharField(max_length=32, blank=True)
	parentorder = models.ForeignKey("self", related_name="sub_orders", null=True)
	product = models.ForeignKey("Product", related_name="sold", null=True)
	channel = models.CharField(max_length=10,blank=True)
	product_duration_type = models.CharField(max_length=32,blank=True, default='month')
	
	isfirst =  models.BooleanField(default=False)
	#this is mean price
	amount = models.IntegerField(default=0)
	duration = models.IntegerField(default=0)
	subsidy = models.IntegerField(default=0)
	ordertype = models.CharField(max_length=32,default="pt")

        def refresh(self):
		if self.status == 'done' and self.schedule_set.all().count() != self.product.amount:
			self.status = "inprogress"
                        self.save()

	def done(self):
		if self.status != 'done' and self.schedule_set.filter(done=True).count() == self.product.amount:
			self.status = "done"
			self.coach.order_count += 1
			self.save()
			self.coach.save()
                        self.custom.order_status = None
                        self.custom.save()
	def cal_endtime(self):
		if self.duration == None or self.duration == 0:
			return "N/A"
		if self.product_duration_type == 'month':
			endtime = add_months(self.created, self.duration)
		if self.product_duration_type == 'day':
			endtime = self.created + datetime.timedelta(days=1)
		date_str = datetime.datetime.strftime(endtime,"%Y-%m-%d")
		return date_str

        def expire_notification(self):
	    today = datetime.datetime.today().date()
            mkey = "o2_" + self.billid + "_" + str(today)
            checked = cache.get(mkey)
            if not checked is None:
                return
            cache.set(mkey, 1, 60*60*24)

            if self.status == "inprogress" or self.status == "paid":

                from business.models import Todo
		if self.duration == None or self.duration == 0:
			return "N/A"
		endtime = add_months(self.paidtime, self.duration)
                delta = endtime - today
                d = 0
                if delta.days == 60:
                    d = 60
                    #create notification
                if delta.days == 30:
                    d = 30
                    #create notification
                if delta.days == 10:
                    d = 10
                    #create notification
                if delta.days == 3:
                    d = 3
                    #create notification
                print d
                if d == 0:
                    return

                print "creating ........" + self.billid
                Todo.objects.create( \
                        content = self.custom.displayname + "订单还有" + str(d) + "天过期",
                        gym = self.gym.id,\
                        by = "系统通知",\
                        schedule_date = today)

                


class Product(models.Model):
	id = models.AutoField(primary_key=True)
	coach = models.ForeignKey("usr.User", to_field="name", related_name="products", null=True)
	pic = models.CharField(max_length=256, blank=True)
	introduction = models.TextField(blank=True)
	amount =  models.IntegerField()
	price = models.IntegerField()
	promotion = models.IntegerField(blank=True)
	product_type = models.IntegerField(default=0)



class BalanceOrder(models.Model):
	id = models.AutoField(primary_key=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	billid = models.CharField(max_length=20, blank=True, db_index=True)
        customer = models.CharField(max_length=64)
        groupcourse_count = models.IntegerField(default=0)
        amount = models.IntegerField()
        gym = models.IntegerField()
        paid_amount = models.IntegerField(default=0)
        status = models.CharField(max_length=64)
        comments = models.CharField(max_length=128,default="")


