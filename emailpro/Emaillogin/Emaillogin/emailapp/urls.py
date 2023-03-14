from django.contrib import admin
from django.urls import path
from emailapp.views import Registration,user_login,get_data,Update_data,Update_data_patch,Delete_data,activate,logout_user,Reset_password,Forget_password
# from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    
    path('registration/',Registration),
    # path('registration/', obtain_auth_token),
    path('login/',user_login),
    # path('login/', obtain_auth_token),
    path('get_data/<int:uid>/',get_data),
    path('get_data/',get_data),
    path("Update_data/<int:uid>/",Update_data),
    path("Update_data_patch/<int:uid>/",Update_data_patch),
    path('Delete_data/<uid>/',Delete_data),
    path('activate/<token>/', activate),
    path("reset_password/",Reset_password),
    path('logout/',logout_user),
    path('forget_password/<token>/',Forget_password), 
]
    