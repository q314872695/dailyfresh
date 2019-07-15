# @Time : 2019/7/15 8:10 

# @Author : xx

# @File : search_indexes.py 

# @Software: PyCharm
from haystack import indexes
from .models import GoodsInfo


class GoodsInfoIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return GoodsInfo

    def index_queryset(self, using=None):
        return self.get_model().objects.all()