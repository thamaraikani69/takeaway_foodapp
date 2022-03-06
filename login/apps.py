from django.apps import AppConfig
from sys import platform
from datetime import date, timedelta,datetime
import math, random
import requests
import razorpay

import pytz
ist=pytz.timezone('Asia/Kolkata')
from pytz import timezone
timedate =datetime.now(timezone('Asia/Kolkata'))
timedate=timedate.replace(tzinfo=None)
timedate=timedate
today_=timedate.date()


import http.client
def sms(flow_type,data):

    hotel_name="ElCAFETERIA RESTAURANT"
    name="ElCAFETERIA"

    if flow_type=="otp_login":
        mobile_no=data['mobile_no']
        otp=data['otp']

        flow_id=""

        payload = "{\n  \"flow_id\": \""+flow_id+"\",\n  \"sender\": \"AIBEIN\",\n  \"mobiles\": \""+mobile_no+"\",\n  \"hotelname\": \""+hotel_name+"\",\n  \"otp\": \""+otp+"\",\n  \"name\": \""+name+"\"\n}\n"
        payload_list=[payload]

    elif flow_type=="order":
        mobile_no=''
        # mobile_no=''
        to_mobile=str(data['to_mobile'])
        username=str(data['username'])
        order_id=str(data['order_id'])
        item_list=str(data['item_list'])
        item_list=url_shortner(item_list)
        Total_amount=str(data['amount'])
        Track_link=str(data['track_link'])
        Track_link=url_shortner(Track_link)

        flow_id="618ce7ebcf315c0280690143"

        payload1 = "{\n    \"flow_id\": \""+flow_id+"\",\n  \"sender\": \"AIBEIN\",\n\"mobiles\": \""+mobile_no+"\",\n\"hotelname\": \""+hotel_name+"\",\n \"username\":\"\",    \n  \"name\": \""+name+"\",\n  \"amount\": \""+Total_amount+"\",\n  \"order_id\": \""+order_id+"\",\n  \"item_list\": \""+item_list+"\",\n   \"track_link\": \""+Track_link+"\"\n\n \n}\n"
        # payload2 = "{\n    \"flow_id\": \""+flow_id+"\",\n  \"sender\": \"AIBEIN\",\n\"mobiles\": \""+to_mobile+"\",\n\"hotelname\": \""+hotel_name+"\",\n \"username\":\"\",    \n  \"name\": \""+name+"\",\n  \"amount\": \""+Total_amount+"\",\n  \"order_id\": \""+order_id+"\",\n  \"item_list\": \""+item_list+"\",\n   \"track_link\": \""+Track_link+"\"\n\n \n}\n"
        payload_list=[payload1]

    print(payload_list)
    conn = http.client.HTTPSConnection("api.msg91.com")


    headers = {
        'authkey': "",
        # 'authkey': "",
        'content-type': "application/JSON"
        }

    for p in payload_list:
        print(p)
        conn.request("POST", "/api/v5/flow/", p, headers)

        res = conn.getresponse()
        data = res.read()

        result=(data.decode("utf-8"))
        print(result)
    return result

def url_shortner(short_url):
    url="https://tinyurl.com/api-create.php?url="+str(short_url)
    short_url=requests.get(url)
    short_url=short_url.text
    return short_url

class LoginConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'login'

def site_url():
    if "linux" in platform:
        site_url="https://takeaway.ai-being.com/api/"
        return site_url
    else:
        site_url="http://127.0.0.1:8000/api/"
        return site_url

def payment_url():
    if "linux" in platform:
        payment_url="https://takeaway.ai-being.com/"
        return payment_url
    else:
        payment_url="http://127.0.0.1:8000/"
        return payment_url

def server_path():
    if "linux" in platform:
        server_path="/var/www/takeaway/static/assets/image"
        return server_path
    else:
        server_path="D:\\projects\\Aibeing\\takeaway\\takeaway\\static\\assets\\image"
        return server_path

# def razerpay_key():
#     razorpay_client = razorpay.Client(auth=("rzp_test_ZP1gxC82m6NHFp","Hvu012RrGhUSAlbUSsWKTYDp"))
#     return razorpay_client

def razerpay_key():
    razorpay_client = razorpay.Client(auth=("",""))
    return razorpay_client

def security_key():
    return 'm'
    
def client_key():
    return 'r'

def razerpay_accountno():
    return '23'

def razorpay_trans(product_id,order_amount,currency):

    try:
        order_amount = int(order_amount)
        order_currency = currency
        order_receipt = 'order_rcptid_'+str(product_id)
        notes = {'Transaction Details:order id': product_id}
        order_response=razerpay_key().order.create(dict(amount=int(order_amount)*100, currency=order_currency, receipt=order_receipt, notes=notes, payment_capture='1'))
        order_id = order_response['id']
        order_status = order_response['status']

        if order_status=='created':
            return {'message':True,'trans_data':{'product_id':product_id,'trans_id':order_id}}
        else:
            return {'message':'something wrong...'}
    except Exception as e:
        # print("+++++++++++++++++++++++++++++++++++",e)
        return {'message':'Enter the minimum amount 1RS.'}

def aibeing_razorpay_trans(product_id,order_amount,currency):

    try:
        order_amount = int(order_amount)
        order_currency = currency
        order_receipt = 'order_rcptid_'+str(product_id)
        notes = {'Transaction Details:order id': product_id}
        order_response=razerpay_key().order.create(dict(amount=int(order_amount)*100, currency=order_currency, receipt=order_receipt, notes=notes, payment_capture='1'))
        order_id = order_response['id']
        order_status = order_response['status']

        if order_status=='created':
            return {'message':True,'trans_data':{'product_id':product_id,'trans_id':order_id}}
        else:
            return {'message':'something wrong...'}
    except:
        return {'message':'Enter the minimum amount 1RS.'}

def delivery_otp_():
    digits = "123456789"

    # length of password can be changed
    # by changing value in range
    OTP = ""
    for i in range(4) :
        OTP += digits[math.floor(random.random() * 9)]

    return OTP

def today():
    return today_

def  last_change():
    return timedate

def current_time():
    return str(today_.strftime("%I:%M %p"))

def delivery_time():
    todaydate=timedate + timedelta(minutes = 30)
    del_time=todaydate.strftime("%H:%M")
    # print(del_time)
    return str(del_time)

def dictfetchall(cursor): 
    "Returns all rows from a cursor as a dict" 
    desc = cursor.description 
    return [
            dict(zip([col[0] for col in desc], row)) 
            for row in cursor.fetchall() 
    ]


def access_cretential(access,catagory):
    cretential_list=['banner','banner_add','banner_delete','item_add','item','item_delete',
    'cat','cat_add','cat_delete','catitem_add','catitem_delete','catitem',
    'foodcat_add','foodcat_delete','foodcat','setting','today_order','order_report',
    'cart','cart_item','setting_cus','cart_item_add','item_report','stock_update','order_move','order','company','otp','order_cancel','order_edit','view_company','noti']

    if access=='admin':
        return True
    elif access=='user':
        catagory_list=['banner','setting_cus','cat','catitem','foodcat','item','cart_item',
        'cart_item','cart_item_add','stock_update','order_move','order','cart','view_company','noti']
        if catagory in catagory_list:
            return True
        else:
            return False
