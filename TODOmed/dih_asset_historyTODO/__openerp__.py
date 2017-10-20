# -*- coding: utf-8 -*-

{

	'name': 'Assets History'
	'version': '0.1'
	'summary': 'Asset Modifications History',
	'description': """
	Extension to Assets module to automatic notes on field changes""",
	'author': 'Kevin',
	'category': 'Enterprise Asset Management',
	'sequence': 1,
	'depends': ['stock', 'asset', 'mail.thread'],
	'data':[
		'asset_view.xml',
	],
	'installable': True,
}
