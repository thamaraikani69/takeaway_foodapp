from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
from django.shortcuts import get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

import requests
import json


# -- Imports --#
from . models import admin_login
from . serializers import admin_loginSerializer 
from . tokenvalidation import get_inventory_token, inventory_token, user_encryption, password_encryption
from . apps import site_url
from django.http.response import JsonResponse
from login.tokenvalidation import *

# Create your views here.
def render_login(request):
	return redirect('login','user')

def otp_login(request):
	
	# ------------------------- check data ----------------------------
	if request.method=="POST":

		mobile_no=request.POST['mobile_no']

		url=site_url()+'otp_login/'
		data={"mobile_no":mobile_no}
		responce_data=requests.post(url,json=data)
		result=responce_data.json()
		
		return JsonResponse(({'data':result}))

	else:
		return JsonResponse(({'data':'Invalid Access'}))
		
def login(request,access):
	if rights(request)!=None:
		access=rights(request)['access']
		access_id=rights(request)['access_id']

		if access=='admin':
			return redirect('/dashboard')
		elif access=='user':
			return redirect('/home')
	else:
		if request.method=='POST':
			username=request.POST['username']
			password=request.POST['pass']
			
			username_hash=(username)
			password_hash=(password)

			if (access=='admin') or (access=='user'):
				url=site_url()+'login/'
				data={"username":username_hash,
						"password":password_hash,
						"access":access
						}
				responce_data=requests.post(url,json=data)
				result=responce_data.json()
				
				# login_check=admin_login.objects.filter(username__iexact=username,password__iexact=password)
				# login_check=admin_loginSerializer(login_check,many=True)
				# login_check=login_check.data
				
				if result['message']==True:
					login_check=result['data']
					Session=request.session["inventory_token"] = get_inventory_token(login_check[0]["id"],username_hash, login_check[0]['password'],access)
					messages.success(request, f"Welcome: {login_check[0]['username']}")
					if access=='admin':
						return redirect('/dashboard')
					elif access=='user':
						return redirect('/home')
					
				else:
					messages.error(request, f"Invalid Credentials")

		return render(request,'login.html',{'access':access})

# def signup(request):
# 	if request.method=='POST':
# 		name=request.POST['name']
# 		username=request.POST['username']
# 		password=request.POST['pass']
		
# 		username_hash=(username)
# 		password_hash=(password)
		
# 		url=site_url()+'signup/'
# 		data={	"name":name,
# 				"username":username_hash,
# 				"password":password_hash
# 				}
# 		responce_data=requests.post(url,json=data)
# 		result=responce_data.json()
		
# 		if result['message']==True:
			
# 			messages.success(request, f"Added Successfull")
# 			return redirect('/')
			
# 		else:
# 			messages.error(request, f"{result['message']}")

# 	return render(request,'signup.html')

def logout(request):
	request.session.clear()
	return redirect('render_login')
