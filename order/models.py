from django.db import models

# Create your models here.

STATUS_TYPE = (("unpaid","Initialized"),
		("paid","Paid"),
		("booked","Booked"),
		("inprogress","Inprogress"),
		("done","Done"),
		("canceled","Cancelled"),
		("deleted","Deleted"))

class Order(models.Model):
	id = models.AutoField(primary_key=True)
	created = models.DateTimeField(auto_now_add=True)
	gym = models.ForeignKey("business.Gym", to_field="name", related_name="orders", null=True)
	custom = models.ForeignKey("usr.User", to_field="name", related_name="orders", null=True)
	coach = models.ForeignKey("usr.User", to_field="name", related_name="income_orders", null=True)
	billid = models.CharField(max_length=20, blank=True, db_index=True)
	paidtime = models.DateTimeField(blank=True, null=True)
	status = models.CharField(max_length=32)
	parentorder = models.ForeignKey("self", related_name="sub_orders", null=True)
	product = models.ForeignKey("Product", related_name="sold", null=True)
	channel = models.CharField(max_length=10)
	
	isfirst =  models.BooleanField(default=False)
	#this is mean price
	amount = models.IntegerField()

class Product(models.Model):
	id = models.AutoField(primary_key=True)
	coach = models.ForeignKey("usr.User", to_field="name", related_name="products", null=True)
	pic = models.CharField(max_length=256, blank=True)
	introduction = models.TextField(blank=True)
	amount =  models.IntegerField()
	price = models.IntegerField()
	promotion = models.IntegerField(blank=True)
	product_type = models.IntegerField(default=0)


