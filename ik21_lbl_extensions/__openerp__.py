# -*- coding: utf-8 -*-
{
    'name': "IK21 LBL Extensions",

    'summary': """
        """,

    'description': """
Module Update History:
----------------------

    * 8.0.17.02.21.0.02 :
        - Fixed incorrect Supplier source

    * 8.0.17.02.20.0.01 :
        + Adding Field
            - Add field to Partner
                - VAT(TIN): [Text]
                - Name in Khmer: [Text]
                - Address in Khmer: [Text Area]
                - Payable Name: [Text]
            - Add field to  Project
                - Approval delay (in day) : [Integer]
            - Add field to  Project Task
                - Date Return: [Date], default: empty
                - Submittal Date: [Date], default: today
                - Last day Returning: [Compute], readonly,  Submittal Date + Approval Delay
                - Time left / Late: [Compute], Readonly,
                    - If date return is not set:
                        Time left = last_day_returning - Today
                    - If return is set:
                        Time left = Last Day Returning - Date Return

                - Supplier [Many2one], default: empty
                - Code [Text]
                - Location [Text Area]
                - Remark [Text Area]

        + Customize View
            - Project Task Form
                - Add these field
                    - Date Return: [Date], default: empty
                    - Submittal Date: [Date], default: today
                    - Last day Returning: [Compute], readonly,  Submittal Date + Approval Delay
                    - Time left / Late: [Compute], Readonly
                - Rename the Description tab to Approval
                - Add these field in the Approval Tab
                    - Supplier [Many2one], default: empty
                    - Code [Text]
                    - Location [Text Area]
                    - Remark [Text Area]
            - Approval List
                - Create new view name: Approval List by duplicate of Task list
                - rename the starting date to Submittal date (display the date only, no time included)
                - Remove assign to field
                - Add 3 more field last day return, time left / Late & Remarks
                - Color the field according to the excel file

        + Extra Task
            - Save in History if these field specified has changed:
                - Description
                - Code
                - Used for
                - Location
                - Remarks
                - Date Return


    """,

    'author': "Voathnak Lim"
              ", Innovation K",
    'website': "",

    'category': 'Uncategorized',
    'version': '8.0.17.02.21.0.02',

    'depends': ['base', 'account', 'project'],

    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/partner_view.xml',
        'views/project_view.xml',
        'views/templates.xml',
    ],

    'demo': [
        'demo/demo.xml',
    ],
}