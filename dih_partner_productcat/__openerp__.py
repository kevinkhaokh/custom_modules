{
    'name': 'Partners Product Categories',
    'description': '''<br>
    Add searchable tag field "Product Category" to partners.<br>
    ''',
    'author': 'Kevin Khao',
	'sequence': 17,
    'application': False,
    'depends': ['base', 'product', 'purchase'],
    'data': [
        'views/dih_res_partner_view.xml',
    ]
}
