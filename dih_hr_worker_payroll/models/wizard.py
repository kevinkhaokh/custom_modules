# -*- coding: utf-8 -*-

from openerp import models, fields, api, exceptions


class wizard_generate_template_payroll(models.TransientModel):
	_name = "dih.worker.payroll.wizard"
	site = fields.Many2one('hr.worker.site', string='Select Worker Site', required='True')
	date_start = fields.Date(string='Start Date')
	date_end = fields.Date(string='End Date')

	@api.multi
	def dih_action_worker_payroll_generate(self):
		raise exceptions.ValidationError('works')

"""
	build skeleton with appropriate dates
	for employee in employees:
		append line in appropriate cells with infos : employee id, identification no, team, wage,
	#Function to browse employees and treat the excel file
	save generated file and attach it to selected site 
	auto download it
"""