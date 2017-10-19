# -*- coding: utf-8 -*-
# Iterations of number or letter
from ..share.lib.basic import config

class a2z(config):
	'''
	A list
	From A to Z
	'''
	pass
a2z.val=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

class process_status(config):
	pass
process_status.val=dict({
	"finished":u"审批成功",
	"inprogress":u"审批中",
	"edit":u"申请人修改",
	"revoked":u'自行撤回',
	"done":u"执行完成",
	"dead":u'申请失败',
	})

class decision_dict(config):
	pass
decision_dict.val=dict(
	{
	"refill":u"驳回让申请人修改",
	"accept":u'同意',
	"deny":u'拒绝',
	"repost":u"重新申请",
	"revoked":u'自行撤回',
	"post":u"申请",
	"dispatched":u"已发货",
	"nosupply":u"缺货",
	})