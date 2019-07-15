from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.db import transaction
from df_user.models import *
from df_user import user_decorator
from df_cart.models import *
from df_order.models import *
from datetime import datetime
from decimal import Decimal


# Create your views here.
@user_decorator.login
def order(request):
    user = UserInfo.objects.get(id=request.session['user_id'])
    cart_ids = request.GET.getlist('cart_id')
    cart_ids1 = [int(item) for item in cart_ids]
    carts = CartInfo.objects.filter(id__in=cart_ids1)
    context = {
        'title': '提交订单',
        'carts': carts,
        'user': user,
        'carts_id': ','.join(cart_ids),
        'request': request
    }
    return render(request, 'df_order/place_order.html', context)


@transaction.atomic()
@user_decorator.login
def order_handle(request):
    tran_id = transaction.savepoint()
    cart_ids = request.POST.get('cart_ids')
    total = request.POST.get('total')
    try:
        order = OrderInfo()
        now = datetime.now()
        uid = request.session['user_id']
        order.oid = '%s%d' % (now.strftime('%Y%m%d%H%M%S'), uid)
        order.user_id = uid
        order.odate = now
        order.ototal = Decimal(total)
        order.save()
        # 创建详单对象
        cart_ids1 = [int(item) for item in cart_ids.split(',')]
        print(cart_ids1)
        for id1 in cart_ids1:
            detail = OrderDetailInfo()
            detail.order = order
            # 查询购物车信息
            cart = CartInfo.objects.get(pk=id1)
            goods = cart.goods
            if goods.gkucun >= cart.count:
                goods.gkucun = goods.gkucun - cart.count
                goods.save()
                detail.goods_id = goods.id
                detail.price = goods.gprice
                detail.count = cart.count
                detail.save()
                cart.delete()
            else:
                transaction.savepoint_rollback(tran_id)
                print('库存不足')
                return redirect('/cart/')
    except Exception as e:
        print('=========%s' % e)
        transaction.savepoint_rollback(tran_id)
        return redirect('/cart/')
    return redirect('/user/order/')
    # return JsonResponse({'cart_ids': cart_ids, 'total': total})
