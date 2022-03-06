from rest_framework import serializers
from . models import *

class cartSerializer(serializers.ModelSerializer):
	class Meta:
		model=cart
		# fields=('name','username')
		fields='__all__'

class cart_itemSerializer(serializers.ModelSerializer):
	class Meta:
		model=cart_item
		# fields=('name','username')
		fields='__all__'

class orderSerializer(serializers.ModelSerializer):
	class Meta:
		model=order
		# fields=('name','username')
		fields='__all__'

class aibeingSerializer(serializers.ModelSerializer):
	class Meta:
		model=aibeing
		# fields=('name','username')
		fields='__all__'

class order_itemSerializer(serializers.ModelSerializer):
	class Meta:
		model=order_item
		# fields=('name','username')
		fields='__all__'

class notificationSerializer(serializers.ModelSerializer):
	class Meta:
		model=notification
		# fields=('name','username')
		fields='__all__'

class user_offerSerializer(serializers.ModelSerializer):
	class Meta:
		model=user_offer
		# fields=('name','username')
		fields='__all__'