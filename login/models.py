from django.db import models

# Create your models here.
class admin_login(models.Model):
	added_on = models.DateField()
	name = models.TextField()
	username = models.TextField()
	password = models.TextField()
	status = models.TextField()
	picture=models.TextField()
	last_change=models.DateTimeField()

	def __str__(self):
		return self.username

class user_login(models.Model):
	added_on = models.DateField()
	name = models.TextField()
	username = models.TextField()
	password = models.TextField()
	status = models.TextField()
	picture=models.TextField()
	last_change=models.DateTimeField()
	otp_time=models.TextField()
	
	def __str__(self):
		return self.username