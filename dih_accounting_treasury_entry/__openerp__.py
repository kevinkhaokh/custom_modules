
{
    'name': 'Treasury Entry LBL',
    'version': '1.0',
    'author': 'Kevin Khao',
    'category': 'Generic Modules/Accounting',
    'description': """
    Treasury Entries with autobalance button
    """,
    'depends' : ['account'],
    'installable': True,
    'active': False,
    'sequence' : 50,
	'data':[
		'dih_treasury_entry.xml',
	],
}