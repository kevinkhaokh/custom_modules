# -*- coding: utf-8 -*-
from openerp import models, fields, api
class TodoTask(models.Model):
	_inherit = 'asset.asset'
	dih_description = fields.Text('Description')
