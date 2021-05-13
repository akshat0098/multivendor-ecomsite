from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
#creating urls


urlpatterns = [
    path('',views.index,name="home"),
    path('addtocart/<int:pk>',views.Cart,name='cart'),
    path('cart/',views.view_cart,name='view_cart'),



    path('checkout/order-summary',views.checkout,name='checkout'),
    path('checkout/payment',views.checkout_payment,name='checkout-payment'),
    path('checkout/payment/success',views.checkout_payment_success,name='checkout-payment-success'),

    path('upload_product/',views.Upload_Product,name='Upload_product'),
    path('tracker/<str:pk>',views.order_tracker,name='tracker'),
    path('order_view/',views.order_page,name='order_view'),
    path('product/',views.product_view,name="product"),
    path('cart/<str:pk>',views.Cart,name="cart"),    
    path('update_product/<int:pk>',views.UpdateProduct,name="update_product"),
    path('place_order/<int:pk>',views.PlaceOrder,name="place_order"),
    path('shipping/',views.Shipping,name="shipping"),
   
    
    #  s  path('update_order/<str:pk>',views.Update_Order,name='update_order'),
] 
#+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)