{
    'name': 'Sales modifications',
    'description': '''

    Rename Subject to Project Name

    New text field for Scope of Works 

    New Clients associated tag-field with model Partners

    New Boolean checkable with Tender Received

    New Date of Submission of Tender

    New Estimated Start Date

    New Finish Date

    Add filters on any Date field

    Removed "Create Quotation" button

    New "Create Project" button

    Fields in Misc tab moved to main page

    Removed Leads menu item

    Link date of submission to calendar

    ''',
    'author': 'Kevin Khao',
    'depends': ['account'],
	'sequence': 17,
    'application': False,
    'data': [
        'views/account_invoice_dih_view.xml',
        'workflows/account_invoice_dih_workflow.xml',
    ]
}
