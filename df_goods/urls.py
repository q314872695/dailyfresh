# @Time : 2019/7/10 9:45 

# @Author : xx

# @File : urls.py 

# @Software: PyCharm
from django.conf.urls import url
from django.urls import path,re_path
from .views import *

app_name = 'goods'
urlpatterns = [
    path('', index, name='index'),
    path('list_<int:t_id>_<int:p_index>_<int:sort>/', list, name='list'),
    path('<int:id>/', detail, name='detail'),
    path('search/', MySearchView.as_view(), name='haystack_search'),
]
