# -*- coding: utf-8 -*-
{
	'name': 'Accounting invoice filter on product',
	'version': '0.1',
	'summary': 'Adds a filter on product_id field in invoice_line',
	'description': """
	Adds a filter on product_id field in invoice_line. Only "can be sold=true" will be displayed.""",
	'author': 'Kevin Khao',
	'category': 'Human Resources',
	'sequence': 32,
	'depends': ['account'],
	'data': [
		'account_invoice_view_prodfilter.xml',
	],
	'installable': True,
}
