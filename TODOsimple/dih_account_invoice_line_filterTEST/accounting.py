# -*- coding: utf-8 -*-

from openerp import models, fields, api

class hr_employee(models.Model):
	_inherit = 'hr.employee'
	dih_join_date = fields.Date('Join date')

