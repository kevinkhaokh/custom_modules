# -*- coding: utf-8 -*-
{
	'name': 'Manual Reconcile Reports',
	'version': '0.1',
	'summary': 'Adds a wizard to get a reconcile report, adds end of month balances',
	'description': """
	
	End of months balances (list of eom_balance)

	***

	Add new model : dih_eom_balance with fields :

	Date

	Journal

	End of Month Bank Balance

	***

	Add new Wizard : choose month and choose journal. Requires existence of an appropriate end of month balance. Shows a new view as such:

	Journal Entries with switch reconcile button for this month from the journal with a total of all the debits on the bottom of the list.

""",
	'author': 'Kevin Khao',
	'category': 'Accounting',
	'depends': ['base', 'account', 'report'],
	'application' : False,
	'qweb':  [
		'static/src/xml/dih_manual_reconcile_templates.xml',
		],
	'data': [
		'views/dih_manual_reconcile_reports.xml',
		'static/src/xml/dih_manual_reconcile_assets.xml',
		'reports/report_manual_reconcile.xml',
	],
}
