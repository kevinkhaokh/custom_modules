# -*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp import exceptions

class account_invoice(models.Model):
	_inherit = 'account.invoice'

	"""
	@api.multi
	def to_pay(self):
		self.ensure_one()
		self.write({
			'state': 'to_pay',
		})
	"""

	state = fields.Selection([
			('draft','Draft'),
			('proforma','Pro-forma'),
			('proforma2','Pro-forma'),
			('open','Open'),
			('to_pay','To Pay'),
			('paid','Paid'),
			('cancel','Cancelled'),
		], string='Status', index=True, readonly=True, default='draft',
		track_visibility='onchange', copy=False,
		help=" * The 'Draft' status is used when a user is encoding a new and unconfirmed Invoice.\n"
			 " * The 'Pro-forma' when invoice is in Pro-forma status,invoice does not have an invoice number.\n"
			 " * The 'Open' status is used when user create invoice,a invoice number is generated.Its in open status till user does not pay invoice.\n"
			 " * The 'Paid' status is set automatically when the invoice is paid. Its related journal entries may or may not be reconciled.\n"
			 " * The 'Cancelled' status is used when user cancel invoice.")


class account_invoice_set_to_pay_wizard(models.TransientModel):
	"""
	This wizard will confirm the all the selected draft invoices
	"""
	_name = "account.invoice.set.to.pay.wizard"
	_description = "Confirm set to to pay"

	@api.multi
	def invoice_set_to_pay(self):
		self.ensure_one()
		active_ids = self.env.context['active_ids']
		proxy = self.env['account.invoice']
		for record in proxy.browse(active_ids):
			if record.state not in ('open'):
				raise exceptions.ValidationError('Some of the records are not in an open state !')
			record.write({'state': 'to_pay'})
            
		return {'type': 'ir.actions.act_window_close'}
