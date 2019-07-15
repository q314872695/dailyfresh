# @Time : 2019/7/10 9:45 

# @Author : xx

# @File : urls.py 

# @Software: PyCharm
from django.urls import path
from .views import *

app_name = 'user'
urlpatterns = [
    path('register/', register, name='register'),
    path('register_handle/', register_handle, name='register_handle'),
    path('login/', login, name='login'),
    path('login_handle/', login_handle, name='login_handle'),
    path('register_exist/', register_exist, name='register_exist'),
    path('info/', info, name='info'),
    path('order/', order, name='order'),
    path('site/', site, name='site'),
    path('logout/', logout, name='logout'),
]
