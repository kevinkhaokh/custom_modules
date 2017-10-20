{
    'name': 'Projects modifications',
    'description': '''

    New entity project.dih.project. Created from Leads, contains fields from Leads as well as required from Jerome:

    Found under Projects - DASHBOARDS

    Normal project menuitem is renamed to Projects - APPROVALS


    ''',
    'author': 'Kevin Khao',
    'depends': ['project'],
	'sequence': 17,
    'application': False,
    'data': [
        'views/dih_project_view.xml',
        'views/dih_sales_view.xml',
    ]
}
