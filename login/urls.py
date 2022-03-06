from django.urls import path
from . import views
from . import api

urlpatterns=[
				path('',views.render_login,name='render_login'),
				path('login/<str:access>/',views.login,name='login'),
				path('logout/',views.logout,name='logout'),
				path('otp_login/',views.otp_login,name='otp_login'),
				path('api/otp_login/',api.otp_login.as_view(),name='api_otp_login'),	
				# path('signup/',views.signup,name='signup'),
				path('api/signup/',api.signup.as_view(),name='api_signup'),	
				path('api/login/',api.login.as_view(),name='api_login'),	
				path('api/admin/',api.admin.as_view(),name='admin')
				
			]