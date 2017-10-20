# -*- coding: utf-8 -*-

from openerp import models, fields, api

class employee(models.Model):
	_inherit = 'hr.employee'
	worker_site = fields.Many2one('hr.worker.site', 'Worker Site')#add column for site one2many select NO EDIT CREATE
	worker_team = fields.Char('Worker Team')
	#add string "team"
