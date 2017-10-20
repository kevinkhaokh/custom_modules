# -*- coding: utf-8 -*-

from openerp import fields, models, api, exceptions
from datetime import datetime
import sys

class reconcile_wizard_confirm_screen(models.TransientModel):

    _name = "dih.confirm.reconciles.temp.screen.wizard"
    _description = "Reconcile Wizard Confirmation Screen"

    @api.multi
    def confirm_reconciles(self):

        matches = self.env['account.move'].search([
            ['is_manual_reconciled_virtual', '=', True],
            ])
        print len(matches)
        matches.write({
            'is_manual_reconciled_permanent' : True,
            'dih_date_reconciled' : fields.Date.today()})

        self.generate_report()

        #generate and get it to download and attach
        matches = self.env['dih.accounting.reconcile.temp.data'].search([
            ['stored_uid', '=', self.env.uid]
            ])
        self.current_eomb = matches[0].current_eomb
        self.current_journal_id = matches[0].current_eomb.journal.id

        account_move_model = self.env['account.move']
        all_account_moves = account_move_model.search([
        ['journal_id', '=', self.current_journal_id],
        ])
        all_account_moves_ids = []
        for el in all_account_moves:
            all_account_moves_ids.append(el.id)
        acr = self.env.cr
        auid = self.env.uid
        return self.pool.get('report').get_action(acr, auid, all_account_moves_ids, 'dih_accounting_manual_reconcile_reports.report_dih_manual_reconcile')
#        return {
 #           'type': 'ir.actions.act_window',
  #          'res_model': 'account.move',
   #         'views' : [[False, "tree"]]
    #    }

    def generate_report(self):

        matches = self.env['dih.accounting.reconcile.temp.data'].search([
            ['stored_uid', '=', self.env.uid]
            ])
        self.current_eomb = matches[0].current_eomb
        self.current_journal_id = matches[0].current_eomb.journal.id

        account_moves = self.env['account.move'].search([
        ['journal_id', '=', self.current_journal_id],
        ])
        for element in account_moves:
            print(element.id)
            print(element.is_manual_reconciled_permanent)
            print(element.is_credit_or_debit)