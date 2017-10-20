# -*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp import exceptions

class asset(models.Model):
	_inherit = 'mail.thread'
	_name = 'asset.asset'

	name = fields.Char('Name', track_visibility='onchange', required=True)
	ref = fields.Char('Internal reference', track_visibility='onchange')
	category = fields.Many2one('asset.asset.category')
	specs = fields.Text('Specifications')
	assigned_to = fields.Reference([('hr.employee', 'Employee'), ('project.dashboard', 'Project')], string="Assigned to", track_visibility='onchange')
	price = fields.Float('Buying price')
	ref_invoice = fields.Many2one('account.invoice', string="Reference invoice")
	historynotes = fields.Many2many('asset.historynote', string='Events')
	last_state = fields.Char('Last state', compute='get_last_event_type', default='None', store=True)

	@api.depends('historynotes')
	def get_last_event_type(self):
		if self.historynotes:
			self.last_state = self.historynotes[0].name
		else:
			self.last_state = 'New'

class asset_category(models.Model):
	_name = 'asset.asset.category'
	name = fields.Char('Name')

class asset_historynote(models.Model):
	_name = 'asset.historynote'

	name = fields.Selection([
		('repair', 'Repair'),
		('damage', 'Damage'),
		('retire', 'Retire')
		], required=True,
		string="Type of event")
	date = fields.Date('Date of event', required=True)

	repair_supplier = fields.Many2one('res.partner', 'Supplier')
	repair_price = fields.Float('Reparation price')
	repair_ref = fields.Many2one('account.invoice', 'Reference for invoice')

	damage_text = fields.Text('Description of damaging event')

	retire_text = fields.Text('Comments')