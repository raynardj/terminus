# -*- coding: utf-8 -*-
#raynard's library for major
from django.template import loader
from django.shortcuts import redirect
from pymongo import MongoClient
from pymongo import ASCENDING
from pymongo import DESCENDING
from config import mapping
import os,sys,platform
from math import ceil
from bson.objectid import ObjectId #ObjectId(str) of MongoDB, Hexidecimal
from datetime import datetime,tzinfo,timedelta
from time import time,sleep
# forms2.py is a symbolic link to forms.py to distinguish from the word "forms"
from .forms2 import task_write
from .forms2 import rich_form
from .forms2 import user_auth_apply
from .forms2 import table_book_filter
from .forms2 import office_use_detail
from .forms2 import fm_officeuse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from hashlib import sha512
from base64 import urlsafe_b64encode
from django.forms.utils import flatatt
from django import forms as fm
from collections import OrderedDict
from django.forms.fields import Field, FileField
import xlsxwriter
from xlrd.sheet import Sheet
from urllib2 import urlopen		#the class to open url
from BeautifulSoup import BeautifulSoup	#the class to parse url
import json
import numpy as np
import pandas as pd
from multiprocessing import Process as multip
def dict_reverse(dict1):
	dict2=dict((v,k) for k,v in dict1.iteritems())
	return dict2
num20=list(str(v+1) for v in range(20))
a2z=["a","b","c","d","e","f","g","h","i","j","k"]
stage_symbol=["dead","0"]
alphabate=mapping.a2z.val
num2alpha=dict((k,alphabate[k]) for k in range(25))
userhome='/home/salvor'

process_status=mapping.process_status.val
decision_dict=mapping.decision_dict.val

process_dict=dict(
{
	"officeuse":u"行政领用",
	"auth":u"权限申请",
})
grab_fields=dict({
	"分类id":'cateid',
    "品牌id":'brandid',
    "商品名称":'itemname',
    "商品ID":'pro_id',
    "商品售价":'price',
    "商品图片url":'pic_src',
    "分类名":'catename',
    "品牌名":'brandname',
    "网络价":'lineprice',
    "收藏人数":'collects',
    "商品下架时间":'offline',
	})
cssadv_user=dict({
u"用户ID":u"userId",
u"绑定成本中心":u"costArrayStr",
u"登录名":u"userSysName",
u"密码":u"password",
u"确认密码":u"confirm_password",
u"姓名":u"userRealName",
u"性别":u"sex",
u"联系电话1":u"dftPhone1",
u"分机1":u"dftPhone1Ext",
u"联系电话2":u"dftPhone2",
u"分机2":u"dftPhone2Ext",
u"传真":u"faxNbr",
u"分机3":u"faxNbrExt",
u"手机":u"cellPhoneNbr",
u"Email":u"userEmail",
u"办公耗材":u"userProdAccessList[0].status",
u"电脑及配件":u"userProdAccessList[1].status",
u"通讯设备/手机":u"userProdAccessList[2].status",
u"食品饮料":u"userProdAccessList[3].status",
u"劳防用品":u"userProdAccessList[4].status",
u"卡券及商务礼品":u"userProdAccessList[5].status",
u"办公用纸":u"userProdAccessList[6].status",
u"办公文具":u"userProdAccessList[7].status",
u"办公设备":u"userProdAccessList[8].status",
u"数码设备":u"userProdAccessList[9].status",
u"办公家电":u"userProdAccessList[10].status",
u"生活用品":u"userProdAccessList[11].status",
u"办公家具":u"userProdAccessList[12].status",
u"审批方式":u"isNeetApprove",
u"审批人":u"approveArrayStr",
u"审批金额":u"approveAmt",
u"单笔订单采购限额":u"oneorderLmtAmt",
u"财政年起始月份":u"startMonth",
u"月采购限额有无":u"monthlimit",
u"月采购限额":u"monthlyLmtAmt",
u"月采购余额跨月累计":u"isCumulateMonthLmt",
u"季度采购额度":u"quarterLimitFlag",
u"Q1":u"quarterQ1Amt",
u"Q2":u"quarterQ2Amt",
u"Q3":u"quarterQ3Amt",
u"Q4":u"quarterQ4Amt",
u"季采购余额跨月累计":u"quarterAccumulativeFlag",
u"年采购限额有无":u"yearlimit",
u"年采购限额":u"yearlyLmtAmt",
u"查看报表":u"isAcsRpt",
u"显示热销商品":u"isDispRecomprod",
u"显示广告banner":u"isDispSalePrmt",
})
cssadv_user_r=dict_reverse(cssadv_user)
def save_request(request):
	"""
	A function to record traces
	stored in db trace, collection:visit_co
	"""
	subset_keys=[		#keys of the subset
	#"SERVER_NAME",
	"HTTP_REFERER",
	#"REMOTE_ADDR",		#User's IP address
	"HTTP_USER_AGENT",
	#"SERVER_PORT",
	"CSRF_COOKIE",
	]
	clie=MongoClient()
	db_trace=clie["trace"]
	visit_co=db_trace.visit
	req0=dict(request.META)
	rm_addr=req0["REMOTE_ADDR"]
	req=dict((k,req0[k]) for k in subset_keys if req0.has_key(k))
	# record down the GET and POST dict
	if request.method=="GET":
		req.update({
			"M":"GET",
			"GET":dict(request.GET),
			})
	elif request.method=="POST":
		req.update({
			"M":"POST",
			"GET":dict(request.POST),
			})
	try:
		session_dict=dict(request.session)
		sd2=dict((k,session_dict[k]) for k in ["cnname","mail"] if session_dict.has_key(k))
		req.update({"session":sd2})
	except:
		pass
	req.update({"time":utc8()})
	visit_co.update({"REMOTE_ADDR":rm_addr},{"$push":{"log":req}},upsert=True)
	return req

def get_db(database):
	"""
	A quick way to get MongoDb Client link
	"""
	clientmg=MongoClient()
	db=clientmg[database]
	return db

def utc8():
	# Return current time
	dt = datetime.now()
	return dt#
def mystrify(incode):
	# hash
	t=sha512()
	t.update(incode+"#bc87q)f^")
	outcode=urlsafe_b64encode(t.digest())
	return outcode
def wall_print(request,wall_doc):
	"""
	Print out the wall on personal page,
	load the brick template
	Format the wall time
	"""
	try:
		temp_wall=loader.get_template("parts/wall_brick.html")
		if wall_doc.has_key("time"):
			wall_doc["time"]=wall_doc["time"].strftime("%Y-%m-%d %H:%M")
		rt=temp_wall.render(wall_doc)
		if wall_doc.has_key("_id"):
			wall_doc["id"]=wall_doc["_id"].__str__()
		rt=temp_wall.render(wall_doc)
	except:
		rt=''
	return rt

def index_load(request):
	tl=testlog(request)
	tc=testcnname(request)
	db=get_db("foundation")
	if tl==True:
		context=dict()
		if request.method=="GET":
			get_dict=dict(request.GET)
			if get_dict.has_key("mail"):
				mail=get_dict["mail"][0]
			else:
				mail=None
			if get_dict.has_key("owner"):
				owner=get_dict["owner"][0]
			else:
				owner=None
			if get_dict.has_key("backmsg"):
				backmsg=get_dict["backmsg"][0]
				context.update({"backmsg":backmsg})
		if (owner==None and mail==None):
			ownermail=request.session["mail"]
			po_cn=request.session["cnname"]
			selfown=True
		elif (owner!=None and len(str(owner))>10):
			owner_doc=dict(db.staff.find_one({"_id":ObjectId(owner)},{"cnname":1,"mail":2}))
			ownermail=owner_doc["mail"]
			po_cn=owner_doc["cnname"]
			selfown=False
		elif mail!=None:
			ownermail=mail
			owner_doc=dict(db.staff.find_one({"mail":ownermail},{"cnname":1,"mail":2}))
			po_cn=owner_doc["cnname"]
			selfown=False
		gtiers=get_tiers(ownermail)
		await_count=int(db.process.count({"stage_mails":request.session["mail"],"edit":{"$ne":True},"status":{"$nin":["finished","dead","revoked","done"]}}))	
		userb=userbar(request)
		template=loader.get_template('index.html')
		try:
			wallcount=db.wall.count({"wallowner":ownermail})
		except:
			wallcount=1
		wall_page_max=int(ceil(float(wallcount)/float(20)))
		context.update({
			"userb":userbar(request),
			"wallowner":ownermail,
			"po_cn":po_cn,
			"wall_page_max":wall_page_max,
			"gtiers":gtiers,
			"visitorcn":request.session["cnname"]
			})
		if int(await_count) !=0:
			context.update({"await_count":await_count})
		hr=template.render(context,request)
	else:
		hr=tl
	return HttpResponse(hr)

def linklist(link_list):
	"""
	Example
	link_list=[
			[u"新用户","register"],
			[u"忘记密码","register"],
		]
	"""
	template=loader.get_template("linklist.html")
	context={
		"link_dict":link_list,
	}
	output=template.render(context)
	return output

def testlog(request):
	try:
		if request.session["onboard"]==True:
			return True
		else:
			return logout(request)
			#ubout="out"
	except:
		return logout(request)
		#ubout="out"
def testcnname(request):
	try:
		if len(request.session["cnname"])>1:
			return True
		else:
			return cnnamepage(request)
			#ubout="out"
	except:
		return cnnamepage(request)
def testsu(request):
	db=get_db("foundation")
	if int(db.staff.count({"mail":request.session["mail"],"auth.system.a":"1"}))>0:
		rt=True
	elif int(db.staff.count({"leader":request.session["mail"],"auth.system.a":"1"}))>0:
		rt=True
	else:
		rt=False
	return rt
def userbar(request):
	"""
	Return a user bar on top
	Use it as a variable in template
	Preferably right after first <body> tag in templates
	context={"userb":userbar(request)}
	like :  <body>{{ userb }}<div>Other Contents</div></body>
	"""
	context=dict()
	ubtemplate=loader.get_template("userbar.html")
	output=ubtemplate.render(context,request)
	return output
def cnnamepage(request):
	userinfojump=u"/userinfo"
	return userinfojump
def logout(request):
	try:
		request.session.flush()
	except KeyError:
		pass
	logoutjump=u"/login?ra=%s"%(request.get_full_path())
	return logoutjump
def listsum(dictlist,dictkey):
	"""
	sum up every certain dict value in a list of a dict
	1st arguement: a list of dict
	2nd arguement: which key to sum
	"""
	rt=0
	for dictitem in dictlist:
		if dictitem.has_key(dictkey):
			rt=rt+float(dictitem[dictkey])
	return rt
def strid(mongo_out):
	"""
	transform to string id from a mongo output list
	"""
	for line in mongo_out:
		if line.has_key("_id"):
			line["id"]=line["_id"].__str__()
	return mongo_out
def listdate(dictlist,dictkey):
	"""
	transform mongoresult list time to strint time
	"""
	for line in dictlist:
		if line.has_key(dictkey):
			line[dictkey+"s"]=line[dictkey].strftime("%Y-%m-%d")
	return dictlist
class linkbtn:
	def __init__(self,text,link=''):
		"""
		div_attrs: a dictionary, describe the attrs of <div>
		a_attrs:a dictionary, describe the attrs of <a>
		"""
		self.link=link
		if text:
			self.text=text
		else:
			self.text="Button"
		self.div_attrs={"class":"link_div"}
		self.a_attrs={"class":"link_a"}

	def tohtml(self):
		rt=("<div %(div_attrs)s ><a %(a_attrs)s href='%(href)s'>%(text)s</a></div>") % {"div_attrs":flatatt(self.div_attrs),
		 "a_attrs":flatatt(self.a_attrs),
		 "href":self.link,
		 "text":self.text,
		 }
		return rt
def dict2table(input_dict):
	template=loader.get_template("parts/dict2table.html")
	context={"dict":input_dict}
	return template.render(context)
class form_shell(fm.Form):
	pass
class rich_sheet:
	"""
	Enriched xlrd sheet class
	"""
	def __init__(self,sheet):
		self.sheet=sheet
		self.startr=0
		self.startc=0
		self.endr=3
		self.headr=0
		self.fm= None
		self.head_list=None
		self.endc=5
#		if self.endr<2:
#			self.endr=0
#		if self.endc<2:
#			self.endc=0

	def headr(self,headr):
		self.headr=int(headr)
	def as_table(self):
		if self.endr>self.startr and self.endc>self.startc:
			rlist=range(self.startr,self.endr,1)
			clist=range(self.startc,self.endc,1)
			table="<table cellspacing=0 class='preview_table'>"
			for row in rlist:
				table+="<tr>"
				for col in clist:
					table+="<td class='preview_td'>"
					try:
						table+=str(self.sheet.cell_value(row,col))
					except:
						pass	
					table+="</td>"
				table+="</tr>"
			table+="</table>"
			return table
		else:
			return
	def heads(self):
		"""
		Return the heads list(a dictionary)
		"""
		if self.endc>self.startc:
			self.head_list=list()
			clist=range(self.startc,self.endc,1)
			for col in clist:
				if str(self.sheet.cell_value(self.headr,col))!='':
					self.head_list.append({
						"posi":{
							"r":self.headr,
							"c":col,
							},
						"val":str(self.sheet.cell_value(self.headr,col)),
						})
	def field_set(self):
		"""
		Setup the form fields,
		according to the self.head_list.
		"""
		self.heads()
		field_list=list()
		self.fm=form_shell()
		for head_dic in self.head_list:
			self.fm.__new__(fm.CharField,"Hello",{},{})
	def field_tohtml(self):
		"""
		Output the fields to the html
		"""
		self.field_set()
		fhtml='<table>'
		fhtml+=self.fm.as_table()
		fhtml+='</table>'
		return fhtml
def usejs(js_add):
	"""
	Use it like rendere_js=usejs("js/js_file_name.js")
	"""
	jstemp=loader.get_template("js.html")
	rt=jstemp.render({"js_add":js_add})
	#rt="No such template:"+str(js_add)
	return rt

def parse_stb_url(pro_id):
	"""
	A function to parse the staples url
	Since the url input prefix could vary from www to http:// to nothing
	We use the product id as argument
	"""
	stburl="http://www.staples.cn/product/"+str(pro_id)#more standardized url format
	try:
		page=urlopen(stburl)
	except:
		page=u'无法加载'
	soup=BeautifulSoup(page)
	keystr_start=str(soup).find("addGoods")
	if keystr_start>20:
		start_pos=int(keystr_start)+22
		end_pos=str(soup).find("]);",start_pos)-1
		if int(end_pos)>0:
			slice1=str(soup)[start_pos:end_pos]
			slice1=slice1.replace("*/","':")
			slice1=slice1.replace(",\r\n       ",",")
			slice1=slice1.replace(",\r\n","")
			slice1=slice1.replace(",","")
			slice1=slice1.replace("\n","")
			slice1=slice1.replace("     ","")
			slice_dict_list=slice1.split("/*")
			rt_list=list()
			rt_dic=dict()
			for dict_pair in slice_dict_list:
				if int(len(str(dict_pair)))>2:
					dict_pair="{'"+str(dict_pair)+"}"
					try:
						rt_dic.update(dict(eval(dict_pair)))
					except:
						pass
						# for testing
						#rt_dic.update({"err|"+dict_pair:dict_pair})
				else:
					pass
			rt_dic2=dict()
			for k,v in rt_dic.iteritems():
				if grab_fields.has_key(k):
					rt_dic2.update({grab_fields[k]:v})
			rt=json.dumps(rt_dic2)
			#rt=json.dumps(rt_dic)
		else:
			rt="no"
	else:
		rt="no"
			#rt=page[start_pos:(start_pos+500)]
	#SET the empety  value
#	sp_price="0"
#	sp_price=u"not set"
	#soup=BeautifulSoup(page)
#	ele_productInfo=soup.find("div",{"class":"productInfo"})
#	ele_productPrice=soup.find("div",{"id":"priceDiv"})
#	ele_price=ele_productPrice.find("span",{"class":"nowPrice"})
#	ele_unit=ele_price.findNextSiblings("span")[0]
#	rt=dict()
#	sp_price=str(ele_price.contents[0])
#	sp_unit=str(ele_unit.contents[0])
#	ele_h3=ele_productInfo.find("h3")
#	ele_iname=ele_h3.find("span")
#	sp_itemname=str(ele_iname.contents[0])
#	rt.update({"pro_id":str(pro_id)})
#	rt.update({"price":sp_price})
#	rt.update({"unit":sp_unit})
#	rt.update({"itemname":sp_itemname})
#	rt.update({"qtt":1})
	return rt

class usertrace:
	"""
	A class to output the user trace dict
	__init__(self,useremail,db="foundation",usertable="staff")
	use it like
	usert=usertrace("r@s.cn")
	trace_dict=usert.trace()
	"""
	def __init__(self,useremail,dbname="foundation"):
		self.dbname=dbname
		self.mail=useremail
		self.subset_keys=[#produce a subset dict, according to the following list of keys
		"mail",   	#email, key is not "email", but "mail"
		"cnname",  	#Chinese Name
		"ext",      #Extension Number
		]

	def trace(self):
		"""
		Return the trace dict
		"""
		self.db=get_db(self.dbname)  #login db, default db is foundation
		self.user_mongo=dict(self.db.staff.find_one({"mail":self.mail}))	#use mail as search condition
		self.trace_dict=dict((k,self.user_mongo[k]) for k in self.subset_keys if self.user_mongo.has_key(k))  	#get a subset of dict according to a list of keys
		self.trace_dict.update({"time":utc8()})		#combine the time stamp pair to the dict
		return self.trace_dict

def process_main(request):
	save_request(request)
	tl=testlog(request)
	if tl==True:
		temp_process_main=loader.get_template("a.html")
		bodies=OrderedDict()
		temp_pro=loader.get_template("processmain.html")
		con_pro=OrderedDict({})
		db=get_db("foundation")
		await_count=int(db.process.count({"stage_mails":request.session["mail"],"edit":{"$ne":True},"status":{"$nin":["finished","revoked","dead","done"]}}))
		con_pro.update({"await_count":await_count})
		loaded_process_main=temp_pro.render(con_pro,request)
		bodies.update({"b2":usejs("js/jquery.js")})
		bodies.update({"c1":loaded_process_main})
		context=dict({
			"title":u"申请服务中心",
			"userb":userbar(request),
			"bodies":bodies,
			})
		tl=temp_process_main.render(context,request)	
	return HttpResponse(tl)

class MongoOut:
	"""
	A class to print out the mongo extraction
	Dosen't apply to find_one
	*  You have to assign the OrderedDict self.fmatching.update({"mgfield":u"Field Label"})
	"""
	def __init__(self,mongofindresult):
		self.limit=20
		self.class_extra=""
		self.thclass="mg_th_class"
		self.thclass_extra=""	#user specify extra string, we can start the string with a space to seperate the classes
		self.tdclass="mg_td_class"
		self.tdclass_extra=""	#user specify extra string, we can start the string with a space to seperate the classes
		self.attrs={}#attributes besides id and class
		self.fmatching=OrderedDict() #use it like instance.fmatching.update({"dbField":u"Label"})
		self.result_list=mongofindresult #The class argument, result of db.something.find({"a":"b"})
	
	def final_concat(self):
		"""
		A function to concatenate the extra string to original class_string
		Turn dict values of fmatching to list
		"""
		self.thclass=str(self.thclass)+str(self.thclass_extra)
		self.tdclass=str(self.tdclass)+str(self.tdclass_extra)
		self.label_list=list(labels for ffield,labels in self.fmatching.iteritems())

	def as_table(self):
		"""
		Final print out of mongodb result
		"""
		self.final_concat()
		temp_table=loader.get_template("parts/mgtable.html")
		temp_table_row=loader.get_template("parts/mgtable_row.html")
		self.table_rows_list=OrderedDict()
		row_cur=0 #row cursor
		td_list=OrderedDict()	#<td> content list
		row_loaded=OrderedDict()
		for MgLine in self.result_list:  #iterate the MongoDB Search Result
			td_list[row_cur]=OrderedDict()
			for fd_name,lbl_name in self.fmatching.iteritems():
				if MgLine.has_key(fd_name):# in case the value is empety
					td_list[row_cur].update({fd_name:MgLine[fd_name]})
				else:
					td_list[row_cur].update({fd_name:""})
			row_loaded[row_cur]=temp_table_row.render({
				"rowlist":td_list[row_cur],
				"tdclass":self.tdclass,})#tdclass defined before
			self.table_rows_list.update({row_cur:row_loaded[row_cur]})
			row_cur=row_cur+1
		#render the table template
		self.table_print=temp_table.render({
			"class_extra":self.class_extra,   #extra string of class
			"thclass":self.thclass,
			"label_dict":self.fmatching,		#field matching dict, preferably OrderedDict, key is field name from database, value is the field label, like utf string
			"table_rows":self.table_rows_list,
			})
		return self.table_print
class user_auth:
	"""
	=========== User Authentication Class ==========

	The structure of user authentication:
	userdoc
		{
		"enname":u"Raynard",
		"email":u"raynard.zhang@staples.cn",
		"auth":{
			"taskname":{
				"r":"1",		# read authorization, 1:yes, 0:no, -1: in the blacklist(Does not get auth from group)
				"w":"1",		# write authorization, 1:yes, 0:no, -1: in the blacklist(Does not get auth from group)
				"d":"0",		# delete authorization, 1:yes, 0:no, -1: in the blacklist(Does not get auth from group)
				"a":"-1",		# approve authorization, 1:yes, 0:no, -1: in the blacklist(Does not get auth from group)
				"s":"1",      # Super authorization to set rows, 1:yes, 0:no
				}
			"log":[							#log, a list of dict, the alteration log 
						{
						"tk":"taskname",				#The task name
						"ch":{"r":"1","w","1"},				#The Change
						"tm":"ISODate....",				#Time Stamp
						"mail":ObjectId("12345abc"),		#user email as ID
						},
				]
			},
		}
	"""
	def __init__(self,user_email):
		self.email=user_email
		self.db=get_db("foundation")
	def guide_page(self,request):
		temp_guide=loader.get_template("a.html")
		temp_guide_sub=loader.get_template("parts/auth_guide_sub.html")
		con_guide_sub=OrderedDict()
		bodies=OrderedDict()
		bodies.update({"c1":usejs("js/jquery.js")})
		bodies.update({"c2":u"<h2 style='color:#09c;'>Authorization Management</h2>"})
		bodies.update({"c3":temp_guide_sub.render(con_guide_sub,request)})
		context=({
			"title":u"User Authorization Management",
			"bodies":bodies,
			"userb":userbar(request),
			})
		return temp_guide.render(context)
	def test_super(self,task):
		"""
		Test if have the super authorization
		return 1 or zero
		"""
		if self.db.staff.count({"mail":self.email,"auth.%s.s"%(task):"1"})>0:
			rt=1
		else:
			rt=0
		return rt
	def isGroup(self,groupname):
		"""
		Test is the user a group member
		return True or False
		"""
		membercount=self.db.staff.count({"groupname":groupname,"member":self.email})
		if membercount>0:
			return True
		else:
			return False
	def isLeader(self,groupname):
		"""
		Test is the user a group leader
		return True or False
		"""
		leadercount=self.db.staff.count({"groupname":groupname,"leader":self.email})
		if leadercount>0:
			return True
		elif int(self.db.staff.count({"mail":self.email,"auth.system.a":"1"}))>0:
			return True
		else:
			return False
	def set_auth(self,task,auth_dict,usermail):
		"""
		Use it like
		instance.set_auth("taskname",{"r":1,"w":0})
		"r":1,		# Read authorization, 1:yes, 0:no, -1: in the blacklist
		"w":1,		# Write authorization, 1:yes, 0:no, -1: in the blacklist
		"d":0,		# Selete authorization, 1:yes, 0:no, -1: in the blacklist
		"a":1,		# Approve authorization, 1:yes, 0:no, -1: in the blacklist
		"s":1,      # Super authorization to set rows, 1:yes, 0:no
		"""
		if self.test_super(task)==1:
			self.taskname=task
			self.db.staff.update(
				{"mail":usermail},
				{"$set":{
					"auth.%s"%(self.taskname):auth_dict,
					},
				"$push":{
					"auth.log":{
						"tk":self.taskname,
						"ch":auth_dict,
						"tm":utc8(),
						"mail":self.email,
						}
					},
				},
				upsert=True)
		else:
			pass
	def write_auth(self,task):
		"""
		Get writing authorization from a user
		"""
		rt="1"
		if self.db.tasks.count({"taskname":task,"default.w":"0"})>0:
			rt="0"
		if self.db.staff.count({"mail":self.email,"atuh.%s.w"%(task):"0"})>0:
			rt="0"
		if rt=="0":
			if self.db.staff.count({"member":self.email,"atuh.%s.w"%(task):"1"})>0:
				rt="1"
		return rt
	def get_auth_form(self,req,task=None,process_doc=None):
		"""
		Return a rendered form,
		For user to apply authorization
		"req" arg is the request
		The form will post application to db
		See class.post_apply()

		use it like get_auth_form(req,None,process_doc)
		use it like get_auth_form(req,task,None)
		task or process_doc, one of them have to be set
		"""
		# if process_doc is set
		if task==None:
			stages=process_doc["stages"]
			task=process_doc["taskname"]
			processid=process_doc["_id"].__str__()
			self.task_auth=dict()
			self.task_auth.update({})
			self.task_auth.update(process_doc)
			self.task_auth.update({"taskname":task,"usermail":self.email,"process":"auth","apid":processid})
			w_au=self.write_auth(task)
		#if task name:task is set
		else:
			task_doc=self.db.tasks.find_one({"taskname":task},{"_id":0,"stages":1,"default":2})
			stages=task_doc["stages"]
			default=task_doc["default"]
			self.task_auth=dict()
			self.task_auth.update(default)
			self.task_auth.update({"taskname":task,"usermail":self.email,"process":"auth"})
			w_au=self.write_auth(task)
		if w_au=="1":
			temp_apply=loader.get_template("form_set.html")
			#get a super-intendent list
			# co self.superlist=list([k['mail'],k['cnname']] for k in list(self.db.staff.find({"auth.%s.s"%(task):"1"},{"_id":0,"mail":1,"cnname":2})))
			#self.task_auth.update({""})			
			stages_list=list([k["stname"],k["des"]] for k in stages)
			self.apply_auth_form=user_auth_apply(self.task_auth)
			self.apply_auth_form.is_valid()
			if process_doc==None:
				del self.apply_auth_form.fields["apid"]
			self.apply_auth_form.fields["a"]=fm.TypedChoiceField(label=u'Approve',widget=fm.widgets.CheckboxSelectMultiple,choices=stages_list)
			#set_choices is a method in rich_form to set a list of pairs to the TypedChoiceField
			# co self.apply_auth_form.set_choices("supers",self.superlist)
			userb=userbar(req)
			self.apply_auth_form_loaded=temp_apply.render({
				"userb":userb,
				"form":self.apply_auth_form,
				"title":u"Apply for authorizations on task: '%s'"%(task),
				"act":"authset",
				"act_cn":u"Apply For Authorization On %s"%(task),
				"extra":self.task_guide(task),
				},req)
			rt=self.apply_auth_form_loaded
		else:
			rt=u"您没有权限申请"
		return rt
	def post_apply(self,req):
		"""
		Use the self.post_func_name
		post_func_name pointed to a function,
		the function will return a dict
		The dict is a filtered & process the post dict:
		def post_func_name(request)
			return_dict=dict((k,request.POST[k]) for k in a_list_of_keys if request.POST.has_key(k))
		...
		"""
		post_dict=dict(req.POST)
		#
		to_mg_dict=dict()
		to_mg_dict.update({"mail":self.email,"tm":utc8(),"edit":False})
		if req.session.has_key("cnname"):
			to_mg_dict.update({"cnname":req.session['cnname']})
		post_extract_func=eval(self.post_func_name)
		taskname=post_dict["taskname"][0]
		to_mg_dict.update(post_extract_func(req))
		
		# POST OPTION I
		# application already existed (if apid is set)
		# if the mgid is set, the application id
		if post_dict.has_key('apid'):
			to_mg_dict.update({"stage_mails":self.stage_mails(taskname,post_dict["apid"][0])}) 
			self.db.process.update(
				#Identify the doc
				{"_id":ObjectId(post_dict["apid"][0])},
				#make changes
				{"$set":to_mg_dict,
				"$push":{"log":{
					"time":utc8(),
					"from":self.email,
					"fromcn":req.session["cnname"],
					"decision":"repost",
					}}
				},
				upsert=True)
		# POST OPTION II
		# new application
		else:
			# The application log
			start_stage=to_mg_dict["stage"]
			to_mg_dict.update({"stage_mails":self.stage_mails(taskname)}) 
			to_mg_dict.update({"log":[{"time":utc8(),"fromcn":req.session["cnname"],"decision":"post","from":self.email,"start_stage":start_stage}]})
			self.db.process.insert(to_mg_dict)
	def stage_mails(self,taskname,processid=None,start_stage=list()):
		"""
		A funtion to produce stage_mails
		"""
		db=get_db("foundation")
		if processid==None:
			# No process id
			# Hence a new process, take the stages list form the db.tasks
			task_doc=dict(db.tasks.find_one({"taskname":taskname}))
			stages=task_doc["stages"]
			stages_finished=start_stage
		else:# if we do have process id
			process_doc=self.db.process.find_one({"_id":ObjectId(processid)},{"_id":0,"stages":1,"stage":2})
			if process_doc == None:
				return HttpResponse(u"lib.stage_mails, record not found")
			stages=process_doc["stages"]
			stages_finished=process_doc["stage"]
		# stages_list = all the stages required
		stages_list=list(str(v["stname"]) for v in stages if v.has_key("stname"))
		stages_tdict=dict((str(v["stname"]),str(v["utier"])) for v in stages if (v.has_key("utier") and v.has_key("stname")))
		# stages_await = every stages not finished
		stages_await=list(v for v in stages_list if v not in stages_finished)
		# if no more stages_await, clear the stage mails list
		stage_mails=list()
		if len(stages_await)==0:
			pass
		else:
			# Split the stages_await into num_await and other_wait
			# num_await could be serialized
			num_await=list(v for v in stages_await if v in num20)
			others_await=list(v for v in stages_await if v not in num_await)
			if len(num_await)>0:
				# pick the smallest num_await
				stages_await=others_await+list(str(min(int(v) for v in num_await)))
			for s in stages_await:
				# Search 
				#if count(db.gtier.find({"auth.%s.a"%(taskname):s,"leader":self.email})>0:
				#	stage_mails=self.email
				try:
					# Get utier in user profile
					user_tier=dict(db.staff.find_one({"mail":self.email,"utier":{"$exists":True}},{"utier":1}))["utier"]
					if stages_tdict.has_key(s):
						# is the user_tier in the utier of stages_tdict?
						if user_tier in stages_tdict[s]:
							stage_mails.append(self.email)
				except:
					pass
				for v in list(db.staff.find({
					"auth.%s.a"%(taskname):s, # s the approval status iterated here
					"leader":{"$exists":True},
					"$or":[{"member":self.email},{"member":"all"}],
					},{"_id":0,"leader":1})):
					stage_mails=stage_mails+v["leader"]
			# Need to remove  some duplicate mails
		stage_mails=list(set(stage_mails))
		return stage_mails
	def get_auth_attr(self,task,attr_name):
		"""
		Get the a specific attribute authorit from db
		result=instance.get_auth_attr("taskname","r")	#get the authorization 1 or 0 or -1 of "taskname" on READ from db 
		"""
		self.task_auth_attr=self.db.staff.find_one({"mail":self.email},{"auth.%s.%s"%(task,attr_name):1})
		return self.task_auth_attr
	def create_task_form(self,req):
		"""
		Return a loaded task creating form
		"""
		temp_set=loader.get_template("form_set.html")
		set_form=task_write()
		context={
			"form":set_form,
			"title":u"Authorization Setup",
			"act_cn":u"Authorization Management",
			"act":"authset",
			}
		rt=temp_set.render(context,req)
		return rt
	def create_task(self,task,default_status_dict):
		"""
		Create a new task
		default_status_dict:{"w":1,"r":0,....(all of them)}
		"""
		if self.db.tasks.count({"taskname":task}) > 0:
			self.db.tasks.update(
				{"taskname":task},
				{
					"$set":{"default":default_status_dict},
					"$push":{
						"log":{
							"mail":self.email,
							"ch":default_status_dict,
							"tm":utc8(),
							}
						}
				},
				upsert=True,
				)
			self.db.staff.update(
				{
					"mail":self.email,
				},
				{"$set":{"auth.%s.s"%(task):1}},
				upsert=True
				)
		else:
			 self.db.tasks.insert({
			"taskname":task,
			"create_time":utc8(),
			"creator":self.email,
			"default":default_status_dict,
			})
	def task_guide(self,task):
		"""
		Return a task guide bar
		"""
		temp_task_bar=loader.get_template("parts/auth_task_bar.html")
		con_task=dict({"task":task})
		return temp_task_bar.render(con_task)

	def my_applications(self,request):
		"""
		Show a list of all my applications
		"""
		#self.db.process.find()
		self.sf_table_book=table_book("process",{"mail":self.email})
		self.sf_table_book.sort=[("tm",DESCENDING)]
		self.sf_table_book.row_func_name="auth_sf_line"
		self.sf_table_book.tool_form=loader.get_template("parts/myapp_filter.html").render({})
		self.sf_table_book.title=u"我递交的申请"
		# Update field_dict (OrderedDict) one by one
		self.sf_table_book.field_dict.update({"check":" "})
		self.sf_table_book.field_dict.update({"Detail":u"展开"})
		self.sf_table_book.field_dict.update({"cnname":u"申请人"})
		self.sf_table_book.field_dict.update({"processcn":u"申请种类"})
		self.sf_table_book.field_dict.update({"tm":u"提交时间"})
		# co self.sf_table_book.field_dict.update({"supers":"Reviewer"})
		self.sf_table_book.field_dict.update({"stage":u"进程"})
		self.sf_table_book.field_dict.update({"action":u"操作"})
		bodies=self.sf_table_book.bodies
		bodies.update({"b2":u"<h2>我递交的申请</h2>"})
		#bodies.update({"b3":self.task_guide(task)})
		return self.sf_table_book.book(request)

	def review_application(self,request):
		"""
		Show a list of all applications related to the task
		"""
		condi={"log.from":self.email}
		self.rv_table_book=table_book("process",condi)
		self.rv_table_book.sort=[("tm",DESCENDING)]
		self.rv_table_book.row_func_name="auth_review_line"
		self.rv_table_book.tool_form=loader.get_template("parts/review_filter.html").render({})
		self.rv_table_book.title=u"申请"
		self.rv_table_book.field_dict.update({"aptype":u"申请种类"})
		self.rv_table_book.field_dict.update({"name":u"申请人"})
		self.rv_table_book.field_dict.update({"details":u"展开"})
		self.rv_table_book.field_dict.update({"time":u"提交时间"})
		self.rv_table_book.field_dict.update({"status":u"状态"})
		self.rv_table_book.field_dict.update({"action":u"操作"})
		self.rv_table_book.field_dict.update({"feedback":u"反馈"})
		bodies=self.rv_table_book.bodies
		bodies.update({"b2":u"<h2>与我有关的申请</h2>"})
		#bodies.update({"b3":self.task_guide(task)})
		return self.rv_table_book.book(request)
	def await_application(self,request):
		"""
		Show a list of all applications awaiting your approval
		"""
		self.rv_table_book=table_book("process",{"stage_mails":self.email,"edit":{"$ne":True},"status":{"$nin":["finished","revoked","dead","done"]}})
		self.rv_table_book.sort=[("tm",DESCENDING)]
		self.rv_table_book.row_func_name="auth_review_line"
		self.rv_table_book.tool_form=loader.get_template("parts/review_filter.html").render({})
		self.rv_table_book.title=u"等待我审批的申请"
		self.rv_table_book.field_dict.update({"aptype":u"申请种类"})
		self.rv_table_book.field_dict.update({"name":u"申请人"})
		self.rv_table_book.field_dict.update({"details":u"展开"})
		self.rv_table_book.field_dict.update({"time":u"提交时间"})
		self.rv_table_book.field_dict.update({"status":u"状态"})
		self.rv_table_book.field_dict.update({"action":u"操作"})
		self.rv_table_book.field_dict.update({"feedback":u"反馈"})
		bodies=self.rv_table_book.bodies
		bodies.update({"b2":u"<h2> 待我审批的申请</h2>"})
		#bodies.update({"b3":self.task_guide(task)})
		return self.rv_table_book.book(request)
	def read_stage(self,processid):
		"""
		Read and process the "stage" and "stages" process doc
		Example for such return
		loaded_stage={
			"abc":{"await":["a"],"ok",["b"]},
			"num":{"await":[3],"ok":["1","2"]},
			"symb":{"await":[]}
			"status":"edit",
			"ican":["3","a"],
			}
		"""
		process_doc=dict(self.db.process.find_one({"_id":ObjectId(processid)}))
		stage=process_doc["stage"]
		taskname=process_doc["taskname"]
		stage_list=list(v["stname"] for v in process_doc["stages"])  #All stages required
		# Stages required (stage_list) are divided to categories
		stage_list_num=list(v for v in stage_list if v in num20)
		stage_list_abc=list(v for v in stage_list if v in a2z)
		stage_list_symb=list(v for v in stage_list if v in stage_symbol)
		self.loaded_stage=dict({"abc":dict(),"num":dict(),"symb":dict(),"status":dict()})
		# ============================
		# The alphabate authorizations
		# ============================
		if len(stage_list_abc)==0:
			self.loaded_stage["abc"].update({"await":[]})
		else:
			self.loaded_stage["abc"].update({"await":list(v for v in stage_list_abc not in stage)})
			self.loaded_stage["abc"].update({"ok":list(v for v in stage_list_abc in stage)})
		# ============================
		# The symbolic authorizations
		# ============================
		if len(stage_list_symb)==0:
			self.loaded_stage["symb"].update({"await":[]})
		else:
			self.loaded_stage["symb"].update({"await":list(v for v in stage_list_symb not in stage)})
			self.loaded_stage["symb"].update({"ok":list(v for v in stage_list_symb in stage)})		
		# ============================
		# The numeric authorizations
		# ============================
		if len(stage_list_num)==0:
			self.loaded_stage["num"].update({"await":[]})
		else:
			# await num is the minimun num required
			num_await_full=list(int(v) for v in stage_list_num if v not in stage)
			if len(num_await_full)>0:
				required_num=str(min(num_await_full))
				self.loaded_stage["num"].update({"await":[required_num]})
			else:
				self.loaded_stage["num"].update({"await":[]})
			self.loaded_stage["num"].update({"ok":list(v for v in stage_list_num if v in stage)})
		# ============================
		# Status Check
		# ===========================
		if stage_list==stage:
			self.loaded_stage.update({"status":"finished"})
		if process_doc.has_key("status"):
			self.loaded_stage["status"]=process_doc["status"]
		elif process_doc.has_key("edit"):
			if process_doc["edit"]==True:
				self.loaded_stage.update({"status":"edit"})
			else:
				self.loaded_stage.update({"status":"inprogress"})
		else:
			self.loaded_stage.update({"status":"inprogress"})
		applier_mail=process_doc["mail"]
		# All the awaitings: stage_await
		stage_await=self.loaded_stage["abc"]["await"]+self.loaded_stage["symb"]["await"]+self.loaded_stage["num"]["await"]
		# ican: a list of awaitings that I can approve/deny
		# ihave is the stages authority I have over such issue
		# ican is the subset of ihave, subtract the stages already approved on the process
		self.loaded_stage.update({"ihave":list()})
		for single_stage in stage_list:
			if self.db.staff.count({"mail":self.email,"auth.%s.a"%(taskname):single_stage})>0:
				self.loaded_stage["ihave"].append(single_stage)
			elif self.db.staff.count({"member":applier_mail,"auth.%s.a"%(taskname):single_stage,"leader":self.email})>0:
				self.loaded_stage["ihave"].append(single_stage)
			elif self.db.staff.count({"member":None,"auth.%s.a"%(taskname):single_stage,"leader":self.email})>0:
				self.loaded_stage["ihave"].append(single_stage)	
			else:
				pass
		self.loaded_stage.update({"ican":list(v for v in stage_await if v in self.loaded_stage["ihave"])})
		return self.loaded_stage
	def edit_my(self,process_doc,req):
		"""
		An interface where we can edit our own application
		Return a rendered form,
		For user to apply authorization
		"req" arg is the request
		The form will post application to db
		See class.post_apply()
		"""
		task=process_doc["taskname"]
		processid=process_doc["_id"].__str__()
		process_doc.update({"apid":processid})
		temp_apply=loader.get_template("form_set.html")
		self.apply_auth_form=user_auth_apply(process_doc)
		#add the id in
		self.apply_auth_form.fields["apid"]=fm.CharField(label='Application ID',widget=fm.widgets.HiddenInput,)
		#set_choices is a method in rich_form to set a list of pairs to the TypedChoiceField
		userb=userbar(req)
		self.apply_auth_form_loaded=temp_apply.render({
			"userb":userb,
			"form":self.apply_auth_form,
			"title":u"Apply for authorizations on task: '%s'"%(task),
			"act":"authset",
			"act_cn":u"Apply For Authorization On %s"%(task),
			},req)
		return self.apply_auth_form_loaded

class table_book:
	"""
	A class to create table book
	A mongo db table that we can flip pages
	You have to define instance.row_func from a function, before you use book
	"""
	def __init__(self,collection,condi_dict_1={},db="foundation"):
		self.condi_dict_1=condi_dict_1
		self.aj_id=u"aj_id"# Notice: if there will be several table books, must assign this id
		self.page_limit=20
		self.page_skip=0
		self.dbname=db
		self.title="Detail Page"
		self.bodies=OrderedDict()
		self.eachrow_extra=OrderedDict()
		self.table_extra=OrderedDict()
		self.bodies.update({"b1":usejs("js/jquery.js")})
		self.db=get_db("foundation")
		self.collection_name=collection
		self.collection=self.db[collection]
		self.sort=list()
		self.field_dict=OrderedDict({})
		self.tool_form=None		# Assign with a form class, when this form changed, contents changes accordingly
		self.row_func=None		# Assign with a row layout function
		self.css_url="css/book_table_default.css"
	def mongo_count(self):
		"""
		Count the docs with matching condition
		"""
		self.count=int(self.collection.count(self.condi_dict_1))
		return self.count

	def mongo(self,request):
		"""
		Extract data from mongodb
		"""
		self.mgresult=self.collection.find(self.condi_dict_1,sort=self.sort).limit(self.page_limit).skip(self.page_skip)
		rendered_rows=OrderedDict()
		row_cur=1
		temp_table=loader.get_template("parts/mgtable.html")
		for eachrow in self.mgresult:
			eachrow.update(self.eachrow_extra)
			rendered_rows.update({row_cur:self.row_func(eachrow,request)})
			row_cur=row_cur+1
		con_table={
			"table_rows":rendered_rows,
			#"table_rows":self.mgresult,
			"label_dict":self.field_dict,
			}
		if len(rendered_rows)==0:
			con_table=dict({"table_rows":[{"Nodata":"<h2>No data records</h2>"}]})
		con_table.update(self.table_extra)
		self.rendered_table=temp_table.render(con_table)
		return self.rendered_table
	def book(self,req):
		"""
		Define the variable instance.row_func from a function before you use instance.book()
		"""
		temp_page=loader.get_template("a.html")
		temp_book=loader.get_template("parts/table_book.html")
		con_book=dict({
			"field_form":self.tool_form,# Tool form, have to be assigned with a form class
			"aj_id":self.aj_id,
			"css_url":self.css_url,
			"condi_dict1":self.condi_dict_1,
			"collection":self.collection_name,
			"page_limit":self.page_limit,
			"row_func_name":self.row_func_name,   # Has to be set up before
			"db":self.dbname,
			"field_dict":self.field_dict,
			})
		db=get_db("foundation")
		if req.method=="GET":
			if dict(req.GET).has_key("list"):
				self.bodies.update({"b9":process_guide(req)})
		self.bodies.update({"c1":temp_book.render(con_book)})
		con_page=dict({
			"title":self.title,
			"userb":userbar(req),
			"bodies":self.bodies,
			})
		self.rendered=temp_page.render(con_page,req)
		return self.rendered
def auth_translate(input_dict):
	trans_table=dict({
		"1":"Yes",
		"0":"No",
		"-1":"-",
		})
	return dict((k,trans_table[input_dict[k]]) for k in ["w","r","d","a","s"] if input_dict.has_key(k))

def auth_sf_line(row_dict,request):
	"""
	A row_func variable for table_book class,
	To see my own applications
	"""
	for k,v in row_dict.iteritems():
		if k=="_id":
			row_dict[k]=v.__str__()
		if k=="tm":
			row_dict["tm"]=v.strftime("%Y-%m-%d")
	row_dict.update(auth_translate(row_dict))
	temp_row=loader.get_template("row_func/auth_sf_line.html")
	user_au=user_auth(request.session["mail"])
	#use read stage function to see what you can approve
	stage_loaded=user_au.read_stage(row_dict["_id"])
	context=dict({
		"name":get_db("foundation").staff.find_one({"mail":row_dict["mail"]}).get("cnname"),
		"time":row_dict["tm"],
	#	"all_dict":row_dict,
		"applier_email":row_dict["mail"],
		"stage_des":process_status[stage_loaded["status"]],
		"process":row_dict["process"],
		"processcn":process_dict[row_dict["process"]],
		"id":row_dict["_id"],
		"review_brief":review_brief(row_dict)
		})
	if stage_loaded["status"]=="edit":
		context.update({"edit":u"改动申请"})
	if stage_loaded["status"]=="finished":
		context.update({"removable":True})
	return temp_row.render(context)
def auth_review_line(row_dict,request):
	"""
	A row_func variable for table_book class
	To review applications
	"""
	try:
		for k,v in row_dict.iteritems():
			if k=="_id":
				row_dict[k]=v.__str__()
			if k=="tm":
				row_dict["tm"]=v.strftime("%Y-%m-%d %H:%M")
		row_dict.update(auth_translate(row_dict))
		user_au=user_auth(request.session["mail"])
		#use read stage function to see what you can approve
		stage_loaded=user_au.read_stage(row_dict["_id"])
		temp_row=loader.get_template("row_func/auth_review_line.html")
		context=dict({
			"time":row_dict["tm"],
		#	"all_dict":row_dict,
			"id":row_dict["_id"],
			"process":row_dict["process"],
			"processcn":process_dict[row_dict["process"]],
			"status":process_status[stage_loaded["status"]],
			"review_brief":review_brief(row_dict),
			"applier_email":row_dict["mail"],
			#"all_dict":row_dict,#for testing
			})
		if row_dict.has_key("cnname"):
			context.update({"name":row_dict["cnname"]})
		if stage_loaded["status"]in ["edit","revoked","dead","finished"]:
			context.update({"ican":"no"})
		elif len(stage_loaded["ihave"])>0:
			context.update({"ican":"yes"})
		else:
			context.update({"ican":"no"})
		rt=temp_row.render(context)
	except:
		rt=u"申请单"+row_dict["_id"].__str__()+" 无法显示"
	return rt
def review_brief(process_doc):
	if process_doc["process"]=="officeuse":
		price=process_doc["price"]
		qtt=process_doc["qtt"]
		rt=str(qtt)+"*<span class='text_red'>￥"+str(price)+"</span>"
		rt=rt+'|'+process_doc["itemname"]
	elif process_doc["process"]=="auth":
		rt=process_doc["taskname"]
	return rt
def auth_post_filter(request):
	"""
	Use function
	define user_auth.post_func_name="auth_post_filter"
	"""
	db=get_db("foundation")
	taskname=request.POST['taskname']
	rt_dict=dict((k,request.POST[k][0]) for k in ["a","r","w","s"] if request.POST.has_key(k))
	task_info=dict(db.tasks.find_one({
		"taskname":taskname,
		}))
	rt_dict.update(dict((k,task_info[k]) for k in ["stages","taskname"] if task_info.has_key(k)))
	rt_dict.update({"process":"auth","stage":list()})
	return rt_dict

class group_set(rich_form):
	grp=fm.CharField(
		label=u'群组名称',
		strip=True,
		required=True,
		max_length=50,
		)
	def members(self):
		if not self.is_bound:
			return
		self.full_clean()
		self.grp=self.cleaned_data["grp"]
		db=get_db("foundation")
		names=list(db.staff.aggregate(
				[{"$match":{"grp":self.grp,"cnname":{"$exists":True}}},{"$project":{"cnname":1}}]
				))
		tags=tagform("cnname",names)
		tags.update_cross_pull=dict({"grp":self.grp})
		return tags.tagtile()

def process_detail_show(request):
	"""
	Name the process show function name like :" process_detail_show_"+ Process Name
	"""
	get_dict=request.GET
	show_func=eval("process_detail_show_"+get_dict["process"])
	rt=show_func(request)
	return rt
def process_detail_show_auth(request):
	"""
	"""
	get_dict=request.GET
	processid=get_dict["processid"]
	db=get_db("foundation")
	process_doc=db.process.find_one({"_id":ObjectId(processid)})
	temp_detail=loader.get_template("parts/showdetail.html")
	context=process_doc #usethe document form mongo directly
	return read_process_auth(process_doc,request)

def process_detail_show_officeuse(request):
	"""
	Office Use
	"""
	get_dict=request.GET
	processid=get_dict["processid"]
	db=get_db("foundation")
	process_doc=db.process.find_one({"_id":ObjectId(processid)})
	return read_process_officeuse(process_doc,request)

#====================[Edit Process]===================
def edit_process(processid,request):
	"""
	Return the page to edit process
	"""
	db=get_db("foundation")
	process_doc=dict(db.process.find_one({"_id":ObjectId(processid)}))
	process_name=process_doc["process"]
	taskname=process_doc["taskname"]
	user_au=user_auth(request.session["mail"])
	# A logic has to decide if the user can edit, read, or blocked from the process record
	rt=False
	if process_doc["mail"]==request.session["mail"]:
		if process_doc["edit"]==True:
			edit_func=eval("edit_process_"+str(process_name))
			rt=edit_func(process_doc,request)	#Enter the Edit process
		else:
			#If the applicant apply the process, but can not edit, the applier sure can  read the process
			rt=read_process(process_doc,request)
	elif process_doc.has_key("log"):
		for log_entry in process_doc["log"]:
			if log_entry.has_key("from"):
				if log_entry["from"]==request.session["mail"]:
					rt=read_process(process_doc,request)
					break
	else:
		stage_mails=user_au.stage_mails(taskname,processid)
		if stage_mails.count(request.session["mail"]):
			rt=read_process(process_doc,request)
	if rt==False:
		rt=cant_access_process(request)
	return rt
def edit_process_auth(process_doc,request):
	user_au=user_auth(request.session["mail"])
	return user_au.get_auth_form(request,None,process_doc)
def edit_process_officeuse(process_doc,request):
	bodies=OrderedDict()
	bodies.update({"e2":usejs("js/varys_input.js")})
	ou_temp=loader.get_template("a.html")
	a_con=dict()
	if process_doc.has_key("_buyagain"):
		empety_form=office_use_detail(process_doc)
		del empety_form.fields["processid"]
		bodies.update({"a10":usejs("js/buyagain.js")})
	else:
		processid=process_doc["_id"].__str__()
		process_doc.update({"processid":processid})
		empety_form=office_use_detail(process_doc)
	#load templates
	temp_css=loader.get_template("css/officeuse.css")
	temp_ou1=loader.get_template("officeuse/officeuse1.html")
	#render the templates
	loaded_css=temp_css.render({})
	loaded_ou1=temp_ou1.render({
		"empety_form":empety_form,
		"urlform":fm_officeuse(),
		},request)
#update the page body
	bodies.update({"c4":u"<h2 style='color:#4682B4;'>领取您的装备</h2>"})
#	bodies.update({"d0":postrt})
	bodies.update({"d1":loaded_ou1})
#the context of template:ou_temp
	a_con.update({
	"userb":userbar(request),
	"loaded_css":loaded_css,
	"title":u'办公用品行政领用',
	"bodies":bodies,
	})
	return ou_temp.render(a_con,request)
#====================[Edit Process]===================


#====================[Read Process]===================
def read_process(process_doc,request):
	process_name=process_doc["process"]
	read_func=eval("read_process_"+str(process_name))
	temp_read_process=loader.get_template("a.html")
	bodies=OrderedDict({})
	bodies.update({"b1":usejs("js/jquery.js")})
	bodies.update({"c1":read_func(process_doc,request)})
	context=({
		"userb":userbar(request),
		"bodies":bodies,
		"title":"Read Details",
		})
	rt=temp_read_process.render(context,request)
	return rt
def read_process_auth(process_doc,request):
	"""
	A function to translate process_doc to read-esay page
	"""
	processid=process_doc["_id"].__str__()
	temp_detail=loader.get_template("parts/showdetail.html")
	context=process_doc #usethe document form mongo directly
	context.update({"processid":processid})
	if process_doc.has_key("tm"):
		context.update({"date":process_doc["tm"].strftime("%Y-%m-%d")})
		context.update({"time":process_doc["tm"].strftime("%H:%M:%S")})
	if process_doc.has_key("stages"):
		stages=process_doc["stages"]
		new_a=list(v["des"] for v in stages if v["stname"] in process_doc["a"])
		context.update({"a":new_a})
	if process_doc.has_key("log"):
		context.update({"loaded_log":show_log(process_doc["log"])})
	return temp_detail.render(context,request)
def read_process_officeuse(process_doc,request):
	processid=process_doc["_id"].__str__()
	temp_detail_officeuse=loader.get_template("parts/showdetail_officeuse.html")
	context=dict(process_doc)
	context.update({"processid":processid})
	if process_doc.has_key("log"):
		context.update({"loaded_log":show_log(process_doc["log"])})
	if process_doc.has_key("tm"):
		context.update({"date":process_doc["tm"].strftime("%Y-%m-%d")})
		context.update({"time":process_doc["tm"].strftime("%H:%M:%S")})
	if process_doc.has_key("price"):
		if process_doc.has_key("qtt"):
			qtt=int(process_doc["qtt"])
		else:
			qtt=1
		context.update({"totalprice":qtt*float(process_doc["price"])})
	return temp_detail_officeuse.render(context,request)
	
def cant_access_process(request):
	temp_cap=loader.get_template("a.html")
	bodies=OrderedDict()
	bodies.update({"c1":"<h1>Access Denied</h1>"})
	bodies.update({"d1":"<div> You don't have any access to EDIT/READ this process </div>"})
	context=dict({
		"userb":userbar(request),
		"bodies":bodies,
		"title":u"Access Denied",
		})
	return HttpResponse(temp_cap.render(context,request))
#====================[Read Process]===================
def show_log(log_list):
	"""
	Show the log record
	"""
	temp_log=loader.get_template("parts/single_log.html")
	loaded_log=OrderedDict()
	ic=0
	log_list.reverse()
	for log in log_list:
		context=dict()
		try:
			if log.has_key("fromcn"):
				context.update({"fromcn":log["fromcn"]})
			elif log.has_key("from"):
				try:
					db=get_db("foundation")
					cnname=db.staff.find_one({"mail":log["from"]},{"cnname":1,"_id":0})["cnname"]
				except:
					cnname=log["from"]
				context.update({"fromcn":cnname})
			if log.has_key("decision"):
				context.update({"decision":decision_dict[log["decision"]]})
			if log.has_key("time"):
				context.update({
					"date":log["time"].strftime("%Y-%m-%d"),
					"time":log["time"].strftime("%H:%M:%S"),
					})
			if log.has_key("remark"):
				context.update({"remark":log["remark"]})
			loaded_log.update({ic:temp_log.render(context)})
			ic=ic+1
		except:
			pass
	return loaded_log
def process_guide(request):
	temp_p_g=loader.get_template("parts/process_guide.html")
	return temp_p_g.render({},request)
def date_parse(datestring):
	"""
	Parse the date formate and return a datetime date
	Format "YYYY-MM-DD"
	"""
	dates_list=str(datestring).split("-")
	dt_year=int(dates_list[0])
	dt_month=int(dates_list[1])
	dt_day=int(dates_list[2])
	#dt_hour=int(dates_list[3])
	#dt_min=int(dates_list[4])
	return datetime(dt_year,dt_month,dt_day,0,0)
def xlwt_officeuse(context):
	pathstr="dl_officeuse_"+str(time())+".xlsx"
	wb=xlsxwriter.Workbook(userhome+"/mt01/major/static/xlwt/"+pathstr,{'tmpdir':"/home/salvor/mt01/major/static/xlwt"})
	coldict=OrderedDict({
		"cnname":u"申请人",
		})
	coldict.update({"gtiers":u"领用部门"})
	coldict.update({"id":u"行政领用单号"})
	coldict.update({"tm":u"申请时间",})
	coldict.update({"itemname":u"领用物品",})
	coldict.update({"pro_id":u"产品编号",})
	coldict.update({"qtt":u"数量",})
	coldict.update({"price":u"单价",})
	coldict.update({"ttl_price":u"总价",})
	coldict.update({"vat_ex":u"不含税价",})
	coldict.update({"est_cost":u"成本估计",})
	collist=coldict.keys()
	ws_b=wb.add_worksheet(u"明细")
	ws_s=wb.add_worksheet("Summary")
	fo_num=wb.add_format({
		'font_name':"Arial",
		'font_size':11,
		'num_format':'#,##0.00',
		})
	fo_text=wb.add_format({
		'font_name':"Arial",
		'font_size':11,
		})
	fo_head=wb.add_format({
		'font_name':"Arial",
		'font_size':11,
		'font_color':'#4682B4',
		})
	fo_total=wb.add_format({
		'font_name':"Arial",
		'font_size':11,
		'bold':True,
		'num_format':'#,##0.00',
		})
	fo_head_title=wb.add_format({
		'font_name':"Arial",
		'font_size':20,
		'font_color':'#4682B4',
		})
	ws_b.set_row(3,None,fo_total)
	ws_b.write(0,0,u"行政领用明细",fo_head_title)
	ws_b.write(1,0,u"开始日期",fo_head)
	ws_b.write(2,0,u"结束日期",fo_head)
	ws_b.write(1,1,context["datestart"],fo_head)
	ws_b.write(2,1,context["dateend"],fo_head)
	rcount=5
	colheadc=0
	for col in collist:
		ws_b.write(4,colheadc,coldict[col],fo_head)
		colheadc+=1
	for dl_line in context["dl_list"]:
		colcount=0
		for colname in collist:
			if dl_line.has_key(colname):
				if colname in ["price","ttl_price","vat_ex","est_cost"]:
					ws_b.write(rcount,colcount,float(dl_line[colname]),fo_num)
				else:
					ws_b.write(rcount,colcount,dl_line[colname],fo_text)
			else:
				ws_b.write(rcount,colcount,"",fo_text)
			colcount+=1
		rcount+=1
	colcount=0
	for colname in collist:
		if colname=="itemname":
			str(num2alpha[colcount])+"4"
			ws_b.write(3,colcount,u"加总",fo_total)
		elif colname in ["qtt","ttl_price","vat_ex","est_cost"]:
			xl_sum_col(ws_b,num2alpha[colcount],4)
		colcount+=1
	rcount+=1
	#===generate the summary page
	namelist=officeuse_namelist(context["dl_list"])
	sm_rcount=3
	ws_s.set_column(1,3,None,fo_num)
	endl=len(namelist)+sm_rcount+2
	ws_s.write(sm_rcount-1,0,u"申请人",fo_head)
	ws_s.write(sm_rcount-1,1,u"总价",fo_head)
	ws_s.write(sm_rcount-1,2,u"不含税",fo_head)
	ws_s.write(sm_rcount-1,3,u"成本估计",fo_head)
	for smname in namelist:
		ws_s.write(sm_rcount,0,smname,fo_text)
		ws_s.write_formula("B%s"%(sm_rcount+1),"=SUMIFS(明细!I:I,明细!$A:$A,$A:$A)")
		ws_s.write_formula("C%s"%(sm_rcount+1),"=SUMIFS(明细!J:J,明细!$A:$A,$A:$A)")
		ws_s.write_formula("D%s"%(sm_rcount+1),"=SUMIFS(明细!K:K,明细!$A:$A,$A:$A)")
		sm_rcount+=1
	wb.close()
#	os.system("sleep 10;rm %s"%())
#	mtp=multip(target=to_delete_path,args=(userhome+"/mt01/major/static/xlwt/"+pathstr,300))
#	mtp.start()
	return "/static/xlwt/"+pathstr
def xl_sum_col(xlsx_worksheet,letter,sumrow):
	letter=letter.upper()
	xlsx_worksheet.write_formula(
		letter+str(sumrow),
		"=SUM(%s:%s)"%(letter+str(int(sumrow)+1),letter+"200000")
		)
def to_delete_path(path,seconds):
	sleep(seconds)
	os.remove(path)
def officeuse_namelist(dl_list):
	namelist=list(set(v["cnname"] for v in dl_list))
	return namelist

def kill_user(usermail,request):
	"""
	Deactivate user account
	copy the user into the ghosts table
	"""
	db=get_db("foundation")
	socialshadow=kill_user_from_group(usermail)
	try:
		ghosts=list(db.staff.find({"mail":usermail}))
		db.staff.update({
			"mail":usermail
			},
			{
			"$set":{"vitality":"nomore"} # Set the vitality of a user to no more
			},
			upsert=True)
	except:
		ghosts=list(dict({
			"reality":"Try to kill nobody:%s"%(usermail),
			"killtm":utc8(),
			"killer":request.session["mail"],
			"killercn":request.session["cnname"],
			}))
	for ghost in ghosts:
		try:
			if dict(ghost).has_key("_id"):
				ghost["ori_id"]=ghost["_id"]#turn the tag name _id to original id
				del ghost["id"]
				ghost.update({
					"socialshadow":socialshadow,
					"killtm":utc8(),
					"killer":request.session["mail"],
					"killercn":request.session["cnname"],
					})
		except:
			pass
		db.ghosts.insert(ghost)

def kill_user_from_group(usermail):
	"""
	Remove the user from all kinds of groups
	"""
	db=get_db("foundation")
	groupm=list(db.staff.find({"member":usermail},{"groupname":1,"cnname":2}))
	for mgroup in groupm:
		db.staff.update({"_id":mgroup["_id"]},{"$pull":{"member":usermail}},upsert=True)
	groupl=list(db.staff.find({"leader":usermail},{"groupname":1,"cnname":2}))
	for lgroup in groupl:
		db.staff.update({"_id":lgroup["_id"]},{"$pull":{"leader":usermail}},upsert=True)
	groupshadow=dict({
		"memberof":groupm,
		"leaderof":groupl,
		})
	return groupshadow


def refresh_bound_simple(fromgroup,togroup):
	"""
	If one group is bound to another,
	We can Import groupmember from another group
	"""
	db=get_db("foundation")
	try:
		f_member_list=dict(db.staff.find_one({"groupname":fromgroup},{"_id":0,"member":1}))["member"]
	except:
		#f_member_list=dict(db.staff.find_one({"groupname":fromgroup},{"_id":0,"member":1}))["member"]
		f_member_list=list()
	try:
		t_member_list=dict(db.staff.find_one({"groupname":togroup},{"_id":0,"member":1}))["member"]
	except:
		#f_member_list=dict(db.staff.find_one({"groupname":fromgroup},{"_id":0,"member":1}))["member"]
		t_member_list=list()
	if len(f_member_list)==0:
		pass
	else:
		upd_list=list(set(f_member_list+t_member_list)) #using set() to remvoe the duplicates
		db.staff.update({"groupname":togroup},{"$set":{"member":upd_list}})
			
def refresh_group_bound(fromgroup,togroup,request):
	"""
	If one group is bound to another,
	We can Import groupmember from another group
	"""
	db=get_db("foundation")
	if db.staff.count({"groupname":togroup,"leader":request.session["mail"]})>0:
		try:
			f_member_list=dict(db.staff.find_one({"groupname":fromgroup},{"_id":0,"member":1}))["member"]
		except:
			#f_member_list=dict(db.staff.find_one({"groupname":fromgroup},{"_id":0,"member":1}))["member"]
			f_member_list=list()
		try:
			t_member_list=dict(db.staff.find_one({"groupname":togroup},{"_id":0,"member":1}))["member"]
		except:
			#f_member_list=dict(db.staff.find_one({"groupname":fromgroup},{"_id":0,"member":1}))["member"]
			t_member_list=list()
		if len(f_member_list)==0:
			rt=str('already')
		else:
			upd_list=list(set(f_member_list+t_member_list)) #using set() to remvoe the duplicates
			db.staff.update({"groupname":togroup},{"$set":{"member":upd_list}})
			rt=str(u'人员已添加，请刷新')
	else:
		rt=str('already')
	return rt
def get_tiers(useremail):
	"""
	Get group information on a user, sort by tiers
	return tier dict
	Sample of tier dict:
	{"2":
		[
			{"groupname":"arteam","cnname":"应收账款团队"},
			{"groupnmae":"annualdinner","cnname":"nianhui"},
		]
	}
	"""
	db=get_db("foundation")
	try:
		tierlist=list(db.staff.find({"member":useremail,"gtier":{"$exists":True}},{"groupname":1,"gtier":2,"cnname":3}))
	except:
		tierlist=list()
	tiers_dict=dict()
	for group in tierlist:
		try:
			tiers_dict[group["gtier"]]=list()
			tiers_dict[group["gtier"]].append(dict({"groupname":group["groupname"],"cnname":group["cnname"]}))
		except:
			pass
	return tiers_dict
def disk_stat(path,name):  
    hd=OrderedDict()  
    disk = os.statvfs(path)  
    hd['%s_vailable'%(name)] = str(disk.f_bsize * disk.f_bavail/(1000)/(1024))+" MB"
    hd['%s_Used'%(name)] = str(disk.f_bsize * (disk.f_blocks-disk.f_bavail)/(1000)/(1024))+" MB"
    hd['%s_Capacity'%(name)] = str(disk.f_bsize * disk.f_blocks/(1000)/(1024))+" MB"
    hd["%s_Percentage"%(name)]=str("<progress value='%s' max='%s'></progress>"%((disk.f_bsize * (disk.f_blocks-disk.f_bavail)/(1000)/(1024),(disk.f_bsize * disk.f_blocks/(1000)/(1024)))))
    return hd
def mgdb_stat(dbname,collection):
	db=get_db(dbname)
	mgdict=dict(db.command("collstats",collection))
	mgdict['size']=str(int(mgdict['size'])/1024)+" MB"
	mgdict['totalIndexSize']=str(int(mgdict['totalIndexSize'])/1024)+" MB"
	mgdict['storageSize']=str(int(mgdict['storageSize'])/1024)+" MB"
	mgdict['lastExtentSize']=str(int(mgdict['lastExtentSize'])/1024)+" MB"
	del mgdict["ns"]
	del mgdict["ok"]
	del mgdict["systemFlags"]
	del mgdict["userFlags"]
	del mgdict["nindexes"]
	del mgdict["indexSizes"]
	rtdict=dict((k+'_'+str(collection),mgdict[k]) for k in mgdict.iterkeys())
	return rtdict
def read_sys():
	"""
	Read System Information
	Mostly storage capacity of hard disk and database
	"""
	rtdict=OrderedDict()
	rtdict.update({"System":'====================================================='})
	rtdict.update({"Platform":platform.uname()})
	rtdict.update({"Hard_Drive":'====================================================='})
	rtdict.update(disk_stat("/","sys"))
	rtdict.update({"Mongo01":'staff=============================================='})
	rtdict.update(mgdb_stat("foundation","staff"))
	rtdict.update({"Mongo02":'process=============================================='})
	rtdict.update(mgdb_stat("foundation","process"))
	rtdict.update({"Mongo03":'visit=============================================='})
	rtdict.update(mgdb_stat("trace","visit"))
	templ=loader.get_template("parts/tict2table.html")
	return templ.render({"dict":rtdict})
def gtierrefresh(totalgroup,gtier):
	for group in totalgroup:
		if (group.has_key("gtier") and group["gtier"]==gtier):
			boundgrouplist=group["boundgroup"]
			for bg in boundgrouplist:
				refresh_bound_simple(bg,group["groupname"])
def boundrefresh():
	db=get_db("foundation")
	grouplist=list(db.staff.find({"boundgroup":{"$exists":True}},{"boundgroup":1,"groupname":2,"gtier":3}))
	gtierrefresh(grouplist,"0")
	gtierrefresh(grouplist,"1")
	gtierrefresh(grouplist,"2")
	gtierrefresh(grouplist,"3")
	gtierrefresh(grouplist,"4")
	gtierrefresh(grouplist,"5")
	for group in grouplist:
		if group.has_key("gtier")==False:
			boundgrouplist=group["boundgroup"]
			for bg in boundgrouplist:
				refresh_bound_simple(bg,group["groupname"])
	return HttpResponse("ok")

def inform_write(request):
	pass


def _advcss_user(cnword):
	"""
	Translate Cn word of advcss_user fields to En Word
	"""
	return advcss_user(cnword)

def _advcss_user_r(enword):
	"""
	Translate En word of advcss_user fields to Cn Word
	"""
	return advcss_user(enword)
def seenan(input_value):
	try:
		if np.isnan(input_value):
			return False
		else:
			return True
	except:
		return True

def overdue_line(rd):
	"""
	rd for "row dict"
	input the row dict and format the row
	return the formated dict
	"""
	rkeys=["city","cnm","ctyp","amt","oamt","iamt","damt","odt","ddt","idt","odr","oodr","inv","dn","itt","cid"]
	rd2=dict()
	for k in rkeys:
		if rd.has_key(k):
			if k in ["amt","oamt","damt"]:# Process Number, float, and round to 2 decimal points
				rd2.update({k:round(rd[k],2)})
			elif k in ["cid","odr","oodr","dn","inv","cnm"]: #Process Serial Numbers
				try:
					rd2.update({k:str(int(rd[k]))})
				except:
					rd2.update({k:str(rd[k])})
			elif k in ["odt","ddt","idt"]:#Process date format
				if type(rd[k])==pd.tslib.Timestamp:
					rd2.update({k:rd[k].to_datetime()})
			else:
				rd2.update({k:rd[k]})
	return rd2

def match_cplist():
	'''
	Match the cplist from foundation db cplist colleciton
	to every entry in the armonth
	'''
	db=get_db("foundation")
	cp_list=list(db.cplist.find(dict()))
	for cpmatch in cp_list:
		arlist=list(db.armonth.find({u"cid":cpmatch[u"cid"]},{"_id":1}))
		if len(arlist)>0:
			for arline in arlist:
				if cpmatch["cp"] not in [u"国网项目",u"移动项目"]:
					cpmatch["cp"]=u"其他CP项目"
				db.armonth.update({"_id":dict(arline)["_id"]},{"$set":{"bu":cpmatch["cp"]}})
	#print "%s of matching rules applied"%(len(cp_list))
def match_cplist_uc():
	'''
	Match the cplist from foundation db cplist colleciton
	to every entry in the armonth
	'''
	db=get_db("foundation")
	cp_list=list(db.cplist.find(dict()))
	for cpmatch in cp_list:
		arlist=list(db.ucmonth.find({u"cid":str(int(cpmatch[u"cid"]))},{"_id":1}))
		if len(arlist)>0:
			#print len(arlist)
			for arline in arlist:
				if cpmatch["cp"] not in [u"国网项目",u"移动项目"]:
					cpmatch["cp"]=u"其他CP项目"
				db.ucmonth.update({"_id":dict(arline)["_id"]},{"$set":{"BU":cpmatch["cp"]}})
	#print "%s of matching rules applied"%(len(cp_list))