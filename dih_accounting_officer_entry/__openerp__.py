# -*- coding: utf-8 -*-
{
	'name': 'Accounting Officer entries',
	'version': '0.1',
	'summary': 'Menu item to show only entries created by self',
	'description': """

	New menu item to show journal entries that have been created by the user himself

""",
	'author': 'Kevin Khao',
	'category': 'Accounting',
	'sequence': 30,
	'depends': ['account'],
	'data': [
		'views/dih_accounting_officer_entry.xml',
	],
	'installable': True,
}
