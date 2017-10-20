
{
    'name': 'Asset Tracking',
    'version': '1.0',
    'author': 'Kevin Khao',
    'description': """
	Asset tracking for LBL
    """,
    'depends' : ['base', 'purchase', 'hr'],
    'installable': True,
	'data':[
        'asset_view.xml',
        'hr_view.xml'
	],
}