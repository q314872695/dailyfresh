from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import *
from df_goods.models import *
from hashlib import sha1
from . import user_decorator
from df_order.models import *
from django.core.paginator import Paginator


# Create your views here.


def register(request):
    return render(request, 'df_user/register.html', {'title': '注册'})


def register_handle(request):
    # 接受用户输入
    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('pwd')
    upwd2 = post.get('cpwd')
    uemail = post.get('email')
    # 判断两次密码
    if upwd != upwd2:
        return redirect('/user/register/')
    # 密码加密
    s1 = sha1()
    s1.update(upwd.encode('utf-8'))
    upwd3 = s1.hexdigest()
    # 创建对象
    user = UserInfo()
    user.uname = uname
    user.upwd = upwd3
    user.uemail = uemail
    user.save()
    # 注册成功，转到登录页
    return redirect('/user/login/')


def register_exist(request):
    """
    ajsx注册时判断用户名是否存在
    :param request:
    :return: 不存在则返回{"count": 0}，存在返回{"count": 1}
    """
    name = request.GET.get('uname', '')
    count = UserInfo.objects.filter(uname=name).count()
    return JsonResponse({'count': count})


def login(request):
    uname = request.COOKIES.get('uname', '')
    context = {
        'title': '用户登录',
        'error_name': 0,
        'error_pwd': 0,
        'uname': uname
    }
    return render(request, 'df_user/login.html', context)


def login_handle(request):
    post = request.POST
    uname = post.get('username')
    upwd = post.get('pwd')
    # 0表示没有记住用户名，1表示记住用户名
    remember_name = post.get('check', 0)
    # 对接受的密码就行加密
    s1 = sha1()
    s1.update(upwd.encode('utf-8'))
    upwd1 = s1.hexdigest()
    # 验证密码与数据库中的密码是否一致
    user = UserInfo.objects.filter(uname=uname)
    # print(user)
    if len(user) == 1:
        # 该用户存在
        if upwd1 == user[0].upwd:
            # 密码正确
            url = request.COOKIES.get('url', '/')
            red = redirect(url)
            if remember_name == '1':
                red.set_cookie('uname', uname)
                # print('cook')
            else:
                red.set_cookie('uname', '', max_age=-1)

                # print('no_cook')
            request.session['user_id'] = user[0].id
            request.session['user_name'] = uname
            print(red)
            print(request)
            return red
        else:
            # 密码错误
            context = {
                'title': '用户登录',
                'error_name': 0,
                'error_pwd': 1,
                'uname': uname,
                'upwd': upwd
            }
            return render(request, 'df_user/login.html', context)
    else:
        # 该用户不存在
        context = {
            'title': '用户登录',
            'error_name': 1,
            'error_pwd': 0,
            'uname': uname,
            'upwd': upwd
        }
        return render(request, 'df_user/login.html', context)


def logout(request):
    request.session.flush()
    return redirect('/')


@user_decorator.login
def info(request):
    user = UserInfo.objects.get(pk=request.session['user_id'])

    goods_ids = request.COOKIES.get('goods_ids', '')
    goods_ids1 = goods_ids.split(',')
    goods_list = []
    # print(goods_ids)
    # print(goods_ids1)
    # print(len(goods_ids1))
    if len(goods_ids1) > 1:
        for goods_id in goods_ids1:
            # print(type(goods_id))
            goods_list.append(GoodsInfo.objects.get(pk=int(goods_id)))

    context = {
        'title': '用户中心',
        'user': user,
        'goods_list': goods_list,
        'request': request
    }
    return render(request, 'df_user/user_center_info.html', context)


@user_decorator.login
def order(request):
    index = request.GET.get('page', '1')
    order1 = OrderInfo.objects.filter(user_id=request.session['user_id'])
    paginator = Paginator(order1, 2)
    page = paginator.page(int(index))
    context = {
        'title': '用户中心',
        'reuqest': request,
        'page': page,
        'paginator': paginator
    }

    return render(request, 'df_user/user_center_order.html', context)


@user_decorator.login
def site(request):
    user = UserInfo.objects.get(pk=request.session['user_id'])
    if request.method == 'POST':
        post = request.POST
        user.ushou = post.get('ushou')
        user.uaddress = post.get('uaddress')
        user.uyoubian = post.get('uyoubian')
        user.uphone = post.get('uphone')
        user.save()
    context = {
        'title': '用户中心',
        'user': user,
        'request': request
    }
    return render(request, 'df_user/user_center_site.html', context)
