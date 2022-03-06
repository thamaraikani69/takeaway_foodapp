from django.urls import path
from . import views
from . import api

urlpatterns=[
				
    			path('home/',views.dashboard,name='dashboard'),
    			path('view_all/<int:id>',views.view_all,name='view_all'),
    			path('item_catagory/<int:id>',views.item_catagory,name='item_catagory'),
    			path('account/',views.account,name='account'),
    			path('contact_us/',views.contact_us,name='contact_us'),

			]