# SWAMI KARUPPASWAMI THUNNAI

import time
import jwt
from django.utils.functional import wraps

from . models import *
from . serializers import * 
from django.shortcuts import get_object_or_404,redirect

# --- hash ---
import hashlib

salt='jeeva$kani*vichu&69'
salt=hashlib.sha512(salt.encode("utf-8")).hexdigest()

def get_inventory_token(inventory_id,token_user, password,level):
    inventory_secret = "jeeva$kani*vichu&69_7#%%^"
    expiry = time.time() + 259200
    token = {"inventory_id": inventory_id,'level':level,'token_user':token_user, "expiry": expiry}
    encoded_token = jwt.encode(token, key=password+inventory_secret)
    return encoded_token.decode("utf-8")


def inventory_token(_function):

  @wraps(_function)
  def wrapper_function(request,*args, **kwargs):
      if "inventory_token" not in request.session:
          return redirect("/")
      token = request.session["inventory_token"]
      try:
          decoded_token = jwt.decode(token, verify=False)
      except jwt.DecodeError:
          return redirect("/")
      admin_id = decoded_token["inventory_id"]
      access = decoded_token["level"]
      expiry_time = decoded_token["expiry"]
      if time.time() > expiry_time:
          request.session.clear()
          return redirect("/")

      if access=='admin':
          result=admin_login.objects.filter(id=admin_id)
          result=admin_loginSerializer(result,many=True)
          result=result.data
      elif access=='user':
          result=user_login.objects.filter(id=admin_id)
          result=user_loginSerializer(result,many=True)
          result=result.data
      else:
          return redirect("/")
      # print("+++++++++++++++++++++ result ==================",result)
      if result==[]:
          return redirect("/")
      password_hash = result[0]["password"]
      try:
          inventory_secret = "jeeva$kani*vichu&69_7#%%^"
          jwt.decode(token, key=password_hash+inventory_secret)
      except jwt.DecodeError:
          return redirect("/")
      return _function(request,*args, **kwargs)
  return wrapper_function


def user_encryption(username):
    username=username+salt
    username_hash = hashlib.sha512(username.encode("utf-8")).hexdigest()
    username_hash=salt+username_hash+salt
    username_hash=  hashlib.sha512(username_hash.encode("utf-8")).hexdigest()
    return username_hash

def password_encryption(password):
    password=password+salt
    password_hash = hashlib.sha512(password.encode("utf-8")).hexdigest()
    password_hash=salt+password_hash+salt
    password_hash=  hashlib.sha512(password_hash.encode("utf-8")).hexdigest()
    print(password_hash)
    return password_hash


def rights(request):
    try:
        token=None
        if 'x-access-token' in request.headers:
            token=request.headers['x-access-token']
            request.session['inventory_token']=token
        
        elif ("inventory_token" in request.session):
            token=request.session['inventory_token']
        # print(token)
        if not token:
            return None
        else:
            
            token=request.session["inventory_token"]
            decoded_token=jwt.decode(token,verify=False)
            if ("inventory_id" not in decoded_token) | ("token_user" not in decoded_token) | ("level" not in decoded_token):
                return None
            # print('decoded_token',decoded_token)
            admin_id=decoded_token["inventory_id"]
            token_user=decoded_token["token_user"]
            access= decoded_token['level']

            username_hash=token_user

            if access=="admin":
                right=admin_login.objects.filter(id=admin_id)
                right=admin_loginSerializer(right,many=True)
                right=right.data
            elif access=='user':
                right=user_login.objects.filter(id=admin_id)
                right=user_loginSerializer(right,many=True)
                right=right.data
            else:
                return None

            if right[0]['username']==username_hash:
                return {'access_id':admin_id,'access':access,'name':right[0]['name'],'username':username_hash,'profile':right[0]['picture']}
            else:
                return None
    except Exception as e:
        # print(e)
        pass
        return None