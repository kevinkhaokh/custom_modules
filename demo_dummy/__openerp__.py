# -*- coding: utf-8 -*-
{
    'name': "Dummy view Demo",

    'summary': """
        Page to demonstrate dummy view
        """,

    'description': """
        Area to demonstrate dummy view
    """,

    'author': "Bahr Solutions",
    'website': "http://www.bahrsolutions.net",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base','web_dummy'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'templates.xml',
    ],
}