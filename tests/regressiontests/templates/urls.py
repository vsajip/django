# coding: utf-8
from __future__ import absolute_import, unicode_literals

from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns('',

    # Test urls for testing reverse lookups
    (r'^$', views.index),
    (r'^client/([\d,]+)/$', views.client),
    (r'^client/(?P<id>\d+)/(?P<action>[^/]+)/$', views.client_action),
    (r'^client/(?P<client_id>\d+)/(?P<action>[^/]+)/$', views.client_action),
    url(r'^named-client/(\d+)/$', views.client2, name="named.client"),

    # Unicode strings are permitted everywhere.
    url('^\u042e\u043d\u0438\u043a\u043e\u0434/(\w+)/$', views.client2, name="\u043c\u0435\u0442\u043a\u0430_\u043e\u043f\u0435\u0440\u0430\u0442\u043e\u0440\u0430"),
    url('^\u042e\u043d\u0438\u043a\u043e\u0434/(?P<tag>\S+)/$', 'regressiontests.templates.views.client2', name="\u043c\u0435\u0442\u043a\u0430_\u043e\u043f\u0435\u0440\u0430\u0442\u043e\u0440\u0430_2"),
)
