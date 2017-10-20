from openerp import fields, api, models

class example_report_parser(object):
	def __init__(self, cr, uid, name, context):
		self.localcontext = {
			'some_value' : 'some static value',
			'somefunc' : self._somefunc,
		}

	def _somefunc(self):
		return 'FUNCVALUE'

	def set_context(self, objects, data, ids, report_type = None):
		self.localcontext['data'] = data
		self.localcontext['objects'] = objects

class report_test1_parser(models.AbstractModel):
	_name="report.dih_reports_test.report_dih_move"
	_inherit='report.abstract_report'
	_template='dih_reports_test.report_dih_move'
	_wrapped_report_class=example_report_parser