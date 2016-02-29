
from django.conf.urls import include, url
#from django.views.generic import TemplateView
#from django.views.decorators.cache import cache_page

import sixer.views as views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^no1/$', views.index),
    url(r'^products/$', views.products, name='products'),
    url(r'^share/$', views.share, name='share'),
    url(r'^logincb/$', views.login_cb, name='logincb'),
    url(r'^getdiscount/$', views.get_discount, name='getdiscount'),

    url(r'^wechatcb/$', views.wechat_cb, name='wechatcb'),
    url(r'^no2/$', views.index2, name="index2"),
    url(r'^share2/(?P<rid>\w+)/$', views.share2, name='share2'),
    url(r'^inspection/$', views.inspection, name='inspection'),
    url(r'^result/$', views.result, name='result'),
]
