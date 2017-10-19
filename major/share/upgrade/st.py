# -*- coding: utf-8 -*-

#Web site general settings

from ..share.lib.basic import config
class gen(config):
	pass
gen.info=dict({
	"sitename":u"sitenamehere",
	"sitemotto":u"Agile, smart and effective",
	"sitenamecn":u"CNNAME",
	"sitemail":"abc@def.com",
	"siteadmin":"admin@def.cn",#Site Administrator's mail box
	})
gen.reg=dict({
	#"domain":"staples" # mandatary mail domain, remove this entry if the register mail addrss is not mandatory
	})
gen.session=dict({
	"expire":60*60*24*15,# Last number is days
	})
