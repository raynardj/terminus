# -*- coding: utf-8 -*-

from django import forms
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from pymongo import MongoClient
from datetime import datetime
from django.forms.utils import flatatt
from hashlib import sha512
from base64 import urlsafe_b64encode
from fm import email_login,userset
from random import randint
try:
	from urllib import urlencode # python 2.7
except:
	from urllib.parse import urlencode #python 3
from django.core.mail import send_mail

def dict_reverse(dict1):
	"""
	Reverse the dict
	Dict key and dict value
	"""
	dict2=dict((v,k) for k,v in dict1.iteritems())
	return dict2

def get_db(database):
	"""
	A quick way to get MongoDb Client link
	"""
	clientmg=MongoClient()
	db=clientmg[database]
	return db

def utc8():
	dt = datetime.now()
	#delta = timedelta(hours=0)
	#delta = timedelta(hours=8)
	return dt#+delta

def logout(request):
	"""
	Logout and mark down the return address
	"""
	try:
		request.session.flush()
	except KeyError:
		pass
	logoutjump=u"/login?ra=%s"%(request.get_full_path())
	return logoutjump

class config(object):
	def __init__(self):
		pass
		self.val=None

def mid_str(dict_in):
	"""
	Mongo ID transfer to string
	"""
	dict_in["id"]=dict_in["_id"].__str__()
	del dict_in["_id"]
	return dict_in

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

def utc8():
	dt = datetime.now()
	#delta = timedelta(hours=0)
	#delta = timedelta(hours=8)
	return dt#+delta

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

def mystrify(incode):
	t=sha512()
	t.update(str(incode+"#bc87q)f^").encode("utf-8"))
	outcode=urlsafe_b64encode(t.digest())
	return outcode

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
def ub(request,settings):
	temp=loader.get_template("userbar.html")
	context=dict({
		"st":settings,
		"session":request.session,
		})
	return temp.render(context,request)

def rtway(way,val):
	return dict({"w":way,"v":val})
class adm:
	"""
	Administration class
	admcls=adm(basic.gen)
	"""
	# return the basic administration page
	def __init__(self,gen):
		"""
		Arg:
		in app folder: config/st.py
		class gen
		(The setting page)
		"""
		self.st=gen
		self.f_save_request=None
		self.f_userbar=None
		self.i_userset_extra=forms.Form

	def login(self,request):
		"""
		login method of class adm
		"""
		context={}
		if self.f_save_request!=None:
			self.f_save_request(request)
		try:
			if request.GET["logout"]=="1":
				request.session.flush()
		except:
			pass
		template=loader.get_template('tpl/login.html')
		if request.method=="POST":
			form=email_login(request.POST)
			if form.is_valid():
				db=get_db("foundation")
				if db.staff.find({"mail":form.cleaned_data['email']}).count()==0:
					context.update({"msg_return":u"邮箱或密码错误",})
				else:
					getusr=db.staff.find_one({"mail":form.cleaned_data['email']})
					usertiers=get_tiers(form.cleaned_data['email'])
					if getusr["password"]==mystrify(form.cleaned_data['password']):# Password matched
						# Login successfully
						request.session.set_expiry(self.st.session["expire"])# Expiring time of session: 15 days
						request.session["onboard"]=True
						request.session["mail"]=form.cleaned_data['email']
						request.session["id"]=getusr['_id'].__str__()
						request.session["tiers"]=usertiers
						if "cnname" in getusr:
							request.session['cnname']=getusr['cnname']
						else:
							return rtway("redirect","/userinfo")# No CNName, goes to user setting page
						if "ra" in dict(request.POST):
							return rtway("redirect",request.POST["ra"])# Has return address
						else:
							return rtway("HttpResponseRedirect","/")# Doesn't have any return address, go to the root page
					else:
						context.update({"msg_return":u"邮箱或密码错误",})# Password didn't match
		else:
			form=email_login()#load the login form
			context.update({"form":form,})
		if request.method=="GET":
			get_dict=dict(request.GET)
			if "ra" in get_dict:# Pass on the return address
				return_address=get_dict["ra"][0]
				context.update({"ra":return_address})
		return rtway("HttpResponse",template.render(context,request))
	def register(self,request):
		"""
		register method of class admin
		"""
		if self.f_save_request!=None:
			self.f_save_request(request)
		template=loader.get_template('tpl/register.html')
		if request.method=="POST":
			form=email_login(request.POST)
			if form.is_valid():
				# Test if the mail address is a company mail address
				if "domain" in self.st.reg:
					if str(form.cleaned_data["email"]).lower().find("@%s."%(self.st.reg["domain"]))<0:
						return rtway("HttpResponse",u"不得使用公司邮箱以外的邮箱注册")
				mgclient=MongoClient()
				staffco=mgclient["foundation"].staff
				regmailco=mgclient["foundation"].regmail
				rand=randint(100000000,999999999)# create random number
				regmailco.update({"mail":form.cleaned_data["email"],},
					{"$set":{
					"mail":form.cleaned_data["email"],
					"password":form.cleaned_data["password"],
					"time":utc8(),
					"rand":rand,
					}},
					upsert=True,
					)
				qspair=dict({"mail":form.cleaned_data["email"],"rit":rand,"subfrom":"register"})
				qstring=urlencode(qspair)
				http_host=request.META['HTTP_HOST']
				urlb="http://"+str(http_host)+"/rabbithole?"+qstring		# Generate a query string
				mailcontext=dict({
					"urlb":urlb,
					"sitename":self.st.info["sitename"],
					"siteadmin":self.st.info["siteadmin"]
					})
				mailtem=loader.get_template("tpl/mailconfirm.html")
				send_mail(
					u'%s邮箱验证'%(self.st.info["sitename"]),
					urlb,
					self.st.info["sitemail"],
					[form.cleaned_data["email"]],
					fail_silently=False,
					html_message=mailtem.render(mailcontext,request),
				)
				msgtp=loader.get_template("tpl/msg.html")
				context={
					"msg_title":u"邮件已发送",
					"msg_head":u"确认邮件已发送[您有15分钟]",
					"msg_body":u"确认邮件已发送至:<br>"+form.cleaned_data["email"]+u"<br>请于十五分钟内访问邮件中的链接<br>找不到的话可以翻翻垃圾邮件:-)<br><br>务必注意，在点击邮箱中的确认链接时<strong>不要使用IE</strong><br><br><br>我要重新<a href='/register'>注册</a>",
					}
				return rtway("HttpResponse",msgtp.render(context,request))
		else:
			form=email_login()
			context={"form":form,}
		return rtway("HttpResponse",template.render(context,request))
	def reset(self,request):
		"""
		reset method of class admin
		"""
		if self.f_save_request!=None:
			self.f_save_request(request)
		template=loader.get_template('tpl/reset.html')
		if request.method=="POST":
			form=email_login(request.POST)
			if form.is_valid():
				# Test if the mail address is a company mail address
				if "domain" in self.st.reg:
					if str(form.cleaned_data["email"]).lower().find("@%s."%(self.st.reg["domain"]))<0:
						return rtway("HttpResponse",u"请输入正确的邮箱地址")
				mgclient=MongoClient()
				staffco=mgclient["foundation"].staff
				regmailco=mgclient["foundation"].regmail
				rand=randint(100000000,999999999)# create random number
				regmailco.update({"mail":form.cleaned_data["email"],},
					{"$set":{
					"mail":form.cleaned_data["email"],
					"password":form.cleaned_data["password"],
					"time":utc8(),
					"rand":rand,
					}},
					upsert=True,
					)
				qspair=dict({"mail":form.cleaned_data["email"],"rit":rand,"subfrom":"reset"})
				qstring=urlencode(qspair)
				http_host=request.META['HTTP_HOST']
				urlb="http://"+str(http_host)+"/rabbithole?"+qstring		# Generate a query string
				mailcontext=dict({
					"urlb":urlb,
					"sitename":self.st.info["sitename"],
					"siteadmin":self.st.info["siteadmin"]
					})
				mailtem=loader.get_template("tpl/mailconfirm.html")
				send_mail(
					'%s邮箱验证'%(self.st.info["sitename"]),
					urlb,
					self.st.info["sitemail"],
					[form.cleaned_data["email"]],
					fail_silently=False,
					html_message=mailtem.render(mailcontext,request),
				)
				msgtp=loader.get_template("tpl/msg.html")
				context={
					"msg_title":u"邮件已发送",
					"msg_head":u"确认邮件已发送[您有15分钟]",
					"msg_body":u"确认邮件已发送至:<br>"+form.cleaned_data["email"]+u"<br>请于十五分钟内访问邮件中的链接<br>找不到的话可以翻翻垃圾邮件:-)<br><br>务必注意，在点击邮箱中的确认链接时<strong>不要使用IE</strong><br><br><br>我要重新<a href='/register'>注册</a>",
					}
				return rtway("HttpResponse",msgtp.render(context,request))
		else:
			form=email_login()
			context={"form":form,}
		return rtway("HttpResponse",template.render(context,request))
	def after_reg(self,request):
		rgmail=request.GET["mail"]
		rdcode=int(request.GET["rit"])
		subfrom=request.GET["subfrom"]
		if subfrom=="reset":
			subm_cn=u"重设密码"
		else:
			subm_cn=u"注册"
		db=get_db('foundation')
		template=loader.get_template("tpl/msg.html")
		try:
			record=db.regmail.find_one({"mail":rgmail,"rand":rdcode})
			delta=(utc8()-record['time']).total_seconds()
			if 0<delta<900: # verification within fifteen minutes
				setuser=linkbtn(u"登录并设置个人信息","userinfo")
				context={
					"msg_title":u"%s成功"%(subm_cn),
					"msg_head":u"%s成功，请填写详细信息"%(subm_cn),
					"msg_body":rgmail+u"<br>%s成功，<br>请填写详细信息"%(subm_cn),
					"msg_links":setuser.tohtml(),
				}
				del record['rand']
				del record['time']
				del record['_id']
				record.update({
					'password':mystrify(record['password']),# hash the password
					'regtime':utc8(),
					})
				db.staff.update(
					{"mail":record['mail']},# matching and update according to the mail
					{"$set":record}, 
					upsert=True,
					)
				db.regmail.remove({"mail":rgmail})
			else:# verification expired
				resetu=linkbtn(u"重新%s"%(subm_cn),"register")
				context={
					"msg_title":u"%s未成功"%(subm_cn),
					"msg_head":u"验证链接超过15分钟",
					"msg_body":rgmail+u"<br>验证链接仅在15分钟内有效<br>请重新%s"%(subm_cn),
					"msg_links":resetu.tohtml(),
				}
				try:
					db.regmail.remove({"mail":rgmail})
				except:
					pass
			return rtway("HttpResponse",template.render(context,request))
		except: #(NameError,SyntaxError,IndexError,KeyError,IOError,AttributeError,ValueError),errmsg:
			resetu=linkbtn(subm_cn,"register")
			context={
				"msg_title":u"%s未成功"%(subm_cn),
				"msg_head":u"%s未成功，请重新%s"%(subm_cn,subm_cn),
				"msg_body":u"%s未成功，请重新%s"%(subm_cn,subm_cn),
				"msg_links":resetu.tohtml(),
			}
			return rtway("HttpResponse",template.render(context,request))
	def userinfo(self,request):
		"""
		User info function in adm class
		set and receive post of user info.
		default userinfo:enname,cnname.
		You can put more fiels in by setting self.i_userset_extra as a form you want to specify additional setting
		"""
		if self.f_save_request!=None:
			self.f_save_request(request)
		if self.f_userbar!=None:
			userb=self.f_userbar(request)
		else:
			userb=""
		tl=testlog(request)
		if tl==True:
			db=get_db("foundation")
			context=dict()
			if request.method=="POST":
				try:
					if request.session["onboard"]==True:
						form=userset(request.POST)
						form_extra=self.i_userset_extra(request.POST)
						if form.is_valid() and form_extra.is_valid():
							usercgdict=dict(form.cleaned_data)
							usercgdict.update(form_extra.cleaned_data)
							db.staff.update(
								{"mail":request.session["mail"]},
								{"$set":usercgdict},
								upsert=True,
								)
							context.update({"msgback":u"修改成功"})
							if len(form.cleaned_data["cnname"])>1:
								request.session["cnname"]=form.cleaned_data["cnname"]
							return rtway("redirect",u"/userinfo?backmsg=设置完成")
						else:
							msg_return=u"输入信息有误"
					else:
						return rtway("HttpResponseRedirect","/login")
				except:
					return rtway("HttpResponseRedirect","/login")
			else:
				pass
			template=loader.get_template("tpl/userset.html")
			try:
				userdict=db.staff.find_one({"mail":request.session["mail"]})
				form=userset(userdict)
				form_extra=self.i_userset_extra(userdict)
				context.update({
				"form":form,
				"form_extra":form_extra,
				"userb":userb,
				})
			except:
				return rtway("HttpResponseRedirect","register")
			hr=template.render(context,request)
		else:
			return rtway("redirect",tl)
		return rtway("HttpResponse",hr)
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

def getdict(requestget):
	return dict((k,dict(requestget)[k][0]) for k,v in dict(requestget).iteritems())