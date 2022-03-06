from django.urls import path
from . import views
from . import api

urlpatterns=[
    			path('dashboard/',views.dashboard,name='dashboard'),

    			path('add_company/',views.add_company,name='add_company'),
				path('api/company/',api.api_company.as_view(),name='api_company'),	
    			path('payment_service_fee/',views.payment_service_fee,name='payment_service_fee'),
    			path('service_fee/',views.service_fee,name='service_fee'),
				path('api/service_fee/',api.api_service_fee.as_view(),name='api_service_fee'),	

				path('banner/',views.add_banner,name='add_banner'),
				path('edit_banner/<int:id>',views.edit_banner,name='edit_banner'),
				path('api/banner/',api.api_banner.as_view(),name='api_banner'),	

				path('item/',views.add_item,name='add_item'),
				path('edit_item/<int:id>',views.edit_item,name='edit_item'),
				path('api/item/',api.api_item.as_view(),name='api_item'),	

				path('catagory/',views.add_cat,name='add_cat'),
				path('edit_catagory/<int:id>',views.edit_cat,name='edit_cat'),
				path('api/catagory/',api.api_cat.as_view(),name='api_cat'),	

				path('list_catagory/',views.list_cat,name='list_cat'),
				path('return-files/<str:folder_name>/<str:file_name>',views.return_files_tut,name='return_files_tut'),

				path('catitem/<int:id>',views.add_catitem,name='add_catitem'),
				path('api/catitem/',api.api_catitem.as_view(),name='api_catitem'),	

				path('food_catagory/',views.add_foodcat,name='add_foodcat'),
				path('edit_food_catagory/<int:id>',views.edit_foodcat,name='edit_foodcat'),
				path('api/food_catagory/',api.api_foodcat.as_view(),name='api_foodcat'),

				path('setting/',views.add_setting,name='add_setting'),
				path('api/setting/',api.api_setting.as_view(),name='setting'),

				path('today_order/',views.add_today_order,name='add_today_order'),
				path('today_order_call/',views.add_today_order_call,name='add_today_order_call'),
				path('api/today_order/',api.api_today_order.as_view(),name='today_order'),

				path('order_report/',views.add_order_report,name='add_order_report'),
				path('api/order_report/',api.api_order_report.as_view(),name='order_report'),

				path('404/',views.add_404,name='add_404'),

				path('item_report/',views.add_item_report,name='add_item_report'),
				path('api/item_report/',api.api_item_report.as_view(),name='item_report'),

				path('customer_food_report/',views.add_customer_food_report,name='add_customer_food_report'),
				path('offer/',views.add_offer,name='add_offer'),
				path('api/offer/',api.api_offer.as_view(),name='offer'),

				path('out_of_stock/',views.add_out_of_stock,name='add_out_of_stock'),
				path('edit_order/<int:id>',views.edit_order,name='edit_order'),

				path('view_order/<int:id>',views.view_order,name='view_order'),
			]

			# https://www.youtube.com/watch?v=UjLH-40RHZo
			# https://www.youtube.com/watch?v=VyipWmv61C4