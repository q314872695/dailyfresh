# @Time : 2019/7/12 9:30 

# @Author : xx

# @File : user_decorator.py 

# @Software: PyCharm
from django.http import HttpResponseRedirect


# 如果未登录，则跳转到登录界面
def login(func):
    def login_func(request, *args, **kwargs):
        if request.session.has_key('user_id'):
            return func(request, *args, **kwargs)
        else:
            red = HttpResponseRedirect('/user/login/')
            red.set_cookie('url', request.get_full_path())
            return red
    return login_func


"""
http://127.0.0.1:8080/200/?type=10
reuqest.path 表示当前路径 /200/
request.get_full_path() 表示完整路径 /200/?type=10

"""
