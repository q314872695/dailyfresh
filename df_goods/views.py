from django.shortcuts import render
from .models import *
from django.core.paginator import Paginator
from df_cart.models import *
from haystack.generic_views import SearchView


# Create your views here.
def index(request):
    # 查询各分类的4条最新4条最热数据
    typelist = TypeInfo.objects.all()
    if len(typelist) != 0:
        type0 = typelist[0].goodsinfo_set.order_by('-id')[0:4]
        type1 = typelist[1].goodsinfo_set.order_by('-id')[0:4]
        type2 = typelist[2].goodsinfo_set.order_by('-id')[0:4]
        type3 = typelist[3].goodsinfo_set.order_by('-id')[0:4]
        type4 = typelist[4].goodsinfo_set.order_by('-id')[0:4]
        type5 = typelist[5].goodsinfo_set.order_by('-id')[0:4]
        type01 = typelist[0].goodsinfo_set.order_by('-gclick')[0:4]
        type11 = typelist[1].goodsinfo_set.order_by('-gclick')[0:4]
        type21 = typelist[2].goodsinfo_set.order_by('-gclick')[0:4]
        type31 = typelist[3].goodsinfo_set.order_by('-gclick')[0:4]
        type41 = typelist[4].goodsinfo_set.order_by('-gclick')[0:4]
        type51 = typelist[5].goodsinfo_set.order_by('-gclick')[0:4]
    else:
        type0 = []
        type1 = []
        type2 = []
        type3 = []
        type4 = []
        type5 = []
        type01 = []
        type11 = []
        type21 = []
        type31 = []
        type41 = []
        type51 = []
    count = CartInfo.objects.filter(user_id=request.session.get('user_id', 0)).count()
    # print(count)
    context = {
        'title': '首页',
        'type0': type0,
        'type1': type1,
        'type2': type2,
        'type3': type3,
        'type4': type4,
        'type5': type5,
        'type01': type01,
        'type11': type11,
        'type21': type21,
        'type31': type31,
        'type41': type41,
        'type51': type51,
        'request': request,
        'count': count
    }
    return render(request, 'df_goods/index.html', context)


def list(request, t_id, p_index, sort):
    typeinfo = TypeInfo.objects.get(pk=t_id)
    news = typeinfo.goodsinfo_set.order_by('-id')[0:2]
    count = CartInfo.objects.filter(user_id=request.session.get('user_id', 0)).count()
    goods_list = []
    if sort == 1:
        # 默认 最新
        goods_list = GoodsInfo.objects.filter(gtype_id=t_id).order_by('-id')
    elif sort == 2:
        # 价格
        goods_list = GoodsInfo.objects.filter(gtype_id=t_id).order_by('-gprice')
    elif sort == 3:
        # 人气 点击量
        goods_list = GoodsInfo.objects.filter(gtype_id=t_id).order_by('-gclick')
    paginator = Paginator(goods_list, 10)
    page = paginator.page(p_index)
    context = {
        'title': '商品列表',
        'page': page,
        'paginator': paginator,
        'typeinfo': typeinfo,
        'sort': sort,
        'news': news,
        'name': typeinfo.ttitle,
        'request': request,
        'count': count
    }
    return render(request, 'df_goods/list.html', context)


def detail(request, id):
    goods = GoodsInfo.objects.get(pk=id)
    goods.gclick = goods.gclick + 1
    goods.save()
    news = goods.gtype.goodsinfo_set.order_by('-id')[0:2]
    count = CartInfo.objects.filter(user_id=request.session.get('user_id', 0)).count()
    context = {
        'title': '商品详情',
        'g': goods,
        'news': news,
        'id': id,
        'name': goods.gtype.ttitle,
        'request': request,
        'count': count
    }
    goods_ids = request.COOKIES.get('goods_ids', '')
    goods_id = str(goods.id)
    if goods_ids != '':
        # 有浏览记录
        goods_ids1 = goods_ids.split(',')
        if goods_ids1.count(goods_id) >= 1:
            goods_ids1.remove(goods_id)
        goods_ids1.insert(0, goods_id)
        if len(goods_ids1) >= 6:
            del goods_ids1[5]
        goods_ids = ','.join(goods_ids1)
    else:
        goods_ids = goods_id
    response = render(request, 'df_goods/detail.html', context)
    response.set_cookie('goods_ids', goods_ids)
    return response


class MySearchView(SearchView):
    #    自定义视图搜不出结果
    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        count = CartInfo.objects.filter(user_id=self.request.session.get('user_id', 0)).count()
        news = GoodsInfo.objects.all().order_by('-id')[0:2]
        context['title'] = '搜索'
        context['name'] = '搜索'
        context['request'] = self.request
        context['count'] = count
        context['news'] = news
        # print(context)
        return context
