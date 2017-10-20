# -*- coding: utf-8 -*-

from openerp import models, fields, api

# add new class for sites
class dih_worker_site(models.Model):
	_name='hr.worker.site'
	name = fields.Char('Site', required=True)