# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views
urlpatterns=[
	#url(r'^$',views.index,name="index"),
	url(r'^login$',views.login,name="login"),# Administration Pages
	url(r'^register$',views.register,name="register"),# Administration Pages
	url(r'^reset$',views.reset,name="reset"),# Administration Pages
	url(r'^rabbithole$',views.after_reg,name="after_reg"),# Administration Pages
	url(r'^userinfo$',views.userinfo,name="userinfo"),# Administration Pages
]