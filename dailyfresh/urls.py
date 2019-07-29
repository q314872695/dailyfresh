"""dailyfresh URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('df_user.urls', namespace='user')),
    path('tinymce/', include('tinymce.urls')),
    path('', include('df_goods.urls', namespace='goods')),
    path('cart/', include('df_cart.urls', namespace='cart')),
    path('order/', include('df_order.urls', namespace='order')),
    # path('search/', include('haystack.urls')),
]
# 在setting.py中的INSTALLED_APPS 把django.contrib.staticfiles 注释掉后,需要单独配置static的url
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# 部署时把静态文件交给网页服务器处理，故注释掉
