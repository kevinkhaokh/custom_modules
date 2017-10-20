# -*- coding: utf-8 -*-

from openerp import models, fields, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.multi
    def generate_balancing(self):
        generate_record_value = {
            'is_generated': True,
            'name': '',
            'debit': 0,
            'credit': 0
        }
        for move in self:
            total_debit = 0
            total_credit = 0
            for line in move.line_id:
                if not line.is_generated:
                    total_credit += line.credit
                    total_debit += line.debit
                else:
                    self.write({'line_id': [(2, line.id)]})
            if total_credit < total_debit:
                generate_record_value['account_id'] = move.journal_id.default_credit_account_id.id
                generate_record_value['credit'] = total_debit - total_credit
            elif total_credit > total_debit:
                generate_record_value['account_id'] = move.journal_id.default_debit_account_id.id
                generate_record_value['debit'] = total_credit - total_debit
            if total_credit != total_debit:
                self.write({'line_id' : [(0, 0, generate_record_value)]})

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    is_generated = fields.Boolean(string="is Generated Record", default=False)

    @api.model
    def default_get(self, fields):
        vals = super(AccountMoveLine, self).default_get(fields)
        config_id = 0
        if config_id:
            lines = self.env['account.cashbox.line'].search([('default_pos_id', '=', config_id)])
            if self.env.context.get('balance', False) == 'start':
                vals['cashbox_lines_ids'] = [[0, 0, {'coin_value': line.coin_value, 'number': line.number, 'subtotal': line.subtotal}] for line in lines]
            else:
                vals['cashbox_lines_ids'] = [[0, 0, {'coin_value': line.coin_value, 'number': 0, 'subtotal': 0.0}] for line in lines]

        vals['name'] = None
        vals['account_id'] = None
        vals['credit'] = 0
        vals['debit'] = 0
        return vals