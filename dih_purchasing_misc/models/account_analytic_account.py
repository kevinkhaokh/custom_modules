from openerp import models, fields, api
import datetime

class account_analytic_account(models.Model):
	_inherit = "account.analytic.account"

	dih_seqname = fields.Char('Prefix for internal PO number for purchasers', required=True)