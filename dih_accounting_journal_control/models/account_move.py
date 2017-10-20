# -*- coding: utf-8 -*-
from openerp import models, fields, api

class account_move(models.Model):
	_inherit = 'account.move'
	
	@api.multi
	def dih_button_cancel(self):
		self.ensure_one()
		self.button_cancel()

		view = {
			'view_type': 'form',
			'view_mode': 'form',
			'res_model': 'account.move',
			'type': 'ir.actions.act_window',
			'res_id': self.id,
			'target': 'new',
			'flags': {'form': {'action_buttons': True}},
		}
		
		return view