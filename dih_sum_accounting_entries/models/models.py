# -*- coding: utf-8 -*-

from openerp import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    def read_group(self, cr, uid, domain, fields, groupby, offset=0, limit=None, context=None, orderby=False, lazy=True):
        res = super(AccountMove, self).read_group(cr, uid, domain, fields, groupby, offset, limit=limit, context=context, orderby=orderby, lazy=lazy)
        if 'amount_pending' in fields:
            for line in res:
                if '__domain' in line:
                    lines = self.search(cr, uid, line['__domain'], context=context)
                    pending_value = 0.0
                    for current_account in self.browse(cr, uid, lines, context=context):
                        pending_value += current_account.amount_pending
                    line['amount_pending'] = pending_value
        if 'amount' in fields:
            for line in res:
                if '__domain' in line:
                    lines = self.search(cr, uid, line['__domain'], context=context)
                    amount_value = 0.0
                    for current_account in self.browse(cr, uid, lines, context=context):
                        amount_value += current_account.amount
                    line['amount'] = amount_value
        if 'amount_payed' in fields:
            for line in res:
                if '__domain' in line:
                    lines = self.search(cr, uid, line['__domain'], context=context)
                    payed_value = 0.0
                    for current_account in self.browse(cr, uid, lines, context=context):
                        payed_value += current_account.amount_payed
                    line['amount_payed'] = payed_value
        return res