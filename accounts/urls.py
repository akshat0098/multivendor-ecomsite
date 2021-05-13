from django.urls import path , include
from . import views 
from django.contrib.auth import views as auth_views
#Writing the urls

urlpatterns = [
    path('Register/',views.register,name='Register'),
    path('accounts/login/',views.Login,name='login'),
    path('Register_vendor/',views.register_vendor,name='register_vendor'),
    path('accounts/vendor_dashboard',views.vendor_dashboard,name='vendor_dashboard'),
    
    path('logout/',views.logoutUser,name='logout'),

    path('token' , views.token_send , name="token_send"),
    path('success' , views.success , name='success'),
    path('verify/<auth_token>' , views.verify , name="verify"),
    path('error' , views.error_page , name="error"),
    
    #path('accounts/', include('django.contrib.auth.urls')),
    path('reset_password/',
     auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),
     name="reset_password"),

    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"), 
        name="password_reset_done"),
    
    path('reset/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"), 
     name="password_reset_confirm"),

    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"), 
        name="password_reset_complete"),

]
   