from django.db import models
import datetime, calendar

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
	
	isfirst =  models.BooleanField(default=False)
	#this is mean price
	amount = models.IntegerField(default=0)
	duration = models.IntegerField(default=0)
	subsidy = models.IntegerField(default=0)

	def done(self):
		if self.status != 'done' and self.schedule_set.count() == self.product.amount:
			self.status = "done"
			self.coach.order_count += 1
			self.save()
			self.coach.save()
	def cal_endtime(self):
		if self.duration == None or self.duration == 0:
			return "N/A"
		endtime = add_months(self.created, self.duration)
		date_str = datetime.datetime.strftime(endtime,"%Y-%m-%d")
		return date_str

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
        customer = models.IntegerField()
        amount = models.IntegerField()
        status = models.CharField(max_length=64)
        comments = models.CharField(max_length=128,default="")


