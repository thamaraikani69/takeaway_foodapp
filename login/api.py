							# ---------------- Shivaya nama om -------------------------------

from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
import json

# -- Rest APi Framework --#
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# -- Imports --#
from . models import *
from . serializers import * 
from . tokenvalidation import *
from login.apps import *
import time
# Create your views here.

class otp_login(APIView):
	def post(self,request):
		data=json.loads(request.body)
		mobile_no=data['mobile_no']

		username_hash=(mobile_no)
		if len(username_hash)==10:
			otp=delivery_otp_()
			# print("___________________ otp ----------------------",otp)
			password_hash=password_encryption(otp)
			access='user'

			added_on=today()
			last_change_=last_change()
			status='active'

			if (access=='user'):
				
				user_check=user_login.objects.all().filter(username=username_hash)
				user_check=user_loginSerializer(user_check,many=True)
				user_check=user_check.data

				otp_time=time.time() + 60
				if user_check==[]:
					user_add=user_login(picture='dog.jpg',username=username_hash,password=password_hash,name="",added_on=added_on,last_change=last_change_,status='active',otp_time=otp_time)
					user_add.save()
					sms_msg=True
					
				else:
					try:
						if user_check[0]['otp_time']!=None:
							old_otp_time=user_check[0]['otp_time']
							# old_otp_time=old_otp_time.replace("T"," ")
							# old_otp_time=old_otp_time.replace("Z","")
							print( time.time(),(old_otp_time))
							# old_otp_time=datetime.fromisoformat(old_otp_time[:-1])
							# old_otp_time=datetime.strftime(old_otp_time,'%y-%m-%d %H:%M:%S')
							# old_otp_time=datetime.strptime(old_otp_time,'%y-%m-%d %H:%M:%S')
							# print(last_change_,"***************","old_otp_time")
							if time.time()<=float(old_otp_time):
								# user_update=user_login.objects.filter(status='active',username=user_check[0]['username']).update(last_change=last_change_,password=password_hash)
								sms_msg="Otp already send to your mobile no . otp is a login password"
								return Response({'message':sms_msg})
							else:
								user_update=user_login.objects.filter(status='active',username=user_check[0]['username']).update(last_change=last_change_,password=password_hash,otp_time=otp_time)
								sms_msg=True
						else:
								user_update=user_login.objects.filter(status='active',username=user_check[0]['username']).update(last_change=last_change_,password=password_hash,otp_time=otp_time)
								sms_msg=True
					except Exception as e:
						print("Exception",e)
						user_update=user_login.objects.filter(status='active',username=user_check[0]['username']).update(last_change=last_change_,password=password_hash,otp_time=otp_time)
						sms_msg=True

				if sms_msg==True:
					pass
					# ------------------------------------------------ SMS API --------------------------------------
					data={'mobile_no':'91'+username_hash,"otp":otp}
					sms_data=sms('otp_login',data)
					try:
						message=sms_data['message']
						type_=sms_data['type']
						return Response({'message':True})
					except Exception as e:
							None
							# return Response({'message':str(e)})
					# ------------------------------------------------------------------------------------------------
				else:
					return Response({'message':sms_msg})
			else:
				return Response({'message':'Invalid Access'})
		else:
				return Response({'message':'Invalid Mobile Number'})

class admin(APIView):
	def get(self,request):
		access=rights(request)['access']
		access_id=rights(request)['access_id']
		
		if access=='admin':
			data=json.loads(request.body)
			type_=data['type_']
			if type_=='admin_all':
				admin_List=admin_login.objects.all()
				serializer=admin_loginSerializer(admin_List,many=True)
				return Response({'message':True,'data':serializer.data})
			elif type_=='customer_all':
				user_List=user_login.objects.all().filter(status='active')
				serializer=user_loginSerializer(user_List,many=True)
				return Response({'message':True,'data':serializer.data})
		else:
			return Response({'message':'Invalid Access'})

class login(APIView):
	def post(self,request):
		data=json.loads(request.body)
		username=data['username']
		password=data['password']
		access=data['access']

		username_hash=(username)
		password_hash=password_encryption(password)

		if access=='admin':
			
			admin_check=admin_login.objects.all().filter(username=username_hash,password=password_hash)
			admin_check=admin_loginSerializer(admin_check,many=True)
			admin_check=admin_check.data
			
			if admin_check!=[]:
				return Response({'message':True,'data':admin_check,'access':access})
			else:
				return Response({'message':False})

		if access=='user':
			
			user_check=user_login.objects.all().filter(username=username_hash,password=password_hash)
			user_check=user_loginSerializer(user_check,many=True)
			user_check=user_check.data
			
			if user_check!=[]:
				return Response({'message':True,'data':user_check,'access':access})
			else:
				return Response({'message':False})

		else:
			return Response({'message':False})

class signup(APIView):
	def post(self,request):
		data=json.loads(request.body)
		name=data['name']
		username=data['username']
		password=data['password']

		username_hash=(username)
		password_hash=password_encryption(password)
		access='user'

		added_on=today()
		last_change_=last_change()
		status='active'

		if (access=='user'):
			
			user_check=user_login.objects.all().filter(username=username_hash)
			user_check=user_loginSerializer(user_check,many=True)
			user_check=user_check.data

			if user_check==[]:
				user_add=user_login(picture='dog.jpg',username=username,password=password_hash,name=name,added_on=added_on,last_change=last_change_,status='active')
				user_add.save()
				
				return Response({'message':True})
			else:
				return Response({"message":'Mobile Number Already Register'})

		else:
			return Response({'message':'Invalid Access'})

	def put(self,request):
		access=rights(request)['access']
		access_id=rights(request)['access_id']
		
		added_on=today()
		last_change_=last_change()

		if access=='admin':
			data=json.loads(request.body)
			name=data['name']
			
			admin_List=admin_login.objects.all().filter(id=access_id,status='active')
			serializer=admin_loginSerializer(admin_List,many=True)
			admin_check=serializer.data
			if admin_check!=[]:
				account_update=admin_login.objects.filter(status='active',id=access_id).update(last_change=last_change_,name=name)
				return Response({'message':True,'data':access_id})
			else:
				return Response({'message':'Invalid Access'})
		elif access=='user':
				data=json.loads(request.body)
				name=data['name']
				
				user_List=user_login.objects.all().filter(id=access_id,status='active')
				serializer=user_loginSerializer(user_List,many=True)
				user_check=serializer.data
				if user_check!=[]:
					account_update=user_login.objects.filter(status='active',id=access_id).update(last_change=last_change_,name=name)
					return Response({'message':True,'data':access_id})
				else:
					return Response({'message':'Invalid Access'})
		else:
			return Response({'message':'Invalid Access'})
