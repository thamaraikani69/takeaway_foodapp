from rest_framework import serializers
from . models import *

class companySerializer(serializers.ModelSerializer):
	class Meta:
		model=company
		# fields=('name','username')
		fields='__all__'

class bannerSerializer(serializers.ModelSerializer):
	class Meta:
		model=banner
		fields='__all__'
class offerSerializer(serializers.ModelSerializer):
	class Meta:
		model=offer
		fields='__all__'
class itemSerializer(serializers.ModelSerializer):
	class Meta:
		model=item
		fields='__all__'

class catSerializer(serializers.ModelSerializer):
	class Meta:
		model=catagory
		fields='__all__'

class foodcatSerializer(serializers.ModelSerializer):
	class Meta:
		model=food_catagory
		fields='__all__'

class catitemSerializer(serializers.ModelSerializer):
	class Meta:
		model=cat_item
		fields='__all__'

class settingSerializer(serializers.ModelSerializer):
	class Meta:
		model=setting
		fields='__all__'