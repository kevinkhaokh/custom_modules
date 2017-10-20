# -*- coding: utf-8 -*-

from openerp import models, fields, api

class hr_employee(models.Model):
	_inherit = 'hr.employee'
	dih_allowance_spouse = fields.Boolean('Allowance for spouse')
	dih_allowance_children = fields.Integer('Allowance for dependable child')

