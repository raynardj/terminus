# -*- coding: utf-8 -*-
from django import forms
from bson.objectid import ObjectId
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

# class email_login(forms.Form):
# 	email=forms.EmailField(
# 		label=u'公司邮箱',
# 		strip=True,
# 		required=True,
# 		)
# 	password=forms.CharField(
# 		widget=forms.widgets.PasswordInput,
# 		label=u'密码',
# 		required=True,
# 		)
#	department=forms.TypedChoiceField(
#		label=u'部门',
#		choices=[
#		['finance',u'财务部'],
#		['it',u'资讯科技部'],
#		],
#		)
#	taskname=forms.CharField(
#		widget=forms.widgets.HiddenInput,
#		)
#	fileup=forms.FileField(
#		label=u'文件',
#		)