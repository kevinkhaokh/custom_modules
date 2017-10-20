{
    'name': 'Accounting Invoice Workflow modifications',
    'description': 'Customized Invoice workflow, adds to pay workflow step',
    'author': 'Kevin Khao',
    'depends': ['account'],
	'sequence': 17,
    'application': False,
    'data': [
        'views/account_invoice_dih_view.xml',
        'workflows/account_invoice_dih_workflow.xml',
    ]
}
