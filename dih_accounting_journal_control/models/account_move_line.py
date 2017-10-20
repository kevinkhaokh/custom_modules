# -*- coding: utf-8 -*-
from openerp import models, fields, api

class account_move_line(models.Model):
	_inherit = 'account.move.line'

	@api.multi
	def open_journal_control_view(self):
		self.ensure_one()
		view = {
			'view_mode': 'form',
			'res_model': 'account.move',
			'type': 'ir.actions.act_window',
			'res_id': self.move_id.id,
			'target': 'new',
		}

		return view