
{
    'name': 'jsthing test',
    'version': '1.0',
    'author': 'Kevin Khao',
    'category': 'Generic Modules/Accounting',
    'description': """
    Treasury Entries with autobalance button
    """,
    'installable': True,
    'active': False,
    'sequence' : 50,
	'data':[
		'views/project.xml',
	],
    'qweb' :
    ['static/src/xml/project_button.xml',
    ]
}