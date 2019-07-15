# @Time : 2019/7/10 9:45 

# @Author : xx

# @File : urls.py 

# @Software: PyCharm
from django.urls import path
from .views import *

app_name = 'order'
urlpatterns = [
    path('', order, name='order'),
    path('order_handle/', order_handle, name='order_handle'),
]
