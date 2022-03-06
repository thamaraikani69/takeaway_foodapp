from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
from django.shortcuts import get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages


from login.apps import *
from company.image import *

import requests
import json
import os

from login.tokenvalidation import *


@inventory_token
def dashboard(request):
	
	access=rights(request)['access']
	access_id=rights(request)['access_id']

	# ------------------------- List Banner ----------------------------
	if access_cretential(access,'banner'):
		url=site_url()+'banner/'

		data={"type":"ALL"}
		headers={'X-access-token':request.session['inventory_token']}
		responce_data=requests.get(url,json=data,headers=headers)
		result=responce_data.json()

		if result['message']==True:
			banner_data=result['data']
		else:
			banner_data=""
			messages.error(request, f"Banner Error: {result['message']}")
	
	# ------------------------- List catagory ----------------------------
	
		url=site_url()+'catagory/'

		data={"type":"ALL"}
		headers={'X-access-token':request.session['inventory_token']}
		responce_data=requests.get(url,json=data,headers=headers)
		result=responce_data.json()

		if result['message']==True:
			cat_data=result['data']
			cat_json_data=[]
			for i in cat_data:
				cat_json_data.append(i['id'])
			# cat_json_data=json.dumps(cat_json_data)
		else:
			cat_data=""
			cat_json_data=""
			messages.error(request, f"List Catagory Error:{result['message']}")

		# ------------------------- List cat item ----------------------------
		url=site_url()+'catitem/'

		data={"type":"ALL"}
		headers={'X-access-token':request.session['inventory_token']}
		responce_data=requests.get(url,json=data,headers=headers)
		result=responce_data.json()
		if result['message']==True:
			catitem_data=result['data']
		else:
			catitem_data=""
			messages.error(request, f"Cat Item Error:{result['message']}")

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
			messages.error(request, f"Food Cat Error:{result['message']}")

			# ------------------------- List card item ----------------------------
		url=site_url()+'cart_item/'

		data={"type":"ALL"}
		headers={'X-access-token':request.session['inventory_token']}
		responce_data=requests.get(url,json=data,headers=headers)
		result=responce_data.json()

		if result['message']==True:
			cartitem_data=result['data']
		else:
			cartitem_data=""
			messages.error(request, f"Cart Item Error:{result['message']}")
		
		print('======================================================',last_change())

		return render(request,'index.html',{'banner_data':banner_data,'cat_json_data':cat_json_data,'cartitem_data':cartitem_data,'cat_data':cat_data,'catitem_data':catitem_data,'foodcat_data':foodcat_data})
	else:
		messages.error(request,f("Error:Invalid access"))
		return redirect('/logout')

# ---------------------------------- View all ---------------------------
@inventory_token
def contact_us(request):
	access=rights(request)['access']
	access_id=rights(request)['access_id']

	# ------------------------- List cat item ----------------------------
	if access_cretential(access,'catitem'):
		url=site_url()+'company/'
		headers={'X-access-token':request.session['inventory_token']}
		responce_data=requests.get(url,headers=headers)
		result=responce_data.json()
		# print("**************************",result)
		if result['message']==True:
			company_data=result['data'][0]
		else:
			company_data=[]
			
	return render(request,'contactus.html',{'company_data':company_data})

# ---------------------------------- View all ---------------------------
@inventory_token
def view_all(request,id):
	
	access=rights(request)['access']
	access_id=rights(request)['access_id']

	# ------------------------- List cat item ----------------------------
	if access_cretential(access,'catitem'):
		url=site_url()+'catitem/'

		data={"type":"one_all","cat_id":id}
		headers={'X-access-token':request.session['inventory_token']}
		responce_data=requests.get(url,json=data,headers=headers)
		result=responce_data.json()
		if result['message']==True:
			catitem_data=result['data']
		else:
			catitem_data=""
			messages.error(request, f"view all Error: {result['message']}")

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

	return render(request,'view_all.html',{'catitem_data':catitem_data,'cartitem_data':cartitem_data})

# ---------------------------------- Account ---------------------------
@inventory_token
def account(request):
	access=rights(request)['access']
	access_id=rights(request)['access_id']
	name=rights(request)['name']
	username=rights(request)['username']
	profile=rights(request)['profile']

	if request.method=='POST':
		url=site_url()+'signup/'

		name=request.POST['name']
		data={"name":name}

		headers={'X-access-token':request.session['inventory_token']}
		responce_data=requests.put(url,json=data,headers=headers)
		result=responce_data.json()

		if result['message']==True:
			try:
				file_=request.FILES['picture']
				# ------------------------- banner image save ----------------------------
				id=result['data']
				file_path=os.path.join(server_path(), 'profile')
				if access=='admin':
					type_='account_admin'
				elif access=='admin':
					type_='account_user'

				image_save= image_(file_,id,file_path,type_)

				if image_save['message'] == True:
					messages.info(request, f"Image Save Successfull")
				messages.success(request,f"Account Updated!!")
				return redirect('/account')
			except Exception as e:
				print(e)
				messages.info(request, f"{e}")
		else:
			messages.error(request, f"view all Error: {result['message']}")

	return render(request,'account.html',{'name':name,'username':username,'profile':profile})

# ---------------------------------- item cat ---------------------------
@inventory_token
def item_catagory(request,id):
	access=rights(request)['access']
	access_id=rights(request)['access_id']

	# ------------------------- List Banner ----------------------------
	if access_cretential(access,'banner'):
		url=site_url()+'banner/'

		data={"type":"ALL"}
		headers={'X-access-token':request.session['inventory_token']}
		responce_data=requests.get(url,json=data,headers=headers)
		result=responce_data.json()

		if result['message']==True:
			banner_data=result['data']
		else:
			banner_data=""
			messages.error(request, f"Banner Error: {result['message']}")

	# ------------------------- List Food catagory ----------------------------
	
		url=site_url()+'food_catagory/'

		data={"type":"ALL"}
		headers={'X-access-token':request.session['inventory_token']}
		responce_data=requests.get(url,json=data,headers=headers)
		result=responce_data.json()
		if result['message']==True:
			foodcat_data=result['data']
		else:
			foodcat_data=""
			messages.error(request, f"Food Catagory Error: {result['message']}")

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
			messages.error(request, f"List Item Error: {result['message']}")

	# ------------------------- List card item ----------------------------
	
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


	foodcat_data_list=[]
	for i in foodcat_data:
		foodcat_data_list.append(i['id'])

	return render(request,'item_catagory.html',{'cartitem_data':cartitem_data,'item_data':item_data,'foodcat_data':foodcat_data,'banner_data':banner_data,'id':id,'foodcat_data_list':foodcat_data_list})