# -*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp.exceptions import ValidationError

class account_move(models.Model):
	_inherit = 'account.move'
	'''
	@api.model
	def create(self, vals):
		record = super(account_move, self).create(vals)
		totaldebit = 0
		if record['line_id']:
			for line in record['line_id']:
				totaldebit += line.debit
			chosenAcc = record['line_id'].account_id
			newline = {'credit': totaldebit, 'name': 'Autobalance', 'account': chosenAcc}
			record.write({'line_id': [(0, 0, newline)]})
		else: 
			raise ValidationError('There are no journal entry lines! (dih)')
		return record
	'''

	@api.multi
	def action_account_move_create_autodebitsum(self):
		newline = False
		totalcredit = 0
		totaldebit = 0
		if self.line_id:
			for line in self.line_id:
				totalcredit += line.credit
				totaldebit += line.debit
			newline = {'debit': totalcredit, 'name': 'Autobalance'}
		else:
			raise ValidationError('There are no journal entry lines ! (dih)')

		if abs(totaldebit - totalcredit) > 0.00001:
			self.write({'line_id': [(0, 0, newline)]})
			return {'type': 'ir.actions.act_window_close'}
		else:
			raise ValidationError('Lines are already balanced !')

	@api.multi
	def action_account_move_create_autocreditsum(self):
		newline = False
		totalcredit = 0
		totaldebit = 0
		if self.line_id:
			for line in self.line_id:
				totalcredit += line.credit
				totaldebit += line.debit
			newline = {'credit': totaldebit, 'name': 'Autobalance'}
		else:
			raise ValidationError('There are no journal entry lines ! (dih)')

		if abs(totaldebit - totalcredit) > 0.00001:
			self.write({'line_id': [(0, 0, newline)]})
			return {'type': 'ir.actions.act_window_close'}
		else:
			raise ValidationError('Lines are already balanced !')




		'''
	@api.one
	def _compute_debitsum_line(self):
		vals = {
			'line_id': self.line_id,
			'journal_id': self.journal_id,
			'period_id': self.period_id,
			'date': self.date,
		}
		record = super(account_move, self).create(vals)
		totaldebit = 0
		if record['line_id']:
			for line in record['line_id']:
				totaldebit += line.debit
			chosenAcc = record['line_id'].account_id
			newline = {'credit': totaldebit, 'name': 'Autobalance', 'account': chosenAcc}
			record.write({'line_id': [(0, 0, newline)]})
		else: 
			raise ValidationError('There are no journal entry lines! (dih)')
		return record
		'''