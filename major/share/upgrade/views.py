# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from config.st import gen
from share.lib.basic import get_db,adm

# Create your views here.
# Administration pages ===========
admcls=adm(gen)
# admcls.f_save_request=save_request
# admcls.f_userbar=userbar
# admcls.i_userset_extra=userset_extra
def login(request):
	rtway=admcls.login(request)
	return eval(rtway["w"])(rtway["v"])
def register(request):
	rtway=admcls.register(request)
	return eval(rtway["w"])(rtway["v"])
def reset(request):
	rtway=admcls.reset(request)
	return eval(rtway["w"])(rtway["v"])
def userinfo(request):
	rtway=admcls.userinfo(request)
	return eval(rtway["w"])(rtway["v"])
def after_reg(request):
	rtway=admcls.after_reg(request)
	return eval(rtway["w"])(rtway["v"])
# Administration Pages ===========