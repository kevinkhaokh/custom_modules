# -*- coding: utf-8 -*-

from openerp import models, fields, api

class project(models.Model):
	_inherit = 'project.project'

	partner_ids = fields.Many2many('res.partner', string="Customers")
	amt_work_tbc = fields.Float('Amount of works to be completed')
	employees_included = fields.Many2many('hr.employee', string="Employees" )
	budget = fields.Float('Budget for project')

