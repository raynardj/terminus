# -*- coding: utf-8 -*-
#hr stand for HttpResponse
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from django.core.files.uploadedfile import TemporaryUploadedFile as tu
from django.shortcuts import redirect
from pymongo import MongoClient
from pymongo import ASCENDING
from pymongo import DESCENDING
from bson.objectid import ObjectId
from math import ceil
import datetime
from datetime import timedelta
import json
from time import time as timestamp
#forms
from .forms import email_login
from .forms import userset_extra
from .forms import clientset
from .forms import tagform
from .forms import cssadv_list
from .forms import uploadset
from .forms import upload_input
from .forms import upload_hidden
from .forms import fm_officeuse
from .forms import fm_officeuse_proid
from .forms import office_use_detail
from .forms import page_selector_form
from .forms import download_range
from .forms import loadback
from .forms import groupinfo_form
from .forms import transparent_set
from .forms import process_status
from .forms import cssupload
from .forms import ar_upload,od_upload
from django.forms import IntegerField
from django.forms.widgets import HiddenInput
# Import from the custom made libarary :lib.py
from  share.lib.basic import get_db,adm,mid_str,getdict
from lib import save_request
#from lib import get_db
from lib import index_load
from lib import wall_print
from lib import mystrify
from lib import linklist
from lib import process_main #Load the process main page
from lib import userbar
from lib import group_set
from lib import testlog
from lib import testcnname
from lib import process_detail_show
from lib import linkbtn
from lib import rich_sheet
from lib import usejs
from lib import parse_stb_url # A function to parse staples url
from lib import usertrace #a class to generate user trace dict
from lib import MongoOut
from lib import user_auth
from lib import table_book
from lib import auth_review_line
from lib import auth_sf_line
from lib import utc8
from lib import edit_process
from lib import date_parse
from lib import xlwt_officeuse
from lib import edit_process_officeuse
from lib import refresh_group_bound
from lib import get_tiers
from lib import read_sys
from lib import listsum
from lib import strid
from lib import listdate
from lib import testsu
from lib import boundrefresh
from lib import _advcss_user,_advcss_user_r,seenan
from lib import overdue_line
from lib import match_cplist,match_cplist_uc
from collections import OrderedDict
from urllib import urlencode
from django.core.mail import send_mail
from xlrd import open_workbook
import pandas as pd
import numpy as np
from config.st import gen
from timeit import timeit
import pickle
from sqlalchemy import create_engine as ce
import sqlalchemy
# Create your views here. 
#global Variables
num20=list(str(v+1) for v in range(20))
a2z=["a","b","c","d","e","f","g","h","i","j","k"]
stage_symbol=["dead","0"]
brand_keys=["staples","brighton","arc",u"史泰博"]
emailkw="@staples."
pct=range(101)
#set up the brand keywords
def index(request):
	"""
	Index Page View:
	"""
	save_request(request)
	tl=testlog(request)
	if tl==True:
		tc=testcnname(request)
		if tc!=True:
			return redirect("/userinfo")
		hr=index_load(request)
	else:
		return redirect(tl)
	return HttpResponse(hr)
def index_aj(request):
	"""
	Index Page Ajax:
	"""
	save_request(request)
	tl=testlog(request)
	db=get_db("foundation")
	if tl==True:
		tc=testcnname(request)
		if tc!=True:
			return redirect("/userinfo")
		if request.method=="POST":
			post_dict=dict(request.POST)
			if post_dict.has_key("md"):
				if post_dict["md"][0]=="wall":
					# shrink the dict
					aj_dict=dict((k,post_dict[k][0]) for k in ["wallowner","writes"] if post_dict.has_key(k))
					aj_dict.update({
						"time":utc8(),
						"fromcn":request.session["cnname"],
						"from":request.session["mail"],
						})
					db.wall.insert(aj_dict)
		elif request.method=="GET":
			get_dict=dict(request.GET)
			if get_dict.has_key("md"):
				if get_dict["md"][0]=="wallin":
					#write the wall
					aj_dict=dict((k,get_dict[k][0]) for k in ["wallowner","to","writes","replyto","replytocn","tobrick"] if get_dict.has_key(k))
					if aj_dict.has_key("to"):
						try:
							aj_dict["tocn"]=dict(db.staff.find_one({"mail":aj_dict["to"]},{"_id":0,"cnname":1}))["cnname"]
						except:
							pass
					aj_dict.update({
						"time":utc8(),
						"fromcn":request.session["cnname"],
						"from":request.session["mail"],
						})
					db.wall.insert(aj_dict)
					wallrows=db.wall.find({"wallowner":aj_dict["wallowner"]}).sort("time",DESCENDING).limit(20).skip(0)
					rt=''
					selfmail=request.session["mail"]
					for brick in wallrows:
						if brick['wallowner']==selfmail:
							brick['remove_brick']=True
						elif brick['from']==selfmail:
							brick['remove_brick']=True
						else:
							pass
						rt=rt+str(wall_print(request,dict(brick)))
					return HttpResponse(rt)
					#rt=rt+"<script>$(document).ready(function(){remove_brick();})</script>"
				elif get_dict["md"][0]=="wall":
					#show the entire wall
					aj_dict=dict((k,get_dict[k][0]) for k in ["wallowner","skippages"] if get_dict.has_key(k))
					if aj_dict.has_key("skippages"):
						pass
					else:
						aj_dict["skippages"]=0
					wallrows=db.wall.find({"wallowner":aj_dict["wallowner"]}).sort("time",DESCENDING).limit(20).skip(20*int(aj_dict["skippages"]))
					rt=''
					selfmail=request.session["mail"]
					for brick in wallrows:
						if brick['wallowner']==selfmail:
							brick['remove_brick']=True
						elif brick['from']==selfmail:
							brick['remove_brick']=True
						else:
							pass
						rt=rt+str(wall_print(request,dict(brick)))
					#rt=rt+"<script>$(document).ready(function(){remove_brick();})</script>"
					return HttpResponse(rt)
				elif get_dict["md"][0]=='remove_brick':
					# Brick remove btn ajax
					bid=get_dict['bid'][0]
					db=get_db("foundation")
					try:
						brick_doc=dict(db.wall.find_one({"_id":ObjectId(bid)},{"_id":0,"from":1,"wallowner":2}))
						if request.session['mail']==brick_doc['from'] or request.session["mail"]==brick_doc['wallowner']:
							db.wall.remove({"_id":ObjectId(bid)})
							return HttpResponse("brick_removed")
						else:
							return HttpResponse("No_auth_to_delete")
					except:
						return HttpResponse("CannotDelete")

	else:
		return redirect(tl)
def worldsync(request):
	"""
	Sync the different databases
	"""
	save_request(request)
	tl=testlog(request)
	if tl==True:
		tc=testcnname(request)
		if tc!=True:
			return redirect("/userinfo")
		userb=userbar(request)
		template=loader.get_template('w.html')
		temps=[]
		context=dict()
		context.update({
			"userb":userb,
			"title":u"数据库同步",
			"temps":temps,#alist of subtemplates
			})
		hr=template.render(context,request)
	else:
		return redirect(tl)
	return HttpResponse(hr)
def termap(request):
	"""
	Map of Terminus:
	Used as a page or a menu
	"""
	save_request(request)
	tl=testlog(request)
	if tl==True:
		tc=testcnname(request)
		if tc!=True:
			return redirect("/userinfo")
		userb=userbar(request)
		template=loader.get_template('termap.html')
		context=dict()
		context.update({
			"userb":userb,
			})
		hr=template.render(context,request)
	else:
		return redirect(tl)
	return HttpResponse(hr)
# Administration pages ===========
admcls=adm(gen)
admcls.f_save_request=save_request
admcls.f_userbar=userbar
admcls.i_userset_extra=userset_extra
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

def clients(request,cid):
	tl=testlog(request)
	if tl==True:
		tc=testcnname(request)
		if tc!=True:
			return redirect("/userinfo")
		userb=userbar(request)
		db=get_db("foundation")
		if request.method=="POST":
			try:
				if request.session["onboard"]==True:
					form=clientset(request.POST)
					if form.is_valid():
						db.clients.update(
							{"client":cid},
							{"$set":form.cleaned_data},
							upsert=True,
							)
					else:
						msg_return=u"输入信息有误"
				else:
					return HttpResponseRedirect("login")
			except:
				return HttpResponseRedirect("login")
		else:
			pass
		template=loader.get_template("form_set.html")
		context=dict()
		try:
			clidict=db.clients.find_one({"client":int(cid)})
			form=clientset(clidict)
			context.update({
			"form":form,
			"userb":userb,
			"act":"clients/"+cid,
			"act_cn":u"客户",
			})
		except KeyError:
			context={}
		hr=template.render(context,request)
	else:
		return redirect(tl)
	return HttpResponse(hr)
def reg(request):
	template=loader.get_template('reg.html')
	if request.method=="POST":
		form=user_reg(request.Post)
		if form.is_valid():
			return HttpResponseRedirect("reged")
	else:
		form=user_reg()
	context={
		"form":form,
		}
	return HttpResponse(template.render(context,request))
def objid(client_colle,qsid):
	clientobj=client_colle.find_one({"_id":ObjectId(qsid)})
	return clientobj

def search_suggest(request):
	tl=testlog(request)
	if tl==True:
		tc=testcnname(request)
		if tc!=True:
			return redirect("/userinfo")
		if request.method=="GET":
			get_dict=dict(request.GET)
			if get_dict.has_key("task"):
				if get_dict["task"][0]=="topersonpage":
					kw=get_dict["kw"][0]
					db=get_db("foundation")
					matchlist=list(db.staff.find({"$or":[
						{"mail":{"$regex":"%s"%(kw)}},
						{"cnname":{"$regex":"%s"%(kw)}},
						],
						"groupname":{"$exists":False},#Not a group
						},{"cnname":1,"enname":2}).limit(7)
						)
					if len(matchlist)>0:
						rt=''
						for candidate in matchlist:
							candidate["id"]=candidate["_id"].__str__()
							rt=rt+str(loader.get_template("parts/search_suggest_line.html").render(candidate))
						return HttpResponse(rt)
					else:
						return HttpResponse(u"未找到相关人员")
				if get_dict["task"][0]=="group":
					db=get_db("foundation")
					kw=get_dict["kw"][0]
					groupname=get_dict["groupname"][0]
					user_au=user_auth(request.session["mail"])
					if user_au.isLeader(groupname):
						staff_list=list(db.staff.find({
							"$or":[
							{"mail":{"$regex":"%s"%(kw)}},
							{"cnname":{"$regex":"%s"%(kw)}},
							{"groupname":{"$regex":"%s"%(kw)}},
							]
							},{"cnname":1,"groupname":3,"mail":2,"enname":4}).limit(5))
						rt=''
						temp_ss=loader.get_template("parts/groupsee_search_suggest.html")
						addtype=get_dict["addtype"][0]
						remake=list()
						for staff in staff_list:
							staff=dict(staff)
							if (addtype=="leader" and staff.has_key("groupname")):
								pass
								# Group leaders do not have bound group function
							elif (staff.has_key("groupname") and addtype=="member"):
								if staff["groupname"]!=groupname:
									staff.update({
										"boundgroup":staff["groupname"],
										"addtype":"boundgroup",})
									staff.update({"groupname":groupname})
									remake.append(staff)
								else:
									pass
							else:
								staff.update({"groupname":groupname})
								staff.update({"addtype":addtype})
								remake.append(staff)
						con_ss=dict({"staffs":remake})
						return HttpResponse(temp_ss.render(con_ss,request))
					else:
						return HttpResponse("No group management authority")
				elif get_dict["task"][0]=="group_add":
					add_staff=dict((k,get_dict[k][0]) for k in ["addtype","groupname","mail","boundgroup"] if get_dict.has_key(k))
					user_au=user_auth(request.session["mail"])
					if add_staff["addtype"]=="boundgroup": 
						pushin=add_staff["boundgroup"]
					else:
						pushin=add_staff["mail"]
					# Check if the user is the groupleader
					if user_au.isLeader(add_staff["groupname"]):
						db=get_db("foundation")
						# Check if the user is already in the category
						if db.staff.count({"groupname":add_staff["groupname"],add_staff["addtype"]:pushin})>0:
							rtstr="already"
						else:

							# push in the update
							db.staff.update({
								"groupname":add_staff["groupname"],
								},
								{"$push":{add_staff["addtype"]:pushin}},
								upsert=True,
								)
							if add_staff["addtype"]=="boundgroup": 
								if add_staff["boundgroup"]!=add_staff["groupname"]:
									staff_cnname=dict(db.staff.find_one({"groupname":add_staff["boundgroup"]},{"cnname":1,"_id":0}))["cnname"]
									rtstr="<tr><td class='groupsee_name'>%s</td><td class='refresh_group_list' data-groupname='%s' data-boundgroup='%s' data-md='refreshbg'>导入团队成员</td><td class='groupsee_action_td group_remove_click' data-groupname='%s' data-addtype='%s' data-mail='%s'>移出</td></tr>"%(
										staff_cnname,
										add_staff["groupname"],
										add_staff["boundgroup"],
										add_staff["groupname"],
										add_staff["addtype"],
										add_staff["boundgroup"])
								else:
									rtstr="already"
							else:
								staff_cnname=dict(db.staff.find_one({"mail":add_staff["mail"]},{"cnname":1,"_id":0}))["cnname"]
								rtstr="<tr><td class='groupsee_name'>%s</td><td>%s</td><td class='groupsee_action_td group_remove_click' data-groupname='%s' data-addtype='%s' data-mail='%s'>移出</td></tr>"%(staff_cnname,add_staff["mail"],add_staff["groupname"],add_staff["addtype"],add_staff["mail"])
					return HttpResponse(rtstr)
				elif get_dict["task"][0]=="group_remove":
					remove_staff=dict((k,get_dict[k][0]) for k in ["addtype","groupname","mail"] if get_dict.has_key(k))
					user_au=user_auth(request.session["mail"])
					if user_au.isLeader(remove_staff["groupname"]):
						db=get_db("foundation")
						db.staff.update({
							"groupname":remove_staff["groupname"],
							},
							{"$pull":{remove_staff["addtype"]:remove_staff["mail"]}},
							upsert=True,
							)
					return HttpResponse("yes")
			else:
				return HttpResponse("wrong task")
		else:
			return HttpResponse("wrong method")
	else:
		return redirect(tl)
def group(request):
	tl=testlog(request)
	if tl==True:
		tc=testcnname(request)
		if tc!=True:
			return redirect("/userinfo")
		db=get_db("foundation")
		template=loader.get_template("a.html")
		temp_group=loader.get_template("parts/group.html")
		con_group=dict({})
		bodies=OrderedDict()
		groups=list(db.staff.find(
			{"$or":[{"member":request.session["mail"]},{"leader":request.session["mail"]}]}
			,{"_id":0,"groupname":1,"cnname":2}))
		#groups2=list(db.staff.find({"member":"all"},{"_id":0,"groupname":1,"cnname":2}))
		#groups=groups+groups2
		if len(groups)==0:
			pass
		else:
			for group in groups:
				group=dict(group)
		con_group.update({"groups":groups})
		if request.method=="GET":
			get_dict=dict(request.GET)
			if get_dict.has_key("groupsee"):
				# if groupsee is set in the initial query string, get it's groupsee automatically
				backjs=get_dict["groupsee"][0]
				con_group.update({"backjs":backjs})
		bodies.update({"c1":temp_group.render(con_group)})
		context=dict({
			"userb":userbar(request),
			"title":u"我的团体",
			"bodies":bodies,
			})
		return HttpResponse(template.render(context,request))
	else:
		return redirect(tl)
#	save_request(request)
#	tl=testlog(request)
#	template=loader.get_template("msg.html")
#	if tl==True:
#		userb=userbar(request)
#		newgbtn=linkbtn(u"新建群组",'groupn')
#		msgbody=''
#		grpbound={}
#		try:
#			grpname=request.GET["groupname"]
#			grpbound.update({"grp":grpname})
#			grpset=group_set({"grp":grpname})
#			msgbody+=grpset.as_table()
#			msgbody+=grpset.members()
#			context={
#			"msg_title":grpname+u"群组设置",
#			"msg_head":u"群组设置",
#			}
#		except(NameError,SyntaxError,IndexError,KeyError,IOError,AttributeError,ValueError),errmsg:
#			context={
#			"msg_title":u"群组设置",
#			"msg_head":u"请选择群组：",
#			"msg_body":errmsg,
#			}
#		context.update(
#			{
#			"userb":userb,
#			"msg_links":newgbtn.tohtml(),
#			"msg_body":msgbody,
#			}
#			)
#		return HttpResponse(template.render(context,request))
#	else:
#		return tl
def groupinfo(request):
	tl=testlog(request)
	if tl==True:
		tc=testcnname(request)
		if tc!=True:
			return redirect("/userinfo")
		temp_groupinfo=loader.get_template("a.html")
		con_gi=dict()
		bodies=OrderedDict()
		temp_groupinfo_ctt=loader.get_template("parts/groupinfo.html")
		if request.method=="GET":
			get_dict=dict(request.GET)
			if get_dict.has_key("groupname"):
				# existed group
				groupname=str(get_dict["groupname"][0]).lower()
				db=get_db("foundation")
				try:
					group_doc=dict(db.staff.find_one({"groupname":groupname},{"groupname":1,"cnname":2}))
					group_doc["groupid"]=group_doc["_id"].__str__()
					groupid=group_doc["groupid"]
					if db.staff.count({"_id":ObjectId(groupid),"$or":[{"leader":request.session["mail"]},{"member":request.session["mail"]}]})==0:
						return redirect("/groupinfo?backmsg=您没有查看该团队设置的权限,尝试新建自己的团队")
					gi_form=groupinfo_form(group_doc)
					gi_form.fields["groupname"].widget=HiddenInput()
				except:
					return redirect("/groupinfo?backmsg=没有该团队设置,尝试新建自己的团队")
			else:
				# new group
				# an empety form
				gi_form=groupinfo_form()
				del gi_form.fields["groupid"]
			if get_dict.has_key("backmsg"):
				con_gi.update({"backmsg":get_dict["backmsg"][0]})
		elif request.method=="POST":
			post_dict=dict(request.POST)
			if post_dict.has_key("groupid"):
			# Existed group
				groupid=post_dict["groupid"][0]
				# Process the  groupname, change to lower case and use the lower case
				groupname=str(post_dict["groupname"][0]).lower()
				# Letters and numerics only
				lnn=[chr(i) for i in range(97,123)]+range(10)
				db=get_db("foundation")
				groupname=''.join(list(letter for letter in groupname if letter in lnn))
				try:
					groupname_ori=db.staff.find_one({"_id":ObjectId(groupid)},{"_id":0,"groupname":1})["groupname"]
				except:
					groupname_ori=groupname
				cnname=post_dict["cnname"][0]
				if (len(groupname)<2 or len(cnname)<2):
					return redirect("/groupinfo?groupname="+str(groupname_ori)+"&backmsg=输入有效中文名/英文名")
				if int(db.staff.count({"_id":ObjectId(groupid),"leader":request.session["mail"]}))==0:
					return redirect("/groupinfo?groupname="+str(groupname_ori)+"&backmsg=只有团队的管理员可以修改团队的信息")
				if int(db.staff.count({"$or":[{"groupname":groupname},{"cnname":cnname}],"_id":{"$ne":ObjectId(groupid)}}))>0:
					return redirect("/groupinfo?groupname="+str(groupname_ori)+"&backmsg=中文名或英文名已被其他团队占用")
				else:
					db.staff.update({"_id":ObjectId(groupid)},{"$set":{"groupname":groupname,"cnname":cnname}})
					gi_form=groupinfo_form({"groupname":groupname,"cnname":cnname,"groupid":groupid})
					gi_form.fields["groupname"].widget=HiddenInput()
					return redirect("/group?groupsee="+str(groupname))
			else:
			# New group
				groupname=str(post_dict["groupname"][0]).lower()
				# Letters and numerics only
				lnn=[chr(i) for i in range(97,123)]+range(10)
				db=get_db("foundation")
				groupname=''.join(list(letter for letter in groupname if letter in lnn))
				cnname=post_dict["cnname"][0]
				if (len(groupname)<2 or len(cnname)<2):
					return redirect("/groupinfo?groupname="+str(groupname_ori)+"&backmsg=输入有效中文名/英文名")
				# Check name duplicate
				if int(db.staff.count({"$or":[{"groupname":groupname},{"cnname":cnname}]}))>0:
					return redirect("/groupinfo?backmsg=中文名或英文名已被其他团队占用")
				else:
					db.staff.insert({"groupname":groupname,"cnname":cnname,"leader":[request.session["mail"]],"member":[request.session["mail"]]})
					return redirect("/group?groupsee="+str(groupname))
		else:
			gi_form=groupinfo_form()
			del gi_form.fields["groupid"]
		con_gi2=dict({"gi_form":gi_form})
		bodies.update({"c2":temp_groupinfo_ctt.render(con_gi2,request)})
		con_gi.update({
			"userb":userbar(request),
			"bodies":bodies,
			})
		return HttpResponse(temp_groupinfo.render(con_gi,request))
	else:
		return redirect(tl)
def group_aj(request):
	tl=testlog(request)
	if tl==True:
		tc=testcnname(request)
		if tc!=True:
			return redirect("/userinfo")
		if request.method=="GET":
			get_dict=dict(request.GET)
			if get_dict.has_key("md"):
				db=get_db("foundation")
				if get_dict["md"][0]=="groupchat":
					groupname=get_dict["groupname"][0]
					member_c=int(db.staff.count({"groupname":groupname,"member":request.session["mail"]}))
					leader_c=int(db.staff.count({"groupname":groupname,"leader":request.session["mail"]}))
					all_c=int(db.staff.count({"groupname":groupname,"member":"all"}))
					if member_c+leader_c+all_c>0:
						group_cnname=dict(db.staff.find_one({"groupname":groupname},{"_id":0,"cnname":1}))["cnname"]
						temp_groupchat=loader.get_template("parts/group_chat.html")
						# Render the initial chat area
						con_gchat=dict({
							"groupname":groupname,# group name
							"group_cnname":group_cnname, #group description
							"initial_time":str(timestamp()),
							})
						return HttpResponse(temp_groupchat.render(con_gchat,request))
					else:
						return HttpResponse(u"没有参加%s群聊的权限"%(groupname))
				elif get_dict["md"][0]=="groupsee":
					# Print out the group leader list & member list
					user_au=user_auth(request.session["mail"])
					groupname=get_dict["groupname"][0]
					#Check if the user is a member or a leader of the group
					asgroup_m=user_au.isGroup(groupname)
					asgroup_l=user_au.isLeader(groupname)
					#if (asgroup_m|asgroup_l):
					if (1==1):
						group_doc=dict(db.staff.find_one({"groupname":groupname}))
						if group_doc.has_key("member"):
							memberlist=list(group_doc["member"])
							member_detail_list=list(db.staff.find({
								"mail":{"$in":memberlist}
								},
								{"cnname":1,"mail":2},
								))
							if group_doc.has_key("boundgroup"):
								bgrouplist=list(group_doc["boundgroup"])
								# Allocate the boundgroup
								member_detail_list.extend(list(
									db.staff.find({"groupname":{"$in":bgrouplist}},{"cnname":1,"groupname":2})
									))
						else:
							member_detail_list=list()
						if group_doc.has_key("leader"):
							leaderlist=list(group_doc["leader"])
							leader_detail_list=list(db.staff.find({
								"mail":{"$in":leaderlist}
								},
								{"cnname":1,"mail":2},
								))
						else:
							leader_detail_list=list()
						temp_groupsee=loader.get_template("parts/groupsee.html")
						del group_doc["member"]
						del group_doc["leader"]
						con_groupsee=dict(group_doc)
						if len(member_detail_list)>0:
							con_groupsee.update({"member":member_detail_list})
						if len(leader_detail_list)>0:
							con_groupsee.update({"leader":leader_detail_list})
						if asgroup_l:
							con_groupsee.update({"isleader":True}) 
						return HttpResponse(temp_groupsee.render(con_groupsee,request))
				elif get_dict["md"][0]=="refreshbg":
					# If md is an ajax click to refresh the memberlist by boundgroup relationships
					bdgroup_get=dict((k,get_dict[k][0]) for k in ["groupname","boundgroup"])
					return HttpResponse(refresh_group_bound(
						bdgroup_get["boundgroup"],# Arg fromgroup
						bdgroup_get["groupname"],# Arg togroup
						request# Arg reqeust, to use session information to validate if the user has the authorization to do so
						))
	else:
		return redirect(tl)
def gchat_aj(request):
	tl=testlog(request)
	if tl==True:
		tc=testcnname(request)
		if tc!=True:
			return redirect("/userinfo")
		if request.method=="GET":
			get_dict=dict(request.GET)
			db=get_db("foundation")
			if get_dict["md"][0]=="chatin":
				chat2wall=dict((k,get_dict[k][0]) for k in ["gchatowner","chat"] if get_dict.has_key(k))
				chat2wall.update({
					"from":request.session["mail"],
					"fromcn":request.session["cnname"],
					"time":utc8(),
					})
				db.wall.insert(chat2wall)
				return HttpResponse("")
			elif get_dict["md"][0]=="gchat_backward":
				wall2chat=dict((k,get_dict[k][0]) for k in ["gchatowner","beforetime","skippages","limit"] if get_dict.has_key(k))
				wall2chat_list=list(db.wall.find(
					{
					"gchatowner":wall2chat["gchatowner"],
					"time":{"$lte":datetime.datetime.fromtimestamp(float(wall2chat["beforetime"]))},
					}
					).sort("time",DESCENDING).limit(int(wall2chat["limit"])).skip(int(wall2chat["limit"])*int(wall2chat["skippages"]))
				)
				if len(wall2chat_list)==0:
					return HttpResponse(u"没有更早记录了")
				else:
					rt=''
					selfmail=request.session["mail"]
					temp_chatline=loader.get_template("parts/gchat_line.html")
					rev_list=wall2chat_list.__reversed__()
					for chatline in rev_list:
						chatline["time"]=chatline["time"].strftime("%m-%d %H:%M")
						chatline["id"]=chatline["_id"].__str__()
						context=dict(chatline)
						if chatline["from"]==selfmail:
							context.update({"self_mark":"self_mark"})
						rt=rt+u"<div id='backid_%s' class='gchat_block'>"%(chatline["id"])+temp_chatline.render(context)+u"</div>"
					return HttpResponse(rt)
			elif get_dict["md"][0]=="gchat_forward":
				wall2chat=dict((k,get_dict[k][0]) for k in ["gchatowner","sincetime",] if get_dict.has_key(k))
				wall2chat_list=list(db.wall.find(
					{
					"gchatowner":wall2chat["gchatowner"],
					"time":{"$gte":datetime.datetime.fromtimestamp(float(wall2chat["sincetime"]))},
					}
					).sort("time")
				)
				if len(wall2chat_list)>0:
					rt=''
					selfmail=request.session["mail"]
					temp_chatline=loader.get_template("parts/gchat_line.html")
					for chatline in wall2chat_list:
						chatline["time"]=chatline["time"].strftime("%m-%d %H:%M")
						chatline["id"]=chatline["_id"].__str__()
						context=dict(chatline)
						if chatline["from"]==selfmail:
							context.update({"self_mark":"self_mark"})
						rt=rt+temp_chatline.render(context)
					rt=rt+u"<div class='sincetime_refresh' style='display:none;'>%s</div>"%(timestamp())
					return HttpResponse(rt)
				else:
					return HttpResponse("")
	else:
		return redirect(tl)
def testview(request):
	db=get_db("foundation")
	template=loader.get_template("msg.html")
	grouplist=list(
			db.staff.aggregate(
				[{"$match":{"grp":"Finance","cnname":{"$exists":True}}},{"$project":{"cnname":1}}]
				)
			)
	testobj=tagform(
		"cnname",
		grouplist,
		)
	testobj.update_cross_pull=dict({"grp":"Finance"})
	context={
	"msg_title":"Tagform Test",
	"msg_body":testobj.tagtile(),
	}
	return HttpResponse(template.render(context,request))

def condi_rearm(condi_json):
	condi_json=dict({"_id":ObjectId(condi_json["_id"])})
	return condi_json

def authportal(request,job):
	tl=testlog(request)
	db=get_db("foundation")
	if tl==True:
		tc=testcnname(request)
		if tc!=True:
			return redirect("/userinfo")
		if request.method=="GET":
			ajin=dict()
			for k,v in eval(request.GET["jsons"]).iteritems():
				ajin.update({k:v})
			db.staff.update(condi_rearm(ajin["update_condi"]),ajin["update_cross_pull"])
			tl=1
		else:
			tl=0
	else:
		tl=0
	return HttpResponse(tl)
def process(request):
	"""
	The page to edit,approve/deny the ongoing process
	"""
	tl=testlog(request)
	if tl==True:
		tc=testcnname(request)
		if tc!=True:
			return redirect("/userinfo")
		db=get_db("foundation")
		#Instantiate user_auth class, by input an argument(user email as id)
		user_au=user_auth(request.session['mail'])
		#=================================
		# GET method
		if request.method=="GET":
			get_dict=dict(request.GET)
			if get_dict.has_key("processid"):
				prid=get_dict["processid"][0]
				if get_dict.has_key("buyagain"):
					db=get_db("foundation")
					process_doc=dict(db.process.find_one({"_id":ObjectId(prid)}))
					process_doc["_buyagain"]=True
					tl=edit_process_officeuse(process_doc,request)
				else:
					tl=edit_process(prid,request)
			elif get_dict.has_key("list"):
				if get_dict["list"][0]=="sf":
					tl=user_au.my_applications(request)
				elif get_dict["list"][0]=="review":
					tl=user_au.review_application(request)
				elif get_dict["list"][0]=="await":
					tl=user_au.await_application(request)
				else:
					tl=u'No such way of list'
			else:
				tl=process_main(request)
		else:
			tl=process_main(request)
	else:
		return redirect(tl)
	return HttpResponse(tl)
def authset(request):
	"""
	The page we used to apply, set, or approve authorization
	"""
	save_request(request)
	tl=testlog(request)
	if tl==True:
		tc=testcnname(request)
		if tc!=True:
			return redirect("/userinfo")
		db=get_db("foundation")
		#Instantiate user_auth class, by input an argument(user email as id)
		user_au=user_auth(request.session['mail'])
		#=================================
		# GET method
		if request.method=="GET":
			get_dict=dict(request.GET)
			if get_dict.has_key("taskname"):
				taskname=get_dict["taskname"][0]
				taskname_n=db.tasks.count({"taskname":taskname})
				tl=user_au.get_auth_form(request,taskname,None)
			# If no task name ("taskname") in the query string,
			# We go into the page to create a new task
			else:
				tl=user_au.guide_page(request)
		#=================================
		# POST method
		elif request.method=="POST":
			post_dict=dict(request.POST)
			taskname=post_dict["taskname"][0]
			# "settype" might be 1)settask 2)setuser
			if post_dict.has_key("process"):
				temp_msg=loader.get_template("msg.html")
				if post_dict["process"][0]=="auth":
					if user_au.test_super(taskname)==1:
						# Extract sub-dict by using some of the keys,
						# Input the infomation to the MongoDB
						user_au.post_func_name="auth_post_filter"
						user_au.post_apply(request)
						tl=user_au.my_applications(request)
					else:
						tl=temp_msg.render({
						"msg_head":u"You don't have the authority to change that",
						"msg_body":u"You don't have the authority to change settings on %s"%(taskname)
						},request)
				else:
					tl=temp_msg.render(
							{
							"msg_head":u"Set Error",
							"msg_body2":post_dict,
							"msg_body":u"Error: Set type error"
							}
						)
		else:
			tl=user_au.create_task_form()
	else:
		return redirect(tl)
	return HttpResponse(tl)

def tablebook_aj(request):
	"""
	Work with the table_book class in lib
	"""
	tl=testlog(request)
	if tl==True:
		tc=testcnname(request)
		if tc!=True:
			return redirect("/userinfo")
		if request.method=="GET":
			get_dict=dict(request.GET)
			if get_dict["type"][0]=="page_selector":
				# Return the page flipper
				db=get_db(get_dict["db"][0])
				collection=db[get_dict["coll"][0]]
				condi=eval(get_dict["condi"][0])
				extra_condi=get_dict["extra_condi"][0]
				if extra_condi!='':
					condi.update(eval(extra_condi))
				page_limit=int(get_dict["page_limit"][0])
				# Count entries in databases
				mgcount=int(collection.count(condi))
				temp_page_selector=loader.get_template("parts/page_selector.html")
				form_ps=page_selector_form()
				form_ps.fields["page"]=IntegerField(label=u"页",initial=1,max_value=int(ceil(float(mgcount)/float(page_limit))),min_value=1)
				con_ps=dict({
					"form":form_ps,
					"ttl":mgcount,
					"page_limit":page_limit,
					})
				tl=temp_page_selector.render(con_ps,request)
			elif get_dict["type"][0]=="detail":
				tl=process_detail_show(request)
			elif get_dict["type"][0]=="killprocess":
				try:
					processid=get_dict["processid"][0]
					remover=request.session["mail"]
					db=get_db("foundation")
					process_doc=dict(db.process.find_one({"_id":ObjectId(processid)},{"mail":1}))
					if process_doc["mail"]==remover:
						db.process.update({"_id":ObjectId(processid)},{"$set":{"status":"revoked"},"$push":{
							"log":{
							"time":utc8(),
							"from":request.session["mail"],
							"fromcn":request.session["cnname"],
							"to":process_doc["mail"],
							"decision":"revoked",
							}
							}})
						tl="revoked"
				except:
					tl="fail"
			elif get_dict["type"][0]=="process_approve":
				#The approcondive/deny section
				db=get_db(get_dict["db"][0])
				processid=get_dict["processid"][0]
				decision=get_dict["decision"][0]
				user_au=user_auth(request.session["mail"])
				process_dict=db.process.find_one({"_id":ObjectId(processid)})
				loaded_stage=user_au.read_stage(processid)
				log_dict=dict({
					"time":utc8(),
					"from":request.session["mail"],
					"fromcn":request.session["cnname"],
					"to":process_dict["mail"],
					"decision":decision,
					})
				if get_dict.has_key("remark"):
					log_dict.update({"remark":get_dict["remark"][0]})
				# 3 Decisions:
				#================================================
				if decision=='accept':
					ican_list=loaded_stage["ican"]
					if ican_list==0:
						tl=u"You can't approve this"
					else:
						db.process.update(
							{"_id":ObjectId(processid)},
							{"$pushAll":
								{"stage":ican_list},
							"$push":{
								"log":log_dict
								},
							"$set":{"edit":False,"status":"finished"}
							},
							upsert=True)
						# Reset the stage_mails
						db.process.update(
							{"_id":ObjectId(processid)},
							{"$set":{"stage_mails":user_au.stage_mails(process_dict["taskname"],processid)}}
							)
						loaded_stage=user_au.read_stage(processid)
						if loaded_stage["status"]=="finished":
							tl=u"Appication Finished"
						else:
							tl=u"Accepted (id:%s)"%loaded_stage
				if decision=='refill':
					ican_list=loaded_stage["ican"]
					if ican_list==0:
						tl=u"You can't approve this"
					else:
						try:
							start_stage=process_dict["log"]["start_stage"]
						except:
							start_stage=list()
						db.process.update(
							{"_id":ObjectId(processid)},
							{"$set":
								{"stage":start_stage},
							"$push":{
								"log":log_dict
								},
							"$set":{"edit":True}
							},
							upsert=True)
						db.process.update(# reset the stage_mails
							{"_id":ObjectId(processid)},
							{"$set":{"stage_mails":user_au.stage_mails(process_dict["taskname"],processid)}}
							)
						tl=u"驳回让申请人修改"
				if decision=='deny':
					db.process.update(
						{"_id":ObjectId(processid)},
						{
						"$push":{"log":log_dict},
						"$set":{"status":"dead","edit":False,"stage_mails":list()},
						},
						upsert=True)
					tl="Deny"
			elif get_dict["type"][0]=="mgdt":
				db=get_db(get_dict["db"][0])
				collection=db[get_dict["coll"][0]]
				row_func_name=get_dict["row_func"][0]
				condi=eval(get_dict["condi"][0])
				extra_condi=get_dict["extra_condi"][0]
				if extra_condi!='':
					condi.update(eval(extra_condi))
				page_limit=int(get_dict["page_limit"][0])
				if get_dict.has_key("skips"):
					skips=int(get_dict["skips"][0])
				else:
					skips=0;
				page_skip=int(page_limit*skips)
				condi=dict(condi)
				user_au=user_auth(request.session["mail"])
				table_book1=table_book(get_dict["coll"][0],condi)
				table_book1.row_func=eval(row_func_name)
				table_book1.sort=[("tm",DESCENDING)]
				table_book1.field_dict=eval(get_dict["field_dict"][0])
				table_book1.page_skip=page_skip
				tl=table_book1.mongo(request)
			else:
				tl="No type setting"
		else:
			tl="request method not 'GET'"
	else:
		return redirect(tl)
	return HttpResponse(tl)
# The page desgined to grab office supply url
def officeuse(request):# the page to claim office supply
	save_request(request)
	tl=testlog(request)
	db=get_db("foundation")
	#db=get_db("foundation")
	if tl==True:
		tc=testcnname(request)
		if tc!=True:
			return redirect("/userinfo")
		if request.method=="POST":		
			input_beta=office_use_detail(request.POST)
			empety_form=office_use_detail()
			del empety_form.fields["processid"]
			if input_beta.is_valid():
				if len(input_beta.cleaned_data["processid"]) >10:
					# Update an existed process
					data_dict=dict(input_beta.cleaned_data)
					data_dict["price"]=float(data_dict["price"])
					# Calculate the total price
					# data_dict["tprice"]=float(data_dict["price"])*float(data_dict["qtt"])
					stage=list()
					brand_has=False
					try:
						#Test if the brand is from staples
						brandname=str(data_dict["brandname"])
						brandname=brandname.lower()			
						for bran in brand_keys:
							if brandname.find(bran)>-1:
								brand_has=True
					except:
						pass
					if (float(data_dict["price"])*float(data_dict["qtt"])<100 and brand_has):
						stage.append("1")
					data_dict.update({
						"mail":request.session["mail"],
						"edit":False,
						"cnname":request.session["cnname"],
						"process":"officeuse",
						"taskname":"officeuse",
						"stage":stage,
						"applier_tier":get_tiers(request.session["mail"]),
						"tm":utc8()})
					user_au=user_auth(request.session["mail"])
					task_doc=db.tasks.find_one({"taskname":"officeuse"},{"stages":1,"_id":0})
					data_dict.update({"stage_mails":user_au.stage_mails("officeuse",input_beta.cleaned_data["processid"])}) 
					ttlamt=float(float(data_dict["price"])*float(data_dict["qtt"]))
					data_dict.update({"ttlamt":ttlamt})
					# The self auto approve logic
					# If it's not approved and you can approve yourself
					# Then do so
					if ("1" not in data_dict["stage"] and data_dict["mail"] in data_dict["stage_mails"]):
						data_dict["stage"]=["1"]
						data_dict.update({"status":"finished"})
					if (len(stage)==0 and len(data_dict["stage_mails"])==0):
						return redirect("/officeuse?backmsg=没有管理人员进行相应的审批，请联系您的经理尽快进行设置")
					data_dict.update({"stages":task_doc["stages"]})
					logdict={
						"from":request.session["mail"],
						"fromcn":request.session["cnname"],"decision":"repost","time":utc8()}
					db.process.update({
						"_id":ObjectId(input_beta.cleaned_data["processid"])},
						{"$set":data_dict},upsert=True) #put the data into mongo
					db.process.update({
						"_id":ObjectId(input_beta.cleaned_data["processid"])},
						{"$push":{"log":logdict}},upsert=True) #put the data log into mongo					
					temp_ou_post=loader.get_template("officeuse/officeusepost.html")
					postrt=temp_ou_post.render(data_dict,request)
				else:
					# Insert new process
					data_dict=dict(input_beta.cleaned_data)
					del data_dict["processid"]
					data_dict["price"]=float(data_dict["price"])
					# data_dict["price"]=data_dict["price"].__format__("f")
					# Calculate the total price
					# data_dict["tprice"]=float(data_dict["price"])*float(data_dict["qtt"])
					stage=list()
					brand_has=False
					try:
						#Test if the brand is from staples
						brandname=str(data_dict["brandname"])
						brandname=brandname.lower()			
						for bran in brand_keys:
							if brandname.find(bran)>-1:
								brand_has=True
					except:
						pass
					if (float(data_dict["price"])*float(data_dict["qtt"])<100 and brand_has):
						stage.append("1")
						data_dict.update({"status":"finished"})
					data_dict.update({
						"mail":request.session["mail"],
						"edit":False,
						"cnname":request.session["cnname"],
						"process":"officeuse",
						"taskname":"officeuse",
						"stage":stage,
						"applier_tier":get_tiers(request.session["mail"]),
						"tm":utc8()})
					task_doc=db.tasks.find_one({"taskname":"officeuse"},{"stages":1,"_id":0})
					user_au=user_auth(request.session["mail"])
					data_dict.update({"stage_mails":user_au.stage_mails("officeuse")})
					ttlamt=float(float(data_dict["price"])*float(data_dict["qtt"]))
					data_dict.update({"ttlamt":ttlamt})
					# The self auto approve logic
					# If it's not approved and you can approve yourself
					# Then do so
					if ("1" not in data_dict["stage"] and data_dict["mail"] in data_dict["stage_mails"]):
						data_dict["stage"]=["1"]
						data_dict.update({"status":"finished"})
					if (len(stage)==0 and len(data_dict["stage_mails"])==0):
						return redirect("/officeuse?backmsg=没有管理人员进行相应的审批，请联系您的经理尽快进行设置")
					data_dict.update({"stages":task_doc["stages"]})
					logdict={"from":request.session["mail"],
							"fromcn":request.session["cnname"],
							"time":utc8(),
							"decision":"post"}
					data_dict.update({"log":[logdict]}) #combine the trace stamp
					db.process.insert(data_dict) #put the data into mongo
					temp_ou_post=loader.get_template("officeuse/officeusepost.html")
					postrt=temp_ou_post.render(data_dict,request)
			else:
				postrt=u'input not valid'
		else:
			postrt=""
		process_doc=None
		bodies=OrderedDict()
		ou_temp=loader.get_template("a.html")
		backmsg_dict=dict()
		if request.method=="GET":
			if request.GET.has_key("backmsg"):
				backmsg=dict(request.GET)["backmsg"][0]
				backmsg_dict.update({"backmsg":backmsg})
			if request.GET.has_key("processid"):
				processid=request.GET["processid"]
				process_doc=db.process.find_one({"_id":ObjectId(processid)})	
			#load the empety form
			if process_doc==None:
			#the historic data
#				hist_mg=db.process.find({"mail":request.session["mail"],"process":"officeuse","status":{"$nin":["finished"]}})
#				hist_table=MongoOut(hist_mg) #use the class:MongoOut from lib, 
#				hist_table.fmatching.update({"cnname":u"申请人"})		#Have to update it one by one to use the OrderedDict's order
#				hist_table.fmatching.update({"time":u"时间"})
#				hist_table.fmatching.update({"itemname":u"Item"})
#				hist_table.fmatching.update({"price":u"Cost"})
#				hist_table.fmatching.update({"pro_id":u"Product ID"})
#				hist_loaded=hist_table.as_table()
#				bodies.update({"c1":hist_loaded})
				empety_form=office_use_detail()
				del empety_form.fields["processid"]
			else:
				process_doc.update({"processid":process_doc["_id"].__str__()})
				empety_form=office_use_detail(process_doc)
		#load templates
		temp_css=loader.get_template("css/officeuse.css")
		temp_ou1=loader.get_template("officeuse/officeuse1.html")
		#render the templates
		loaded_css=temp_css.render({})
		ou1dict=dict({
			"empety_form":empety_form,
			"urlform":fm_officeuse(),
			})
		ou1dict.update(backmsg_dict)
		loaded_ou1=temp_ou1.render(ou1dict,request)
	#update the page body
		bodies.update({"c4":u"<h2 style='color:#4682B4;'>领取您的装备</h2>"})
		bodies.update({"d0":postrt})
		bodies.update({"d1":loaded_ou1})
		bodies.update({"e2":usejs("js/varys_input.js")})
	#the context of template:ou_temp
		a_con={
		"userb":userbar(request),
		"loaded_css":loaded_css,
		"title":u'办公用品行政领用',
		"bodies":bodies,
		}
		hr=HttpResponse(ou_temp.render(a_con,request))
	else:
		return redirect(tl)
	return HttpResponse(hr)

def ajax_officeuse(request):# ajax function after the url input
	tl=testlog(request)
	if tl==True:
		tc=testcnname(request)
		if tc!=True:
			return redirect("/userinfo")
		if request.method=="GET":
				#fetch from cleaned_data
			stburl=dict(request.GET)["stburl"][0]
			pro_id=dict(request.GET)["pro_id"][0]
			grab_down=parse_stb_url(pro_id)
			tl=grab_down
			return HttpResponse(tl)
	else:
		return redirect(tl)
	return HttpResponse(hr)
def download(request):
	save_request(request)
	tl=testlog(request)
	if tl==True:
		tc=testcnname(request)
		if tc!=True:
			return redirect("/userinfo")
		if request.method=="GET":
			get_dict=dict(request.GET)
			if get_dict.has_key("loadback"):
				temp_lb=loader.get_template("a.html")
				temp_loadback=loader.get_template("loadback.html")
				bodies=OrderedDict({})
				upform=loadback()
				bodies.update({"a1":temp_loadback.render({"upform":upform},request)})
				con_lb=dict({
					"userb":userbar(request),
					"bodies":bodies,
					"title":u"回传数据",
					})
				return HttpResponse(temp_lb.render(con_lb,request))
		db=get_db("foundation")
		template=loader.get_template("download.html")
		range_form=download_range()
		context=dict({
			"userb":userbar(request),
			"form":range_form,
			})
		if request.method=="GET":
			get_dict=dict(request.GET)
			if get_dict.has_key("backmsg"):
				context.update({"backmsg":get_dict["backmsg"][0]})
		return HttpResponse(template.render(context,request))
	else:
		return redirect(tl)

def download_aj(request):
	'''
	Download Ajax

	'''
	save_request(request)
	tl=testlog(request)
	if tl==True:
		tc=testcnname(request)
		if tc!=True:
			return redirect("/userinfo")
		if request.method=="GET":
			get_dict=dict(request.GET)
			down_dict=dict((k,get_dict[k][0]) for k in get_dict.keys())
			template=loader.get_template("download_aj.html")
			find_condi=dict()
			context=dict({
				"datestart":u"未设置开始时间",
				"dateend":u"未设置结束时间",
				})
			tm=dict()
			# Date Start, 
			if down_dict.has_key("datestart"):
				if len(down_dict["datestart"])>6:
					datestart=date_parse(down_dict["datestart"])
					tm.update({"$gte":datestart})
					context.update({
						"datestart":datestart.strftime("%Y-%m-%d"),
						})
			# Date End
			if down_dict.has_key("dateend"):
				if len(down_dict["dateend"])>6:
					dateend=date_parse(down_dict["dateend"])
					tm.update({"$lt":dateend+timedelta(hours=24)})
					context.update({
						"dateend":dateend.strftime("%Y-%m-%d"),
						})
			if len(tm)>0:
				find_condi.update({"tm":tm})
			taskname=down_dict["taskname"]
			find_condi.update({"status":"finished","process":taskname})
			db=get_db("foundation")
			if int(db.staff.count({"auth.%s.d"%(taskname):"1","$or":[{"member":request.session["mail"]},{"mail":request.session["mail"]}]}))<1:
				return redirect("/download?backmsg=您没有相应的权限下载该数据")
			pdscope=dict(db.staff.find_one({"mail":request.session["mail"]},{"_id":0,"dscope":1}))
			if pdscope.has_key("dscope"):
				dscopelist=pdscope["dscope"]
				dscopeg=list(db.staff.find({"groupname":{"$in":dscopelist}},{"_id":0,"member":1}))
				if len(dscopeg)>0:
					ds_users=list()
					for g in dscopeg:
						if g.has_key("member"):
							ds_users=ds_users+g["member"]
					ds_users=list(set(ds_users))
					find_condi.update({"mail":{"$in":ds_users}})
				else:
					return redirect("/download?backmsg=没有想对应的群组是在您这里下载的")
			else:
				return redirect("/download?backmsg=没有想对应的用户群组是在您这里下载的")
			dl_list=list(
				db.process.find(
					find_condi
					)
				)
			context.update({
				"taskname":taskname,
				"userb":userbar(request),
				})
			sum_price=0
			sum_vat_ex=0
			sum_est_cost=0
			sum_qtt=0
			for dline in dl_list:
				# Each line that need to download
				ttl_price=float(dline['price'])*float(dline["qtt"])
				vat_ex=float(ttl_price)/1.17
				est_cost=vat_ex*0.8
				dline["ttl_price"]=ttl_price
				sum_price+=ttl_price
				sum_vat_ex+=vat_ex
				sum_est_cost+=est_cost
				sum_qtt+=float(dline["qtt"])
				try:
					dline['gtiers']=get_tiers(dline['mail'])['3'][0]['cnname']
				except:
					dline['gtiers']=u'用户没有设置团队'
				dline["vat_ex"]=("%.2f"%vat_ex)
				dline["est_cost"]=("%.2f"%est_cost)
				dline["pro_id"]=filter(str.isdigit,str(dline["pro_id"]))
				dline["tm"]=dline["tm"].strftime("%Y-%m-%d")
				dline["id"]=dline["_id"].__str__()
			context.update({"dl_list":dl_list})
			context.update({
				"sum_price":sum_price,
				"sum_qtt":sum_qtt,
				"sum_vat_ex":("%.2f"%sum_vat_ex),
				"sum_est_cost":("%.2f"%sum_est_cost),
				})
			dl_path=xlwt_officeuse(context)
			context.update({"dl_path":dl_path})
			return HttpResponse(template.render(context,request))
		elif request.method=="POST":
			post_dict=dict(request.POST)
			try:
				if (post_dict["md"][0]=="loadback" and post_dict["taskname"][0]=="officeuse"):
					#load back the data
					md="lb_officeuse"
				else:
					md=""
			except:
				md=""
			if md=="lb_officeuse":
				# Load Back Office Use
				fm=loadback(post_dict,request.FILES)
				for k,v in request.FILES.iteritems():
					if v.size>5000000:
						return redirect("/download?backmsg=回传文件不得大于5MB")
					else:
						filepath=v.temporary_file_path()
						bk=open_workbook(filepath)
						upl_sheet=bk.sheet_by_index(0)
						idcol=False
						dncol=False
						for ic in range(upl_sheet.ncols):
							# Allocate 2 key columnes
							# The field name has to be in the FIRST ROW (aka row 0)
							# The field name must be the following:
							cellv=str(upl_sheet.cell_value(0,ic)).lower()
							if cellv in [u"行政领用单号","id"]:
								idcol=ic
							if cellv in [u"运单号","dn"]:
								dncol=ic
						if idcol==False:
							return redirect("/download?backmsg=未找到'行政领用单号/id'列")
						elif dncol==False:
							return redirect("/download?backmsg=未找到'运单号/dn'列")
						else:
							nrows=upl_sheet.nrows
							updt=list()
							ids=list()
							for ic2 in range(nrows):
								if len(upl_sheet.cell_value(ic2,idcol))>22:
									ids.append(upl_sheet.cell_value(ic2,idcol))
									if len(str(upl_sheet.cell_value(ic2,dncol)))<5:
										updt.append({"id":upl_sheet.cell_value(ic2,idcol),"dn":u"仓库缺货"})
									else:
										updt.append({"id":upl_sheet.cell_value(ic2,idcol),"dn":upl_sheet.cell_value(ic2,dncol)})
							ids=list(set(ids))
							oids=list(ObjectId(sid) for sid in ids)
							db=get_db("foundation")
							logdict=dict({
								"from":request.session["mail"],
								"fromcn":request.session["cnname"],
								"time":utc8(),
								})
							for uline in updt:
								if uline["dn"]==u"仓库缺货":
									logdict.update({"decision":"nosupply"})
									db.process.update({
										"_id":ObjectId(uline["id"])
										},
										{
											"$set":{
												"dn":uline["dn"],	# dn, the delivery status, "仓库缺货" in this case
												"status":"dead",	# If dn not found, the status is dead
												"edit":False 		# Lock the edit status
												},
											"$push":
												{
												"log":logdict,		# Log the alteration
												}
										},
										upsert=True)
								else:
									logdict.update({"decision":"dispatched"})
									db.process.update(
										{"_id":ObjectId(uline["id"])},
										{"$set":
											{
											"dn":uline["dn"],		# dn, in this case, the delivery note number
											"status":"done", 		# done is the last successful status
											"edit":False 			# lock the edit status
											},
										"$push":
											{
											"log":logdict  			#log the alteration
											}
										},
										upsert=True)
							upd_preview=list(db.process.find({"_id":{"$in":oids}},{"itemname":1,"cnname":2,"qtt":3,"dn":4,"tm":5}))
							for upre in upd_preview:
								upre["id"]=upre["_id"].__str__()
								upre["date"]=upre["tm"].strftime("%Y-%m-%d")
							temp_a=loader.get_template("a.html")
							temp_loadedxl=loader.get_template("loadback_xl.html")
							loadedxl=temp_loadedxl.render({"updt":upd_preview},request)
							bodies=OrderedDict()
							bodies.update({"c1":loadedxl})
							con_a=dict({
								"userb":userbar(request),
								"title":u"回传数据",
								"bodies":bodies,
								})
							return HttpResponse(temp_a.render(con_a,request))
				return redirect("/download?backmsg=filenum%s"%len(request.FILES))
			else:
				return redirect("/download?backmsg=没有相应事务权限")
		else:
			return redirect("/")
	else:
		return redirect(tl)
def upload(request):
	tl=testlog(request)
	template=loader.get_template("msg.html")
	if tl==True:
		tc=testcnname(request)
		if tc!=True:
			return redirect("/userinfo")
		context={}
		userb=userbar(request)
		if request.method=="POST":
			msg_form=upload_input(request.POST,request.FILES)
			msg_body2=''
			for k,v in request.FILES.iteritems():
				if v.size>20000000:
					msg_body2+="文件超过20 MB<br>"
				else:
					filepath=v.temporary_file_path()
					booktemp=loader.get_template("upload/book.html")
					book_con={
					"book_name":str(v.name),
					"book_size":str(v.size),
					"book_content_type":str(v.content_type),
					}
					msg_body2+=booktemp.render(book_con)
					bk=open_workbook(filepath)
					sheets=bk.sheet_names()
					sheethtml=loader.get_template("upload/sheet.html")
					#Process Each Sheet
					for sheet in sheets:
						sheetobj=bk.sheet_by_name(sheet)
						rich_sh=rich_sheet(sheetobj)
						rich_sh.field_set()
						she_con={
						"sheet_name":sheet,
						"sheet_nrows":rich_sh.sheet.nrows,
						"sheet_ncols":rich_sh.sheet.ncols,
						"sheet_preview":rich_sh.as_table(),
						"sheet_fields":'',
						}
						#
						#Process each field
						for head_json in rich_sh.head_list:
							sheetfm=uploadset()
							#
							#Change the field name(the key name of the fields dict)
							sheetfm['schema'].label=head_json["val"]
							for fieldname,fielditem in sheetfm.fields.iteritems():
								sheetfm.fields["schema"].label=str(head_json["val"])
								sheetfm.fields[str(sheet)+"_"+str(head_json["posi"]["c"])+'_schema']=sheetfm.fields.pop('schema')
							she_con.update({"sheet_fields":she_con['sheet_fields']+sheetfm.as_table()})
						msg_body2+=sheethtml.render(she_con)
			context.update({"msg_body2":msg_body2,})
		else:
			msg_form=upload_input()
		context.update({
			"msg_title":u"上传文件",
			"msg_head":u"上传文件",
			"msg_body":u"<h2>选择上传的文件</h2>",
			"msg_form":msg_form,
			})
	else:
		return redirect(tl)
	return HttpResponse(template.render(context,request))
def help(request):
	"""
	Help page does not require log on
	"""
	save_request(request)
	temp_frame=loader.get_template("a.html")
	temp_help=loader.get_template("parts/help.html")
	bodies=OrderedDict()
	bodies.update({"a1":temp_help.render({},request)})
	con_frame=dict({
		"userb":userbar(request),
		"bodies":bodies,
		"title":u"帮助文档",
		})
	return HttpResponse(temp_frame.render(con_frame,request))
def crontab(request):
	tl=testlog(request)
	if request.method=="GET":
		get_dict=dict(request.GET)
		if get_dict.has_key("pwd"):
			if get_dict["pwd"][0]=="cptbtptp":
				boundrefresh()
				return HttpResponse("ok")
def authassign(request):
	save_request(request)
	tl=testlog(request)
	if tl==True:
		tc=testcnname(request)
		if tc!=True:
			return redirect("/userinfo")
		tsu=testsu(request)
		if tsu!=True:
			return redirect(u"/?backmsg=您没有系统管理员权限")
		temp_basic=loader.get_template("a.html")
		con_basic=dict()
		bodies=OrderedDict()
		db=get_db("foundation")
		if request.method=="GET":
			get_dict=dict(request.GET)
			if get_dict.has_key("mail"):
				mail=get_dict["mail"][0]
				profile=dict(db.staff.find_one({"mail":mail}))
				uidkey="mail"
			elif get_dict.has_key("groupname"):
				groupname=get_dict["groupname"][0]
				profile=dict(db.staff.find_one({"groupname":groupname}))
				uidkey="groupname"
			if (get_dict.has_key("mail") or get_dict.has_key("groupname")):
				temp_aa=loader.get_template("parts/authassign.html")
				con_aa=dict(profile)
				con_aa.update({"uidkey":uidkey})
				rd_aa=temp_aa.render(con_aa,request)
				bodies.update({"c1":rd_aa})
				con_basic.update({
					"bodies":bodies,
					"title":u"权限分配",
					"userb":userbar(request),
				})
				rt=temp_basic.render(con_basic,request)
				return HttpResponse(rt)
			elif get_dict.has_key("uidkey"):
				uidkey=get_dict["uidkey"][0]
				uidval=get_dict["uidval"][0]
				if get_dict.has_key("setkey"):
					setkey=get_dict["setkey"][0]
					setval=get_dict["setval"][0]
					upd=db.staff.update({uidkey:uidval},{"$set":{setkey:setval}})
					return HttpResponse(str(upd))
				if get_dict.has_key("pushkey"):
					pushkey=get_dict["pushkey"][0]
					pushval=get_dict["pushval"][0]
					upd=db.staff.update({uidkey:uidval},{"$push":{pushkey:pushval}})
					return HttpResponse(str(upd))
				if get_dict.has_key("pullkey"):
					pullkey=get_dict["pullkey"][0]
					pullval=get_dict["pullval"][0]
					upd=db.staff.update({uidkey:uidval},{"$pull":{pullkey:pullval}})
					return HttpResponse(str(upd))
	else:
		return redirect(tl)
def sys(request):
	save_request(request)
	tl=testlog(request)
	if tl==True:
		tc=testcnname(request)
		if tc!=True:
			return redirect("/userinfo")
		tsu=testsu(request)
		if tsu!=True:
			return redirect("/?backmsg=您没有系统管理员权限")
		temp_sys=loader.get_template("a.html")
		con_sys=dict()
		bodies=OrderedDict()
		prpty=read_sys()
		bodies.update({
			"b1":u"<h2>Terminus Mark II</h2>",
			"b2":prpty,
			"b3":"<style>body{color:#fff;background-color:#265274;}</style>"})
		con_sys.update({
			"title":u"Terminus The Planet",
			"userb":userbar(request),
			"bodies":bodies,
			})
		return HttpResponse(temp_sys.render(con_sys,request))
	else:
		return redirect(tl)
def private_msg(request):
	tl=testlog(request)
	if tl==True:
		tc=testcnname(request)
		if tc!=True:
			return redirect("/userinfo")
		temp_basic=loader.get_template("a.html")
		bodies=OrderedDict()
		primsg_head=loader.get_template("parts/primsg_head.html").render({})
		temp_pri=loader.get_template("parts/pri_msg.html")
		bodies.update({"b6":primsg_head})
		bodies.update({"c1":temp_pri.render({"usermail":request.session["mail"]},request)})
		return HttpResponse(temp_basic.render({
			"userb":userbar(request),
			"bodies":bodies,
			"title":"%s的私信"%(request.session["cnname"])
			},request))
	else:
		return redirect(tl)
def userlist(request):
	save_request(request)
	tl=testlog(request)
	if tl==True:
		tc=testcnname(request)
		if tc!=True:
			return redirect("/userinfo")
		db=get_db("foundation")
		bodies=OrderedDict()
		temp_userlist_head=loader.get_template("parts/userlist_head.html")
		usercount=int(db.staff.count({"mail":{"$exists":True}}))
		userlist_head=temp_userlist_head.render({"usernumber":usercount})
		bodies.update({"b6":userlist_head})
		userl=list(db.staff.find({"mail":{"$exists":True}},
								{
									"cnname":1,
									"enname":2,
									"mail":3,
									"ext":4,
									"department":5,
									"manager":6,
								}))
		rt="<table class='table_center'>"
		for userline in userl:
			temp_userline=loader.get_template("parts/userline.html")
			rt=rt+temp_userline.render(userline,request)
		rt=rt+'</table>'
		bodies.update({"c1":rt})
		groupcount=int(db.staff.count({"groupname":{"$exists":True}}))
		grouplist=list(db.staff.find({
			"groupname":{"$exists":True},
			},
			{
				"groupname":2,
				"cnname":1,
				"gtier":3,
				"leader":4,
				"member":5,
			}))
		grrt="<h3>共有小组 %s 个</h3><table class='table_center'>"%(groupcount)
		for groupline in grouplist:
			temp_grouplist=loader.get_template("parts/grouplist.html")
			groupline['leadercount']=len(groupline['leader'])
			groupline['membercount']=len(groupline['member'])
			grrt=grrt+temp_grouplist.render(groupline)
		grrt=grrt+'</table>'
		bodies.update({"c3":grrt})
		temp_basic=loader.get_template("a.html")
		context=dict({
			"userb":userbar(request),
			"title":"Terminus Citizens",
			"bodies":bodies,
			})
		return HttpResponse(temp_basic.render(context,request))
	else:
		return redirect(tl)
def privatemsg_aj(request):
	save_request(request)
	tl=testlog(request)
	if tl==True:
		tc=testcnname(request)
		if tc!=True:
			return redirect("/userinfo")
		if request.method=="GET":
			get_dict=dict(request.GET)
			if get_dict["md"][0]=="pmbload":
				usermail=get_dict["usermail"][0]
				limit=int(get_dict["limit"][0])
				skips=int(get_dict["skips"][0])
				db=get_db("foundation")
				prilist=list(db.wall.find({
					"$or":[
						{"from":usermail},
						{"to":usermail}
						],
					"wallowner":"private"
					},
					{	#data export format
						"from":1,
						"fromcn":2,
						"to":3,
						"tocn":4,
						"writes":5,
						"time":6,
					}
					).sort("time",DESCENDING).limit(limit).skip(skips)
				)
				rt=''
				for pri in prilist:
					temp_c=loader.get_template("parts/pri_line.html")
					pri["tm"]=pri["time"].strftime("%m-%d %H:%M")
					rt=rt+temp_c.render(pri)
				return HttpResponse(rt)
			else:
				return HttpResponse("")	
		else:
			return HttpResponse("")
	else:
		return redirect(tl)
def transparent(request):
	save_request(request)
	tl=testlog(request)
	if tl==True:
		tc=testcnname(request)
		if tc!=True:
			return redirect("/userinfo")
		temp_basic=loader.get_template("a.html")
		temp_tran=loader.get_template("parts/transparent.html")
		con_tran=dict()
		form_initial=dict({
			"datestart":utc8()-timedelta(days=30),
			"dateend":utc8(),
			"prospect":"sf",
			"task":"officeuse",
			})
		form_tran=transparent_set(form_initial)
		con_tran.update({"form":form_tran})
		tran_loaded=temp_tran.render(con_tran,request)
		bodies=OrderedDict()
		bodies.update({"c1":tran_loaded})
		con_basic=dict({})
		con_basic.update({
			"userb":userbar(request),
			"title":u"审阅记录",
			"bodies":bodies,
			})
		rt=temp_basic.render(con_basic,request)
		return HttpResponse(rt)
	else:
		return redirect(tl)	
def transparent_aj(request):
	save_request(request)
	tl=testlog(request)
	if tl==True:
		tc=testcnname(request)
		if tc!=True:
			return redirect("/userinfo")
		if request.method=="GET":
			condition=dict()
			get_dict=dict(request.GET)
			layer=get_dict["layer"][0]
			datestart=get_dict["datestart"][0]
			tm=dict()
			try:
				tm.update({"$gte":date_parse(datestart)})
			except:
				pass 
			dateend=get_dict["dateend"][0]
			try:
				tm.update({"$lt":date_parse(dateend)+timedelta(hours=24)})
			except:
				pass
			pstatus=dict()
			if get_dict.has_key("pstatus"):
				pstatuslist=get_dict["pstatus"][0].split(",")
				pstatus.update({"status":{"$in":pstatuslist}})
				if "inprogress" in pstatuslist:
					pstatus=dict({"$or":[{"status":{"$exists":False}},{"status":{"$in":pstatuslist}}]})
			#if len(tm)>0:
			#	condition.update({"tm":tm})
			task=get_dict["task"][0]
			prospect=get_dict["prospect"][0]
			db=get_db("foundation")
			if(prospect=="dp" and task=="officeuse"):
				if int(layer)==1:
					person=request.session["mail"]
					condition.update({
						"gtier":{"$exists":True},
						"leader":person,
						})
					gt_groups=list(db.staff.find(condition,
						{
						"cnname":1,
						"groupname":2,
						"leader":3,
						"member":4,
						"gtier":5,
						"boundgroup":6,
						}))
					bglist=list()
					for group in gt_groups:
						group["id"]=group["_id"].__str__()
						if group.has_key("boundgroup"):
							bglist=bglist+list(group["boundgroup"])
					bglist=list(set(bglist))
					bggroups=list(db.staff.find(
						{"gtier":{"$exists":True},"groupname":{"$in":bglist}},
						{
						"cnname":1,
						"groupname":2,
						"leader":3,
						"member":4,
						"gtier":5,
						"boundgroup":6,
						}
						))
					for group in bggroups:
						group["id"]=group["_id"].__str__()
					if len(gt_groups)==0:
						return HttpResponse("您当前的权限没有相关的部门信息可以查看")
					else:
						temp_layer2=loader.get_template("parts/trans_layer2.html")
						cbform=process_status()#{"pstatus":list(["finished","done"])})
						rd_layer2=temp_layer2.render({
							"cbform":cbform,
							"groups":gt_groups,
							"boundgroup":bggroups,
							})
						return HttpResponse(rd_layer2)
				elif int(layer)==2:
					groupid=get_dict["groupid"][0]
					members=list(dict(db.staff.find_one({"_id":ObjectId(groupid)},{"member":1}))["member"])
					condition.update({"mail":{"$in":members}})
					if len(tm)>0:
						condition.update({"tm":tm})
					condition.update(pstatus)
					match=dict({"$match":condition})
					output=dict()
					output.update({
						"$group":{"_id":"$mail","mail":{"$first":"$mail"},"ttlamt":{"$sum":"$ttlamt"},"cnname":{"$first":"$cnname"}}
						})
					plist=list(db.process.aggregate([match,output]))
					temp_layer3=loader.get_template("parts/trans_layer3.html")
					rd_layer3=temp_layer3.render(
						{
						"users":plist,
						}
						)
					return HttpResponse(rd_layer3)
				elif int(layer)==3:
					mail=get_dict["mail"][0]
					if mail=="self":
						mail=request.session["mail"]
					condition.update({"mail":mail})
					if len(tm)>0:
						condition.update({"tm":tm})
					condition.update(pstatus)
					prolist=list(db.process.find(condition))
					prolist=strid(prolist)
					prolist=listdate(prolist,"tm")
					cnname=''
					try:
						cnname=prolist[0]["cnname"]
					except:
						pass
					total=listsum(prolist,"ttlamt")
					temp_layer4=loader.get_template("parts/trans_layer4.html")
					rd_layer4=temp_layer4.render({
						"prolist":prolist,
						"cnname":cnname,
						"total":total,
						},request)
					return HttpResponse(rd_layer4)
			elif(prospect=="sf" and task=="officeuse"):
				if int(layer)==1:
					temp_layer2=loader.get_template("parts/trans_layer2.html")
					cbform=process_status()#{"pstatus":list(["finished","done"])})
					rd_layer2=temp_layer2.render({
						"cbform":cbform,
						})
					return HttpResponse(rd_layer2)
				elif int(layer)==3:
					mail=get_dict["mail"][0]
					if mail=="self":
						mail=request.session["mail"]
					condition.update({"mail":mail})
					if len(tm)>0:
						condition.update({"tm":tm})
					condition.update(pstatus)
					prolist=list(db.process.find(condition))
					prolist=strid(prolist)
					prolist=listdate(prolist,"tm")
					cnname=''
					try:
						cnname=prolist[0]["cnname"]
					except:
						pass
					total=listsum(prolist,"ttlamt")
					temp_layer4=loader.get_template("parts/trans_layer4.html")
					rd_layer4=temp_layer4.render({
						"prolist":prolist,
						"cnname":cnname,
						"total":total,
						},request)
					return HttpResponse(rd_layer4)
	else:
		return redirect(tl)


def cssadvlist(request):
	save_request(request)
	tl=testlog(request)
	if tl==True:
		context=dict()
		range_form=cssadv_list()
		context.update({"userb":userbar(request)})
		context.update({"range_form":range_form})
		cal_temp=loader.get_template("parts/cssadvlist.html")
		return HttpResponse(cal_temp.render(context,request))
	else:
		return redirect(tl)
def cssadvlist_aj(request):
	save_request(request)
	tl=testlog(request)
	if tl==True:
		context=dict()
		if request.method=="GET":
			tm=dict()
			get_dict=dict(request.GET)
			down_dict=dict((k,get_dict[k][0]) for k in get_dict.keys())
			if get_dict.has_key("csstask"):
				csstask=get_dict["csstask"][0]
				status=get_dict["status"][0]
				skippg=0
				eachpg=30
				temp_cal=loader.get_template("parts/cssadvlines.html")
				find_condi=dict({"csstask":csstask,"status":status})
				#process date information
				#date start
				if get_dict.has_key("datestart"):
					if len(down_dict["datestart"])>6:
						datestart=date_parse(down_dict["datestart"])
						tm.update({"$gte":datestart})
						context.update({
							"datestart":datestart.strftime("%Y-%m-%d"),
							})
				# Date End
				if get_dict.has_key("dateend"):
					if len(down_dict["dateend"])>6:
						dateend=date_parse(down_dict["dateend"])
						tm.update({"$lt":dateend+timedelta(hours=24)})
						context.update({
							"dateend":dateend.strftime("%Y-%m-%d"),
							})
				if len(tm)>0:
					find_condi.update({"log.uptime":tm})
				if get_dict.has_key("skippg"):
					skippg=int(get_dict["skippg"][0])
				db=get_db("foundation")
				ttlr=db.cssadv.find(find_condi).count()
				ttlpg=int(ceil(ttlr/eachpg))
				context.update({"ttlpg":range(ttlpg)})
				csstask=get_dict["csstask"][0]
				showlist0=list(db.cssadv.find(find_condi).skip(eachpg*skippg).sort("log.uptime",DESCENDING).limit(eachpg))
				showlist=list(mid_str(v) for v in showlist0)
				context.update({"showlist":showlist,"csstask":csstask,"status":status})
				print "ttlr:%s,ttlpg:%s,skippg:%s,eachpg:%s"%(ttlr,ttlpg,skippg,eachpg)
			else:
				pass
			return HttpResponse(temp_cal.render(context,request)) 
	else:
		return redirect(tl)
def cssadvupload(request):
	save_request(request)
	tl=testlog(request)
	if tl==True:
		pass
	else:
		return redirect(tl)
	context=dict()
	if request.method=="GET":
		get_dict=dict(request.GET)
		if get_dict.has_key("backmsg"):
			backmsg=get_dict["backmsg"][0]
			context.update({"backmsg":backmsg})
	if request.method=="POST":
		post_dict=dict(request.POST)
		if post_dict.has_key("csstask"):
			csstask=post_dict["csstask"][0]
			thefile=request.FILES["fileup"]
			if thefile.size>5000000:
				print "The upload file is too large"
				return redirect("/cssadvupload?backmsg=文件不得大于5MB")
			else:
				filepath=thefile.temporary_file_path()
				print "The filepath is %s"%(filepath)
			if csstask=="contact":
				cssdf=pd.read_excel(filepath)
				context.update({"data_preview":cssdf.to_html()})
				rows=len(cssdf)
				print "%s rows in the sheet"%(rows)
				rowdicts=list()
				db=get_db("foundation")
				for i in range(rows):
					rowdict=dict(cssdf.loc[i])
					rmlist=list()
					for k,v in rowdict.iteritems():
						try:
						 	if np.isnan(v):
						 		rmlist.append(k)
						except:
							pass
#					print rmlist
					for rk in rmlist:
						del rowdict[rk]
#					print rowdict
#					for k,v in rowdict.iteritems():
#						print "%s:	%s"%(k,v)
#					print "==========line========="
					rowdict.update({"log":{
						"upsu":request.session["mail"],
						"upip":request.META["REMOTE_ADDR"],
						"uptime":utc8(),
						},
						"csstask":csstask,
						})
					rowdict.update({"status":"0"})
					db.cssadv.insert(rowdict)
					print rowdict
					rowdicts.append(rowdict)
			elif csstask=="user":
				cssdf=pd.read_excel(filepath)
				if "联系电话1" not in list(cssdf.columns):
					return redirect("/cssadvupload?backmsg=上传文件不是标准的用户信息编辑表")
				context.update({"data_preview":cssdf.to_html()})
				rows=len(cssdf)
				#Remove the duplictes of the admins
				admins=list(set(cssdf[u"admin"]))
				admindf=dict()
				userids=dict()
				rowdict=dict()
				rowdf=dict()
				db=get_db("foundation")
				for adm in admins:
					admindf[adm]=cssdf[cssdf.admin.isin([adm])]
					print "[Admin User Name]:%s"%(adm)
					userids[adm]=list(set(admindf[adm][u"userid"]))
					for uid in userids[adm]:
						print ">>>[User ID]:%s"%(uid)
						rowdf[adm]=dict()
						rowdf[adm][uid]=admindf[adm][admindf[adm].userid.isin([uid])]
						rowdict[adm]=dict()
						rowdict[adm][uid]=dict()
						alist=list()
						ulist=list()
						for line in rowdf[adm][uid].index:
							for k,v in dict(rowdf[adm][uid].loc[line]).iteritems():
								if seenan(v):
									if k ==u"成本中心all":
										app_list=list(v.split(","))
										for approver in app_list:
											alist.append(str(int(approver))) 
									elif k in [u"成本中心1",u"成本中心2",u"成本中心3"]:
										alist.append(str(int(v))) 
									elif k in [u"审批人1",u"审批人2",u"审批人3"]:
										ulist.append(str(int(v))) # Minus 100000 for costcenter code in website
									else:
										rowdict[adm][uid].update({k:v})
							if len(alist) != 0:
								alist=list(set(alist))
								astr=",".join(alist)+","
								rowdict[adm][uid].update({u"绑定成本中心":astr})
							if len(ulist) != 0:
								ulist=list(set(ulist))
								ustr=",".join(ulist)+","
								rowdict[adm][uid].update({u"审批人":ustr})
						rowdict[adm][uid].update({
							"log":
								{
								"upsu":request.session["mail"],
								"upip":request.META["REMOTE_ADDR"],
								"uptime":utc8(),
								},
							"csstask":csstask,
							"status":"0",
							})
						db.cssadv.insert(rowdict[adm][uid])
						print "Row Dict [%s][%s]:"%(adm,uid),rowdict[adm][uid]
			elif csstask=="costcenter":
				cssdf=pd.read_excel(filepath)
				if "成本中心名称" not in list(cssdf.columns):
					return redirect("/cssadvupload?backmsg=上传文件不是标准的成本中心编辑表")
				context.update({"data_preview":cssdf.head().to_html()})
				rows=len(cssdf)
				#Remove the duplictes of the admins
				admins=list(set(cssdf[u"admin"]))
				admindf=dict()
				userids=dict()
				rowdict=dict()
				rowdf=dict()
				db=get_db("foundation")
				for adm in admins:
					admindf[adm]=cssdf[cssdf.admin.isin([adm])]
					print "[Admin User Name]:%s"%(adm)
					userids[adm]=list(set(admindf[adm][u"userid"]))
					for uid in userids[adm]:
						print ">>>[User ID]:%s"%(uid)
						rowdf[adm]=dict()
						rowdf[adm][uid]=admindf[adm][admindf[adm].userid.isin([uid])]
						rowdict[adm]=dict()
						rowdict[adm][uid]=dict()
						alist=list()
						for line in rowdf[adm][uid].index:
							for k,v in dict(rowdf[adm][uid].loc[line]).iteritems():
								if seenan(v):
									if k in [u"审批人",u"审批人2",u"审批人3"]:
										alist.append(str(int(v)-100000))
									else:
										rowdict[adm][uid].update({k:v})
							if len(alist) != 0:
								alist=list(set(alist))
								astr=",".join(alist)+","
								rowdict[adm][uid].update({u"审批人":astr})
								#print "[Value Pair]:Key>%s, Val>%s"%(k,v)
						rowdict[adm][uid].update({
							"log":
								{
								"upsu":request.session["mail"],
								"upip":request.META["REMOTE_ADDR"],
								"uptime":utc8(),
								},
							"csstask":csstask,
							"status":"0",
							})
						db.cssadv.insert(rowdict[adm][uid])
						print "Row Dict [%s][%s]:"%(adm,uid),rowdict[adm][uid]
			elif csstask=="addr":
				#for now it's exactly like "contact"
				cssdf=pd.read_excel(filepath)
				context.update({"data_preview":cssdf.to_html()})
				rows=len(cssdf)
				rowdicts=list()
				#Remove the duplictes of the admins
				db=get_db("foundation")
				for i in range(rows):
					rowdict=dict(cssdf.loc[i])
					rmlist=list()
					for k,v in rowdict.iteritems():
						try:
						 	if np.isnan(v):
						 		rmlist.append(k)
						except:
							pass
#					print rmlist
					for rk in rmlist:
						del rowdict[rk]
					rowdict.update({"log":{
						"upsu":request.session["mail"],
						"upip":request.META["REMOTE_ADDR"],
						"uptime":utc8(),
						},
						"csstask":csstask,
						})
					rowdict.update({"status":"0"})
					db.cssadv.insert(rowdict)
					print rowdict
					rowdicts.append(rowdict)
	form=cssupload({"csstask":"contact"})
	temp=loader.get_template("cssadvupload.html")
	context.update({
		"userb":userbar(request),
		"form":form,
		})
	return HttpResponse(temp.render(context,request))
def color_dial(request):
	temp=loader.get_template("color.html")
	return HttpResponse(temp.render({},request))
def cssadvjs(request):
	if request.method=="GET":
		get_dict=dict(request.GET)
		if get_dict.has_key("md"):
			md=get_dict["md"][0]
			rtdict=dict()
			db=get_db("foundation")
			#=========================================
			# return contact information through jsonp
			if md=="contact":
				uid=get_dict["uid"][0]
				dtlist=list(db.cssadv.find({"usern":int(uid),"status":"0","csstask":md},{"name":1,"phone":2,"cellphone":3,"fax":4,"email":5}))
				for line in dtlist:
					line["_id"]=line["_id"].__str__()
				rtdict.update({"data":dtlist})
				rtjson = json.dumps(rtdict, ensure_ascii=False)
				response= HttpResponse(rtjson)
			#======================================
			# return user information through jsonp
			if md=="user":
				admin=get_dict["admin"][0]
				dtlist=list(db.cssadv.find({"status":"0","csstask":md,"admin":admin}))
				for line in dtlist:
					line["id"]=line["_id"].__str__()
					del line["_id"]
					del line["log"]
					del line["csstask"]
					del line["status"]
				rtdict.update({"data":dtlist})
				rtjson = json.dumps(rtdict, ensure_ascii=False)
				response= HttpResponse(rtjson)
			#======================================
			# return user information through jsonp
			if md=="costcenter":
				admin=get_dict["admin"][0]
				dtlist=list(db.cssadv.find({"status":"0","csstask":md,"admin":admin}))
				for line in dtlist:
					line["id"]=line["_id"].__str__()
					del line["_id"]
					del line["log"]
					del line["csstask"]
					del line["status"]
				rtdict.update({"data":dtlist})
				rtjson = json.dumps(rtdict, ensure_ascii=False)
				response= HttpResponse(rtjson)
			#=========================================
			# return address information through jsonp
			if md=='addr':
				admin=get_dict["admin"][0]
				dtlist=list(db.cssadv.find({"status":"0","admin":admin,"csstask":md}))
				for line in dtlist:
					line["id"]=line["_id"].__str__()
					del line["_id"]
					del line["log"]
					del line["csstask"]
					del line["status"]
				rtdict.update({"data":dtlist})
				rtjson = json.dumps(rtdict, ensure_ascii=False)
				response= HttpResponse(rtjson)	
			#======================================
			# an entry was done through jsonp				
			if md=="fbdone":
				uid=get_dict["uid"][0]
				db.cssadv.update({"_id":ObjectId(uid)},{"$set":{"status":"1","log.doneip":request.META["REMOTE_ADDR"]}})
				rtjson =json.dumps({"fb":"Line %s is processed"%(uid)},ensure_ascii=False)
				response= HttpResponse(rtjson)
			#======================================
			# an entry was removed through jsonp				
			if md=="fbremove":
				uid=get_dict["uid"][0]
				db.cssadv.update({"_id":ObjectId(uid)},{"$set":{"status":"-1"}})
				rtjson =json.dumps({"fb":"Line %s is removed"%(uid),"uid":uid},ensure_ascii=False)
				response= HttpResponse(rtjson)
			if md=="userremove":
				uid=get_dict["uid"][0]
				c_err=get_dict["c_err"][0]# Check Error
				userid=dict(db.cssadv.find_one({"_id":ObjectId(uid)},{"_id":0,"userid":1}))["userid"]
				db.cssadv.update({"_id":ObjectId(uid)},{"$set":{"status":"-1"}})
				rtjson =json.dumps({"reply":uid+" Deleted","userid":userid})
				response= HttpResponse(rtjson)
			if md=="errormsg":
				uid=get_dict["uid"][0]
				errormsg=get_dict["errormsg"][0]
				db.cssadv.update({"_id":ObjectId(uid)},{"$set":{"status":"0"},"$push":{"log.error":errormsg}})
				rtjson =json.dumps({"fb":"Line %s is checked"%(uid)},ensure_ascii=False)
				response= HttpResponse(rtjson)
			if md=="changeval":
				uid=get_dict["mid"][0]
				fpath=get_dict["fpath"][0]
				chval=get_dict["chval"][0]
				db.cssadv.update({"_id":ObjectId(uid)},{"$set":{fpath:chval}})
				response= HttpResponse("ok")
	# allow cross origin
	response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
	response["Access-Control-Max-Age"] = "1000"
	response["Access-Control-Allow-Headers"] = "*"
	response["Access-Control-Allow-Origin"] = "*"
	return response
def cadetail(request):
	"""
	the ajax return of lines detail in /cssadvlist page
	"""
	if request.method=="GET":
		get_dict= getdict(request.GET)
		csstask=get_dict["csstask"]
		mid=get_dict["mid"]
		db=get_db("foundation")
		detail=dict(db.cssadv.find_one({"_id":ObjectId(mid)}))
		# load specific html template according to csstask
		temp=loader.get_template("cadetail_%s.html"%(csstask))
		context=dict({
			"mid":mid,
			"csstask":csstask,
			"detail":detail,
			})
		loaded=temp.render(context)
		return HttpResponse(loaded)
		
def cajs(request):
	"""
	return jspage
	"""
	if request.method=="GET":
		get_dict=dict(request.GET)
		md=get_dict["md"][0]
		host=request.META["HTTP_HOST"]
		temp=loader.get_template("cssadv_%s.js"%(md))
		return HttpResponse(temp.render({"host":host}))

od_fields=dict({
u'城市':"city",
u'客户编号':"cid",
u'客户名称':"cnm",
u'客户类型':"ctyp",
u'逾期天数':"oday",
u'账期':"term",
u'未核销金额':"amt",
u'下单日期':"odt",
u'发货日期':"ddt",
u'原始销售订单':"oodr",
u'销售订单':"odr",
u'销售订单金额':"oamt",
u'交货单':"dn",
u'开票日期':"idt",
u'手工发票号':"inv",
u'发票金额':"iamt",
u'发票抬头':"itt",
u'已核销金额':"aamt",
u'发票类型':"ityp",
u'付款方式':"pay",
})
def arupload(request):
	"""
	Upload the Account Receivable Overdue Report
	"""
	tl=testlog(request)
	if tl==True:
		tc=testcnname(request)
		if tc==True:
			mail=request.session["mail"]
			db=get_db("foundation")
			if len(list(db.staff.find({"mail":mail,"auth.ar.a":"1"})))>0:
				temp=loader.get_template("ar/arupload.html")
				context=dict({
					"userb":userbar(request),
					"cnname":request.session["cnname"],
					"fm":ar_upload(),
					})
				if request.method=="GET":
					# The back message setting
					get_dict=dict(request.GET)
					if get_dict.has_key("backmsg"):
						context.update({"backmsg":get_dict["backmsg"][0]})
				if request.method=="POST":
					# If any upload form was detected
					post_dict=dict(request.POST)
					if post_dict.has_key("formtype"):
						if post_dict["formtype"][0]=="overdue":
							#process the time
							exdate=date_parse(post_dict["exdate"][0])
							# process the file
							thefile=request.FILES["fileup"]
							print ">>> The file size is %s Bytes"%(thefile.size)
							filepath=thefile.temporary_file_path()
							print filepath
							df_od=pd.read_excel(filepath)
							df_od=df_od.rename(columns=od_fields) # change the column names accordint to the dictionary
							preview="Head<br>"+df_od.head().to_html()+"<br><br><br>Tail<br><br><br>"+df_od.tail().to_html()
							context.update({"preview":preview})
							#t01=0
							#t02=0
							#t03=0
							#t04=0
							#t05=0
							#t06=0
							for rowid in range(len(df_od)):# store things in line one by one
								#mk=timestamp()*1000
								rd=overdue_line(df_od.loc[rowid].to_dict()) #overdue_line  a function in lib to transform row dict
								#t01+=mk-timestamp()*1000
								#mk=timestamp()*1000
								arids=[rd[idhead] if rd.has_key(idhead) else "e" for idhead in ["odr","dn","inv"]]
								arid="_".join(arids)
								#t02+=mk-timestamp()*1000
								#mk=timestamp()*1000
								clientset=dict((kc,rd[kc]) for kc in ["cnm","city","ctyp","itt","term"] if rd.has_key(kc))
								#t03+=mk-timestamp()*1000
								#mk=timestamp()*1000
								db.arclient.update({
									"cid":rd["cid"]
									},
									{
									"$set":{
										"cid":rd["cid"],
										},
									"$addToSet":clientset,
									},
									upsert=True
									)
								#t04+=mk-timestamp()*1000
								#mk=timestamp()*1000
								line_dt=dict({"arid":arid})
								line_dt.update(dict((kl,rd[kl]) for kl in ["city","ctyp","cid","odr","oodr","inv","dn","iamt","oamt","damt","itt","cnm","odt","idt","ddt"] if rd.has_key(kl)))
								amt_dt=dict({"amt":rd["amt"],"exd":exdate})
								#t05+=mk-timestamp()*1000
								#mk=timestamp()*1000
								line_dt.update(amt_dt)
								db.arline.insert(line_dt)
								#t06+=mk-timestamp()*1000
								#print "R%s,1:%s,2:%s,3:%s,client:%s,5:%s,line:%s"%(rowid,int(t01),int(t02),int(t03),int(t04),int(t05),int(t06))
						elif post_dict["formtype"][0]=="cplist":
							thefile=request.FILES["fileup"]
							print ">>> The file size is %s Bytes"%(thefile.size)
							filepath=thefile.temporary_file_path()
							print filepath
							cpnames="A,C"
							cpdf=pd.read_excel(filepath,parse_cols=cpnames)
							# Rename the columns
							cpdf=cpdf.rename(columns={u"客户编号":u"cid",u"是否CP":u"cp"})
							context.update({"preview":cpdf.head().to_html()})
							for cprow in range(len(cpdf)):
								db.cplist.update({"cid":dict(cpdf.loc[cprow])["cid"]},dict(cpdf.loc[cprow]),upsert=True)
							print "db.splist.update done"
						elif post_dict["formtype"][0]=="arbd":
							#process the time
							exdate=date_parse(post_dict["exdate"][0])
							# process the file
							thefile=request.FILES["fileup"]
							print ">>> The file size is %s Bytes"%(thefile.size)
							filepath=thefile.temporary_file_path()
							print filepath
							arnames="A,G,L,M,AC,AG,AH"
							ardf=pd.read_excel(filepath,sheetname="TOTAL AR",parse_cols=arnames)
							# Rename the arbreakdown
							ardf=ardf.rename(columns={
								u"City":u"city",
								u"本币金额":u"amt",
								u"客户":u"cid",
								u"客户描述":u"cname",
								u"BU":u"bu",
								u"账期天数":u"term",
								u"aging P7 end":u"age",
								})
							ucnames="E,F,K,P,Q,R,S,T,U"
							ucdf=pd.read_excel(filepath,sheetname="TOTAL UNAPL CASH",parse_cols=ucnames)
							# Rename the unapplied cash
							ucdf=ucdf.rename(columns={
								u"bu":u"bu",
								u"Aging":u"age",
								u"本币金额":u"amt",
								u"公司代码":u"citid",
								u"总账科目":u"gac",
								u"客户":u"cname",
								u"客户号":u"cid",
								u"票据抬头":u"ttl",
								u"是否关联方":u"inter",
								})
							# Load ar and unapplied cash information to the database
							db.armonth.remove({"exyear":exdate.year,"exmon":exdate.month})
							db.ucmonth.remove({"exyear":exdate.year,"exmon":exdate.month})
							for arrow in range(len(ardf)):
								ardict=ardf.loc[arrow].to_dict()
								ardict.update({"exyear":exdate.year,"exmon":exdate.month})
								db.armonth.insert(ardict)
								#print "AR Breakdown Row No:%s."%(arrow)
							for ucrow in range(len(ucdf)):
								ucdict=ucdf.loc[ucrow].to_dict()
								ucdict.update({"exyear":exdate.year,"exmon":exdate.month})
								db.ucmonth.insert(ucdict)
								#print "Unapplied Cash Row No:%s."%(ucrow)
							preview="AR Breakdown<br>"+ardf.head().to_html()+"<br>"+ucdf.head().to_html()
							context.update({"preview":preview})
				return HttpResponse(temp.render(context,request))
			else:
				return redirect(u"/?backmsg=用户没有相应的权限")
		else:
			return redirect("/userinfo")
	else:
		return redirect(tl)

def viewclient(request):
	tl=testlog(request)
	if tl==True:
		tc=testcnname(request)
		if tc==True:
			db=get_db("foundation")
			if len(list(db.staff.find({"mail":request.session["mail"],"auth.ar.r":"1"})))>0:
				get_dict=dict(request.GET)
				if get_dict.has_key("cid"):
					cid=get_dict["cid"][0]
					temp=loader.get_template("ar/client.html")
					context=dict({"userb":userbar(request)})
					clientl=list(db.arclient.find({"cid":cid}))
					if len(clientl)==0:
						return HttpResponse("No such client:<br>%s"%(cid))
					else:
						arclient=dict(clientl[0])
						context.update({"arclient":arclient})
					return HttpResponse(temp.render(context,request))
			else:
				return redirect("/?backmsg=您没有权限")
		else:
			return redirect("/userinfo")
	else:
		return redirect(tl)

def arreport(request):
	tl=testlog(request)
	if tl==True:
		tc=testcnname(request)
		if tc==True:
			db=get_db("foundation")
			if len(list(db.staff.find({"mail":request.session["mail"],"auth.ar.r":"1"})))>0:
				get_dict=dict(request.GET)
				if get_dict.has_key("md")==False:
					temp=loader.get_template("ar/reportmajor.html")
					context={"userb":userbar(request)}
					periods=list(db.armonth_age_rp.find({},{"_id":0,"year":1,"month":2}).sort([("year",DESCENDING),("month",DESCENDING)]))
					context.update({"periods":periods})
					if get_dict.has_key("backmsg"):
						context.update({"backmsg":get_dict["backmsg"][0]})
					return HttpResponse(temp.render(context))
				md=get_dict["md"][0]
				if md=="armonth":
					temp=loader.get_template("ar/%s.html"%(md))
					context={"userb":userbar(request)}
					try:
						month=int(get_dict["month"][0])
						year=int(get_dict["year"][0])
					except:
						return redirect("/arreport")
					# Build the pipeline block one by one
					if db.armonth_rp.find({"year":year,"month":month}).count()>0 and get_dict.has_key("recalc")==False:
						armonth_df=pickle.loads(dict(db.armonth_rp.find_one({"year":year,"month":month},{"_id":0,"df":1}))["df"])
					else:
						db.armonth_rp.remove({"year":year,"month":month})
						db.armonth_age_rp.remove({"year":year,"month":month})
						if db.armonth.find({"exyear":year,"exmon":month},{"cid":1}).limit(10).count()==0:
							return redirect("/arreport?backmsg=No Such Report")
						bu_list=[u"SEA",u"SBA",u"GOV",u"SBD",u"国网项目",u"移动项目",u"其他CP项目"]
						match_dict0=dict({"$match":{
							"exyear":year,
							"exmon":month,
							"bu":{"$in":bu_list},
							"age":{"$lte":0},
							}})
						match_dict1=dict({"$match":{
							"exyear":year,
							"exmon":month,
							"bu":{"$in":bu_list},
							"age":{"$gt":0},
							}})
						match_dict2=dict({"$match":{
							"exyear":year,
							"exmon":month,
							"bu":{"$in":bu_list},
							"age":{"$gt":90},
							}})
						match_dict3=dict({"$match":{
							"exyear":year,
							"exmon":month,
							"bu":{"$in":bu_list},
							"age":{"$gt":180},
							}})
						match_dict4=dict({"$match":{
							"exyear":year,
							"exmon":month,
							"bu":{"$in":bu_list},
							}})
						group_dict=dict({"$group":{
							"_id":"$bu",
							"amt":{"$sum":"$amt"},
							}})
						pivot=list()
						for i in range(5):
							pivot.append(list(db.armonth.aggregate([eval("match_dict%s"%(i)),group_dict])))
						armonth_df=pd.DataFrame(pivot[0]).rename(columns={u"amt":u"Current"})
						armonth_df=pd.merge(armonth_df,(pd.DataFrame(pivot[1]).rename(columns={u"amt":u"Days 0+"})),on="_id",how="outer")
						armonth_df=pd.merge(armonth_df,(pd.DataFrame(pivot[2]).rename(columns={u"amt":u"Days 90+"})),on="_id",how="outer")
						armonth_df=pd.merge(armonth_df,(pd.DataFrame(pivot[3]).rename(columns={u"amt":u"Days 180+"})),on="_id",how="outer")
						armonth_df=pd.merge(armonth_df,(pd.DataFrame(pivot[4]).rename(columns={u"amt":u"Total"})),on="_id",how="outer")
						armonth_df=armonth_df.round(0).rename(columns={u"_id":u"BU"}).set_index(u"BU").fillna(value=0)
						armonth_df=armonth_df.sort_index(ascending=True)
						db.armonth_rp.insert({"year":year,"month":month,"df":pickle.dumps(armonth_df)})
					context.update({"pivot":armonth_df.to_html(float_format=lambda x:'{:,}'.format(int(x/1000))).replace('border="1"','border="0"')})
					# print match_dict0,match_dict1,match_dict3
					chart_data=dict()
					#
					cd_totalar=armonth_df["Total"].reset_index().rename(columns={"BU":"name","Total":"value"})
					cd_totalar=json.dumps(list(dict(cd_totalar.loc[i]) for i in range(len(cd_totalar))), ensure_ascii=False)
					chart_data.update({"ar_month_total":cd_totalar})
					#
					cd_gt0_ar=armonth_df["Days 0+"].reset_index().rename(columns={"BU":"name","Days 0+":"value"})
					cd_gt0_ar=json.dumps(list(dict(cd_gt0_ar.loc[i]) for i in range(len(cd_gt0_ar))), ensure_ascii=False)
					chart_data.update({"ar_month_gt0":cd_gt0_ar})
					#
					cd_gt90_ar=armonth_df["Days 90+"].reset_index().rename(columns={"BU":"name","Days 90+":"value"})
					cd_gt90_ar=json.dumps(list(dict(cd_gt90_ar.loc[i]) for i in range(len(cd_gt90_ar))), ensure_ascii=False)
					chart_data.update({"ar_month_gt90":cd_gt90_ar})
					#
					cd_gt180_ar=armonth_df["Days 180+"].reset_index().rename(columns={"BU":"name","Days 180+":"value"})
					cd_gt180_ar=json.dumps(list(dict(cd_gt180_ar.loc[i]) for i in range(len(cd_gt180_ar))), ensure_ascii=False)
					chart_data.update({"ar_month_gt180":cd_gt180_ar})
					#####
					bu_list=[u"SEA",u"SBA",u"GOV",u"SBD",u"国网项目",u"移动项目",u"其他CP项目"]
					line_color=dict({
							u"SEA":u"%s,%s,%s"%(247,145,170),
							u"SBA":u"%s,%s,%s"%(1,243,243),
							u"SBD":u"%s,%s,%s"%(255,1,243),
							u"GOV":u"%s,%s,%s"%(253,246,36),
							u"国网项目":u"%s,%s,%s"%(255,114,0),
							u"移动项目":u"%s,%s,%s"%(38,248,1),
							u"其他CP项目":u"%s,%s,%s"%(252,16,12),
							})
					if db.armonth_age_rp.find({"year":year,"month":month}).count()>0:
						age_curve_df=pickle.loads(dict(db.armonth_age_rp.find_one({"year":year,"month":month},{"_id":0,"df":1}))["df"])
					else:
						agelist=list(db.armonth.find({"exmon":month,"exyear":year,"bu":{"$in":bu_list},},{"_id":0,"bu":1,"amt":2,"age":3}))
						age_curve_df=pd.DataFrame(agelist).round(0)
						#Cutting seperators
						bins=[-200000]
						bins+=list((i)*10 for i in range(37))
						bins+=[200000]
						#Categories
						cates=["Current"]
						cates+=list("%s~%s Days"%((i)*10,(i+1)*10) for i in range(36))
						cates+=["360 Days +"]
						beforecut=age_curve_df[age_curve_df.columns[0]]
						age_curve_df["slot"]=pd.cut(beforecut,bins,labels=cates)
						age_curve_df=pd.pivot_table(age_curve_df,index=u"bu",columns=u"slot",values=u"amt", aggfunc=np.sum).fillna(value=0).round(0)
						db.armonth_age_rp.insert({"year":year,"month":month,"df":pickle.dumps(age_curve_df)})
					#print age_curve_df
					acdf=age_curve_df.to_html(float_format=lambda x:'{:,}'.format(int(x/1000))).replace('border="1"','border="0"')
					age_cols=json.dumps(list(age_curve_df.columns), ensure_ascii=False)
					age_curve_df_t=age_curve_df.T
					age_rows=json.dumps(list(age_curve_df_t.columns), ensure_ascii=False)
					age_datas=dict((c,dict({
						"data":list(age_curve_df_t[c]),
						"rgb":line_color[c],
						})) for c in age_curve_df_t.columns)
					#print age_datas
					chart_data.update({"acdf":acdf,"age_cols":age_cols,"age_datas":age_datas,"age_rows":age_rows})
					# Aggregate all the chart data
					context.update({"chart":chart_data,"year":year,"month":month})
				if md=="ucmonth":
					temp=loader.get_template("ar/%s.html"%(md))
					context={"userb":userbar(request)}
					try:
						month=int(get_dict["month"][0])
						year=int(get_dict["year"][0])
					except:
						return redirect("/arreport")
					if db.ucmonth_rp.find({"year":year,"month":month}).count()>0 and get_dict.has_key("recalc")==False:
						ucmonth_df=pickle.loads(dict(db.ucmonth_rp.find_one({"year":year,"month":month},{"_id":0,"df":1}))["df"])
					else:
						db.ucmonth_rp.remove({"year":year,"month":month})
						db.ucmonth_age_rp.remove({"year":year,"month":month})
						if db.ucmonth.find({"exyear":year,"exmon":month},{"cid":1}).limit(10).count()==0:
							return redirect("/arreport?backmsg=No Such Report")
						bu_list=[u"SEA",u"SBA",u"GOV",u"SBD",u"国网项目",u"移动项目",u"其他CP项目"]
						match_dict0=dict({"$match":{
							"exyear":year,
							"exmon":month,
							"BU":{"$in":bu_list},
							"age":{"$lte":6},
							}})
						match_dict1=dict({"$match":{
							"exyear":year,
							"exmon":month,
							"BU":{"$in":bu_list},
							"age":{"$gt":6},
							}})
						match_dict2=dict({"$match":{
							"exyear":year,
							"exmon":month,
							"BU":{"$in":bu_list},
							"age":{"$gt":90},
							}})
						match_dict3=dict({"$match":{
							"exyear":year,
							"exmon":month,
							"BU":{"$in":bu_list},
							"age":{"$gt":180},
							}})
						match_dict4=dict({"$match":{
							"exyear":year,
							"exmon":month,
							"BU":{"$in":bu_list},
							}})
						group_dict=dict({"$group":{
							"_id":"$BU",
							"amt":{"$sum":"$amt"},
							}})
						pivot=list()
						for i in range(5):
							pivot.append(list(db.ucmonth.aggregate([eval("match_dict%s"%(i)),group_dict])))
						ucmonth_df=pd.DataFrame(pivot[0]).rename(columns={u"amt":u"Current"})
						ucmonth_df=pd.merge(ucmonth_df,(pd.DataFrame(pivot[1]).rename(columns={u"amt":u"Days 6+"})),on="_id",how="outer")
						ucmonth_df=pd.merge(ucmonth_df,(pd.DataFrame(pivot[2]).rename(columns={u"amt":u"Days 90+"})),on="_id",how="outer")
						ucmonth_df=pd.merge(ucmonth_df,(pd.DataFrame(pivot[3]).rename(columns={u"amt":u"Days 180+"})),on="_id",how="outer")
						ucmonth_df=pd.merge(ucmonth_df,(pd.DataFrame(pivot[4]).rename(columns={u"amt":u"Total"})),on="_id",how="outer")
						ucmonth_df=ucmonth_df.round(0).rename(columns={u"_id":u"BU"}).set_index(u"BU").fillna(value=0)
						ucmonth_df=ucmonth_df.sort_index(ascending=True)
						db.ucmonth_rp.insert({"year":year,"month":month,"df":pickle.dumps(ucmonth_df)})
					context.update({"pivot":ucmonth_df.to_html(float_format=lambda x:'{:,}'.format(int(x/1000))).replace('border="1"','border="0"')})
					# print match_dict0,match_dict1,match_dict3
					chart_data=dict()
					#
					cd_totalar=ucmonth_df["Total"].reset_index().rename(columns={"BU":"name","Total":"value"})
					cd_totalar=json.dumps(list(dict(cd_totalar.loc[i]) for i in range(len(cd_totalar))), ensure_ascii=False)
					chart_data.update({"ar_month_total":cd_totalar})
					#
					cd_gt0_ar=ucmonth_df["Days 6+"].reset_index().rename(columns={"BU":"name","Days 6+":"value"})
					cd_gt0_ar=json.dumps(list(dict(cd_gt0_ar.loc[i]) for i in range(len(cd_gt0_ar))), ensure_ascii=False)
					chart_data.update({"ar_month_gt0":cd_gt0_ar})
					#
					cd_gt90_ar=ucmonth_df["Days 90+"].reset_index().rename(columns={"BU":"name","Days 90+":"value"})
					cd_gt90_ar=json.dumps(list(dict(cd_gt90_ar.loc[i]) for i in range(len(cd_gt90_ar))), ensure_ascii=False)
					chart_data.update({"ar_month_gt90":cd_gt90_ar})
					#
					cd_gt180_ar=ucmonth_df["Days 180+"].reset_index().rename(columns={"BU":"name","Days 180+":"value"})
					cd_gt180_ar=json.dumps(list(dict(cd_gt180_ar.loc[i]) for i in range(len(cd_gt180_ar))), ensure_ascii=False)
					chart_data.update({"ar_month_gt180":cd_gt180_ar})
					#####
					bu_list=[u"SEA",u"SBA",u"GOV",u"国网项目",u"移动项目",u"其他CP项目"]
					line_color=dict({
							u"SEA":u"%s,%s,%s"%(247,145,170),
							u"SBA":u"%s,%s,%s"%(1,243,243),
							u"GOV":u"%s,%s,%s"%(253,246,36),
							u"国网项目":u"%s,%s,%s"%(255,114,0),
							u"移动项目":u"%s,%s,%s"%(38,248,1),
							u"其他CP项目":u"%s,%s,%s"%(252,16,12),
							})
					if db.ucmonth_age_rp.find({"year":year,"month":month}).count()>0:
						age_curve_df=pickle.loads(dict(db.ucmonth_age_rp.find_one({"year":year,"month":month},{"_id":0,"df":1}))["df"])
					else:
						agelist=list(db.ucmonth.find({"exmon":month,"exyear":year,"BU":{"$in":bu_list},},{"_id":0,"BU":1,"amt":2,"age":3}))
						age_curve_df=pd.DataFrame(agelist).round(0)
						#Cutting seperators
						bins=[-200000]
						bins+=list((i)*10 for i in range(37))
						bins+=[200000]
						#Categories
						cates=["Current"]
						cates+=list("%s~%s Days"%((i)*10,(i+1)*10) for i in range(36))
						cates+=["360 Days +"]
						beforecut=age_curve_df[u"age"]
						age_curve_df["slot"]=pd.cut(beforecut,bins,labels=cates)
						age_curve_df=pd.pivot_table(age_curve_df,index=u"BU",columns=u"slot",values=u"amt", aggfunc=np.sum).fillna(value=0).round(0)
						db.ucmonth_age_rp.insert({"year":year,"month":month,"df":pickle.dumps(age_curve_df)})
					#print age_curve_df
					acdf=age_curve_df.to_html(float_format=lambda x:'{:,}'.format(int(x/1000))).replace('border="1"','border="0"')
					age_cols=json.dumps(list(age_curve_df.columns), ensure_ascii=False)
					age_curve_df_t=age_curve_df.T
					age_rows=json.dumps(list(age_curve_df_t.columns), ensure_ascii=False)
					age_datas=dict((c,dict({
						"data":list(age_curve_df_t[c]),
						"rgb":line_color[c],
						})) for c in age_curve_df_t.columns)
					#print age_datas
					chart_data.update({"acdf":acdf,"age_cols":age_cols,"age_datas":age_datas,"age_rows":age_rows})
					# Aggregate all the chart data
					context.update({"chart":chart_data,"year":year,"month":month})
				if get_dict.has_key("backmsg"):
					context.update({"backmsg":get_dict["backmsg"][0]})
				return HttpResponse(temp.render(context,request))
			else:
				return redirect("/?backmsg=您没有权限")
		else:
			return redirect("/userinfo")
	else:
		return redirect(tl)

def button(request):
	get_dict=dict(request.GET)
	btn=get_dict["btn"][0]
	eval(btn)()
	return HttpResponse("ok")

def arreport_aj(request):
	tl=testlog(request)
	if tl==True:
		tc=testcnname(request)
		if tc==True:
			get_dict=dict(request.GET)
			if get_dict["md"][0]=="see3d":
				db=get_db("foundation")
				span=int(get_dict["month_span"][0])
				# year3d=get_dict["year3d"][0]
				# month3d=get_dict["month3d"][0]
				age_dfs=list(db.armonth_age_rp.find({}).sort([("year",DESCENDING),("month",DESCENDING)]).limit(span))
				temp=loader.get_template("ar/see3d.js")
				context=dict()
				true_span=len(age_dfs)
				alldf=pd.DataFrame()
				for month in range(true_span):
					df=pickle.loads(age_dfs[month]["df"])
					alldf["P:%s,Year:%s"%(age_dfs[month]["month"],age_dfs[month]["year"],)]=df.sum(axis=0)
				alldf=alldf.drop(["Current"])
				huedf=(220-(alldf-alldf.min())/(alldf.max()-alldf.min())*200).astype(int)
				cols=list(alldf.columns)
				indices=list(alldf.index)
				row_len=len(indices)
				dataarray=list()
				for x in range(true_span):
					for y in range(row_len):
						#dataarray.append([cols[x],indices[y],alldf.iloc[y,x]])
						dataarray.append({
							"value":[x,y,alldf.iloc[y,x]],
							"itemStyle":{"color":"hsla(%s,1,0.45,1)"%(huedf.iloc[y,x])},
							})
				print "span:%s"%(true_span)
				dataarray=json.dumps(dataarray, ensure_ascii=False)
				context.update({"cols":tojson
					(cols),"indices":tojson(indices),"row_len":row_len,"col_len":true_span,"data":dataarray})
				return HttpResponse(temp.render(context))
			else:
				return redirect("/?backmsg=No Such Report")
		else:
			return redirect("/userinfo")
	else:
		return redirect(tl)

def tojson(dictorlist):
	return json.dumps(dictorlist,ensure_ascii=False)

def sqlupdate(request):
	tl=testlog(request)
	if tl==True:
		tc=testcnname(request)
		if tc==True:
			temp=loader.get_template("ar/odupload.html")
			context=dict({
					"userb":userbar(request),
					"cnname":request.session["cnname"],
					"fm":od_upload(),
					})
			if request.method=="GET":
					# The back message setting
				get_dict=dict(request.GET)
				if get_dict.has_key("backmsg"):
					context.update({"backmsg":get_dict["backmsg"][0]})
			if request.method=="POST":
					# If any upload form was detected
					post_dict=dict(request.POST)
					if post_dict.has_key("formtype"):
						if post_dict["formtype"][0]=="overdue":
							# process the file
							thefile=request.FILES["fileup"]
							print ">>> The file size is %s Bytes"%(thefile.size)
							filepath=thefile.temporary_file_path()
							print filepath
							od=pd.read_excel(filepath)
							od.index.name="id"
							od.fillna("")
							# Create 2 columns to give the invoice property
							inv2amt=od[[u"手工发票号",u'未核销金额']].rename(columns={u"未核销金额":u"invamt"}).groupby(u"手工发票号").sum().reset_index()
							inv2cnt=od[[u"手工发票号",u'客户编号']].rename(columns={u"客户编号":u"invclient"}).groupby(u"手工发票号").count().reset_index()
							od=pd.merge(od,inv2amt,on=u"手工发票号",how="inner")
							od=pd.merge(od,inv2cnt,on=u"手工发票号",how="inner")
							od.index.name="id"
							# connect to the database
							engine=ce("mysql+pymysql://ray:46ym46ydq8@10.10.5.101/exceldata?charset=utf8")
							conn=engine.connect()
							date_format=sqlalchemy.types.String(length=20)
							dtype_dict=dict({
								u"客户编号":sqlalchemy.types.String(length=12),
								u"客户类型":sqlalchemy.types.String(length=50),
								u'逾期天数':sqlalchemy.types.Integer(),
								u'invclient':sqlalchemy.types.Float(precision=0,asdecimal=True),
								u'账期':sqlalchemy.types.String(length=50),
								u'未核销金额':sqlalchemy.types.Float(precision=2,asdecimal=True),
								u'已核销金额':sqlalchemy.types.Float(precision=2,),
								u'销售订单金额':sqlalchemy.types.Float(precision=2,),
								u'发票金额':sqlalchemy.types.Float(precision=2,),
								u'invamt':sqlalchemy.types.Float(precision=2,),
								u'销售订单':sqlalchemy.types.String(length=50),
								u'原始销售订单':sqlalchemy.types.String(length=100),
								u'手工发票号':sqlalchemy.types.String(length=50),
								u'交货单':sqlalchemy.types.String(length=50),
								u'发票类型':sqlalchemy.types.String(length=50),
								u'客户名称':sqlalchemy.types.String(length=255),
								u'发票抬头':sqlalchemy.types.String(length=255),
								u'城市':sqlalchemy.types.String(length=10),
								u'开票日期':date_format,
								u'下单日期':date_format,
								u'发货日期':date_format,
								u'付款方式':sqlalchemy.types.String(length=50),
								u"id":sqlalchemy.types.Integer(),
							})
							od.to_sql("overdue_today",conn,if_exists="replace",dtype=dtype_dict)
							preview="Overdue Report<br>"+od.head().to_html()
							context.update({"preview":preview})
			return HttpResponse(temp.render(context,request))
		else:
			return redirect("/userinfo")
	else:
		return redirect(tl)