from django.db import models

class user_offer(models.Model):
	added_on = models.DateField()
	offer_id = models.BigIntegerField()
	customer_id=models.BigIntegerField()
	customer_access = models.TextField()
	last_change=models.DateTimeField()

	def __str__(self):
		return str(self.id)

# Create your models here.
class notification(models.Model):
	added_on = models.DateField()
	noti_type = models.TextField()
	noti_id = models.BigIntegerField()
	customer_id=models.BigIntegerField()
	customer_access=models.TextField()
	noti_status=models.TextField()
	noti_ringtone=models.TextField()
	status = models.TextField()
	last_change=models.DateTimeField()

	def __str__(self):
		return str(self.id)


# Create your models here.
class cart(models.Model):
	added_on = models.DateField()
	total = models.BigIntegerField()
	gst = models.IntegerField()
	after_gst = models.BigIntegerField()
	service_charge = models.IntegerField()
	delivery_charge = models.IntegerField()
	grand_total=models.BigIntegerField()
	customer_id=models.BigIntegerField()
	customer_access=models.TextField()
	cart_status=models.TextField()
	delivery_type=models.TextField()
	arrival_time=models.TimeField()
	payment_id=models.TextField()
	payment_status=models.TextField()
	delivery_name=models.TextField()
	delivery_address=models.TextField()
	status = models.TextField()
	last_change=models.DateTimeField()
	offer_percentage_amount=models.BigIntegerField()

	def __str__(self):
		return str(self.id)

# ----------------------------------------
		# cart_status
		# 'cart' -- stay in cart
		# 'order' -- movie in order
# ----------------------------------------

class cart_item(models.Model):
	added_on = models.DateField()
	cart_id=models.BigIntegerField()
	item_id = models.IntegerField()
	item_name=models.TextField()
	item_image=models.TextField()
	quantity = models.IntegerField()
	bef_disc_price = models.BigIntegerField()
	discount = models.IntegerField()
	price=models.IntegerField()
	status = models.TextField()
	last_change=models.DateTimeField()

	def __str__(self):
		return str(self.id)

class order(models.Model):
	added_on = models.DateField()
	cart_id =models.BigIntegerField()
	total = models.BigIntegerField()
	gst = models.IntegerField()
	after_gst = models.BigIntegerField()
	service_charge = models.IntegerField()
	delivery_charge = models.IntegerField()
	grand_total=models.BigIntegerField()
	customer_id=models.BigIntegerField()
	customer_access=models.TextField()
	order_status=models.TextField()
	delivery_type=models.TextField()
	payment_mode=models.TextField()
	arrival_time=models.TimeField()
	payment_id=models.TextField()
	razor_payment_id=models.TextField()
	razor_signature_id=models.TextField()
	delivery_otp=models.IntegerField()
	confirm_otp=models.IntegerField()
	cancel_reason=models.TextField()
	payment_status=models.TextField()
	delivery_name=models.TextField()
	delivery_address=models.TextField()
	url_hex=models.TextField()
	status = models.TextField()
	last_change=models.DateTimeField()
	offer_percentage_amount=models.BigIntegerField()

	def __str__(self):
		return str(self.id)

# ----------------------------------------
		# order_status
		# 'order placed' 
		# 'order accept'
		# 'preparing food'
		# 'ready for takeaway'
		# 'ready for delivery'
		# 'order handed over'
		# 'order cancelled'
# ----------------------------------------

class order_item(models.Model):
	added_on = models.DateField()
	order_id=models.BigIntegerField()
	item_id = models.IntegerField()
	item_name=models.TextField()
	item_image=models.TextField()
	quantity = models.IntegerField()
	bef_disc_price = models.BigIntegerField()
	discount = models.IntegerField()
	price=models.IntegerField()
	status = models.TextField()
	last_change=models.DateTimeField()

	def __str__(self):
		return str(self.id)

class aibeing(models.Model):
	added_on = models.DateField()
	order_id=models.BigIntegerField()
	payment=models.BigIntegerField()
	Entry_date = models.DateField()
	order_id=models.TextField()
	payment_id=models.TextField()
	payment_signature_id=models.TextField()
	last_change=models.DateTimeField()

	def __str__(self):
		return str(self.id)