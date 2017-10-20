# -*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp import exceptions

class hr_employee(models.Model):
	_inherit = 'hr.employee'

	assets_currently_assigned = fields.Many2many('asset.asset', string="Assets assigned", compute='get_assets')

	@api.one
	def get_assets(self):
		self.assets_currently_assigned = self.env['asset.asset'].search([('assigned_to.id', '=', self.id)])