# -*- coding: utf-8 -*-
{
	'name': 'Interactive Accounting Reports',
	'version': '0.1',
	'summary': 'Adds interactive accounting reports : balance sheet and profit and loss, detailed.',
	'description': """
	
	Adds interactive accounting reports : balance sheet and profit and loss, detailed.

	IMPLEMENTATION DETAIL : CREATE METHOD OF IR UI VIEWS ARE MODIFIED. THIS IS GLOBAL. SHOULD UPDATE FOR NEW VIEWS

""",
	'author': 'Kevin Khao',
	'category': 'Accounting',
	'depends': ['base', 'account', 'report'],
	'application' : False,
	'qweb':  [
		'static/src/xml/dih_int_rep_templates.xml',
		],
	'data': [
		'views/dih_int_rep_views.xml',
		'static/src/xml/dih_int_rep_assets.xml',
	],
}
