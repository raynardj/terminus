# -*- coding: utf-8 -*-
# Shared form configurations
from django import forms
from bson.objectid import ObjectId


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
		label=u'邮箱',
	#	strip=True,
		required=True,
		)
	password=forms.CharField(
		widget=forms.widgets.PasswordInput,
		label=u'密码',
		required=True,
		)

class userset(forms.Form):
	cnname=forms.CharField(
		label=u'中文名',
		strip=True,
		required=False,
		max_length=50,
		)
	enname=forms.CharField(
		label=u'英文名',
		strip=True,
		required=False,
		max_length=30,
		)
