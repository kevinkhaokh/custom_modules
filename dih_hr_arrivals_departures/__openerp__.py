# -*- coding: utf-8 -*-
{
	'name': 'HR arrivals and departures',
	'version': '0.1',
	'summary': 'Adds a new menu to keep track of arrivals and departures within the company.',
	'description': """
	Adds a new menu to keep track of arrivals and departures within the company.""",
	'author': 'Kevin Khao',
	'category': 'Asset Tracking',
	'sequence': 30,
	'depends': ['hr', 'dih_asset_tracking'],
	'data': [
		'hr_view.xml',
	],
	'installable': True,
	'application': True,
}
