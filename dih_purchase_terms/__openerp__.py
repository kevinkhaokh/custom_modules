{
    'name': 'Purchasing terms interface and template',
    'description': '''
    RFQ/PO :
    Move incoterms to deliveries and invoices tab
    Move Terms and Conditions to deliveries and invoices tab
    Autofill Terms and Conditions with template
    Hide "Payment Terms" field
    ''',
    'author': 'Kevin Khao',
    'depends': ['purchase', 'account'],
	'sequence': 17,
    'application': False,
    'data': [
        'views/dih_purchase_order_view.xml',
    ]
}
