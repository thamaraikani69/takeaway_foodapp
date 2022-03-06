							
							# ---------------- Shivaya nama om -------------------------------

from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.db import connection
import json

# -- Rest APi Framework --#
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# -- Imports --#
from . models import *
from customer.models import *
from . serializers import *
from customer.serializers import *
from login.apps import *
from login.tokenvalidation import *

# Create your views here.
class api_company(APIView):

	def get(self,request):
		access=rights(request)['access']
		access_id=rights(request)['access_id']

		if access_cretential(access,'view_company'):
			company_check=company.objects.all()
			company_check=companySerializer(company_check,many=True)
			company_data=company_check.data

			return Response({'message':True,'data':company_data})
		else:
			return Response({'message':"Invalid Access"})
		
	def post(self,request):

		data=json.loads(request.body)
		company_name=data['company_name']
		email=data['email']
		address=data['address']
		gst=data['gst']
		phonenumber=data['phonenumber']
		filename=data['filename']
		access=data['access']
		access=rights(request)['access']
		access_id=rights(request)['access_id']
		status='active'
		added_on=today()
		last_change_=last_change()

		if access_cretential(access,'company'):
			company_check=company.objects.all()
			company_check=companySerializer(company_check,many=True)
			company_check=company_check.data
			if company_check==[]:
				try:
					add_company=company(added_on=added_on,name=company_name,email_id=email,address=address,gst=gst,phone=phonenumber,file=filename,status=status,last_change=last_change_)
					add_company.save()
					return Response({'message':True,'access':access,'data':str(add_company)})
				except Exception as e:
					return Response({'message':str(e)})
			else:
				update_company=company.objects.filter(id=company_check[0]['id']).update(name=company_name,email_id=email,address=address,gst=gst,phone=phonenumber,status=status,last_change=last_change_)

				return Response({'message':True,'access':access,'data':str(company_check[0]['id'])})
		else:
			return Response({'message':"Invalid Access"})

class api_service_fee(APIView):

	def get(self,request):
		access=rights(request)['access']
		access_id=rights(request)['access_id']

		if access_cretential(access,'company'):
			data=json.loads(request.body)
			service_type=data['type']
			if service_type=='fee':
				change_aibeing=aibeing.objects.filter(payment=0).update(payment=1)
				cursor=connection.cursor()
				cursor.execute("SELECT * from customer_aibeing,customer_order where customer_aibeing.order_id=customer_order.id and customer_aibeing.payment=1")
				aibeing_data=dictfetchall(cursor)

				tot_service_cost=0
				payment_id=""
				if aibeing_data!=[]:
					id=1
					for i in aibeing_data:
						id=i['id']
						tot_service_cost=tot_service_cost+i['service_charge']

					# ========================= Razor pay order =======================
					razor_trans_id=aibeing_razorpay_trans(product_id=id,order_amount=tot_service_cost,currency='INR')
					if razor_trans_id['message']==True:
						payment_id=razor_trans_id['trans_data']['trans_id']
					else:
						payment_id=None
						return Response({'message':razor_trans_id['message']})
				# print(tot_service_cost)
			return Response({'message':True,'data':{'order_data':aibeing_data,'service_charges':tot_service_cost,'payment_id':payment_id}})
		else:
			return Response({'message':"Invalid Access"})

	def post(self,request):

		
		data=json.loads(request.body)
		service_type=data['type']
		if service_type=='fee':
			payment_id=data['payment_id']
			signature=data['signature']
			order_id=data['order_id']

			added_on=today()
			last_change_=last_change()

			change_aibeing=aibeing.objects.filter(payment=1).update(Entry_date=added_on,payment=2,payment_id=payment_id,payment_signature_id=signature,last_change=last_change_)
			
			return Response({'message':True})
		else:
			return Response({'message':"Invalid Access"})

class api_offer(APIView):
	def post(self,request):
		data=json.loads(request.body)
		
		added_on=today()
		last_change_=last_change()

		offer_name=data['offer_name']
		offer_percentage=data['offer_percentage']
		status="active"
		times=data['times']
		# offer_cat=data['offer_cat']

		access=rights(request)['access']
		access_id=rights(request)['access_id']

		if access_cretential(access,'banner_add'):
			offer_List=offer.objects.all()
			serializer=offerSerializer(offer_List,many=True)
			offer_check=serializer.data
			try:
				if offer_check==[]:
					add_offer=offer(added_on=added_on,offer_name=offer_name,offer_percentage=offer_percentage,times=times,status=status,last_change=last_change_)
					add_offer.save()
				else:
					# if offer_cat=='update':
					# 	offer_List=offer.objects.all().filter(offer_name=offer_name)
					# 	serializer=offerSerializer(offer_List,many=True)
					# 	offer_check=serializer.data
					# 	if offer_check==[]:
					# 		add_offer=offer.objects.filter(status='active').update(status='inactive',last_change=last_change_)
					# 		add_offer=offer(added_on=added_on,offer_name=offer_name,offer_percentage=offer_percentage,times=times,status=status,last_change=last_change_)
					# 	else:
					# 		add_offer=offer.objects.filter(status='active').update(status='inactive',last_change=last_change_)
					# 		add_offer=offer.objects.filter(offer_name=offer_name).update(status='active',last_change=last_change_,offer_percentage=offer_percentage,times=times)
					# else:
					add_offer=offer.objects.filter(status='active').update(status='inactive',last_change=last_change_)
					add_offer=offer(added_on=added_on,offer_name=offer_name,offer_percentage=offer_percentage,times=times,status=status,last_change=last_change_)
					add_offer.save()
				return Response({'message':True,'data':str(offer_name),'access':access})
			except Exception as e:
				return Response({'message':str(e)})
		else:
			return Response({'message':'Invalid Access'})

	def get(self,request):
		access=rights(request)['access']
		access_id=rights(request)['access_id']

		if access_cretential(access,'banner'):
			
			offer_List=offer.objects.all().order_by('-id')
			serializer=offerSerializer(offer_List,many=True)
			return Response({'message':True,'data':serializer.data})
		else:
			return Response({'message':'Invalid Access'})


class api_banner(APIView):
	def post(self,request):
		data=json.loads(request.body)
		
		added_on=today()
		last_change_=last_change()

		bannername=data['bannername']
		banner_order=data['bannerorder']
		banner_image=data['bannerimage']
		banner_link=data['bannerlink']
		status=data['bannerstatus']
		access=data['access']
		access=rights(request)['access']
		access_id=rights(request)['access_id']

		if access_cretential(access,'banner_add'):
			try:
				add_banner=banner(added_on=added_on,bannername=bannername,banner_order=banner_order,banner_image=banner_image,banner_link=banner_link,status=status,last_change=last_change_)
				add_banner.save()
				return Response({'message':True,'data':str(add_banner),'access':access})
			except Exception as e:
				return Response({'message':str(e)})
		else:
			return Response({'message':'Invalid Access'})

	def get(self,request):
		access=rights(request)['access']
		access_id=rights(request)['access_id']

		if access_cretential(access,'banner'):
			data=json.loads(request.body)
			type_=data['type']
			if type_=="ALL":
				banner_List=banner.objects.all().order_by('-id')
				serializer=bannerSerializer(banner_List,many=True)
				return Response({'message':True,'data':serializer.data})

			elif type_=="one":
				id=data['id']
				banner_List=banner.objects.all().filter(id=id)
				serializer=bannerSerializer(banner_List,many=True)
				return Response({'message':True,'data':serializer.data})
			else:
				return Response({'message':'Invalid Data'})
		else:
			return Response({'message':'Invalid Access'})

	def put(self,request):
		data=json.loads(request.body)
		
		added_on=today()
		last_change_=last_change()

		bannername=data['bannername']
		id=data['id']
		banner_order=data['bannerorder']
		banner_image=data['bannerimage']
		banner_link=data['bannerlink']
		status=data['bannerstatus']
		access=data['access']
		access=rights(request)['access']
		access_id=rights(request)['access_id']

		if access_cretential(access,'banner_add'):
			try:
				add_banner=banner.objects.filter(id=id).update(bannername=bannername,banner_order=banner_order,banner_link=banner_link,status=status,last_change=last_change_)
				return Response({'message':True,'data':str(add_banner),'access':access})
			except Exception as e:
				return Response({'message':str(e)})
		else:
			return Response({'message':'Invalid Access'})

class api_item(APIView):
	def post(self,request):
		data=json.loads(request.body)
		
		added_on=today()
		last_change_=last_change()
		code=data['code']
		itemname=data['itemname'].lower()
		itemimage=data['itemimage']
		rate=data['rate']
		discount=data['discount']
		food_cat=data['food_cat']
		dish_cat=data['dish_cat']
		stock=data['stock']
		quantity=data['quantity']
		stock_alert=data['stock_alert']
		sales_status=data['sales_status']
	
		if int(stock)==0:
			quantity=0
			stock_alert=0

		access=data['access']
		status='active'
		access=rights(request)['access']
		access_id=rights(request)['access_id']
		
		if access_cretential(access,'item_add'):
			try:
				item_List=item.objects.all().filter(itemname=itemname,code=code)
				serializer=itemSerializer(item_List,many=True)
				item_check=serializer.data
				print('_______________________________________',item_check)
				if item_check == []:

					add_item=item(added_on=added_on,code=code,itemname=itemname,itemimage=itemimage,rate=rate,discount=discount,dish_cat=dish_cat,food_cat=food_cat,stock=stock,quantity=quantity,stock_alert=stock_alert,sales_status=sales_status,status=status,last_change=last_change_)
					add_item.save()
					return Response({'message':True,'data':str(add_item),'access':access})
				else:
					return Response({"message":'Already Item Name Registered!!'})
			except Exception as e:
				return Response({'message':str(e)})
		else:
			return Response({'message':'Invalid Access'})

	def get(self,request):
		access=rights(request)['access']
		access_id=rights(request)['access_id']

		if access_cretential(access,'item'):
			data=json.loads(request.body)
			type_=data['type']
			if type_=="ALL":
				item_List=item.objects.all().order_by('-id')
				serializer=itemSerializer(item_List,many=True)
				return Response({'message':True,'data':serializer.data})
			elif type_=="one":
				id=data['id']
				item_List=item.objects.all().filter(id=id)
				serializer=itemSerializer(item_List,many=True)
				return Response({'message':True,'data':serializer.data})
			else:
				return Response({'message':'Invalid Data'})
		else:
			return Response({'message':'Invalid Access'})

	def put(self,request):
		data=json.loads(request.body)
		
		added_on=today()
		last_change_=last_change()
		code=data['code']
		itemname=data['itemname']
		itemimage=data['itemimage']
		rate=data['rate']
		discount=data['discount']
		food_cat=data['food_cat']
		dish_cat=data['dish_cat']
		stock=data['stock']
		quantity=data['quantity']
		stock_alert=data['stock_alert']
		id=data['id']
		sales_status=data['sales_status']
	
		if int(stock)==0:
			quantity=0
			stock_alert=0

		access=data['access']
		if int(sales_status)==10:
			status='active'
		else:
			status='inactive'
		access=rights(request)['access']
		access_id=rights(request)['access_id']
		
		if access_cretential(access,'item_add'):
			item_List=item.objects.all().exclude(id=id).filter(itemname=itemname,code=code)
			serializer=itemSerializer(item_List,many=True)
			item_check=serializer.data
			print('_______________________________________',item_check)
			if item_check == []:
				try:
					add_item=item.objects.filter(id=id).update(code=code,itemname=itemname,rate=rate,discount=discount,dish_cat=dish_cat,food_cat=food_cat,stock=stock,quantity=quantity,stock_alert=stock_alert,sales_status=sales_status,status=status,last_change=last_change_)
					
					return Response({'message':True,'data':str(add_item),'access':access})
				except Exception as e:
					return Response({'message':str(e)})
		else:
			return Response({'message':'Invalid Access'})

class api_cat(APIView):
	def post(self,request):
		data=json.loads(request.body)
		
		added_on=today()
		last_change_=last_change()
		name=data['name']
		order=data['order']

		access=data['access']
		status='active'

		access=rights(request)['access']
		access_id=rights(request)['access_id']

		if access_cretential(access,'cat_add'):
			try:
				add_cat=catagory(added_on=added_on,name=name,order=order,status=status,last_change=last_change_)
				add_cat.save()
				return Response({'message':True,'data':str(add_cat),'access':access})
			except Exception as e:
				return Response({'message':str(e)})
		else:
			return Response({'message':'Invalid Access'})

	def put(self,request):
		data=json.loads(request.body)
		
		added_on=today()
		last_change_=last_change()
		id=data['id']
		name=data['name']
		order=data['order']

		access=data['access']
		status='active'

		access=rights(request)['access']
		access_id=rights(request)['access_id']

		if access_cretential(access,'cat_add'):
			try:
				add_cat=catagory.objects.filter(id=id).update(name=name,order=order,status=status,last_change=last_change_)
				return Response({'message':True,'data':str(add_cat),'access':access})
			except Exception as e:
				return Response({'message':str(e)})
		else:
			return Response({'message':'Invalid Access'})

	def get(self,request):
		access=rights(request)['access']
		access_id=rights(request)['access_id']
		if access_cretential(access,'cat'):
			data=json.loads(request.body)
			type_=data['type']
			if type_=="ALL":
				cat_List=catagory.objects.all()
				serializer=catSerializer(cat_List,many=True)
				return Response({'message':True,'data':serializer.data})
			elif type_=="one":
				id=data['id']
				cat_List=catagory.objects.all().filter(id=id)
				serializer=catSerializer(cat_List,many=True)
				return Response({'message':True,'data':serializer.data})
			else:
				return Response({'message':'Invalid Data'})

		else:
			return Response({'message':'Invalid Access'})

class api_catitem(APIView):
	def post(self,request):
		data=json.loads(request.body)
		
		added_on=today()
		last_change_=last_change()
		cat_id=data['cat_id']
		itemid=data['itemid']
		access=data['access']
		status='active'

		access=rights(request)['access']
		access_id=rights(request)['access_id']

		if access_cretential(access,'catitem_add'):
			if int(itemid)==0:
				item_List=item.objects.all()
				serializer=itemSerializer(item_List,many=True)
				item_check=serializer.data
				if item_check!=[]:
					for i in item_check:
						itemid=i['id']
						try:
							catitem_check=cat_item.objects.all().filter(item_id=itemid,cat_id=cat_id)
							serializer=catitemSerializer(catitem_check,many=True)

							if serializer.data==[]:
								add_catitem=cat_item(added_on=added_on,cat_id=cat_id,item_id=itemid,status=status,last_change=last_change_)
								add_catitem.save()
							else:
								print({'message':'Already Added!!'})
						except Exception as e:
							print("Exception food add ",e)
							# return Response({'message':str(e)})
					return Response({'message':True,'data':str(add_catitem),'access':access})

			else:
				try:
					catitem_check=cat_item.objects.all().filter(item_id=itemid,cat_id=cat_id)
					serializer=catitemSerializer(catitem_check,many=True)

					if serializer.data==[]:
						add_catitem=cat_item(added_on=added_on,cat_id=cat_id,item_id=itemid,status=status,last_change=last_change_)
						add_catitem.save()
						return Response({'message':True,'data':str(add_catitem),'access':access})
					else:
						return Response({'message':'Already Added!!'})
				except Exception as e:
					return Response({'message':str(e)})
		else:
			return Response({'message':'Invalid Access'})

	def get(self,request):
		access=rights(request)['access']
		access_id=rights(request)['access_id']
		if access_cretential(access,'catitem'):
			data=json.loads(request.body)
			type_=data['type']
			if type_=="ALL":
				try:
					cursor=connection.cursor()
					cursor.execute("SELECT *,company_cat_item.id as cat_item_id from company_cat_item,company_item,company_catagory where company_cat_item.item_id=company_item.id and company_cat_item.cat_id=company_catagory.id")
					catitemlist_data=dictfetchall(cursor)

					return Response({'message':True,'data':catitemlist_data})
				finally:
					cursor.close()
					connection.close()
			
			elif type_=="one_all":
				cat_id=data['cat_id']

				try:
					cursor=connection.cursor()
					cursor.execute("SELECT * from company_cat_item,company_item,company_catagory where company_cat_item.item_id=company_item.id and company_cat_item.cat_id=company_catagory.id and company_cat_item.cat_id=%s ",(cat_id,))
					catitemlist_data=dictfetchall(cursor)

					return Response({'message':True,'data':catitemlist_data})
				finally:
					cursor.close()
					connection.close()

			elif type_=="one":
				id=data['id']
				catitem_List=cat_item.objects.all().filter(id=id)
				serializer=catitemSerializer(catitem_List,many=True)
				return Response({'message':True,'data':serializer.data})
			else:
				return Response({'message':'Invalid Data'})
		else:
			return Response({'message':'Invalid Access'})

class api_foodcat(APIView):
	def post(self,request):
		data=json.loads(request.body)
		
		added_on=today()
		last_change_=last_change()
		name=data['name']

		access=data['access']
		dish_image=data['dish_image']
		status='active'
		
		access=rights(request)['access']
		access_id=rights(request)['access_id']

		if access_cretential(access,'foodcat_add'):
			try:
				add_foodcat=food_catagory(added_on=added_on,name=name,dish_image=dish_image,status=status,last_change=last_change_)
				add_foodcat.save()
				return Response({'message':True,'data':str(add_foodcat),'access':access})
			except Exception as e:
				return Response({'message':str(e)})
		else:
			return Response({'message':'Invalid Access'})

	def get(self,request):
		access=rights(request)['access']
		access_id=rights(request)['access_id']
		if access_cretential(access,'foodcat'):
			data=json.loads(request.body)
			type_=data['type']
			if type_=="ALL":
				foodcat_List=food_catagory.objects.all()
				serializer=foodcatSerializer(foodcat_List,many=True)
				return Response({'message':True,'data':serializer.data})
			elif type_=="one":
				id=data['id']
				foodcat_List=food_catagory.objects.all().filter(id=id)
				serializer=foodcatSerializer(foodcat_List,many=True)
				return Response({'message':True,'data':serializer.data})
			else:
				return Response({'message':'Invalid Data'})
		else:
			return Response({'message':'Invalid Access'})

	def put(self,request):
		data=json.loads(request.body)
		
		added_on=today()
		last_change_=last_change()
		name=data['name']
		id=data['id']

		access=data['access']
		dish_image=data['dish_image']
		status='active'
		
		access=rights(request)['access']
		access_id=rights(request)['access_id']

		if access_cretential(access,'foodcat_add'):
			try:
				add_foodcat=food_catagory.objects.filter(id=id).update(name=name,status=status,last_change=last_change_)
				return Response({'message':True,'data':str(add_foodcat),'access':access})
			except Exception as e:
				return Response({'message':str(e)})
		else:
			return Response({'message':'Invalid Access'})

class api_setting(APIView):
	def post(self,request):
		data=json.loads(request.body)
		
		added_on=today()
		last_change_=last_change()
		
		delivery_charges=data['delivery_charges']
		gst=data['gst']
		service_charges=data['service_charges']
		tax=data['tax']
		delivery=data['delivery']
		take_away=data['take_away']
		cash_pay=data['cash_pay']
		online=data['online']
		stock_maintance=data['stock_maintance']
		shop_status=data['shop_status']
		final_datelist=data['final_datelist']

		if tax=='off':
			gst=0
		status='active'

		access=rights(request)['access']
		access_id=rights(request)['access_id']

		if access_cretential(access,'setting'):
			try:
				setting_List=setting.objects.all().filter(name='delivery_charge')
				serializer=settingSerializer(setting_List,many=True)
				setting_check=serializer.data
		
				if setting_check==[]:
					add_setting=setting(added_on=added_on,name='delivery_charge',value=delivery_charges,status=status,last_change=last_change_)
					add_setting.save()
				else:
					update_setting=setting.objects.filter(name='delivery_charge').update(value=delivery_charges,last_change=last_change_)

				setting_List=setting.objects.all().filter(name='gst')
				serializer=settingSerializer(setting_List,many=True)
				setting_check=serializer.data

				if setting_check==[]:
					add_setting=setting(added_on=added_on,name='gst',value=gst,status=status,last_change=last_change_)
					add_setting.save()
				else:
					update_setting=setting.objects.filter(name='gst').update(value=gst,last_change=last_change_)
					
				setting_List=setting.objects.all().filter(name='service_charges')
				serializer=settingSerializer(setting_List,many=True)
				setting_check=serializer.data

				if setting_check==[]:	
					add_setting=setting(added_on=added_on,name='service_charges',value=service_charges,status=status,last_change=last_change_)
					add_setting.save()
				# else:
				# 	update_setting=setting.objects.filter(name='service_charges').update(value=service_charges,last_change=last_change_)

				setting_List=setting.objects.all().filter(name='tax')
				serializer=settingSerializer(setting_List,many=True)
				setting_check=serializer.data

				if setting_check==[]:
					add_setting=setting(added_on=added_on,name='tax',value=tax,status=status,last_change=last_change_)
					add_setting.save()
				else:
					update_setting=setting.objects.filter(name='tax').update(value=tax,last_change=last_change_)

				setting_List=setting.objects.all().filter(name='delivery')
				serializer=settingSerializer(setting_List,many=True)
				setting_check=serializer.data

				if setting_check==[]:
					add_setting=setting(added_on=added_on,name='delivery',value=delivery,status=status,last_change=last_change_)
					add_setting.save()
				else:
					update_setting=setting.objects.filter(name='delivery').update(value=delivery,last_change=last_change_)
				
				setting_List=setting.objects.all().filter(name='take_away')
				serializer=settingSerializer(setting_List,many=True)
				setting_check=serializer.data

				if setting_check==[]:
					add_setting=setting(added_on=added_on,name='take_away',value=take_away,status=status,last_change=last_change_)
					add_setting.save()
				else:
					update_setting=setting.objects.filter(name='take_away').update(value=take_away,last_change=last_change_)

				setting_List=setting.objects.all().filter(name='cash_pay')
				serializer=settingSerializer(setting_List,many=True)
				setting_check=serializer.data

				if setting_check==[]:
					add_setting=setting(added_on=added_on,name='cash_pay',value=cash_pay,status=status,last_change=last_change_)
					add_setting.save()
				else:
					update_setting=setting.objects.filter(name='cash_pay').update(value=cash_pay,last_change=last_change_)

				setting_List=setting.objects.all().filter(name='online')
				serializer=settingSerializer(setting_List,many=True)
				setting_check=serializer.data

				if setting_check==[]:
					add_setting=setting(added_on=added_on,name='online',value=online,status=status,last_change=last_change_)
					add_setting.save()
				else:
					update_setting=setting.objects.filter(name='online').update(value=online,last_change=last_change_)

				setting_List=setting.objects.all().filter(name='stock_maintance')
				serializer=settingSerializer(setting_List,many=True)
				setting_check=serializer.data

				if setting_check==[]:
					add_setting=setting(added_on=added_on,name='stock_maintance',value=stock_maintance,status=status,last_change=last_change_)
					add_setting.save()
				else:
					update_setting=setting.objects.filter(name='stock_maintance').update(value=stock_maintance,last_change=last_change_)

				setting_List=setting.objects.all().filter(name='shop_status')
				serializer=settingSerializer(setting_List,many=True)
				setting_check=serializer.data

				if setting_check==[]:
					add_setting=setting(added_on=added_on,name='shop_status',value=shop_status,status=status,last_change=last_change_)
					add_setting.save()
				else:
					update_setting=setting.objects.filter(name='shop_status').update(value=shop_status,last_change=last_change_)

				for i in final_datelist:
					setting_List=setting.objects.all().filter(name=i['name'])
					serializer=settingSerializer(setting_List,many=True)
					setting_check=serializer.data
					if setting_check==[]:
						add_setting=setting(added_on=added_on,name=i['name'],value=i['time'],status=status,last_change=last_change_)
						add_setting.save()
					else:
						update_setting=setting.objects.filter(name=i['name']).update(value=i['time'],last_change=last_change_)

				return Response({'message':True,'access':access})
			except Exception as e:
				return Response({'message':str(e)})
		else:
			return Response({'message':'Invalid Access'})

	def get(self,request):
		access=rights(request)['access']
		access_id=rights(request)['access_id']
		if access_cretential(access,'setting'):
			data=json.loads(request.body)
			type_=data['type']
			if type_=="ALL":
				setting_List=setting.objects.all()
				serializer=settingSerializer(setting_List,many=True)
				return Response({'message':True,'data':serializer.data})
			elif type_=="one":
				id=data['id']
				setting_List=setting.objects.all().filter(id=id)
				serializer=settingSerializer(setting_List,many=True)
				return Response({'message':True,'data':serializer.data})
			else:
				return Response({'message':'Invalid Data'})

		else:
			return Response({'message':'Invalid Access'})

class api_today_order(APIView):
	def post(self,request):
		data=json.loads(request.body)
		
		added_on=today()
		last_change_=last_change()
		id=data['id']
		updatefield=data['updatefield']
		type_=data['type_']
		status='active'
		access=rights(request)['access']
		access_id=rights(request)['access_id']

		if access_cretential(access,'today_order'):
			try:
				if type_=='order_status_update':
					order_check=order.objects.all().filter(status='active',id=id)
					order_check=orderSerializer(order_check,many=True)
					order_check=order_check.data[0]

					order_update=order.objects.exclude(order_status='order handed over').filter(id=id).update(order_status=updatefield,last_change=last_change_)
					
					if updatefield=='order accept':
						next_button='preparing food'
					elif updatefield=='preparing food':
						if order_check['delivery_type']=='door_delivery':
							next_button='ready for delivery'
						else:
							next_button='ready for takeaway'
					elif( updatefield=='ready for delivery') or (updatefield=='ready for takeaway'):
						next_button='hand over'

					# print(updatefield,next_button)

				elif type_=='out_of_stock':
					item_update=item.objects.filter(id=id).update(sales_status=updatefield,last_change=last_change_)
					next_button=id
				elif type_=="Active All":
					item_update=item.objects.filter(status='active').update(sales_status=1,last_change=last_change_)
				elif type_=="In Active All":
					item_update=item.objects.filter(status='active').update(sales_status=0,last_change=last_change_)
				return Response({'message':True,'next_button':next_button,'access':access})
			except Exception as e:
				return Response({'message':str(e)})
		else:
			return Response({'message':'Invalid Access'})


class api_order_report(APIView):
	def get(self,request):
		access=rights(request)['access']
		access_id=rights(request)['access_id']
		if access_cretential(access,'order_report'):
			data=json.loads(request.body)
			from_date=data['from_date']
			to_date=data['to_date']
			order_type=data['order_type']

			if order_type=="ALL":
				order_data=order.objects.all().filter(added_on__gte=from_date,added_on__lte=to_date)
				serializer=orderSerializer(order_data,many=True)
				return Response({'message':True,'data':serializer.data})
			else:
				order_data=order.objects.all().filter(order_status=order_type,added_on__gte=from_date,added_on__lte=to_date)
				serializer=orderSerializer(order_data,many=True)
				return Response({'message':True,'data':serializer.data})

		else:
			return Response({'message':'Invalid Access'})

class api_item_report(APIView):
	def get(self,request):
		access=rights(request)['access']
		access_id=rights(request)['access_id']

		if access_cretential(access,'item_report'):
			data=json.loads(request.body)
			from_date=data['from_date']
			to_date=data['to_date']
			item_type=data['item_type']

			if item_type=="ALL":
				try:
					cursor=connection.cursor()
					cursor.execute("SELECT * from customer_order_item,customer_order where customer_order.added_on>=%s and customer_order.added_on<=%s and customer_order.order_status='order handed over' and customer_order.id=customer_order_item.order_id ",(from_date,to_date,))
					itemlist_data=dictfetchall(cursor)

					return Response({'message':True,'data':itemlist_data})
				finally:
					cursor.close()
					connection.close()

			elif item_type=='customer_report':
				cus_id=data['cus_id']
				# print('======================= from_date',from_date,to_date,cus_id,)
				try:
					cursor=connection.cursor()
					cursor.execute("SELECT sum(customer_order_item.quantity)as tot_qty,sum(customer_order.total)as tot_amt from customer_order_item,customer_order where customer_order.added_on>=%s and customer_order.added_on<=%s and customer_order.order_status='order handed over' and customer_order.id=customer_order_item.order_id and customer_order.customer_id=%s and customer_order.customer_access='user'",(from_date,to_date,cus_id,))
					custotallist_data=dictfetchall(cursor)

					# cursor.execute("SELECT * from customer_order where  customer_order.order_status='order handed over' customer_order.customer_id=%s and customer_order.customer_access='user' order by customer_order.id desc limit 1",(cus_id,))
					cursor.execute("SELECT * from customer_order where customer_order.customer_id=%s and customer_order.customer_access='user' order by customer_order.id desc limit 1",(cus_id,))
					cuslast_data=dictfetchall(cursor)

				finally:
					cursor.close()
					connection.close()

				return Response({'message':True,'data':custotallist_data,'cuslast_data':cuslast_data})
			else:
				try:
					cursor=connection.cursor()
					cursor.execute("SELECT * from customer_order_item,customer_order where customer_order.added_on>=%s and customer_order.added_on<=%s and customer_order.order_status='order handed over' and customer_order.id=customer_order_item.order_id and customer_order_item.item_id=%s",(from_date,to_date,item_type,))
					itemlist_data=dictfetchall(cursor)
					return Response({'message':True,'data':itemlist_data})
				finally:
					cursor.close()
					connection.close()

		else:
			return Response({'message':'Invalid Access'})
