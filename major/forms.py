# -*- coding: utf-8 -*-
from django import forms
from bson.objectid import ObjectId
from bootstrap3_datetime.widgets import DateTimePicker
#from lib import get_db

class rich_form(forms.Form):
	def as_read(self):
		rt=''
		for k,v in self.cleaned_data.iteritems():
			rt+='<tr><td>'
			rt+=str(self.field[k].label)
			rt+='</td><td>'
			if type(v)==list:
				for ite in v:
					rt+=str(ite)
			else:
				rt+=str(v)
			rt+='</td></tr>'
	def set_choices(self,fieldname,newlist):
		self.fields[fieldname].choices=newlist

class email_login(forms.Form):
	email=forms.EmailField(
		label=u'公司邮箱',
		#strip=True,
		required=True,
		)
	password=forms.CharField(
		widget=forms.widgets.PasswordInput,
		label=u'密码',
		required=True,
		)
class clientset(forms.Form):
	client=forms.IntegerField(
		label=u'客户编码',
		widget=forms.widgets.TextInput,
		)
	client_cn=forms.CharField(
		label=u'客户名称',
		strip=True,
		)
	sales=forms.CharField(
		label=u'销售',
		strip=True,
		required=False,
		)
	cre_term=forms.CharField(
		label=u'账期',
		strip=True,
		required=False,
		)
class userset_extra(forms.Form):
	manager=forms.CharField(
		label=u'直属领导',
		strip=True,
		required=False,
		max_length=30,
		)
	department=forms.TypedChoiceField(
		label=u'部门',
		choices=[
		['finance',u'财务部'],
		['it',u'资讯科技部'],
		],
		)
	ext=forms.CharField(
		label=u'电话/分机号',
		strip=True,
		required=False,
		max_length=20,
		)
from django.template import loader
class tagform:
	def __init__(self,tagfield,inputdict=None):
		if inputdict:
			self.inputdict=inputdict
		else:
			self.inputdict={}
		self.tagfield=tagfield
		self.update_cross_pull={}

	def inputdict_process(self):
		if self.inputdict:
			for item in self.inputdict:
				item.update({"id":item.__getitem__("_id")})
				item.update({"tagname":item[self.tagfield]})
				item.update({"jpack":{
						"update_condi":{
							"_id":str(item.__getitem__("_id"))
							},
						"update_cross_pull":{
							"$pull":self.update_cross_pull
							},
						}
					})
		else:
			pass

	def tagtile(self,template_dir="tagtile.html"):
		self.inputdict_process()
		template=loader.get_template(template_dir)
		context={
		"taglist":self.inputdict,
		"tagfield":self.tagfield,
		}
		return template.render(context)


class uploadset(rich_form):
	schema=forms.TypedChoiceField(
		label=u'空表头',
		initial="ignore",
		widget=forms.widgets.RadioSelect,
		choices=[
		["ignore",u'忽略'],
		["match",u'匹配'],
		["upsert",u'插入/更新'],
		["push",u'推入数组']
		],
		)
#	dbfield=forms.CharField(
#		label=u'数据库字段',
#		required=False,
#		)

class fm_officeuse(rich_form):
	stburl=forms.CharField(
		label=u'链接',
		max_length=100,
		required=False,
		widget=forms.TextInput(attrs={"placeholder":u'贴入史泰博官网的产品链接',},)
		)

class fm_officeuse_proid(fm_officeuse):
	pro_id=forms.CharField()

class office_use_detail(rich_form):
	processid=forms.CharField(
		widget=forms.widgets.HiddenInput,
		required=False,
	)
	pic_src=forms.CharField(
		widget=forms.widgets.HiddenInput,
		required=False,
	)
	brandname=forms.CharField(
		widget=forms.widgets.HiddenInput,
		required=False,
	)
	itemname=forms.CharField(
		label=u'物品名称',
		max_length=100,
		)
	price=forms.DecimalField(
		label=u'单价',
		min_value=0,
		)
	pro_id=forms.CharField(
		label=u'官网编号',
		)
	qtt=forms.IntegerField(
		label=u'数量',
		required=False,
		initial=1,
		min_value=1,
		)
#	pic_src=forms.CharField(
#		required=False,
#		)

class upload_input(rich_form):
	fname=forms.CharField(
		label=u'上传流程',
		max_length=50,
		)
	fileup=forms.FileField(
		label=u'文件地址',
		)
class upload_hidden(rich_form):
	md=forms.CharField(
		initial="upload",
		widget=forms.widgets.HiddenInput,
		)

class auth_default(rich_form):
	r=forms.TypedChoiceField(
		label=u'Read',
		initial=1,
		widget=forms.widgets.RadioSelect,
		choices=[
		[1,u'Yes'],
		[0,u'No'],
		])
	w=forms.TypedChoiceField(
		label=u'Write',
		initial=1,
		widget=forms.widgets.RadioSelect,
		choices=[
		[1,u'Yes'],
		[0,u'No'],
		])
	# Write authorization won't work after the approval was granted
#	s=forms.TypedChoiceField(
#		label=u'Super',
#		initial=0,
#		widget=forms.widgets.RadioSelect,
#		choices=[
#		[1,u'Yes'],
#		[0,u'No'],
#		])
	# User can send emails to super to ask their grand

class user_auth_apply(auth_default):
	"""
	User can apply for user authorization
	"""
	taskname=forms.CharField(
		widget=forms.widgets.HiddenInput,
		)
	process=forms.CharField(
		initial=u"auth",
		widget=forms.widgets.HiddenInput,
	)
	#processid
	apid=forms.CharField(
		widget=forms.widgets.HiddenInput,
		)
	#need to inputa list of super assigner
# co	supers=forms.TypedChoiceField(
# co		label=u'Role Assigner',
# co		widget=forms.widgets.RadioSelect,
# co		)
# co	remark=forms.CharField(
# co		label=u"Remark",
# co		max_length=500,
# co		required=False,
# co		)
class task_write(auth_default):
	s=None
	settype=forms.CharField(
		initial=u"settask",
		widget=forms.widgets.HiddenInput,
	)
	taskname=forms.CharField(
		label=u'Task Name',
		max_length=50,
		)
class page_selector_form(rich_form):
	page=forms.IntegerField(
		label=u"Page",
		initial=1,
		max_value=2,
		min_value=1,
		)
class table_book_filter(rich_form):
	fil_applier=forms.CharField(
		label=u'申请人',
		)

class transparent_set(rich_form):
	task=forms.TypedChoiceField(
		label=u'事务',
		initial="officeuse",
		widget=forms.widgets.RadioSelect,
		choices=[
		["officeuse",u'行政领用'],
		],
		)
	datestart=forms.DateField(
		widget=DateTimePicker(options={"format": "YYYY-MM-DD","pickTime":False}),
		label=u'开始日期',
		required=False,
		)
	dateend=forms.DateField(
		widget=DateTimePicker(options={"format": "YYYY-MM-DD","pickTime":False}),
		label=u'结束日期',
		required=False,
		)
	prospect=forms.TypedChoiceField(
		label=u'查看方式',
		initial="sf",
		widget=forms.widgets.RadioSelect,
		choices=[
		["sf",u'只看自己'],# stands for self
		["dp",u'我的部门'],# stands for department
		],
		)
class download_range(rich_form):
	datestart=forms.DateField(
		widget=DateTimePicker(options={"format": "YYYY-MM-DD","pickTime":False}),
		label=u'开始日期',
		required=False,
		)
	dateend=forms.DateField(
		widget=DateTimePicker(options={"format": "YYYY-MM-DD","pickTime":False}),
		label=u'结束日期',
		required=False,
		)
	taskname=forms.TypedChoiceField(
		label=u'申请种类',
		choices=[
		['officeuse',u'行政领用'],
		['auth',u'权限申请'],
		],
		)
class process_status(rich_form):
	pstatus=forms.TypedChoiceField(
		required=True,
		label=u'表单状态',
		initial=["finished","done"],
		widget=forms.widgets.CheckboxSelectMultiple,
		choices=[
	["finished",u"审批成功"],
	["inprogress",u"审批中"],
	["edit",u"申请人修改"],
	["revoked",u'自行撤回'],
	["done",u"执行完成"],
	["dead",u'申请失败'],
		])
class loadback(rich_form):
	md=forms.CharField(
		widget=forms.widgets.HiddenInput,
		required=False,
		initial='loadback',
	)
	taskname=forms.TypedChoiceField(
		label=u'申请种类',
		choices=[
		['officeuse',u'行政领用'],
		['auth',u'权限申请'],
		],
		)
	lbfile=forms.FileField(
		label=u'文件地址',
		)
class groupinfo_form(rich_form):
	groupname=forms.CharField(
		required=True,
		label=u'团队英文名',
		max_length=20,
		)
	cnname=forms.CharField(
		required=True,
		label=u'团队中文名',
		max_length=20,
		)
	groupid=forms.CharField(
		widget=forms.widgets.HiddenInput,
		required=False,
	)
class cssupload(rich_form):
	csstask=forms.TypedChoiceField(
		label=u'上传任务',
		required=True,
		choices=[
		['contact',u'联系方式'],
		['user',u'用户设置'],
		['costcenter',u'成本中心'],
		['addr',u'新增地址'],
		],
		)
	fileup=forms.FileField(
		label=u'文件',
		)

class cssadv_list(rich_form):
	datestart=forms.DateField(
		widget=DateTimePicker(options={"format": "YYYY-MM-DD","pickTime":False}),
		label=u'开始日期',
		required=False,
		)
	dateend=forms.DateField(
		widget=DateTimePicker(options={"format": "YYYY-MM-DD","pickTime":False}),
		label=u'结束日期',
		required=False,
		)
	csstask=forms.TypedChoiceField(
		label=u'上传任务',
		required=True,
		choices=[
		['contact',u'联系方式'],
		['user',u'用户设置'],
		['costcenter',u'成本中心'],
		['addr',u'新增地址'],
		],
		)
	status=forms.TypedChoiceField(
		label=u'处理状态',
		required=True,
		choices=[
		['0',u'未处理'],
		['1',u'已完成'],
		['-1',u'已删除'],
		],
		)

class ar_upload(rich_form):
	formtype=forms.TypedChoiceField(
		label=u'上传文件',
		required=True,
		choices=[
		['overdue',u'逾期报表'],
		['arbd',u'AR Breakdown'],
		['cplist',u'项目清单'],
		],
		)
	fileup=forms.FileField(
		label=u'文件',
		)
	exdate=forms.DateField(
		widget=DateTimePicker(options={"format": "YYYY-MM-DD","pickTime":False}),
		label=u'导出日期',
		required=True,
		)
class od_upload(rich_form):
	formtype=forms.TypedChoiceField(
		label=u'上传文件',
		required=True,
		choices=[
		['overdue',u'逾期报表'],
		],
		)
	fileup=forms.FileField(
		label=u'文件',
		)
