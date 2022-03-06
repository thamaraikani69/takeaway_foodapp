							
							# ---------------- Shivaya nama om -------------------------------

from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.db import connection
import json
import secrets

# -- Rest APi Framework --#
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# -- Imports --#
from . models import *
from company.models import *
from company.serializers import *

from . serializers import *
from login.apps import *
from login.tokenvalidation import *

import pytz
ist=pytz.timezone('Asia/Kolkata')
from pytz import timezone
timedate =datetime.now(timezone('Asia/Kolkata'))
timedate=timedate.replace(tzinfo=None)
timedate=timedate
today_=timedate.date()

# Create your views here.
# Create your views here.
class api_noti(APIView):

	def post(self,request):
		data=json.loads(request.body)
		type_=data['type_']
		access=rights(request)['access']
		access_id=rights(request)['access_id']
		
		if access_cretential(access,'noti'):
			if access=='admin':
				noti_List=notification.objects.all().filter(customer_access=access,status='active')
				serializer=notificationSerializer(noti_List,many=True)
			elif access=='user':
				noti_List=notification.objects.all().filter(customer_access=access,customer_id=access_id,status='active')
				serializer=notificationSerializer(noti_List,many=True)
			noti_List=serializer.data

			order_=""
			order_item_=""
			data=[]
			noti_msg=0
			if noti_List!=[]:
				for i in noti_List:
					if i['noti_type']=='order':
						print(i['noti_id'],type(i['noti_id']))
						order_List=order.objects.all().filter(id=i['noti_id'])
						serializer=orderSerializer(order_List,many=True)
						order_=serializer.data

						order_item_List=order_item.objects.all().filter(order_id=i['noti_id'])
						serializer=order_itemSerializer(order_item_List,many=True)
						order_item_=serializer.data
						data.append({'order':order_,'order_item':order_item_})
			if type_=='unread':
				if access=='admin':
					noti_update=notification.objects.filter(noti_status='unread',customer_access=access).update(noti_status='read',noti_ringtone='off')
				elif access=='user':
					noti_update=notification.objects.filter(noti_status='unread',customer_access=access,customer_id=access_id).update(noti_status='read',noti_ringtone='off')
			elif type_=='msg_status':
				if access=='admin':
					noti_List=notification.objects.all().filter(customer_access=access,noti_status='unread')
					serializer=notificationSerializer(noti_List,many=True)
					noti_=serializer.data
					if noti_!=[]:
						noti_msg=len(noti_)
			# print(data)
			return Response({'message':True,'data':data,'noti_msg':noti_msg})
			
		else:
				return Response({'message':'Invalid Access'})

class api_search(APIView):

	def post(self,request):
		data=json.loads(request.body)
		item_name=data['item_name']
		access=rights(request)['access']
		access_id=rights(request)['access_id']
		
		if access_cretential(access,'cart'):
			
			item_List=item.objects.all().filter(itemname__contains=item_name,status='active')
			serializer=itemSerializer(item_List,many=True)

			try:
				cursor=connection.cursor()
				cursor.execute("SELECT *,customer_cart_item.quantity as cart_quantity from customer_cart_item,customer_cart where customer_cart_item.status='active' and customer_cart_item.cart_id=customer_cart.id and customer_cart.customer_id=%s and customer_cart.customer_access=%s",(access_id,access,))
				cart_serializer=dictfetchall(cursor)
			finally:
				cursor.close()
				connection.close()

			if serializer.data!=[]:
				return Response({'message':True,'data':serializer.data,'cart_list':cart_serializer})
			else:
				return Response({'message':False})
			
		else:
				return Response({'message':'Invalid Access'})

class api_cart(APIView):

	def get(self,request):
		data=json.loads(request.body)
		type_=data['type']
		access=rights(request)['access']
		access_id=rights(request)['access_id']
		
		shop_open_status=shoping_timing_()['message']
		if shop_open_status == 'on':
			if access_cretential(access,'cart'):
				if type_=="ALL":
					cart_List=cart.objects.all().filter(customer_id=access_id,customer_access=access,status='active',cart_status='cart')
					serializer=cartSerializer(cart_List,many=True)
					return Response({'message':True,'data':serializer.data})
				elif type_=="cart":
					cart_List=cart.objects.all().filter(customer_id=access_id,customer_access=access,status='active',cart_status='cart')
					serializer=cartSerializer(cart_List,many=True)
					cart_check=serializer.data
					if cart_check!=[]:
						cart_check=cart_check[0]
						after_gst=cart_check['after_gst']
						service_charge=cart_check['service_charge']
						delivery_charge=cart_check['delivery_charge']
						grand_total=after_gst+service_charge
						cart_update=cart.objects.filter(cart_status='cart',status='active',id=cart_check['id']).update(delivery_charge=0,grand_total=grand_total)

						cart_List=cart.objects.all().filter(customer_id=access_id,customer_access=access,status='active',cart_status='cart')
						serializer=cartSerializer(cart_List,many=True)
					return Response({'message':True,'data':serializer.data})
				else:
					return Response({'message':'Invalid Data'})
			else:
					return Response({'message':'Invalid Access'})
		else:
			return Response({'message':'Shop Closed'})

class api_cart_item(APIView):

	def get(self,request):

		data=json.loads(request.body)
		type_=data['type']
		access=rights(request)['access']
		access_id=rights(request)['access_id']
		
		if access_cretential(access,'cart_item'):
			shop_open_status=shoping_timing_()['message']
			if shop_open_status == 'on':
				if type_=="ALL":
					try:
						
						gst=int(gst_charge_())
						service_charge=int(service_charge_())


						cart_check=cart.objects.all().filter(status='active',customer_id=access_id,customer_access=access,cart_status='cart')
						cart_check=cartSerializer(cart_check,many=True)
						cart_check=cart_check.data
						if cart_check!=[]:	
							delivery_charge=cart_check[0]['delivery_charge']
							cart_item_check=cart_item.objects.all().filter(status='active',cart_id=cart_check[0]['id'])
							cart_item_check=cart_itemSerializer(cart_item_check,many=True)
							cart_item_check=cart_item_check.data
							if cart_item_check!=[]:
								for i in cart_item_check:
										# ------------------------------------- item check ---------------------------------
									item_check=item.objects.all().filter(id=i['item_id'],status='active')
									item_check=itemSerializer(item_check,many=True)
									item_check=item_check.data
									
									if item_check!=[]:
										item_check=item_check[0]
										if item_check['sales_status']==0:
											amount=i['quantity']*i['price']
											delete_cart=cart_item.objects.filter(status='active',id=i['id']).delete()

											cart_item_check=cart_item.objects.all().filter(status='active',cart_id=cart_check[0]['id'])
											cart_item_check=cart_itemSerializer(cart_item_check,many=True)
											cart_item_check=cart_item_check.data
											if cart_item_check==[]:
												delete_cart=cart.objects.filter(status='active',customer_id=access_id,customer_access=access,cart_status='cart').delete()
											else:
												total=cart_check[0]['total']-amount
												after_gst=total+(total*(gst/100))
												if after_gst+delivery_charge < 100:
													# ==================== Service Charges changes ============================
													service_charge=service_charge

												grand_total=after_gst+service_charge+delivery_charge
												cart_update=cart.objects.filter(cart_status='cart',status='active',id=cart_check[0]['id']).update(total=total,gst=gst,after_gst=after_gst,service_charge=service_charge,delivery_charge=delivery_charge,grand_total=grand_total)


						cursor=connection.cursor()
						cursor.execute("SELECT *,customer_cart_item.quantity as cart_quantity from customer_cart_item,customer_cart where customer_cart_item.status='active' and customer_cart_item.cart_id=customer_cart.id and customer_cart.customer_id=%s and customer_cart.customer_access=%s",(access_id,access,))
						data=dictfetchall(cursor)
						# ------------------------------------- Remove cart check preview---------------------------------
						cart_check=cart.objects.all().filter(status='active',cart_status='cart',customer_id=access_id,customer_access=access)
						cart_check=cartSerializer(cart_check,many=True)
						cart_check=cart_check.data
						if cart_check!=[]:
							cart_check=cart_check[0]
							# print(cart_check['grand_total'],'********************************',type(cart_check['grand_total']),int(cart_check['after_gst'])+int(cart_check['delivery_charge']))

							if (int(cart_check['after_gst'])+int(cart_check['delivery_charge'])) <100:
								print(cart_check['grand_total'],'********************************')
								# ==================== Service Charges changes ============================
								new_service_charge=service_charge
								new_grand_total=int(cart_check['after_gst'])+int(cart_check['delivery_charge'])+new_service_charge
								cart_update=cart.objects.filter(status='active',cart_status='cart',id=cart_check['id']).update(service_charge=new_service_charge,grand_total=new_grand_total)

						cursor=connection.cursor()
						cursor.execute("SELECT *,customer_cart_item.quantity as cart_quantity from customer_cart_item,customer_cart where customer_cart_item.status='active' and customer_cart_item.cart_id=customer_cart.id and customer_cart.customer_id=%s and customer_cart.customer_access=%s",(access_id,access,))
						data=dictfetchall(cursor)
						return Response({'message':True,'data':data})
					finally:
						cursor.close()
						connection.close()
				else:
					return Response({'message':'Invalid Data'})
			else:
				return Response({'message':'Shop Closed'})

		else:
				return Response({'message':'Invalid Access'})
		
	def post(self,request):
		# try:
			data=json.loads(request.body)
			method=data['method']
			item_id=data['item_id']
			
			added_on=today()
			last_change_=last_change()
			if method =='online_payment':
				order_id=data['order_id']
				cursor=connection.cursor()
				cursor.execute("SELECT * from customer_cart where payment_id=%s",(order_id,))
				payment_data=dictfetchall(cursor)
				for i in payment_data:
					access=i['customer_access']
					access_id=i['customer_id']
				method=data['type']
			else:
				access=rights(request)['access']
				access_id=rights(request)['access_id']
			
			if access_cretential(access,'cart_item_add'):
				# --------------------------------- Setting -------------------------------
				setting_List=setting.objects.all().filter()
				serializer=settingSerializer(setting_List,many=True)
				setting_check=serializer.data

				shop_status='off'
				stock_maintance='off'
				shop_open_status=shoping_timing_()['message']
				if setting_check==[]:
					return Response({'message':'some thing wrong inform to shop'})
				else:
					for i in setting_check:
						if i['name']=='shop_status':
							shop_status=i['value']
						elif i['name']=='shop_status':
							stock_maintance=i['value']

				if shop_status=='on' and shop_open_status=='on':
					# ------------------------------------- item check ---------------------------------
					item_check=item.objects.all().filter(id=item_id,status='active')
					item_check=itemSerializer(item_check,many=True)
					item_check=item_check.data
					
					gst=int(gst_charge_())
					service_charge=int(service_charge_())
					delivery_charge=0

					if item_check!=[]:
						item_check=item_check[0]
						if item_check['sales_status']==1:
							# ------------------------------------- cart check ---------------------------------
							cart_check=cart.objects.all().filter(status='active',customer_id=access_id,customer_access=access,cart_status='cart')
							cart_check=cartSerializer(cart_check,many=True)
							cart_check=cart_check.data
							arrival_time="00:00:00"
							delivery_type=""
							payment_id=""
							payment_status="waiting"

							if cart_check == []:
								add_cart=cart(added_on=added_on,total=0,gst=0,after_gst=0,service_charge=0,delivery_charge=0,grand_total=0,customer_id=access_id,customer_access=access,cart_status='cart',delivery_name="",delivery_address="",status='active',last_change=last_change_,arrival_time=arrival_time,payment_id=payment_id,payment_status=payment_status,offer_percentage_amount=0)
								add_cart.save()
								add_cart=add_cart.pk
							else:
								cart_check=cart_check[0]
								add_cart=cart_check['id']
							# ------------------------------------- cart item check ---------------------------------
							cart_item_check=cart_item.objects.all().filter(item_id=item_id,status='active',cart_id=add_cart)
							cart_item_check=cart_itemSerializer(cart_item_check,many=True)
							cart_item_check=cart_item_check.data

							if cart_item_check==[]:
								if method=='add':
									price=int(item_check['rate'])-int(item_check['discount'])

									if cart_check == []:
										total_=0
									else:
										total_=cart_check['total']

									total=total_+(int(item_check['rate'])-int(item_check['discount']))
									after_gst=total+(total*(gst/100))
									grand_total=after_gst+service_charge+delivery_charge
									quantity=1
									add_cart_item=cart_item(added_on=added_on,item_id=item_id,quantity=quantity,bef_disc_price=item_check['rate'],discount=item_check['discount'],price=price,status='active',last_change=last_change_,cart_id=add_cart,item_name=item_check['itemname'],item_image=item_check['itemimage'])
									add_cart_item.save()

									cart_update=cart.objects.filter(status='active',id=add_cart,cart_status='cart').update(total=total,gst=gst,after_gst=after_gst,service_charge=service_charge,delivery_charge=delivery_charge,grand_total=grand_total,last_change=last_change_)

								elif method=='sub':
									# print("IIIIIIIIIIIIIIIIIII")
									# ------------------------------------- cart item check ---------------------------------
									cart_item_check=cart_item.objects.all().filter(status='active',cart_id=add_cart)
									cart_item_check=cart_itemSerializer(cart_item_check,many=True)
									cart_item_check=cart_item_check.data
									if cart_item_check==[]:
										delete_cart=cart.objects.filter(cart_status='cart',status='active',id=add_cart).delete()
										return Response({'message':False,'data':'Empty cart'})
									else:
										return Response({'message':False,'data':'Empty cart item'})
							else:

								cart_item_check=cart_item_check[0]
								if method=='add':
									quantity=int(cart_item_check['quantity'])+1
									cart_item_update=cart_item.objects.filter(item_id=item_id,status='active',cart_id=add_cart).update(quantity=quantity,last_change=last_change_)

									if cart_check == []:
										total_=0
									else:
										total_=cart_check['total']

									total=total_+(int(item_check['rate'])-int(item_check['discount']))
									after_gst=total+(total*(gst/100))
									grand_total=after_gst+service_charge+delivery_charge

									cart_update=cart.objects.filter(status='active',id=add_cart,cart_status='cart').update(total=total,gst=gst,after_gst=after_gst,service_charge=service_charge,delivery_charge=delivery_charge,grand_total=grand_total,last_change=last_change_)


								elif method=='sub':
									quantity=int(cart_item_check['quantity'])-1

									if cart_check == []:
										total_=0
									else:
										total_=cart_check['total']

									total=total_-(int(item_check['rate'])-int(item_check['discount']))
									after_gst=total+(total*(gst/100))
									grand_total=after_gst+service_charge+delivery_charge

									if quantity==0:
										# print("****************************************")
										cart_item_delete=cart_item.objects.filter(item_id=item_id,status='active',cart_id=add_cart).delete()
										# ------------------------------------- cart item check ---------------------------------
										cart_item_check=cart_item.objects.all().filter(status='active',cart_id=add_cart)
										cart_item_check=cart_itemSerializer(cart_item_check,many=True)
										cart_item_check=cart_item_check.data
										# print("___________________ cart_item_check",cart_item_check)
										if cart_item_check==[]:
											delete_cart=cart.objects.filter(cart_status='cart',status='active',id=add_cart).delete()
											return Response({'message':False,'data':'Empty cart'})
										else:
											cart_update=cart.objects.filter(cart_status='cart',status='active',id=add_cart).update(total=total,gst=gst,after_gst=after_gst,service_charge=service_charge,delivery_charge=delivery_charge,grand_total=grand_total,last_change=last_change_)
											# return Response({'message':False,'data':'Empty cart item'})
									else:
										# print("&&&&&&&&&&&&&&&&&&&&&")
										cart_item_update=cart_item.objects.filter(item_id=item_id,status='active',cart_id=add_cart).update(quantity=quantity,last_change=last_change_)
										cart_update=cart.objects.filter(cart_status='cart',status='active',id=add_cart).update(total=total,gst=gst,after_gst=after_gst,service_charge=service_charge,delivery_charge=delivery_charge,grand_total=grand_total,last_change=last_change_)

									# ============================ Cart Detaila =================
							cart_data=cart.objects.all().filter(status='active',customer_id=access_id,customer_access=access,cart_status='cart')
							cart_data=cartSerializer(cart_data,many=True)
							cart_data=cart_data.data

							return Response({'message':True,'data':{'item_id':item_id,'quantity':quantity,'cart_data':cart_data},'access':access})
						else:
							cart_check=cart.objects.all().filter(status='active',customer_id=access_id,customer_access=access,cart_status='cart')
							cart_check=cartSerializer(cart_check,many=True)
							cart_check=cart_check.data
							if cart_check!=[]:	
								cart_item_check=cart_item.objects.all().filter(status='active',item_id=item_id,cart_id=cart_check[0]['id'])
								cart_item_check=cart_itemSerializer(cart_item_check,many=True)
								cart_item_check=cart_item_check.data
								if cart_item_check!=[]:
									amount=0
									for i in cart_item_check:
										amount=i['quantity']*i['price']
									delete_cart=cart_item.objects.filter(status='active',item_id=item_id,cart_id=cart_check[0]['id']).delete()

									cart_item_check=cart_item.objects.all().filter(status='active',item_id=item_id,cart_id=cart_check[0]['id'])
									cart_item_check=cart_itemSerializer(cart_item_check,many=True)
									cart_item_check=cart_item_check.data
									if cart_item_check==[]:
										delete_cart=cart.objects.filter(status='active',customer_id=access_id,customer_access=access,cart_status='cart').delete()
									else:
										
										total=cart_check[0]['total']-amount
										after_gst=total+(total*(gst/100))
										if after_gst+delivery_charge < 100:
											# ==================== Service Charges changes ============================
											service_charge=service_charge

										grand_total=after_gst+service_charge+delivery_charge
										cart_update=cart.objects.filter(cart_status='cart',status='active',id=cart_check[0]['id']).update(total=total,gst=gst,after_gst=after_gst,service_charge=service_charge,delivery_charge=delivery_charge,grand_total=grand_total,last_change=last_change_)

							return Response({'message':False,'data':'Out Of Stock '})
					else:
						return Response({'message':False,'data':'Item Not Active'})
				else:
					return Response({'message':False,'data':'Shop Closed'})
			else:
				return Response({'message':False,'data':'Invalid Access'})
		# except Exception as e:
		# 	print(e)


class api_stock_update(APIView):

	def get(self,request):

		data=json.loads(request.body)
		stock_type=data['stock_type']
		print('*****************************',stock_type)
		if stock_type=='online_stock_update':
			order_id=data['order_id']
			print('*****************************',order_id)
			cursor=connection.cursor()
			cursor.execute("SELECT * from customer_cart where payment_id=%s",(order_id,))
			payment_data=dictfetchall(cursor)
			for i in payment_data:
				access=i['customer_access']
				access_id=i['customer_id']
			stock_type=data['type']

		else:
			access=rights(request)['access']
			access_id=rights(request)['access_id']

		last_change_=last_change()

		if access_cretential(access,'stock_update'):
			if stock_type=="stock_update":
				# --------------------------------- Setting -------------------------------
				setting_List=setting.objects.all().filter()
				serializer=settingSerializer(setting_List,many=True)
				setting_check=serializer.data

				shop_status='off'
				stock_maintance='off'
				shop_open_status=shoping_timing_()['message']

				if setting_check==[]:
					return Response({'message':'some thing wrong inform to shop'})
				else:
					for i in setting_check:
						if i['name']=='shop_status':
							shop_status=i['value']
						elif i['name']=='shop_status':
							stock_maintance=i['value']

				if shop_status == "on" and shop_open_status=='on':
					cursor=connection.cursor()
					cursor.execute("SELECT *,customer_cart_item.quantity as cart_quantity from customer_cart_item,customer_cart,company_item where company_item.id=customer_cart_item.item_id and customer_cart_item.status='active' and customer_cart_item.cart_id=customer_cart.id and customer_cart.customer_id=%s and customer_cart.customer_access=%s",(access_id,access,))
					data=dictfetchall(cursor)

					for i in data:
						cursor.execute("SELECT * from company_item where status='active' and id=%s",(i['item_id'],))
						item_data=dictfetchall(cursor)
						
						if item_data!= []:
							for j in item_data:
								if j['sales_status']==1:
									if stock_maintance == 'on':
										pending_qty=i['cart_quantity']-j['quantity']
										# print('cart quantity ====================',i['cart_quantity'],'item quantity',i['quantity'])
										if int(i['cart_quantity'])>int(j['quantity']):
											if int(j['quantity']==0):
												j['quantity']='not'

											return Response({'message':'delete_item','data':{'item_id':i['item_id'],'method':'sub','quantity':pending_qty,'item_name':i['itemname']},'error_message':j['itemname']+' '+str(j['quantity'])+' available'})
								else:
									return Response({'message':'delete_item','data':{'item_id':i['item_id'],'method':'sub','quantity':0,'item_name':i['itemname']},'error_message':i['itemname']+' Out Of Stock'})
							for j in item_data:

								if j['sales_status']==1:
									if stock_maintance == 'on':
										new_quantity=j['quantity']-i['cart_quantity']
										
										if int(new_quantity) >= 0:
											cursor.execute("UPDATE company_item set quantity=%s,last_change=%s where id=%s",(new_quantity,last_change_,j['id'],))
											connection.commit()
										else:
											return Response({"message":"Some Thing Wrong Take Screen Short and contact administration"})
								else:
									return Response({'message':'delete_item','data':{'item_id':i['item_id'],'method':'sub','quantity':0,'item_name':i['itemname']},'error_message':i['itemname']+' Out Of Stock'})
							return Response({"message":True})
						else:
							return Response({'message':'delete_item','data':{'item_id':i['item_id'],'method':'sub','quantity':i['cart_quantity'],'item_name':i['itemname']},'error_message':j['itemname']+' is not available right now'})
					return Response({'message':True})
				else:
					return Response({"message":'Shop Closed'})

			if stock_type=="re_stock_update":
				cursor=connection.cursor()
				cursor.execute("SELECT *,customer_cart_item.quantity as cart_quantity from customer_cart_item,customer_cart,company_item where company_item.id=customer_cart_item.item_id and customer_cart_item.status='active' and customer_cart_item.cart_id=customer_cart.id and customer_cart.customer_id=%s and customer_cart.customer_access=%s",(access_id,access,))
				data=dictfetchall(cursor)

				# --------------------------------- Setting -------------------------------
				setting_List=setting.objects.all().filter()
				serializer=settingSerializer(setting_List,many=True)
				setting_check=serializer.data

				shop_status='off'
				stock_maintance='off'
				shop_open_status=shoping_timing_()['message']

				if setting_check==[]:
					return Response({'message':'some thing wrong inform to shop'})
				else:
					for i in setting_check:
						if i['name']=='shop_status':
							shop_status=i['value']
						elif i['name']=='shop_status':
							stock_maintance=i['value']

				for i in data:
					cursor.execute("SELECT * from company_item where sales_status=1 and status='active' and id=%s",(i['item_id'],))
					item_data=dictfetchall(cursor)

					for j in item_data:
						new_quantity=i['cart_quantity']+j['quantity']

						cursor.execute("UPDATE company_item set quantity=%s,last_change=%s where id=%s",(new_quantity,last_change_,j['id'],))
						connection.commit()
						
				return Response({"message":True})
					
			else:
				return Response({'message':'Invalid Data'})
		else:
				return Response({'message':'Invalid Access'})
	

class api_order_move(APIView):

	def get(self,request):

		data=json.loads(request.body)
		type_=data['type_']

		delivery_otp=delivery_otp_()
		last_change_=last_change()
		
		if type_=='online_order_update':
			order_id=data['order_id']
			cursor=connection.cursor()
			cursor.execute("SELECT * from customer_cart where payment_id=%s",(order_id,))
			payment_data=dictfetchall(cursor)
			for i in payment_data:
				access=i['customer_access']
				access_id=i['customer_id']
				type_='order_update'

		elif type_=='online_order_out':
			payment_id=data['payment_id']
			payment_mode=data['payment_mode']
			razorpay_payment_id=data['razorpay_payment_id']
			razorpay_signature_id=data['razorpay_signature_id']
			print("**************************",payment_id)
			order_update=order.objects.filter(status='active',payment_id=payment_id).update(payment_mode='online',payment_status='paid',razor_payment_id=razorpay_payment_id,razor_signature_id=razorpay_signature_id,last_change=last_change_)
			return Response({'message':True})

		elif type_=='online_order_payment':
			order_id=data['order_id']
			order_type=data['order_type']
			cursor=connection.cursor()
			if order_type=='id':
				cursor.execute("SELECT * from customer_order where id=%s",(order_id,))
			elif order_type=='hex':
				cursor.execute("SELECT * from customer_order where url_hex=%s",(order_id,))
			payment_data=dictfetchall(cursor)
			for i in payment_data:
				access=i['customer_access']
				access_id=i['customer_id']
		else:
			access=rights(request)['access']
			access_id=rights(request)['access_id']

		# print(access_id,access)
		added_on=today()
		last_change_=last_change()
		delivery_charge=int(delivery_charge_())
		
		if access_cretential(access,'order_move'):
			if type_=='order_update':
				payment_id=data['payment_id']
				payment_mode=data['payment_mode']
				razorpay_payment_id=data['razorpay_payment_id']
				razorpay_signature_id=data['razorpay_signature_id']
				cart_List=cart.objects.all().filter(customer_id=access_id,customer_access=access,status='active',cart_status='cart')
				serializer=cartSerializer(cart_List,many=True)
				cart_List=serializer.data

				for i in cart_List:

					cartitem_List=cart_item.objects.all().filter(status='active',cart_id=i['id'])
					serializer=cart_itemSerializer(cartitem_List,many=True)
					cartitem_List=serializer.data

					arrival_time=i['arrival_time']
					delivery_type=i['delivery_type']

					if delivery_type=='door_delivery':
						# door_delivery_charge=delivery_charge_()
						# grand_total=i['grand_total']+delivery_charge
						door_delivery_charge=i['delivery_charge']
						grand_total=i['grand_total']
					else:
						# door_delivery_charge=0
						door_delivery_charge=i['delivery_charge']
						grand_total=i['grand_total']
					confirm_otp=0
					if payment_mode=='cash':
						i['payment_id']='cash'
						payment_status='waiting'
					elif payment_mode=='online':
						payment_status='paid'

					# print(payment_mode,'---------------------------------',payment_id,i['payment_id'])
					if payment_id==i['payment_id']:
						# ------------------------------------- order check ---------------------------------
						order_check=order.objects.all().order_by('-id')
						order_check=orderSerializer(order_check,many=True)
						order_check=order_check.data
						# print("=============================================== Order Check =========",order_check[0]['id'])
						if order_check!=[]:
							url_hex = secrets.token_hex(2)+str(order_check[0]['id'])
						else:
							url_hex = secrets.token_hex(2)+str(1)

						add_order=order(offer_percentage_amount=i['offer_percentage_amount'],url_hex=url_hex,payment_status=payment_status,added_on=added_on,confirm_otp=confirm_otp,delivery_name=i['delivery_name'],delivery_address=i['delivery_address'],cart_id=i['id'],total=i['total'],gst=i['gst'],after_gst=i['after_gst'],service_charge=i['service_charge'],delivery_charge=door_delivery_charge,grand_total=grand_total,customer_id=access_id,customer_access=access,order_status='order placed',delivery_type=delivery_type,payment_mode=payment_mode,arrival_time=arrival_time,payment_id=payment_id,delivery_otp=delivery_otp,status='active',last_change=last_change_,razor_payment_id=razorpay_payment_id,razor_signature_id=razorpay_signature_id)
						add_order.save()
						add_order=add_order.pk
						# ========================================================= Offer Update =======================
						offer_List=offer.objects.all().filter(status='active')
						serializer=offerSerializer(offer_List,many=True)
						offer_check=serializer.data
						if offer_check!=[]:
							offer_check=offer_check[0]
							offer_id=offer_check['id']

							user_offer_=user_offer(added_on=added_on,offer_id=offer_id,customer_id=access_id,customer_access=access,last_change=last_change_)
							user_offer_.save()

						notification_=notification(added_on=added_on,noti_type='order',noti_id=add_order,customer_id=access_id,customer_access=access,noti_status='unread',noti_ringtone='on',status='active',last_change=last_change_)
						notification_.save()
						notification_=notification(added_on=added_on,noti_type='order',noti_id=add_order,customer_id=1,customer_access='admin',noti_status='unread',noti_ringtone='on',status='active',last_change=last_change_)
						notification_.save()

						for j in cartitem_List:
							add_order_item=order_item(added_on=added_on,order_id=add_order,item_id=j['item_id'],quantity=j['quantity'],bef_disc_price=j['bef_disc_price'],discount=j['discount'],price=j['price'],status='active',last_change=last_change_,item_image=j['item_image'],item_name=j['item_name'])
							add_order_item.save()

						cart_update=cart.objects.filter(status='active',id=i['id']).update(cart_status='order',last_change=last_change_,payment_status='paid',payment_id=payment_id)
						cart_item_update=cart_item.objects.filter(status='active',cart_id=i['id']).update(status='inactive',last_change=last_change_)
						
						order_List=order.objects.all().filter(id=add_order,status='active')
						serializer=orderSerializer(order_List,many=True)
						order_List=serializer.data
						
						order_List=order.objects.all().filter(id=add_order,status='active')
						serializer=orderSerializer(order_List,many=True)
						order_List=serializer.data

						order_item_check=order_item.objects.all().filter(status='active',order_id=add_order)
						order_item_check=order_itemSerializer(order_item_check,many=True)
						order_item_check=order_item_check.data

						user_login_check=user_login.objects.all().filter(status='active',id=access_id)
						user_login_check=user_loginSerializer(user_login_check,many=True)
						user_login_check=user_login_check.data[0]

						data={'order_List':order_List,'order_item':order_item_check,'name':user_login_check['name'],'mobile_no':user_login_check['username']}

						return Response({'message':True,'data':data})

			elif type_=='cart_update':

				arrival_time=data['arrival_time']
				delivery_type=data['delivery_type']
				delivery_name=data['delivery_name']
				delivery_address=data['delivery_address']
				cart_List=cart.objects.all().filter(customer_id=access_id,customer_access=access,status='active',cart_status='cart')
				serializer=cartSerializer(cart_List,many=True)
				cart_List=serializer.data

				for i in cart_List:

					cartitem_List=cart_item.objects.all().filter(status='active',cart_id=i['id'])
					serializer=cart_itemSerializer(cartitem_List,many=True)
					cartitem_List=serializer.data
					i['grand_total']=(i['after_gst']+i['service_charge'])+(i['delivery_charge'])
					if delivery_type=='door_delivery':
						# print("i['delivery_charge==========================",i['delivery_charge'])
						if int(i['delivery_charge'])==0:
							door_delivery_charge=delivery_charge_()
							if i['grand_total']>=300:
								door_delivery_charge=0
								delivery_charge=0
							grand_total=i['grand_total']+delivery_charge
						else:
							door_delivery_charge=delivery_charge_()
							if i['grand_total']>=300:
								door_delivery_charge=0
								grand_total=i['grand_total']-int(i['delivery_charge'])
							else:
								grand_total=i['grand_total']

						print("****************************up",grand_total,(i['after_gst']),(i['service_charge']),(i['delivery_charge']))
					else:
						print("****************************down",i['grand_total'],(i['after_gst']),(i['service_charge']),(i['delivery_charge']))
						if int(i['delivery_charge'])!=0:
							door_delivery_charge=0
							grand_total=i['grand_total']-int(i['delivery_charge'])
						else:
							door_delivery_charge=0
							grand_total=i['grand_total']

					offer_List=offer.objects.all().filter(status='active')
					serializer=offerSerializer(offer_List,many=True)
					offer_check=serializer.data
					offer_percentage_amount=0
					if offer_check!=[]:
						user_offer_List=user_offer.objects.all().filter(offer_id=offer_check[0]['id'],customer_id=access_id,customer_access=access)
						serializer=user_offerSerializer(user_offer_List,many=True)
						user_offer_check=serializer.data
						if user_offer_check==[]:
							user_offer_check=0
						else:
							count=0
							for u in user_offer_check:
								count=count+1
							user_offer_check=count
						if user_offer_check < offer_check[0]['times']:
							offer_percentage=offer_check[0]['offer_percentage']
							offer_percentage_amount=grand_total*(offer_percentage/100)
							grand_total=grand_total- offer_percentage_amount
					confirm_otp=0
					# ========================= Razor pay order =======================
					razor_trans_id=razorpay_trans(product_id=i['id'],order_amount=grand_total,currency='INR')
					if razor_trans_id['message']==True:
						payment_id=razor_trans_id['trans_data']['trans_id']

						cart_update=cart.objects.filter(status='active',id=i['id']).update(offer_percentage_amount=offer_percentage_amount,delivery_name=delivery_name,delivery_address=delivery_address,service_charge=i['service_charge'],delivery_charge=door_delivery_charge,grand_total=grand_total,last_change=last_change_,delivery_type=delivery_type,arrival_time=arrival_time,payment_id=payment_id,payment_status='waiting')
						# cart_update=cart.objects.filter(status='active',id=i['id']).update(offer_percentage_amount=offer_percentage_amount,delivery_name=delivery_name,delivery_address=delivery_address,total=i['total'],gst=i['gst'],after_gst=i['after_gst'],service_charge=i['service_charge'],delivery_charge=door_delivery_charge,grand_total=grand_total,last_change=last_change_,delivery_type=delivery_type,arrival_time=arrival_time,payment_id=payment_id,payment_status='waiting')
						return Response({'message':True})
					else:
						return Response({'message':razor_trans_id['message']})
			elif type_=='online_order_payment':
				for i in payment_data:
					if i['payment_mode']=='cash' and i['razor_signature_id']=='waiting':
						razor_trans_id=razorpay_trans(product_id=i['id'],order_amount=i['grand_total'],currency='INR')
						if razor_trans_id['message']==True:
							payment_id=razor_trans_id['trans_data']['trans_id']
							order_update=order.objects.filter(status='active',id=i['id']).update(payment_id=payment_id,last_change=last_change_)
							print("----------------- payment_id ---------------",payment_id)
							return Response({'message':True})
						else:
							return Response({'message':razor_trans_id['message']})
					else:
						return Response({'message':'Invalid Access'})
		else:
				return Response({'message':'Invalid Access'})

	
class api_order(APIView):

	def get(self,request):

		data=json.loads(request.body)
		type_=data['type']

		if type_=='url_hexa':
			hex_id=data['id']
			# ------------------------------------- order check ---------------------------------
			order_check=order.objects.all().filter(url_hex=hex_id)
			order_check=orderSerializer(order_check,many=True)
			order_check=order_check.data
			if order_check!=[]:
				data['id']=order_check[0]['id']
				access_id=order_check[0]['customer_id']
				access=order_check[0]['customer_access']
			type_='one'
		else:
			access=rights(request)['access']
			access_id=rights(request)['access_id']
		
		last_change_=last_change()
		if access_cretential(access,'order'):
			if type_=="ALL":
				
				# ------------------------------------- order check ---------------------------------
				order_check=order.objects.all().filter(status='active',customer_id=access_id,customer_access=access).order_by('-id')
				order_check=orderSerializer(order_check,many=True)
				order_check=order_check.data

				order_item_check=order_item.objects.all().filter(status='active')
				order_item_check=order_itemSerializer(order_item_check,many=True)
				order_item_check=order_item_check.data

				order_total_items=[]

				for i in order_check:
					total_items=0
					for j in order_item_check:
						if i['id']==j['order_id']:
							total_items=total_items+1
					order_total_items.append({'order_id':i['id'],'total_items':total_items})

				return Response({'message':True,'data':{'order':order_check,'order_item':order_item_check,'order_total_items':order_total_items}})
			
			elif type_=='one':

				id=data['id']
				# ------------------------------------- order check ---------------------------------
				if access=='admin':
					order_check=order.objects.all().filter(status='active',id=id)
				else:
					order_check=order.objects.all().filter(status='active',id=id,customer_id=access_id,customer_access=access)
				order_check=orderSerializer(order_check,many=True)
				order_check=order_check.data

				for i in order_check:
					if i['customer_access']=='user':
						user_login_check=user_login.objects.all().filter(status='active',id=i['customer_id'])
						user_login_check=user_loginSerializer(user_login_check,many=True)
						user_login_check=user_login_check.data[0]
					elif i['customer_access']=='admin':
						admin_login_check=admin_login.objects.all().filter(status='active',id=i['customer_id'])
						admin_login_check=admin_loginSerializer(admin_login_check,many=True)
						user_login_check=admin_login_check.data[0]

					i['username']=user_login_check['username']
					i['name']=user_login_check['name']

				try:
					cursor=connection.cursor()
					if access=='admin':
						cursor.execute("SELECT *,customer_order_item.quantity as order_quantity from customer_order_item,customer_order where  customer_order_item.status='active' and customer_order_item.order_id=customer_order.id and customer_order.id=%s",(id,))
					else:
						cursor.execute("SELECT *,customer_order_item.quantity as order_quantity from customer_order_item,customer_order where  customer_order_item.status='active' and customer_order_item.order_id=customer_order.id and customer_order.customer_id=%s and customer_order.customer_access=%s and customer_order.id=%s",(access_id,access,id,))
					order_item_check=dictfetchall(cursor)
				finally:
					cursor.close()
					connection.close()
				# print(order_item_check)	
				order_total_items=[]

				for i in order_check:
					total_items=0
					for j in order_item_check:
						if i['id']==j['order_id']:
							total_items=total_items+1
					order_total_items.append({'order_id':i['id'],'total_items':total_items})
				# print("______________________________________________________________",order_check)
				return Response({'message':True,'data':{'order':order_check,'order_item':order_item_check,'order_total_items':order_total_items}})

			elif type_=='today_order':
				if access_cretential(access,'today_order'):
					# ------------------------------------- order check ---------------------------------
					order_check=order.objects.all().exclude(order_status='order handed over').filter(status='active',added_on__gte=today()).order_by('-id')
					order_check=orderSerializer(order_check,many=True)
					order_check=order_check.data
					
					# ================================================ order  item ==============================
					order_item_check=order_item.objects.all().filter(status='active',added_on__gte=today())
					order_item_check=order_itemSerializer(order_item_check,many=True)
					order_item_check=order_item_check.data
					# ================================================ Hand over order ==============================
					order_handover=order.objects.all().filter(status='active',added_on__gte=today(),order_status='order handed over').order_by('-id')|order.objects.all().filter(status='active',added_on__gte=today(),order_status='order cancelled').order_by('-id')
					order_handover=orderSerializer(order_handover,many=True)
					order_handover=order_handover.data

					order_total_items=[]

					for i in order_handover:
						if i['customer_access']=='user':
							user_login_check=user_login.objects.all().filter(status='active',id=i['customer_id'])
							user_login_check=user_loginSerializer(user_login_check,many=True)
							user_login_check=user_login_check.data[0]
						elif i['customer_access']=='admin':
							admin_login_check=admin_login.objects.all().filter(status='active',id=i['customer_id'])
							admin_login_check=admin_loginSerializer(admin_login_check,many=True)
							user_login_check=admin_login_check.data[0]

						i['username']=user_login_check['username']
						i['name']=user_login_check['name']

					for i in order_check:
						# ------------------------------------- order check ---------------------------------
						if i['customer_access']=='user':
							user_login_check=user_login.objects.all().filter(status='active',id=i['customer_id'])
							user_login_check=user_loginSerializer(user_login_check,many=True)
							user_login_check=user_login_check.data[0]
						elif i['customer_access']=='admin':
							print("+++++++++++++++++++++++++",i['customer_id'])
							admin_login_check=admin_login.objects.all().filter(status='active',id=i['customer_id'])
							admin_login_check=admin_loginSerializer(admin_login_check,many=True)
							user_login_check=admin_login_check.data[0]
						total_items=0
						for j in order_item_check:
							if i['id']==j['order_id']:
								total_items=total_items+1
						# print("_______________________",user_login_check)
						order_total_items.append({'order_id':i['id'],'total_items':total_items,'customer_name':user_login_check['name']})
						i['username']=user_login_check['username']
						i['name']=user_login_check['name']

					return Response({'message':True,'data':{'order':order_check,'order_item':order_item_check,'order_total_items':order_total_items,'order_handover':order_handover}})
				else:
					return Response({'message':'Invalid Data'})
			elif type_=='otp':
				if access_cretential(access,'otp'):

					id=data['id']
					otp=data['otp']
					# ------------------------------------- order check ---------------------------------
					order_check=order.objects.all().exclude(order_status='order handed over').filter(status='active',delivery_otp=otp,id=id,confirm_otp=0)
					order_check=orderSerializer(order_check,many=True)
					order_check=order_check.data
					if order_check!=[]:
						
						added_on=today()
						last_change_=last_change()

						order_update=order.objects.filter(status='active',id=id).update(confirm_otp=otp,payment_status='paid',order_status='order handed over',last_change=last_change_)
						add_aibeing=aibeing(added_on=added_on,Entry_date=added_on,payment_id=0,payment_signature_id=0,payment=0,order_id=id,last_change=last_change_)
						add_aibeing.save()
						return Response({'message':True})
					else:
						return Response ({'message':'Invalid Otp'})
				else:
					return Response({'message':'Invalid Data'})
			elif type_=='cancel_order':
				if access_cretential(access,'order_cancel'):
					id=data['id']
					cancel_reason=data['cancel_reason']
					order_status='order cancelled'
					# ------------------------------------- order check ---------------------------------
					order_check=order.objects.all().exclude(order_status='order handed over').filter(status='active',id=id)
					order_check=orderSerializer(order_check,many=True)
					order_check=order_check.data
					if order_check!=[]:
						order_update=order.objects.filter(status='active',id=id).update(cancel_reason=cancel_reason,order_status=order_status,last_change=last_change_)

						return Response({'message':True})
					else:
						return Response ({'message':'Invalid Otp'})
				else:
					return Response({'message':'Invalid Data'})
			else:
				return Response({'message':'Invalid Data'})
		else:
				return Response({'message':'Invalid Access'})

	def put(self,request):
		data=json.loads(request.body)
		
		added_on=today()
		last_change_=last_change()

		order_status=data['order_status']
		id=data['id']
		delivery_type=data['delivery_type']
		payment_type=data['payment_type']
		cancel_reason=data['cancel_reason']

		access=rights(request)['access']
		access_id=rights(request)['access_id']	

		if access_cretential(access,'order_edit'):
			try:
				add_order=order.objects.filter(id=id).update(order_status=order_status,delivery_type=delivery_type,payment_mode=payment_type,cancel_reason=cancel_reason,last_change=last_change())
				return Response({'message':True,'data':str(add_order),'access':access})
			except Exception as e:
				return Response({'message':str(e)})
		else:
			return Response({'message':'Invalid Access'})

class api_setting_setting(APIView):

	def get(self,request):

		data=json.loads(request.body)
		type_=data['type']
		access=rights(request)['access']
		access_id=rights(request)['access_id']
		
		if access_cretential(access,'setting_cus'):
			if type_=="ALL":
				setting_List=setting.objects.all()
				serializer=settingSerializer(setting_List,many=True)
				return Response({'message':True,'data':serializer.data})
			else:
				return Response({'message':'Invalid Data'})
		else:
				return Response({'message':'Invalid Access'})



def setting_data(type_):
	if type_=="ALL":
		setting_List=setting.objects.all()
		serializer=settingSerializer(setting_List,many=True)
		return ({'message':True,'data':serializer.data})
	else:
		return ({'message':'Invalid Data'})

def delivery_charge_():
    setting=setting_data('ALL')
    if setting['message']==True:
        delivery_chrge=setting['data']
        for i in delivery_chrge:
            if i['name']=='delivery_charge':
                return i['value']
    else:
        return 50

def service_charge_():
    setting=setting_data('ALL')
    if setting['message']==True:
        service_chrge=setting['data']
        for i in service_chrge:
            if i['name']=='service_charges':
                return i['value']
    else:
        return 5

def gst_charge_():
    setting=setting_data('ALL')
    if setting['message']==True:
        gst_chrge=setting['data']
        for i in gst_chrge:
            if i['name']=='gst':
                return i['value']
    else:
        return 5

def tax_type_():
    setting=setting_data('ALL')
    if setting['message']==True:
        tax_type=setting['data']
        for i in tax_type:
            if i['name']=='tax':
                return i['value']
    else:
        return 'off'

def delivery_type_():
    setting=setting_data('ALL')
    if setting['message']==True:
        delivery_type=setting['data']
        for i in delivery_type:
            if i['name']=='delivery':
                return i['value']
    else:
        return 'off'

def takeaway_type_():
    setting=setting_data('ALL')
    if setting['message']==True:
        takeaway_type=setting['data']
        for i in takeaway_type:
            if i['name']=='take_away':
                return i['value']
    else:
        return 'off'

def cash_pay_type_():
    setting=setting_data('ALL')
    if setting['message']==True:
        cash_pay_type=setting['data']
        for i in cash_pay_type:
            if i['name']=='cash_pay':
                return i['value']
    else:
        return 'off'

def online_type_():
    setting=setting_data('ALL')
    if setting['message']==True:
        online_type=setting['data']
        for i in online_type:
            if i['name']=='online':
                return i['value']
    else:
        return 'off'

def shoping_timing_():
   
	setting=setting_data('ALL')
	if setting['message']==True:

		day=today_.strftime('%A')
		today_day=day.lower()

		shop_data=setting['data']

		from_day=today_day+'_from'
		to_day=today_day+'_to'
		#

		for i in shop_data:
			if i['name']==from_day:
				from_time=i['value']
			elif i['name']==to_day:
				to_time=i['value']

		current_time=timedate
		current_time=current_time.strftime("%H:%M")
		# print(from_time,to_time,current_time,type(from_time),type(current_time))
		try:
			if current_time >= from_time and current_time <= to_time:
				print("Shop Open")
				return {'message':'on'}
			else:
				return {'message':'shop closed'}
		except:
				return {'message':'shop closed'}
			
	else:
	    return {'message':'shop closed'}