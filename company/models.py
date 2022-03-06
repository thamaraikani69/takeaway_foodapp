from django.db import models

# Create your models here.
class company(models.Model):
	added_on = models.DateField()
	name = models.TextField()
	email_id = models.TextField()
	address = models.TextField()
	gst = models.TextField()
	phone = models.TextField()
	file = models.TextField()
	status = models.TextField()
	last_change=models.DateTimeField()

	def __str__(self):
		return str(self.id)

class offer(models.Model):
	added_on = models.DateField()
	offer_name = models.TextField()
	offer_percentage=models.IntegerField()
	times = models.BigIntegerField()
	status = models.TextField()
	last_change=models.DateTimeField()

	def __str__(self):
		return str(self.id)

class banner(models.Model):
	added_on = models.DateField()
	bannername = models.TextField()
	banner_order=models.IntegerField()
	banner_image = models.TextField()
	banner_link = models.TextField()
	status = models.TextField()
	last_change=models.DateTimeField()

	def __str__(self):
		return str(self.id)

class item(models.Model):
	added_on = models.DateField()
	code = models.TextField()
	itemname = models.TextField()
	itemimage = models.TextField()
	rate=models.BigIntegerField()
	discount=models.IntegerField()
	dish_cat=models.IntegerField()
	food_cat=models.IntegerField()
	stock = models.IntegerField()
	quantity = models.IntegerField()
	stock_alert = models.IntegerField()
	sales_status= models.IntegerField()
	status = models.TextField()
	last_change=models.DateTimeField()

	def __str__(self):
		return str(self.id)

class catagory(models.Model):
	added_on = models.DateField()
	name = models.TextField()
	order = models.IntegerField()
	status = models.TextField()
	last_change=models.DateTimeField()

	def __str__(self):
		return str(self.id)

class food_catagory(models.Model):
	added_on = models.DateField()
	name = models.TextField()
	dish_image=models.TextField()
	status = models.TextField()
	last_change=models.DateTimeField()

	def __str__(self):
		return str(self.id)

class cat_item(models.Model):
	added_on = models.DateField()
	cat_id = models.IntegerField()
	item_id = models.IntegerField()
	status = models.TextField()
	last_change=models.DateTimeField()

	def __str__(self):
		return str(self.id)

class setting(models.Model):
	added_on = models.DateField()
	name = models.TextField()
	value = models.TextField()
	status = models.TextField()
	last_change=models.DateTimeField()

	def __str__(self):
		return str(self.id)
