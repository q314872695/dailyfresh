from django.shortcuts import render, redirect
from django.http import JsonResponse
from df_user import user_decorator
from .models import *


# Create your views here.
@user_decorator.login
def cart(request):
    uid = request.session['user_id']
    carts = CartInfo.objects.filter(user_id=uid)
    context = {
        'title': '购物车',
        'page_name': 1,
        'carts': carts,
        'request': request
    }
    return render(request, 'df_cart/cart.html', context)


@user_decorator.login
def add(request, gid, count):
    """
    :param request:
    :param gid: 购买商品的id
    :param count: 购买商品的数量
    :return:如果是ajax则返回json,否则转向购物车
    """
    uid = request.session['user_id']
    carts = CartInfo.objects.filter(user_id=uid, goods_id=gid)
    if len(carts) > 0:
        cart = carts[0]
        cart.count = cart.count + count
    else:
        cart = CartInfo()
        cart.user_id = uid
        cart.goods_id = gid
        cart.count = count
    cart.save()
    # 如果是ajax则返回json,否则转向购物车
    if request.is_ajax():
        count = CartInfo.objects.filter(user_id=uid).count()
        return JsonResponse({'count': count})
    else:
        return redirect('/cart')


@user_decorator.login
def edit(request, cart_id, count):
    try:
        cart = CartInfo.objects.get(pk=cart_id)
        cart.count = count
        cart.save()
        data = {'ok': 0}
    except Exception:
        data = {'ok': count}
    return JsonResponse(data)


@user_decorator.login
def delete(request, cart_id):
    try:
        cart = CartInfo.objects.get(pk=cart_id)
        cart.delete()
        data = {'ok': 1}
    except Exception:
        data = {'ok': 0}
    return JsonResponse(data)
