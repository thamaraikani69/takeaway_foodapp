from rest_framework import serializers
from . models import *

class admin_loginSerializer(serializers.ModelSerializer):
	class Meta:
		model=admin_login
		# fields=('name','username')
		fields='__all__'

class user_loginSerializer(serializers.ModelSerializer):
	class Meta:
		model=user_login
		# fields=('name','username')
		fields='__all__'