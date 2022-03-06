from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.static import serve
from django.http.response import JsonResponse
from django.utils.safestring import SafeString
from django.views.decorators.csrf import csrf_exempt

from login.apps import *
from . image import *

import requests
import json
import os

from datetime import date, timedelta,datetime

import pytz
ist=pytz.timezone('Asia/Kolkata')
from pytz import timezone
timedate =datetime.now(timezone('Asia/Kolkata'))
timedate=timedate.replace(tzinfo=None)
timedate=timedate
todaydate=timedate.date()

from login.tokenvalidation import *

@inventory_token
def add_company(request):
	
	access=rights(request)['access']
	access_id=rights(request)['access_id']
	
	if access_cretential(access,'company'):
		if request.method=='POST':
			company_name=request.POST['company_name']
			email=request.POST['email']
			address=request.POST['address']
			gst=request.POST['gst']
			phonenumber=request.POST['phonenumber']
			filename='logo_default.jpg'
			
			url=site_url()+'company/'
			data={"company_name":company_name,
					"email":email,
					"address":address,
					"gst":gst,
					"phonenumber":phonenumber,
					"filename":'null',
					"access":access
					}
			headers={'X-access-token':request.session['inventory_token']}
			responce_data=requests.post(url,json=data,headers=headers)
			result=responce_data.json()
			
			if result['message']==True:
				try:
					file_=request.FILES['filename']
					# ------------------------- banner image save ----------------------------
					id=result['data']
					file_path=os.path.join(server_path(), 'company')
					image_save= image_(file_,id,file_path,'company')

					if image_save['message'] == True:
						messages.info(request, f"Image Save Successfull")
				except Exception as e:
					print(e)
					messages.info(request, f"{e}")

				messages.success(request, f"Added Successfull")
				return redirect('/add_company')
				
			else:
				messages.error(request, f" {result}")

		
		url=site_url()+'company/'
		headers={'X-access-token':request.session['inventory_token']}
		responce_data=requests.get(url,headers=headers)
		result=responce_data.json()
		
		if result['message']==True:
			company_data=result['data'][0]
		else:
			company_data=[]
			messages.error(request, f" {result}")
		if company_data==[]:
			company_data=None
		return render(request,'company.html',{'company_data':company_data})
	else:
		return redirect('/404')


@inventory_token
def add_offer(request):
	
	access=rights(request)['access']
	access_id=rights(request)['access_id']

	if access_cretential(access,'banner_add'):
		if request.method=='POST':
			offer_name=request.POST['offer_name']
			offer_percentage=request.POST['offer_percentage']
			times=request.POST['offer_times']

			url=site_url()+'offer/'
			data={"offer_name":offer_name,
					"offer_percentage":offer_percentage,
					"times":times
					}
			headers={'X-access-token':request.session['inventory_token']}
			responce_data=requests.post(url,json=data,headers=headers)
			result=responce_data.json()
			
			if result['message']==True:

				messages.success(request, f"Added Successfull")
				return redirect('/offer')
				
			else:
				messages.error(request, f" {result}")

	# ------------------------- List offer ----------------------------
	
		url=site_url()+'offer/'

		headers={'X-access-token':request.session['inventory_token']}
		responce_data=requests.get(url,headers=headers)
		result=responce_data.json()

		if result['message']==True:
			offer_data=result['data']
		else:
			offer_data=""
			messages.error(request, f"Error: {data[0]}")
		return render(request,'offer.html',{'offer_data':offer_data})
	else:
		return redirect('/404')

@inventory_token
def add_banner(request):
	
	access=rights(request)['access']
	access_id=rights(request)['access_id']

	if access_cretential(access,'banner_add'):
		if request.method=='POST':
			bannername=request.POST['bannername']
			# bannerorder=request.POST['bannerorder']
			bannerstatus=request.POST['bannerstatus']
			bannerlink=request.POST['bannerlink']
			bannerorder=0
			bannerimage='bannerdefault.jpg'

			url=site_url()+'banner/'
			data={"bannername":bannername,
					"bannerorder":bannerorder,
					"bannerimage":bannerimage,
					"bannerstatus":bannerstatus,
					"bannerlink":bannerlink,
					"access":access
					}
			headers={'X-access-token':request.session['inventory_token']}
			responce_data=requests.post(url,json=data,headers=headers)
			result=responce_data.json()
			
			if result['message']==True:
				try:
					file_=request.FILES['filename']
					# ------------------------- banner image save ----------------------------
					id=result['data']
					file_path=os.path.join(server_path(), 'banner')
					image_save= image_(file_,id,file_path,'banner')

					if image_save['message'] == True:
						messages.info(request, f"Image Save Successfull")
				except Exception as e:
					print(e)
					messages.info(request, f"{e}")

				messages.success(request, f"Added Successfull")
				return redirect('/banner')
				
			else:
				messages.error(request, f" {result}")

	# ------------------------- List Banner ----------------------------
	
		url=site_url()+'banner/'

		data={"type":"ALL"}
		headers={'X-access-token':request.session['inventory_token']}
		responce_data=requests.get(url,json=data,headers=headers)
		result=responce_data.json()

		if result['message']==True:
			banner_data=result['data']
		else:
			banner_data=""
			messages.error(request, f"Error: {data[0]}")
		return render(request,'banner.html',{'banner_data':banner_data})
	else:
		return redirect('/404')

@inventory_token
def add_item(request):
	
	access=rights(request)['access']
	access_id=rights(request)['access_id']

	if access_cretential(access,'item_add'):
		if request.method=='POST':
			code=request.POST['code']
			itemname=request.POST['itemname'].lower()
			rate=request.POST['rate']
			dish_cat=request.POST['dish_cat']
			discount=request.POST['discount']
			food_cat=request.POST['food_cat']
			stock=request.POST['stock']
			quantity=request.POST['quantity']
			stock_alert=request.POST['stockalert']
			sales_status=request.POST['sales_status']
			itemimage='itemdefault.jpg'
			
			
			url=site_url()+'item/'
			data={"code":code,
					"itemname":itemname,
					"itemimage":itemimage,
					"rate":rate,
					"discount":discount,
					"food_cat":food_cat,
					"dish_cat":dish_cat,
					"stock":stock,
					"quantity":quantity,
					"stock_alert":stock_alert,
					"sales_status":sales_status,
					"access":access
					}
			headers={'X-access-token':request.session['inventory_token']}
			responce_data=requests.post(url,json=data,headers=headers)
			result=responce_data.json()
			# print("*******************",result)
			if result['message']==True:

				try:
					file_=request.FILES['filename']
					# ------------------------- Item image save ----------------------------
					id=result['data']
					file_path=os.path.join(server_path(), 'item')
					image_save= image_(file_,id,file_path,'item')
					# print(image_save)
					if image_save['message'] == True:
						messages.info(request, f"Image Save Successfull")
				except Exception as e:
					messages.info(request, f"{e}")

				messages.success(request, f"Added Successfull")
				return redirect('/item')
				
			else:
				messages.error(request, f" {result}")

	# ------------------------- List Item ----------------------------
	
		url=site_url()+'item/'

		data={"type":"ALL"}
		headers={'X-access-token':request.session['inventory_token']}
		responce_data=requests.get(url,json=data,headers=headers)
		result=responce_data.json()

		if result['message']==True:
			item_data=result['data']
		else:
			item_data=""
			messages.error(request, f"Error: {data[0]}")

	# ------------------------- List Food catagory ----------------------------
	
		url=site_url()+'food_catagory/'

		data={"type":"ALL"}
		headers={'X-access-token':request.session['inventory_token']}
		responce_data=requests.get(url,json=data,headers=headers)
		result=responce_data.json()
		# print(result)
		if result['message']==True:
			foodcat_data=result['data']
		else:
			foodcat_data=""
			messages.error(request, f"Error: {data[0]}")

		return render(request,'item.html',{'item_data':item_data,'foodcat_data':foodcat_data})
	else:
		return redirect('/404')

@inventory_token
def edit_item(request,id):
	
	access=rights(request)['access']
	access_id=rights(request)['access_id']

	if access_cretential(access,'item_add'):
		if request.method=='POST':
			code=request.POST['code']
			itemname=request.POST['itemname'].lower()
			rate=request.POST['rate']
			dish_cat=request.POST['dish_cat']
			discount=request.POST['discount']
			food_cat=request.POST['food_cat']
			stock=request.POST['stock']
			quantity=request.POST['quantity']
			stock_alert=request.POST['stockalert']
			sales_status=request.POST['sales_status']
			itemimage='itemdefault.jpg'
			
			
			url=site_url()+'item/'
			data={"code":code,
					"id":id,
					"itemname":itemname,
					"itemimage":itemimage,
					"rate":rate,
					"discount":discount,
					"food_cat":food_cat,
					"dish_cat":dish_cat,
					"stock":stock,
					"quantity":quantity,
					"stock_alert":stock_alert,
					"sales_status":sales_status,
					"access":access
					}
			headers={'X-access-token':request.session['inventory_token']}
			responce_data=requests.put(url,json=data,headers=headers)
			result=responce_data.json()

			if result['message']==True:

				try:
					file_=request.FILES['filename']
					# ------------------------- Item image save ----------------------------
					id=id
					file_path=os.path.join(server_path(), 'item')
					image_save= image_(file_,id,file_path,'item')
					# print('******************************************',image_save)
					if image_save['message'] == True:
						messages.info(request, f"Image Save Successfull")
				except Exception as e:
					messages.info(request, f"{e}")

				messages.success(request, f"Added Successfull")
				return redirect('/edit_item/'+str(id))
				
			else:
				messages.error(request, f" {result}")

	# ------------------------- List Item ----------------------------
	
		url=site_url()+'item/'

		data={"type":"one",'id':id}
		headers={'X-access-token':request.session['inventory_token']}
		responce_data=requests.get(url,json=data,headers=headers)
		result=responce_data.json()

		if result['message']==True:
			item_data=result['data']
		else:
			item_data=""
			messages.error(request, f"Error: {data[0]}")

	# ------------------------- List Food catagory ----------------------------
	
		url=site_url()+'food_catagory/'

		data={"type":"ALL"}
		headers={'X-access-token':request.session['inventory_token']}
		responce_data=requests.get(url,json=data,headers=headers)
		result=responce_data.json()
		print(result)
		if result['message']==True:
			foodcat_data=result['data']
		else:
			foodcat_data=""
			messages.error(request, f"Error: {data[0]}")

		return render(request,'edit_item.html',{'item_data':item_data,'foodcat_data':foodcat_data})
	else:
		return redirect('/404')

@inventory_token
def edit_order(request,id):
	
	access=rights(request)['access']
	access_id=rights(request)['access_id']

	if access_cretential(access,'item_add'):
		if request.method=='POST':
			order_status=request.POST['order_status']
			delivery_type=request.POST['delivery_type']
			payment_type=request.POST['payment_type']
			cancel_reason=request.POST['cancel_reason']

			url=site_url()+'order/'
			data={"order_status":order_status,
					"id":id,
					"delivery_type":delivery_type,
					"payment_type":payment_type,
					"cancel_reason":cancel_reason
					}
			headers={'X-access-token':request.session['inventory_token']}
			responce_data=requests.put(url,json=data,headers=headers)
			result=responce_data.json()

			if result['message']==True:
				messages.success(request, f"Added Successfull")
				return redirect('/edit_order/'+str(id))
				
			else:
				messages.error(request, f" {result}")

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

		return render(request,'edit_order.html',{'order':order,'order_item':order_item})
	else:
		return redirect('/404')

@inventory_token
def view_order(request,id):
	
	access=rights(request)['access']
	access_id=rights(request)['access_id']

	if access_cretential(access,'item_add'):
		if request.method=='POST':
			order_status=request.POST['order_status']
			delivery_type=request.POST['delivery_type']
			payment_type=request.POST['payment_type']
			cancel_reason=request.POST['cancel_reason']

			url=site_url()+'order/'
			data={"order_status":order_status,
					"id":id,
					"delivery_type":delivery_type,
					"payment_type":payment_type,
					"cancel_reason":cancel_reason
					}
			headers={'X-access-token':request.session['inventory_token']}
			responce_data=requests.put(url,json=data,headers=headers)
			result=responce_data.json()

			if result['message']==True:
				messages.success(request, f"Added Successfull")
				return redirect('/edit_order/'+str(id))
				
			else:
				messages.error(request, f" {result}")

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

		return render(request,'order_view.html',{'order':order,'order_item':order_item})
	else:
		return redirect('/404')

@inventory_token
def edit_banner(request,id):
	
	access=rights(request)['access']
	access_id=rights(request)['access_id']

	if access_cretential(access,'banner_add'):
		if request.method=='POST':
			bannername=request.POST['bannername']
			# bannerorder=request.POST['bannerorder']
			bannerstatus=request.POST['bannerstatus']
			bannerlink=request.POST['bannerlink']
			bannerorder=0
			bannerimage='bannerdefault.jpg'

			url=site_url()+'banner/'
			data={"id":id,
					"bannername":bannername,
					"bannerorder":bannerorder,
					"bannerimage":bannerimage,
					"bannerstatus":bannerstatus,
					"bannerlink":bannerlink,
					"access":access
					}
			headers={'X-access-token':request.session['inventory_token']}
			responce_data=requests.put(url,json=data,headers=headers)
			result=responce_data.json()
			
			if result['message']==True:
				try:
					file_=request.FILES['filename']
					# ------------------------- banner image save ----------------------------
					id=id
					file_path=os.path.join(server_path(), 'banner')
					image_save= image_(file_,id,file_path,'banner')

					if image_save['message'] == True:
						messages.info(request, f"Image Save Successfull")
				except Exception as e:
					print(e)
					messages.info(request, f"{e}")

				messages.success(request, f"Added Successfull")
				return redirect('/edit_banner/'+str(id))
				
			else:
				messages.error(request, f" {result}")

	# ------------------------- List Banner ----------------------------
	
		url=site_url()+'banner/'

		data={"type":"one",'id':id}
		headers={'X-access-token':request.session['inventory_token']}
		responce_data=requests.get(url,json=data,headers=headers)
		result=responce_data.json()

		if result['message']==True:
			banner_data=result['data']
		else:
			banner_data=""
			messages.error(request, f"Error: {result['message']}")
		return render(request,'edit_banner.html',{'banner_data':banner_data})
	else:
		return redirect('/404')


@inventory_token
def add_cat(request):
	
	access=rights(request)['access']
	access_id=rights(request)['access_id']
	
	if access_cretential(access,'add_cat'):
		if request.method=='POST':
			name=request.POST['catagoryname']
			# order=request.POST['order']
			order=0

			
			url=site_url()+'catagory/'
			data={"name":name,
					"order":order,
					"access":access
					}
			headers={'X-access-token':request.session['inventory_token']}
			responce_data=requests.post(url,json=data,headers=headers)
			result=responce_data.json()
			if result['message']==True:
				banner_data=result['data']
				messages.success(request, f"Added Successfull")
				return redirect('/catagory')
				
			else:
				messages.error(request, f" {result}")

		# ------------------------- List catagory ----------------------------
		
		url=site_url()+'catagory/'

		data={"type":"ALL"}
		headers={'X-access-token':request.session['inventory_token']}
		responce_data=requests.get(url,json=data,headers=headers)
		result=responce_data.json()

		if result['message']==True:
			cat_data=result['data']
		else:
			cat_data=""
			messages.error(request, f"Error: {data[0]}")
		return render(request,'catagory.html',{'cat_data':cat_data})
	else:
		return redirect('/404')

@inventory_token
def edit_cat(request,id):
	
	access=rights(request)['access']
	access_id=rights(request)['access_id']
	
	if access_cretential(access,'add_cat'):
		if request.method=='POST':
			name=request.POST['catagoryname']
			# order=request.POST['order']
			order=0

			
			url=site_url()+'catagory/'
			data={"name":name,
					"id":id,
					"order":order,
					"access":access
					}
			headers={'X-access-token':request.session['inventory_token']}
			responce_data=requests.put(url,json=data,headers=headers)
			result=responce_data.json()
			if result['message']==True:
				banner_data=result['data']
				messages.success(request, f"Added Successfull")
				return redirect('/edit_catagory/'+str(id))
				
			else:
				messages.error(request, f" {result}")

		# ------------------------- List catagory ----------------------------
		
		url=site_url()+'catagory/'

		data={"type":"one",'id':id}
		headers={'X-access-token':request.session['inventory_token']}
		responce_data=requests.get(url,json=data,headers=headers)
		result=responce_data.json()

		if result['message']==True:
			cat_data=result['data'][0]
		else:
			cat_data=""
			messages.error(request, f"Error: {data[0]}")
		return render(request,'edit_catagory.html',{'cat_data':cat_data})
	else:
		return redirect('/404')

@inventory_token
def list_cat(request):
	
	access=rights(request)['access']
	access_id=rights(request)['access_id']

	if access_cretential(access,'cat'):
	# ------------------------- List catagory ----------------------------
	
		url=site_url()+'catagory/'

		data={"type":"ALL"}
		headers={'X-access-token':request.session['inventory_token']}
		responce_data=requests.get(url,json=data,headers=headers)
		result=responce_data.json()

		if result['message']==True:
			cat_data=result['data']
		else:
			cat_data=""
			messages.error(request, f"Error: {data[0]}")

		site_url_="/catitem/"
		return render(request,'list_catagory.html',{'cat_data':cat_data,'site_url':site_url_})
	else:
		return redirect('/404')

@inventory_token
def add_catitem(request,id):
	
	access=rights(request)['access']
	access_id=rights(request)['access_id']

	if access_cretential(access,'catitem_add'):
		if request.method=='POST':
			cat_id=id
			itemid=request.POST['item_id']

			url=site_url()+'catitem/'
			data={"cat_id":cat_id,
					"itemid":itemid,
					"access":access
					}
			headers={'X-access-token':request.session['inventory_token']}
			responce_data=requests.post(url,json=data,headers=headers)
			result=responce_data.json()
			if result['message']==True:
				banner_data=result['data']
				messages.success(request, f"Added Successfull")
				return redirect('/catitem/'+str(id))
				
			else:
				messages.error(request, f" {result}")
				return redirect('/catitem/'+str(id))

	# ------------------------- List cat item ----------------------------
	
		url=site_url()+'catitem/'

		data={"type":"one_all","cat_id":id}
		headers={'X-access-token':request.session['inventory_token']}
		responce_data=requests.get(url,json=data,headers=headers)
		result=responce_data.json()
		if result['message']==True:
			catitem_data=result['data']
		else:
			catitem_data=""
			messages.error(request, f"Error: {data[0]}")

	# ------------------------- List catagory ----------------------------
	
		url=site_url()+'catagory/'

		data={"type":"one","id":id}
		headers={'X-access-token':request.session['inventory_token']}
		responce_data=requests.get(url,json=data,headers=headers)
		result=responce_data.json()
		
		if result['message']==True:
			cat_data=result['data']
		else:
			cat_data=""
			messages.error(request, f"Error: {data[0]}")

	# ------------------------- List Item ----------------------------
	
		url=site_url()+'item/'

		data={"type":"ALL"}
		headers={'X-access-token':request.session['inventory_token']}
		responce_data=requests.get(url,json=data,headers=headers)
		result=responce_data.json()

		if result['message']==True:
			item_data=result['data']
		else:
			item_data=""
			messages.error(request, f"Error: {data[0]}")
	
		return render(request,'cat_item.html',{'catitem_data':catitem_data,'cat_data':cat_data[0],'item_data':item_data})
	else:
		return redirect('/404')
@inventory_token
def add_foodcat(request):
	
	access=rights(request)['access']
	access_id=rights(request)['access_id']

	if access_cretential(access,'foodcat_add'):
		if request.method=='POST':
			name=request.POST['catagoryname']
			dishimage='default.jpg'
			
			url=site_url()+'food_catagory/'
			data={"name":name,
					"access":access,
					"dish_image":dishimage
					}
			headers={'X-access-token':request.session['inventory_token']}
			responce_data=requests.post(url,json=data,headers=headers)
			result=responce_data.json()
			if result['message']==True:
				file_=request.FILES['filename']
				# --------------------------------- Image Save ------------------------
				id=result['data']
				file_path=os.path.join(server_path(), 'dish_cat')
				image_save= image_(file_,id,file_path,'dish_cat')
				# print(image_save)
				if image_save['message'] == True:
					messages.info(request, f"Image Save Successfull")
				messages.success(request, f"Added Successfull")
				return redirect('/food_catagory')
				
			else:
				messages.error(request, f" {result}")

	# ------------------------- List Food catagory ----------------------------
	
		url=site_url()+'food_catagory/'

		data={"type":"ALL"}
		headers={'X-access-token':request.session['inventory_token']}
		responce_data=requests.get(url,json=data,headers=headers)
		result=responce_data.json()
		print(result)
		if result['message']==True:
			foodcat_data=result['data']
		else:
			foodcat_data=""
			messages.error(request, f"Error: {data[0]}")
		return render(request,'foodcatagory.html',{'foodcat_data':foodcat_data})
	else:
		return redirect('/404')

@inventory_token
def edit_foodcat(request,id):
	
	access=rights(request)['access']
	access_id=rights(request)['access_id']

	if access_cretential(access,'foodcat_add'):
		if request.method=='POST':
			name=request.POST['catagoryname']
			dishimage='default.jpg'
			
			url=site_url()+'food_catagory/'
			data={"name":name,
					"access":access,
					"dish_image":dishimage,
					"id":id
					}
			headers={'X-access-token':request.session['inventory_token']}
			responce_data=requests.put(url,json=data,headers=headers)
			result=responce_data.json()
			if result['message']==True:
				try:
					file_=request.FILES['filename']

					# --------------------------------- Image Save ------------------------
					
					file_path=os.path.join(server_path(), 'dish_cat')
					image_save= image_(file_,id,file_path,'dish_cat')
					print(image_save)
					if image_save['message'] == True:
						messages.info(request, f"Image Save Successfull")
					messages.success(request, f"Added Successfull")
					return redirect('/edit_food_catagory/'+str(id))
				except Exception as e:
					messages.info(request, f"{e}")
				messages.success(request, f"saved!!")
			else:
				messages.error(request, f" {result}")

	# ------------------------- List Food catagory ----------------------------
	
		url=site_url()+'food_catagory/'

		data={"type":"one",'id':id}
		headers={'X-access-token':request.session['inventory_token']}
		responce_data=requests.get(url,json=data,headers=headers)
		result=responce_data.json()
		# print(result)
		if result['message']==True:
			foodcat_data=result['data'][0]
		else:
			foodcat_data=""
			messages.error(request, f"Error: {result['message']}")
		return render(request,'edit_foodcatagory.html',{'foodcat_data':foodcat_data})
	else:
		return redirect('/404')

@inventory_token
def add_setting(request):
	
	access=rights(request)['access']
	access_id=rights(request)['access_id']
	if access_cretential(access,'setting'):
		if request.method=='POST':

			
			url=site_url()+'setting/'

			try:
				tax=request.POST['tax']
			except:
				tax="off"
			try:
				delivery=request.POST['delivery']
			except:
				delivery="off"
			try:
				take_away=request.POST['take_away']
			except:
				take_away="off"
			try:
				cash_pay=request.POST['cash_pay']
			except:
				cash_pay="off"
			try:
				online=request.POST['online']
			except:
				online="off"
			try:
				shop_status=request.POST['shop_status']
			except:
				shop_status="off"
			try:
				stock_maintance=request.POST['stock_maintance']
			except:
				stock_maintance="off"

			dates_list=[{'date':'from_mon','value':'monday_from'},{'date':'to_mon','value':'monday_to'},{'date':'from_tues','value':'tuesday_from'},{'date':'to_tues','value':'tuesday_to'},{'date':'from_wednes','value':'wednesday_from'},{'date':'to_wednes','value':'wednesday_to'},{'date':'from_thurs','value':'thursday_from'},{'date':'to_thurs','value':'thursday_to'},{'date':'from_fri','value':'friday_from'},{'date':'to_fri','value':'friday_to'},{'date':'from_sat','value':'saturday_from'},{'date':'to_sat','value':'saturday_to'},{'date':'from_sun','value':'sunday_from'},{'date':'to_sun','value':'sunday_to'}]
			final_datelist=[]
			for i in dates_list:
				try:
					date=request.POST[i['date']]
					name=i['value']
				except:
					date="09:00 AM"
					name=i['value']
				final_datelist.append({'time':date,'name':name})
			

			data={
					"delivery_charges":request.POST['delivery_charges'],
					"gst":request.POST['gst'],
					"service_charges":request.POST['service_charges'],
					"tax":tax,
					"delivery":delivery,
					"take_away":take_away,
					"cash_pay":cash_pay,
					"online":online,
					"stock_maintance":stock_maintance,
					"shop_status":shop_status,
					'final_datelist':final_datelist
					}

			headers={'X-access-token':request.session['inventory_token']}
			responce_data=requests.post(url,json=data,headers=headers)
			result=responce_data.json()
			print(result)
			if result['message']==True:

				messages.success(request, f"Added Successfull")
				return redirect('/setting')
				
			else:
				messages.error(request, f" {result}")

	# ------------------------- List Setting ----------------------------
	
		url=site_url()+'setting/'

		data={"type":"ALL"}
		headers={'X-access-token':request.session['inventory_token']}
		responce_data=requests.get(url,json=data,headers=headers)
		result=responce_data.json()

		if result['message']==True:
			setting_data=result['data']
		else:
			setting_data=[]
			messages.error(request, f"Error: {data[0]}")
		if setting_data==[]:
			setting_data=None
		return render(request,'setting.html',{'setting_data':setting_data})
	else:
		return redirect('/404')

@inventory_token
def add_today_order(request):
	
	access=rights(request)['access']
	access_id=rights(request)['access_id']

	if access_cretential(access,'today_order'):
		if request.method=='POST':
			pass

	# ------------------------- check data ----------------------------
	

		url=site_url()+'order/'
		data={"type":'today_order'}
		headers={'X-access-token':request.session['inventory_token']}
		responce_data=requests.get(url,json=data,headers=headers)
		result=responce_data.json()
		# print(result)
		if result['message']==True:
			order=result['data']['order']
			order_item=result['data']['order_item']
			order_total_items=result['data']['order_total_items']
			order_handover=result['data']['order_handover']
		else:
			order=""
			order_item=""
			order_total_items=""

		for i in order:
			i['arrival_time']=datetime.strptime(i['arrival_time'],'%H:%M:%S').strftime("%I:%M %p")

		return render(request,'master_today_order.html',{'order':order,'order_item':order_item,'order_total_items':order_total_items,'order_handover':order_handover})
	else:
		return redirect('/404')

@inventory_token
def add_today_order_call(request):
	
	access=rights(request)['access']
	access_id=rights(request)['access_id']

	# ------------------------- check data ----------------------------
	if access_cretential(access,'today_order_add'):
		if request.method=="POST":
			
			type_=request.POST['type_']
			if type_=='Active All':
				url=site_url()+'today_order/'
				data={"id":'id',"updatefield":'updatefield','type_':type_}
				headers={'X-access-token':request.session['inventory_token']}
				responce_data=requests.post(url,json=data,headers=headers)
				result=responce_data.json()
				messages.success(request, f"All Items active Now")
				return redirect('/out_of_stock')
			elif type_=='In Active All':
				url=site_url()+'today_order/'
				data={"id":'id',"updatefield":'updatefield','type_':type_}
				headers={'X-access-token':request.session['inventory_token']}
				responce_data=requests.post(url,json=data,headers=headers)
				result=responce_data.json()
				messages.success(request, f"All Items Inactive Now")
				return redirect('/out_of_stock')				
			else:
				id=request.POST['id']
				updatefield=request.POST['updatefield']

				url=site_url()+'today_order/'
				data={"id":id,"updatefield":updatefield,'type_':type_}
				headers={'X-access-token':request.session['inventory_token']}
				responce_data=requests.post(url,json=data,headers=headers)
				result=responce_data.json()
				
				return JsonResponse(({'data':result}))
		else:
			return redirect('/out_of_stock')
	else:
		return redirect('/404')

@inventory_token
def add_item_report(request):
	
	access=rights(request)['access']
	access_id=rights(request)['access_id']

	if access_cretential(access,'item_report'):
		item=""
		item_type="ALL"
		graph_data=[]
		if request.method=='POST':
			from_date=request.POST['from_date']
			to_date=request.POST['to_date']
			item_type=request.POST.getlist('item_type')
			
			url=site_url()+'item_report/'
			data={"from_date":from_date,
					"to_date":to_date,
					"item_type":'ALL'
					}
			headers={'X-access-token':request.session['inventory_token']}
			responce_data=requests.get(url,json=data,headers=headers)
			result=responce_data.json()

			if result['message']==True:
				item=result['data']
				if len(item_type)!=1:

					
						# ------------------------------ item dict ------------------------
					gf_dict=dict()
					for j in item_type:
						for i in item:
							if int(i['item_id'])==int(j):
								gf_name=i['item_name']
								gf_quantity=i['quantity']

								if gf_name not in gf_dict:
									gf_dict[str(gf_name)]={'Item Name':gf_name,'Quantity':gf_quantity}
								else:
									gf_dict[gf_name]['Quantity']=int(gf_dict[gf_name]['Quantity'])+int(gf_quantity)
						
					for i in gf_dict:
						graph_data.append(gf_dict[i])
					
					item_type="ALL"
					# -----------------------------------------------------------------------
				else:
					# ------------------------------ item dict ------------------------
					gf_dict=dict()
					for j in item_type:
						for i in item:
							if int(i['item_id'])==int(j):
								gf_date=i['added_on']
								gf_quantity=i['quantity']
								
								if gf_date not in gf_dict:
									gf_dict[str(gf_date)]={'date':gf_date,'Quantity':gf_quantity}
								else:
									gf_dict[gf_date]['Quantity']=int(gf_dict[gf_date]['Quantity'])+int(gf_quantity)
					for i in gf_dict:
						graph_data.append(gf_dict[i])

					item_type="One"
					
					# -----------------------------------------------------------------------
			else:
				messages.error(request, f" {result}")
				item=""
		# =========================================== Item list ================================
		url=site_url()+'item/'

		data={"type":"ALL"}
		headers={'X-access-token':request.session['inventory_token']}
		responce_data=requests.get(url,json=data,headers=headers)
		result=responce_data.json()

		if result['message']==True:
			item_list=result['data']
		else:
			item_list=""
			messages.error(request, f"Error: {result}")

		today_=todaydate
		return render(request,'master_item_report.html',{'item_list':item_list,'today_':today_,'graph_data':SafeString(graph_data),'item_type':item_type,'item':item})

	else:
		return redirect('/404')

@inventory_token
def add_customer_food_report(request):
	
	access=rights(request)['access']
	access_id=rights(request)['access_id']

	if access_cretential(access,'item_report'):
		item=""
		item_type="ALL"
		graph_data=[]
		food_type=""
		customer_list=""
		
		# =========================================== Item list ================================
		url=site_url()+'item/'

		data={"type":"ALL"}
		headers={'X-access-token':request.session['inventory_token']}
		responce_data=requests.get(url,json=data,headers=headers)
		result=responce_data.json()

		if result['message']==True:
			item_list=result['data']
		else:
			item_list=""
			messages.error(request, f"Error: {result}")

		from_date=todaydate
		to_date=todaydate
		if request.method=='POST':
			from_date=request.POST['from_date']
			to_date=request.POST['to_date']
			item_type=request.POST.getlist('item_type')
			food_type=item_type
			# print(item_type,"=================================== Food Type",food_type)
			# ============================================== login details======================
			url=site_url()+'admin/'
			data={"type_":'customer_all'
					}
			headers={'X-access-token':request.session['inventory_token']}
			responce_data=requests.get(url,json=data,headers=headers)
			result=responce_data.json()

			if result['message']==True:
				customer_data=result['data']
			else:
				customer_data=""
			# =====================================================================================
			url=site_url()+'item_report/'
			data={"from_date":from_date,
					"to_date":to_date,
					"item_type":'ALL'
					}
			headers={'X-access-token':request.session['inventory_token']}
			responce_data=requests.get(url,json=data,headers=headers)
			result=responce_data.json()
			# print(result['data'])
			if result['message']==True:
				item=result['data']
				if len(item_type)!=1:

					
						# ------------------------------ item dict ------------------------
					customer_dic=dict()
					for c in customer_data:
						gf_dict=dict()
						for j in item_type:
							for f_item in item_list:
								if int(j) == f_item['id']:
									gf_dict[str(f_item['id'])]={'Item Name':f_item['itemname'],'Quantity':0}
						for j in item_type:
							for i in item:
								if int(i['item_id'])==int(j):
									gf_id=str(i['item_id'])
									gf_name=i['item_name']
									gf_quantity=i['quantity']
									if c['id']==i['customer_id'] and i['customer_access']=='user':
										if gf_name not in gf_dict:
											gf_dict[str(gf_id)]={'Item Name':gf_name,'Quantity':gf_quantity}
										else:
											gf_dict[gf_name]['Quantity']=int(gf_dict[gf_name]['Quantity'])+int(gf_quantity)
						customer_dic[str(c['id'])]={'data':gf_dict,'cus_name':c['name'],'username':c['username']}
						# print(customer_dic,"++++++++++++++++++++ Item ",item,"================customer_dic======",customer_dic)
					customer_list=[]
					# print("+++++++++++++++++++++++++++++++++++++",customer_dic)
					for i in customer_dic:
						# ============================================== customer report ======================
						url=site_url()+'item_report/'
						data={"item_type":'customer_report',
								"from_date":from_date,
								"to_date":to_date,
								'cus_id':i
								}
						headers={'X-access-token':request.session['inventory_token']}
						responce_data=requests.get(url,json=data,headers=headers)
						result=responce_data.json()
						# print("--------------------- Item Report ----------------",result,'===================================',i)
						if result['message']==True:
							customer_report=result['data'][0]
							cuslast_data=result['cuslast_data']
							if cuslast_data!=[]:
								cuslast_data=cuslast_data[0]
								grand_total=cuslast_data['grand_total']
								order_id=cuslast_data['id']
							else:
								grand_total=0
								order_id=0
							tot_qty=customer_report['tot_qty']
							tot_amt=customer_report['tot_amt']

						else:
							customer_report=result['data'][0]
							cuslast_data=result['data'][0]
							tot_qty=customer_report['tot_qty']
							tot_amt=customer_report['tot_amt']
							order_id=cuslast_data['id']
							grand_total=cuslast_data['grand_total']

						final_dic={}
						cus_name=customer_dic[i]['cus_name']
						username=customer_dic[i]['username']
						for j in customer_dic[i]['data']:
							k=customer_dic[i]['data'][j]
							
							item_name=k['Item Name']
							quantity=k['Quantity']
							final_dic.update({item_name:quantity})
						final_dic.update({'customer_name':cus_name})
						final_dic.update({'username':username})
						final_dic.update({'tot_qty':tot_qty})
						final_dic.update({'tot_amt':tot_amt})
						final_dic.update({'order_id':order_id})
						final_dic.update({'grand_total':grand_total})
						customer_list.append(final_dic)


					# ---------------------------------------------------------------------------------------------------------
					for i in gf_dict:
						graph_data.append(gf_dict[i])
					
					item_type="ALL"
					# -----------------------------------------------------------------------
				else:
						# ------------------------------ item dict ------------------------
					customer_dic=dict()
					for c in customer_data:
						gf_dict=dict()
						for j in item_type:
							for f_item in item_list:
								if int(j) == f_item['id']:
									gf_dict[str(f_item['id'])]={'Item Name':f_item['itemname'],'Quantity':0}
						for j in item_type:
							for i in item:
								if int(i['item_id'])==int(j):
									gf_id=str(i['item_id'])
									gf_name=i['item_name']
									gf_quantity=i['quantity']
									if c['id']==i['customer_id'] and i['customer_access']=='user':
										if gf_name not in gf_dict:
											gf_dict[str(gf_id)]={'Item Name':gf_name,'Quantity':gf_quantity}
										else:
											gf_dict[gf_name]['Quantity']=int(gf_dict[gf_name]['Quantity'])+int(gf_quantity)
						customer_dic[str(c['id'])]={'data':gf_dict,'cus_name':c['name'],'username':c['username']}
					# print('=====================ItEM=================',item)
					customer_list=[]
					for i in customer_dic:
						# ============================================== customer report ======================
						url=site_url()+'item_report/'
						data={"item_type":'customer_report',
								"from_date":from_date,
								"to_date":to_date,
								'cus_id':i
								}
						headers={'X-access-token':request.session['inventory_token']}
						responce_data=requests.get(url,json=data,headers=headers)
						result=responce_data.json()
						# print("--------------------- Item Report ----------------",result,'===================================',i)
						if result['message']==True:
							customer_report=result['data'][0]
							cuslast_data=result['cuslast_data']
							if cuslast_data!=[]:
								cuslast_data=cuslast_data[0]
								grand_total=cuslast_data['grand_total']
								order_id=cuslast_data['id']
							else:
								grand_total=0
								order_id=0
							tot_qty=customer_report['tot_qty']
							tot_amt=customer_report['tot_amt']

						else:
							customer_report=result['data'][0]
							cuslast_data=result['data'][0]
							tot_qty=customer_report['tot_qty']
							tot_amt=customer_report['tot_amt']
							order_id=cuslast_data['id']
							grand_total=cuslast_data['grand_total']

						final_dic={}
						cus_name=customer_dic[i]['cus_name']
						username=customer_dic[i]['username']
						for j in customer_dic[i]['data']:
							k=customer_dic[i]['data'][j]
							
							item_name=k['Item Name']
							quantity=k['Quantity']
							final_dic.update({item_name:quantity})
						final_dic.update({'customer_name':cus_name})
						final_dic.update({'username':username})
						final_dic.update({'tot_qty':tot_qty})
						final_dic.update({'tot_amt':tot_amt})
						final_dic.update({'order_id':order_id})
						final_dic.update({'grand_total':grand_total})
						customer_list.append(final_dic)


					# ---------------------------------------------------------------------------------------------------------
					for i in gf_dict:
						graph_data.append(gf_dict[i])

					# print("______________afsdanfjkdasnf_____",gf_dict,customer_list,'***************',item_type,item)
					item_type="One"
					
					# -----------------------------------------------------------------------
			else:
				messages.error(request, f" {result}")
				item=""
		

		from_date=todaydate
		to_date=todaydate
		return render(request,'master_customer_food_report.html',{'from_date':from_date,'to_date':to_date,'food_type':food_type,'customer_list':customer_list,'item_list':item_list,'item_type':item_type})

	else:
		return redirect('/404')


@inventory_token
def dashboard(request):
	
	access=rights(request)['access']
	access_id=rights(request)['access_id']

	if access_cretential(access,'item_report'):

		item_graph_data=[]
		graph_data=[]

		from_date=(timedate-timedelta(30)).date()
		to_date=(timedate-timedelta(-30)).date()
		print(from_date,to_date)
		item_type="ALL"
		order_type="ALL"

		# ---------------------------------- Item Report --------------------------------
		url=site_url()+'item_report/'
		data={"from_date":str(from_date),
				"to_date":str(to_date),
				"item_type":item_type
				}
		headers={'X-access-token':request.session['inventory_token']}
		responce_data=requests.get(url,json=data,headers=headers)
		result=responce_data.json()

		if result['message']==True:
			item=result['data']
			if item_type=='ALL':
				# ------------------------------ item dict ------------------------
				gf_dict=dict()
				for i in item:
					gf_name=i['item_name']
					gf_quantity=i['quantity']
					
					if gf_name not in gf_dict:
						gf_dict[str(gf_name)]={'Item Name':gf_name,'Quantity':gf_quantity}
					else:
						gf_dict[gf_name]['Quantity']=int(gf_dict[gf_name]['Quantity'])+int(gf_quantity)
				for i in gf_dict:
					item_graph_data.append(gf_dict[i])
				# -----------------------------------------------------------------------
		else:
			item=""
			messages.error(request, f" {result}")
		# -----------------------------------------------------------------------------------------------
		# ---------------------------------- Order Report ----------------------------------------------
		url=site_url()+'order_report/'
		data={"from_date":str(from_date),
				"to_date":str(to_date),
				"order_type":order_type
				}
		headers={'X-access-token':request.session['inventory_token']}
		responce_data=requests.get(url,json=data,headers=headers)
		result=responce_data.json()
		if result['message']==True:
			order=result['data']
			# ------------------------------ order dict ------------------------
			gf_dict=dict()
			for i in order:
				gf_date=i['added_on']
				gf_total=i['grand_total']
				
				if gf_date not in gf_dict:
					gf_dict[str(gf_date)]={'date':gf_date,'Amount':gf_total}
				else:
					gf_dict[gf_date]['Amount']=int(gf_dict[gf_date]['Amount'])+int(gf_total)
			for i in gf_dict:
				graph_data.append(gf_dict[i])

			# -----------------------------------------------------------------------
		else:
			messages.error(request, f" {result}")
			order=""
		
		today_=todaydate
		return render(request,'dashboard.html',{'item_graph_data':SafeString(item_graph_data),'graph_data':SafeString(graph_data)})

	else:
		return redirect('/404')

@inventory_token
def add_order_report(request):
	
	access=rights(request)['access']
	access_id=rights(request)['access_id']

	if access_cretential(access,'order_report'):
		order=""

		graph_data=[]
		if request.method=='POST':
			from_date=request.POST['from_date']
			to_date=request.POST['to_date']
			order_type=request.POST['order_type']

			
			url=site_url()+'order_report/'
			data={"from_date":from_date,
					"to_date":to_date,
					"order_type":order_type
					}
			headers={'X-access-token':request.session['inventory_token']}
			responce_data=requests.get(url,json=data,headers=headers)
			result=responce_data.json()

			if result['message']==True:
				order=result['data']
				# ------------------------------ order dict ------------------------
				gf_dict=dict()
				for i in order:
					gf_date=i['added_on']
					gf_total=i['grand_total']
					
					if gf_date not in gf_dict:
						gf_dict[str(gf_date)]={'date':gf_date,'Amount':gf_total}
					else:
						gf_dict[gf_date]['Amount']=int(gf_dict[gf_date]['Amount'])+int(gf_total)
				for i in gf_dict:
					print(gf_dict[i])
					graph_data.append(gf_dict[i])
				# -----------------------------------------------------------------------
			else:
				messages.error(request, f" {result}")
				order=""

		today_=todaydate
		return render(request,'master_order_report.html',{'order':order,'today_':today_,'graph_data':SafeString(graph_data)})

	else:
		return redirect('/404')

@inventory_token
def add_out_of_stock(request):
	
	access=rights(request)['access']
	access_id=rights(request)['access_id']

	if access_cretential(access,'item_add'):
		type_="ALL"
		data={"type":"ALL"}
		if request.method=='POST':
			type_=request.POST['item_type']

			# ------------------------- List Item ----------------------------
			
			data={"type":'one','id':str(type_)}
		url=site_url()+'item/'
		headers={'X-access-token':request.session['inventory_token']}
		responce_data=requests.get(url,json=data,headers=headers)
		result=responce_data.json()

		if result['message']==True:
			item_data=result['data']
		else:
			item_data=""
			messages.error(request, f"Error: {result}")

		url=site_url()+'item/'

		data={"type":"ALL"}
		headers={'X-access-token':request.session['inventory_token']}
		responce_data=requests.get(url,json=data,headers=headers)
		result=responce_data.json()

		if result['message']==True:
			item_list=result['data']
		else:
			item_list=""
			messages.error(request, f"Error: {result}")

		return render(request,'master_outofstock.html',{'item_data':item_data,'item_list':item_list})

	else:
		return redirect('/404')

@csrf_exempt
def payment_service_fee(request):
	try:
		responce_data=request.POST

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
		transcation=False
		# print('================= Payment Error',e)
		messages.error(request, f"Error:'payment failed'")
		return redirect("/service_fee")

	print("******************",transcation)
	if transcation==True:

		url=site_url()+'service_fee/'
		data={"type":'fee',
				"payment_id":payment_id,
				"order_id":razorpay_payment_id,
				"signature":razorpay_signature_id}

		# headers={'X-access-token':request.session['inventory_token']}
		responce_data=requests.post(url,json=data)
		result=responce_data.json()
		# print(result)
		if result['message']==True:
			messages.success(request, f"Paid Successfull")
			return redirect('/service_fee')
		else:
			return ok
			# return redirect('/service_fee')

		
@inventory_token
def service_fee(request):
	
	access=rights(request)['access']
	access_id=rights(request)['access_id']

	if access_cretential(access,'item_add'):

		url=site_url()+'service_fee/'
		data={"type":'fee'}
		headers={'X-access-token':request.session['inventory_token']}
		responce_data=requests.get(url,json=data,headers=headers)
		result=responce_data.json()
		# print(result)
		if result['message']==True:
			service_cost=result['data']['service_charges']
			order_data=result['data']['order_data']
			payment_id=result['data']['payment_id']
		else:
			order_data=""
			payment_id=""
			service_cost=""

		price=service_cost
		currency='INR'
		phone='9789301757'
		name='aibeing'
		order_id=payment_id
		call_url=payment_url()+'payment_service_fee/'
		raz_key=client_key()
		return render(request,'service_cost.html',{'raz_key':raz_key,'call_url':call_url,'order_id':order_id,'price':price,'currency':currency,'phone':phone,'name':name,'service_cost':service_cost,'order_data':order_data,'payment_id':payment_id})
	else:
		return redirect('/404')


# @inventory_token
def return_files_tut(request,folder_name,file_name):
	try:
		link=os.path.join(server_path(),folder_name,file_name)
		print(link)
		# link="D:\\projects\\Aibeing\\takeaway\\takeaway\\static\\assets\\image\\banner\\0d22a1b004d48d6d6217c0e57d2b27be.png"
		return serve(request,os.path.basename(link),os.path.dirname(link))
	except Exception as e:
		print('----------------- Error -------------------',e)
		print(link)
		link=os.path.join(server_path(),folder_name,'default.jpg')
		return serve(request,os.path.basename(link),os.path.dirname(link))

def add_404(request):
	return render(request,'404.html')
