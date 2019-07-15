# @Time : 2019/7/10 9:45 

# @Author : xx

# @File : urls.py 

# @Software: PyCharm
from django.urls import path
from .views import *

app_name = 'cart'
urlpatterns = [
    path('', cart, name='cart'),
    path('add<int:gid>_<int:count>/', add, name='add'),
    path('edit<int:cart_id>_<int:count>/', edit, name='edit'),
    path('delete<int:cart_id>/', delete, name='delete'),
]
