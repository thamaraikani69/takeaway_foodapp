from django.urls import path
from . import views
from . import api

urlpatterns=[
				path('noti/',views.add_noti,name='add_noti'),
    			path('api/noti/',api.api_noti.as_view(),name='api_noti'),

    			path('cart/',views.add_cart,name='add_cart'),
    			path('api/cart_item/',api.api_cart_item.as_view(),name='api_cart_item'),
    			path('api/cart/',api.api_cart.as_view(),name='api_cart'),

    			path('my_cart/',views.my_cart,name='my_cart'),
    			path('cart_preview/',views.cart_preview,name='cart_preview'),
    			path('online_payment/',views.online_payment,name='online_payment'),
    			path('online_payment_out/',views.online_payment_out,name='online_payment_out'),
    			
    			path('api/stock_update/',api.api_stock_update.as_view(),name='api_stock_update'),
    			path('api/order_move/',api.api_order_move.as_view(),name='api_order_move'),

    			path('order/',views.order,name='order'),
    			path('api/order/',api.api_order.as_view(),name='api_order'),
				
				path('order_details/<int:id>',views.order_details,name='order_details'),
				path('order_hex/<str:id>',views.order_details_hex,name='order_details_hex'),
				path('track_order/<int:id>',views.track_order,name='track_order'),

				path('otp/<int:id>',views.add_otp,name='otp'),
				path('cancel_order/<int:id>',views.add_cancel,name='cancel'),

    			path('search/',views.add_search,name='add_search'),
    			path('download/',views.add_download,name='add_download'),
    			path('menu_cart/',views.add_menu_cart,name='add_menu_cart'),
    			path('api/search/',api.api_search.as_view(),name='api_search'),

    			path('api/setting_setting/',api.api_setting_setting.as_view(),name='api_setting_setting'),

			]