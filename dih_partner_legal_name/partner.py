# -*- coding: utf-8 -*-

from openerp import models, fields, api

class res_partner(models.Model):
	_inherit = 'res.partner'
	legal_name = fields.Char('Legal Name')

