from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
from django.shortcuts import get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from django.http.response import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt


from login.apps import *
from company.image import *
from .api import *

import requests
import json
import os

from login.tokenvalidation import *


def add_menu_cart(request):
	name='elcafeteria.apk'
	return render(request,'menu_cart.html',{'name':name})

def add_download(request):
	app_name='elcafeteria.apk'
	return render(request,'download.html',{'app_name':app_name})

@inventory_token
def add_noti(request):
	
	access=rights(request)['access']
	access_id=rights(request)['access_id']

	# ------------------------- check data ----------------------------
	if access_cretential(access,'cart_item_add'):
		if request.method=="POST":

			type_=request.POST['type_']

			url=site_url()+'noti/'
			data={"type_":type_}
			headers={'X-access-token':request.session['inventory_token']}
			responce_data=requests.post(url,json=data,headers=headers)
			result=responce_data.json()
			
			return JsonResponse(({'data':result}))

		else:
			return JsonResponse(({'data':'Invalid Access'}))

@inventory_token
def add_cart(request):
	
	access=rights(request)['access']
	access_id=rights(request)['access_id']

	# ------------------------- check data ----------------------------
	if access_cretential(access,'cart_item_add'):
		if request.method=="POST":

			method=request.POST['method']
			item_id=request.POST['item_id']

			url=site_url()+'cart_item/'
			data={"method":method,"item_id":item_id}
			headers={'X-access-token':request.session['inventory_token']}
			responce_data=requests.post(url,json=data,headers=headers)
			result=responce_data.json()
			
			return JsonResponse(({'data':result}))

		else:
			return JsonResponse(({'data':'Invalid Access'}))

@inventory_token
def add_search(request):
	
	access=rights(request)['access']
	access_id=rights(request)['access_id']

	# ------------------------- check data ----------------------------
	if access_cretential(access,'cart_item_add'):
		if request.method=="POST":

			item_name=request.POST['item_name'].lower()

			url=site_url()+'search/'
			data={"item_name":item_name}
			headers={'X-access-token':request.session['inventory_token']}
			responce_data=requests.post(url,json=data,headers=headers)
			result=responce_data.json()
			if result['message']==True:
				return JsonResponse(({'data':result}))
			else:
				return JsonResponse(({'data':False}))

		else:
			return JsonResponse(({'data':'Invalid Access'}))


@inventory_token
def add_cancel(request,id):
	
	access=rights(request)['access']
	access_id=rights(request)['access_id']

	# ------------------------- check data ----------------------------
	if access_cretential(access,'otp'):
		if request.method=="POST":
			
			cancel_reason=request.POST['cancel_reason']
			url=site_url()+'order/'
			data={"cancel_reason":cancel_reason,"id":id,'type':'cancel_order'}
			headers={'X-access-token':request.session['inventory_token']}
			responce_data=requests.get(url,json=data,headers=headers)
			result=responce_data.json()
		
			if result['message']==True:
				messages.success(request, f"Order Cancelled!!")
				return redirect('/today_order')
			else:
				messages.error(request, f"Error:'{result['message']}'")
				return redirect('/cancel_order/'+str(id))

		url=site_url()+'order/'
		data={"type":'one',
				"id":id}
		headers={'X-access-token':request.session['inventory_token']}
		responce_data=requests.get(url,json=data,headers=headers)
		result=responce_data.json()
		# print(result)
		if result['message']==True:
			order=result['data']['order']
			order_item=result['data']['order_item']
		else:
			order=""
			order_item=""

		return render(request,'cancel_order.html',{'order':order,'order_item':order_item})

	else:
		return redirect('/404')

@inventory_token
def add_otp(request,id):
	
	access=rights(request)['access']
	access_id=rights(request)['access_id']

	# ------------------------- check data ----------------------------
	if access_cretential(access,'otp'):
		if request.method=="POST":
			otp_list=""
			for i in range(1,5):
				otp=request.POST['otp_'+str(i)]
				
				if otp=="":
					messages.error(request, f"Error:'Invalid otp'")
					return redirect('/otp/'+str(id))

				otp_list=otp_list+otp
			try:
				otp_list=int(otp_list)
			except:
				messages.error(request, f"Error:'Invalid otp'")
				return redirect('/otp/'+str(id))

			url=site_url()+'order/'
			data={"otp":otp_list,"id":id,'type':'otp'}
			headers={'X-access-token':request.session['inventory_token']}
			responce_data=requests.get(url,json=data,headers=headers)
			result=responce_data.json()
			print(result)
			if result['message']==True:
				messages.success(request, f"Thanks for your order")
				return redirect('/today_order')
			else:
				messages.error(request, f" Error:'{result['message']}'")
				return redirect('/otp/'+str(id))

		url=site_url()+'order/'
		data={"type":'one',
				"id":id}
		headers={'X-access-token':request.session['inventory_token']}
		responce_data=requests.get(url,json=data,headers=headers)
		result=responce_data.json()
		# print(result)
		if result['message']==True:
			order=result['data']['order']
			order_item=result['data']['order_item']
		else:
			order=""
			order_item=""

		return render(request,'otp.html',{'order':order,'order_item':order_item})

	else:
		return redirect('/404')

@inventory_token
def my_cart(request):
	
	access=rights(request)['access']
	access_id=rights(request)['access_id']

	if access_cretential(access,'stock_update'):
		# <input type="time" name="due_time" id="id_due_time" class="form-control form-control-lg" value="{{ todo.due_time|time:'h:i:s' }}">
		delivery_time_=delivery_time()
		if (request.method=="POST"):
			arrival_time=request.POST['arrival_time']
			delivery_type=request.POST['delivery_type']
			delivery_name=request.POST['delivery_name']
			delivery_address=request.POST['delivery_address']

			# ------------------------------------------- Orders -------------------------------
			data={'arrival_time':arrival_time,
					'delivery_type':delivery_type,
					'type_':'cart_update',
					'delivery_name':delivery_name,
					'delivery_address':delivery_address

					}

			url=site_url()+'order_move/'	
			headers={'X-access-token':request.session['inventory_token']}
			responce_data=requests.get(url,json=data,headers=headers)
			result=responce_data.json()

			if result['message']==True:
				flash_message='Cart Preview !!'
				messages.warning(request, f"{flash_message}")
			else:
				cartitem_data=""
				flash_message=result['message']
			
				messages.error(request, f"{flash_message}")
			return redirect('/cart_preview')

	# ------------------------- List card item ----------------------------
	if access_cretential(access,'cart_item'):
		url=site_url()+'cart_item/'

		data={"type":"ALL"}
		headers={'X-access-token':request.session['inventory_token']}
		responce_data=requests.get(url,json=data,headers=headers)
		result=responce_data.json()

		if result['message']==True:
			cartitem_data=result['data']
		else:
			cartitem_data=""
			messages.error(request, f"{result['message']}")

		# ================================== cart ==========================
		url=site_url()+'cart/'

		data={"type":"cart"}
		headers={'X-access-token':request.session['inventory_token']}
		responce_data=requests.get(url,json=data,headers=headers)
		result=responce_data.json()

		if result['message']==True:
			cart_data=result['data']
		else:
			cart_data=[]
			messages.error(request, f" {result['message']}")

		if cart_data == []:
			cart_data=None
	door_delivery_charge=delivery_charge_()
	cash_pay=cash_pay_type_()
	online_pay=online_type_()
	delivery_type=delivery_type_()
	takeaway_type=takeaway_type_()
	# print(shoping_timing_())
	re_url='/my_cart/'
	return render(request,"cart.html",{'re_url':re_url,'takeaway_type':takeaway_type,'delivery_type':delivery_type,'online_pay':online_pay,'cash_pay':cash_pay,'door_delivery_charge':door_delivery_charge,'cartitem_data':cartitem_data,'cart_data':cart_data,'delivery_time_':delivery_time_})

@inventory_token
def cart_preview(request):
	
	access=rights(request)['access']
	name=rights(request)['name']
	username=rights(request)['username']
	access_id=rights(request)['access_id']

	if access_cretential(access,'stock_update'):
		# <input type="time" name="due_time" id="id_due_time" class="form-control form-control-lg" value="{{ todo.due_time|time:'h:i:s' }}">
		# arrival_time=request.GET['arrival_time']
		print("arrival_time ________________________________",request)
		# delivery_time_=delivery_time()
		# delivery_time_=arrival_time
		if (request.method=="POST"):
			
			payment_mode='cash'
			payment_id='cash'
			razorpay_payment_id='waiting'
			razorpay_signature_id='waiting'
			transcation=True
			
			# ------------------------------------------- Stock Check and Update -------------------------------
			data={
					'stock_type':'stock_update'
					}
			url=site_url()+'stock_update/'	
			headers={'X-access-token':request.session['inventory_token']}
			responce_data=requests.get(url,json=data,headers=headers)
			result=responce_data.json()
			
			if result['message']==True:
				pass
			elif  result['message']=='delete_item':
				item_qty=result['data']['quantity']
				item_id=result['data']['item_id']
				method=result['data']['method']
				item_name=result['data']['item_name']
				error_message=result['error_message']
				
				for i in range(0,int(item_qty)):
					url=site_url()+'cart_item/'
					data={"method":method,"item_id":item_id}
					headers={'X-access-token':request.session['inventory_token']}
					responce_data=requests.post(url,json=data,headers=headers)
					result=responce_data.json()
				
				messages.error(request, f"Error:{error_message}")
				return redirect('/my_cart')
				
			else:
				messages.error(request, f"stock update Error: {result['message']}")
				return redirect('/my_cart')
			# print("******************",transcation)
			if transcation==True:
				# ------------------------------------------- Orders -------------------------------
				data={
						'payment_mode':payment_mode,
						'payment_id':payment_id,
						'razorpay_payment_id':razorpay_payment_id,
						'razorpay_signature_id':razorpay_signature_id,
						'type_':'order_update',

						}

				url=site_url()+'order_move/'	
				headers={'X-access-token':request.session['inventory_token']}
				responce_data=requests.get(url,json=data,headers=headers)
				result=responce_data.json()

				if result['message']==True:
					order=result['data']['order_List']
					order_list=result['data']['order_item']

					item_list=''
					for i in order_list:
						item_name=i['item_name']
						qty=i['quantity']
						item_list=item_list+item_name+'--'+str(qty)+','
						# item_list.append(item)
					# ------------------------------------------------ SMS API --------------------------------------
					track_ink=payment_url()+'track_order/'+str(order[0]['id'])
					order_details=payment_url()+'order_hex/'+str(order[0]['url_hex'])
					# if order[0]['payment_mode']=='cash':
						# track_ink=track_ink+"		payment link: "+payment_url()+'order_hex/'+order[0]['url_hex']
					data={'username':name,'to_mobile':'91'+str(username),'order_id':order[0]['id'],'item_list':order_details,'amount':order[0]['grand_total'],'track_link':track_ink}
					sms_data=sms('order',data)
					try:
						message=sms_data['message']
						type_=sms_data['type']
					except Exception as e:
						None
						# print(e)
						# messages.error(request, f"{e}")

					flash_message='Order Placed !!'
					messages.info(request, f"{flash_message}")
				else:
					cartitem_data=""
					flash_message=result['message']
				
					messages.error(request, f"{flash_message}")
				return redirect('/order')
			else:
				# ------------------------------------------- Stock Check and Update -------------------------------
				data={
						'stock_type':'re_stock_update'
						}
				url=site_url()+'stock_update/'	
				headers={'X-access-token':request.session['inventory_token']}
				responce_data=requests.get(url,json=data,headers=headers)
				result=responce_data.json()

				if result['message']==True:
					messages.error(request, f"Re stock Error: Transcation Failed")
					return redirect('/my_cart')		
	# ------------------------- List card item ----------------------------
	if access_cretential(access,'cart_item'):
		url=site_url()+'cart_item/'

		data={"type":"ALL"}
		headers={'X-access-token':request.session['inventory_token']}
		responce_data=requests.get(url,json=data,headers=headers)
		result=responce_data.json()

		if result['message']==True:
			cartitem_data=result['data']
		else:
			cartitem_data=""
			messages.error(request, f"Cart Item Error: {result['message']}")

		# ================================== cart ==========================
		url=site_url()+'cart/'

		data={"type":"ALL"}
		headers={'X-access-token':request.session['inventory_token']}
		responce_data=requests.get(url,json=data,headers=headers)
		result=responce_data.json()

		if result['message']==True:
			cart_data=result['data']
		else:
			cart_data=[]
			messages.error(request, f"Cart Error: {result['message']}")

		if cart_data == []:
			cart_data=None
			return redirect('/home')
	door_delivery_charge=delivery_charge_()
	cash_pay=cash_pay_type_()
	online_pay=online_type_()
	delivery_type=delivery_type_()
	takeaway_type=takeaway_type_()
	# print(shoping_timing_())
	print('=================================',cart_data)
	price=cart_data[0]['grand_total']
	currency='INR'
	phone=username
	name=name
	order_id=cart_data[0]['payment_id']
	call_url=payment_url()+'online_payment/'
	raz_key=client_key()
	return render(request,"cart_preview.html",{'raz_key':raz_key,'call_url':call_url,'order_id':order_id,'price':price,'currency':currency,'phone':phone,'name':name,'takeaway_type':takeaway_type,'delivery_type':delivery_type,'online_pay':online_pay,'cash_pay':cash_pay,'door_delivery_charge':door_delivery_charge,'cartitem_data':cartitem_data,'cart_data':cart_data})

@csrf_exempt
def online_payment(request):

	if (request.method=="POST"):

		try:
			responce_data=request.POST
			payment_mode='online'

			params_dict = {
				'razorpay_payment_id' : responce_data['razorpay_payment_id'],
				'razorpay_order_id' : responce_data['razorpay_order_id'],
				'razorpay_signature' : responce_data['razorpay_signature']
			}
			status = razerpay_key().utility.verify_payment_signature(params_dict)
			
			payment_id=responce_data['razorpay_order_id']
			razorpay_payment_id=responce_data['razorpay_payment_id']
			razorpay_signature_id=responce_data['razorpay_signature']
			transcation=True
		except Exception as e:
			# print('================= Payment Error',e)
			messages.error(request, f"Error:'payment failed'")
			return redirect("/cart_preview")
		
		print("******************",transcation)
		if transcation==True:
				# ------------------------------------------- Stock Check and Update -------------------------------
			data={
					'stock_type':'online_stock_update',
					'type':'stock_update',
					'order_id':payment_id
					}
			url=site_url()+'stock_update/'
			responce_data=requests.get(url,json=data)
			result=responce_data.json()
			
			if result['message']==True:
				pass
			elif  result['message']=='delete_item':
				item_qty=result['data']['quantity']
				item_id=result['data']['item_id']
				method=result['data']['method']
				item_name=result['data']['item_name']
				error_message=result['error_message']
				
				for i in range(0,int(item_qty)):
					url=site_url()+'cart_item/'
					data={'type':method,"method":'online_payment',"item_id":item_id,'order_id':payment_id}
					responce_data=requests.post(url,json=data)
					result=responce_data.json()
				
				messages.error(request, f"Error:{error_message}")
				return redirect('/my_cart')
				
			else:
				messages.error(request, f"stock update Error: {result['message']}")
				return redirect('/my_cart')
			# ------------------------------------------- Orders -------------------------------
			data={
					'payment_mode':payment_mode,
					'payment_id':payment_id,
					'razorpay_payment_id':razorpay_payment_id,
					'razorpay_signature_id':razorpay_signature_id,
					'type_':'online_order_update',
					'order_id':payment_id

					}

			url=site_url()+'order_move/'	
			responce_data=requests.get(url,json=data)
			result=responce_data.json()

			if result['message']==True:
				order=result['data']['order_List']
				order_list=result['data']['order_item']
				name=result['data']['name']
				username=result['data']['mobile_no']

				item_list=''
				for i in order_list:
					item_name=i['item_name']
					qty=i['quantity']
					item_list=item_list+item_name+'--'+str(qty)+','
					# item_list.append(item)
				# ------------------------------------------------ SMS API --------------------------------------
				track_ink=payment_url()+'track_order/'+str(order[0]['id'])
				order_details=payment_url()+'order_hex/'+str(order[0]['url_hex'])
				# if order[0]['payment_mode']=='cash':
					# track_ink=track_ink+"		payment link: "+payment_url()+'order_hex/'+order[0]['url_hex']
				data={'username':name,'to_mobile':'91'+str(username),'order_id':order[0]['id'],'item_list':order_details,'amount':order[0]['grand_total'],'track_link':track_ink}
				sms_data=sms('order',data)
				try:
					message=sms_data['message']
					type_=sms_data['type']
				except Exception as e:
					None
					# print(e)
					# messages.error(request, f"{e}")

				flash_message='Order Placed !!'
				return redirect('/order')
			else:
				cartitem_data=""
				flash_message=result['message']
			
			messages.error(request, f"{flash_message}")
			return redirect('/order')
		else:
			# ------------------------------------------- Stock Check and Update -------------------------------
			data={
					'stock_type':'online_stock_update',
					'type':'re_stock_update',
					'order_id':payment_id

					}
			url=site_url()+'stock_update/'	
			responce_data=requests.get(url,json=data)
			result=responce_data.json()

			if result['message']==True:
				messages.error(request, f"Re stock Error: Transcation Failed")
				return redirect('/my_cart')	
			else:
				flash_message=result['message']
				messages.error(request, f"{flash_message}")
				return redirect('/home')	
	else:
		return redirect('/home')
@csrf_exempt
def online_payment_out(request):
	if (request.method=="POST"):
		print(request.POST)
		try:
			responce_data=request.POST
			payment_mode='online'

			params_dict = {
				'razorpay_payment_id' : responce_data['razorpay_payment_id'],
				'razorpay_order_id' : responce_data['razorpay_order_id'],
				'razorpay_signature' : responce_data['razorpay_signature']
			}
			status = razerpay_key().utility.verify_payment_signature(params_dict)
			
			payment_id=responce_data['razorpay_order_id']
			razorpay_payment_id=responce_data['razorpay_payment_id']
			razorpay_signature_id=responce_data['razorpay_signature']
			transcation=True
		except Exception as e:
			print('================= Payment Error',e)
			messages.error(request, f"Error:'payment failed'")
			return redirect("/")
		
		# print("******************",transcation)
		if transcation==True:
			# ------------------------------------------- Orders -------------------------------
			data={
					'payment_mode':payment_mode,
					'payment_id':payment_id,
					'razorpay_payment_id':razorpay_payment_id,
					'razorpay_signature_id':razorpay_signature_id,
					'type_':'online_order_out',
					'order_id':payment_id

					}

			url=site_url()+'order_move/'	
			responce_data=requests.get(url,json=data)
			result=responce_data.json()

			if result['message']==True:
				flash_message='Paid success !!'
			else:
				flash_message=result['message']
		return redirect("/order")

@inventory_token
def order(request):
	
	access=rights(request)['access']
	access_id=rights(request)['access_id']

	# ------------------------- order data ----------------------------
	if access_cretential(access,'order'):

		url=site_url()+'order/'
		data={"type":'ALL'}
		headers={'X-access-token':request.session['inventory_token']}
		responce_data=requests.get(url,json=data,headers=headers)
		result=responce_data.json()
		# print(result)
		if result['message']==True:
			order=result['data']['order']
			order_item=result['data']['order_item']
			order_total_items=result['data']['order_total_items']
		else:
			order=""
			order_item=""
			order_total_items=""
			
		if order == []:
			order=None
	return render(request,"orders.html",{'order':order,'order_item':order_item,'order_total_items':order_total_items})

@inventory_token
def order_details(request,id):
	
	access=rights(request)['access']
	name=rights(request)['name']
	username=rights(request)['username']
	access_id=rights(request)['access_id']
	# ------------------------- order data ----------------------------
	if access_cretential(access,'order'):
		
		# print(order)
		# ------------------------------------------- Orders -------------------------------
		data={
				'type_':'online_order_payment',
				'order_type':'id',
				'order_id':id

				}

		url=site_url()+'order_move/'	
		responce_data=requests.get(url,json=data)
		result=responce_data.json()
		
		# if result['message']!=True:
		# 	return redirect("/order")

		price=0
		order_id=''


		url=site_url()+'order/'

		data={"type":'one',
				"id":id}
		headers={'X-access-token':request.session['inventory_token']}
		responce_data=requests.get(url,json=data,headers=headers)
		result=responce_data.json()
		
		if result['message']==True:
			order=result['data']['order']
			order_item=result['data']['order_item']
		else:
			order=""
			order_item="" 

		for i in order:
			i['arrival_time']=datetime.strptime(i['arrival_time'],'%H:%M:%S').strftime("%I:%M %p")
			price=i['grand_total']
			order_id=i['payment_id']

		currency='INR'
		phone=username
		name=name
		call_url=payment_url()+'online_payment_out/'
		raz_key=client_key()

		return render(request,"order_details.html",{'price':price,'order_id':order_id,'phone':phone,'name':name,'call_url':call_url,'raz_key':raz_key,'currency':currency,'order':order,'order_item':order_item})
	else:
		messages.error(request, f"Order Detail Error: Invalid Access")
		return redirect("/logout")

def order_details_hex(request,id):
	
	# ------------------------- order data ----------------------------
	# ------------------------------------------- Orders -------------------------------
	data={
			'type_':'online_order_payment',
			'order_type':'hex',
			'order_id':id

			}

	url=site_url()+'order_move/'	
	responce_data=requests.get(url,json=data)
	result=responce_data.json()

	url=site_url()+'order/'
	data={"type":'url_hexa',
			"id":id}
	responce_data=requests.get(url,json=data)
	result=responce_data.json()
	
	price=0
	order_id=''

	if result['message']==True:
		order=result['data']['order']
		order_item=result['data']['order_item']
	else:
		order=""
		order_item=""
	
	for i in order:
		i['arrival_time']=datetime.strptime(i['arrival_time'],'%H:%M:%S').strftime("%I:%M %p")
		price=i['grand_total']
		order_id=i['payment_id']

	currency='INR'
	phone='9789301757'
	name='online pay'
	call_url=payment_url()+'online_payment_out/'
	raz_key=client_key()
	# print(i['arrival_time'])
	return render(request,"order_details_hex.html",{'price':price,'order_id':order_id,'phone':phone,'name':name,'call_url':call_url,'raz_key':raz_key,'currency':currency,'order':order,'order_item':order_item})
	
@inventory_token
def track_order(request,id):
	
	access=rights(request)['access']
	access_id=rights(request)['access_id']

	# ------------------------- check data ----------------------------
	if access_cretential(access,'order'):

		url=site_url()+'order/'
		data={"type":'one',
				"id":id}
		headers={'X-access-token':request.session['inventory_token']}
		responce_data=requests.get(url,json=data,headers=headers)
		result=responce_data.json()
		# print(result)
		if result['message']==True:
			order=result['data']['order']
			order_item=result['data']['order_item']
		else:
			order=""
			order_item=""

	return render(request,"track_order.html",{'order':order,'order_item':order_item})
