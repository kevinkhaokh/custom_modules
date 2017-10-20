# -*- coding: utf-8 -*-
{
    'name': "DIH Accounting Treasory Entries",

    'summary': """
        """,

    'description': """
        - 8.0.0.1: July 25, 2017
    """,

    'author': "",
    'website': "",


    'category': 'Uncategorized',
    'version': '8.0.0.1',

    'depends': ['base', 'account'],

    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}