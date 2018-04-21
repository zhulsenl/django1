# coding=utf-8
from django.conf.urls import url
from . import views

urlpatterns=[
    # url('^register$', views.register),

    # url('^register_handle$', views.register_handle),
    url('^register$', views.RegisterView.as_view()),
    url('^user_name$', views.user_name),
    # url('^send_active_mail$', views.send_active_mail),
    url('^active/(.+)$', views.user_active),
    url('^login$', views.LoginView.as_view()),
    url('^logout$', views.user_logout),
    url('^$', views.info),
    url('^order$', views.order),
    # url('^site$', views.site),
    url('^site$', views.SiteView.as_view()),
    url('^area$', views.area),


]