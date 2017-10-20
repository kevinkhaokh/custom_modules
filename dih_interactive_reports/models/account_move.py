# -*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp import exceptions
from openerp.tools import float_compare
import datetime, calendar


class account_move(models.Model):
    _inherit = 'account.move'

    date_month = fields.Integer('Computed month', compute="_compute_month", store=True)
    date_year = fields.Integer('Computed year', compute="_compute_year", store=True)

    is_manual_reconciled_virtual = fields.Boolean('Is virtually reconciled', track_visibility="onchange")
    is_manual_reconciled_permanent = fields.Boolean('Is permanently reconciled', track_visibility="onchange")
    dih_date_reconciled = fields.Date('Date permanently reconciled')

    dih_date_virtual_reconciled = fields.Date('Date virtually reconciled', compute="_compute_date_virtual_reconcile", store=True)

    is_credit_or_debit = fields.Char('Is it a debit or a credit', compute="_compute_infos_from_line", store=True)
    dummy_credit = fields.Float('Credit', compute="_compute_infos_from_line", store=True)
    dummy_debit = fields.Float('Debit', compute="_compute_infos_from_line", store=True)
    dummy_rec_report = fields.Float('Reconciled value for reports', compute="_compute_infos_from_line", store=True)

    dummy_name = fields.Char('name or memo for the entry', compute="_compute_infos_from_line")

    dummy_rec = fields.Float('Reconciled', compute="_compute_dummy_recs", store=True)

    @api.one
    @api.depends('is_manual_reconciled_virtual')
    def _compute_date_virtual_reconcile(self):
        self.dih_date_virtual_reconciled = fields.datetime.now()

    @api.one
    @api.depends('date')
    def _compute_month(self):
        self.date_month = int(self.date[5:7])
        
    @api.one
    @api.depends('date')
    def _compute_year(self):
        self.date_year = int(self.date[0:4])

    @api.multi
    def dih_manual_reconcile(self):
        self.is_manual_reconciled_virtual = not self.is_manual_reconciled_virtual
        return True

    @api.one
    @api.depends('line_id')
    def _compute_infos_from_line(self):
        found_debit = 0.0
        found_credit = 0.0
        for line in self.line_id:
            if line.account_id == self.journal_id.default_debit_account_id or line.account_id == self.journal_id.default_credit_account_id:
                found_debit = line.debit
                found_credit = line.credit
                if line.partner_id.name:
                    self.dummy_name = line.name + ' - ' + line.partner_id.name
                else:
                    self.dummy_name = line.name
        self.dummy_credit = found_credit
        self.dummy_debit = found_debit
        if found_credit > found_debit:
            self.is_credit_or_debit = 'credit'
            self.dummy_rec_report = found_credit * -1
        if found_credit < found_debit:
            self.is_credit_or_debit = 'debit'
            self.dummy_rec_report = found_debit

    @api.one
    @api.depends('is_manual_reconciled_virtual', 'is_manual_reconciled_permanent')
    def _compute_dummy_recs(self):
        found_lines = 0
        for line in self.line_id:
            if (line.account_id == self.journal_id.default_debit_account_id) or (line.account_id == self.journal_id.default_credit_account_id):
                found_lines = found_lines + 1
#       if found_lines != 1:
#            raise exceptions.ValidationError('For any entry, there should be exactly ONE line for debit or credit on the journal\'s account. Please check the individual lines on this journal entry.')
        if self.is_manual_reconciled_virtual and (not(self.is_manual_reconciled_permanent)):
            if self.dummy_credit > self.dummy_debit:
                self.dummy_rec = self.dummy_credit * -1
            else:
                self.dummy_rec = self.dummy_debit 
        else:
            self.dummy_rec = 0.0

    @api.multi
    def action_open_edit_view(self):
        self.ensure_one()
        view = {
            'view_mode': 'form',
            'res_model': 'account.move',
            'type': 'ir.actions.act_window',
            'res_id': self.id,
            'target': 'new',
        }
        return view

    @api.model
    def get_confirm_reconciles_confirm_screen(self):
        print("function confirm reconciles confirm called")
        view = {
        'type': 'ir.actions.act_window',
        'res_model': 'dih.confirm.reconciles.temp.screen.wizard',
        'view_id' : 'dih_accounting_manual_reconcile_reports.view_form_confirm_reconciles_wizard',
        'view_mode' : 'form',
        'res_id' : 1,
        'target' : 'new',
        }
        return view

    def _get_temp_data(self, aUID):
        matches = self.env['dih.accounting.reconcile.temp.data'].search([
            ['stored_uid', '=', aUID]
            ])
        return matches

    """
    def _get_amount_manual_reconciled_this_month(self):
        matches_this_month = self.env['account.move'].search([
            ['date_month', '=', ],
            ['date_year', '=', ]
            ['is_manual_reconciled_virtual', '=', True],
        ])
        for element in matches_this_month:
            reconciled_this_month = reconciled_this_month + element.dummy_rec
        return reconciled_this_month
    """

    def _get_total_credits(self, journal_id):
        total_credits = 0.0
        matches_credits = self.env['account.move'].search([
            ['journal_id.id', '=', journal_id],
            ])
        for element in matches_credits:
            total_credits = total_credits + element.dummy_credit
        return total_credits

    def _get_total_debits(self, journal_id):
        total_debits = 0.0
        matches_debits = self.env['account.move'].search([
            ['journal_id.id', '=', journal_id],
            ])
        for element in matches_debits:
            total_debits = total_debits + element.dummy_debit
        return total_debits

    def _get_reconciled_total_credits(self, journal_id):
        total_credits = 0.0
        matches_credits1 = self.env['account.move'].search([
            ['journal_id.id', '=', journal_id],
            ['is_manual_reconciled_virtual', '=', True], #do a union with reconciled virtual or permanent
            ])
        matches_credits2 = self.env['account.move'].search([
            ['journal_id.id', '=', journal_id],
            ['is_manual_reconciled_permanent', '=', True], #do a union with reconciled virtual or permanent
            ])
        matches_credits = matches_credits1 | matches_credits2
        for element in matches_credits:
            total_credits = total_credits + element.dummy_credit
        return total_credits

    def _get_reconciled_total_debits(self, journal_id):
        total_debits = 0.0
        matches_debits1 = self.env['account.move'].search([
            ['journal_id.id', '=', journal_id],
            ['is_manual_reconciled_virtual', '=', True],
            ])
        matches_debits2 = self.env['account.move'].search([
            ['journal_id.id', '=', journal_id],
            ['is_manual_reconciled_permanent', '=', True],
            ])
        matches_debits = matches_debits1 | matches_debits2
        for element in matches_debits:
            total_debits = total_debits + element.dummy_debit
        return total_debits

    def _get_reconciled_this_month(self, journal_id, year, month): #used to be per month. but we don't need that ! instead enforce constraint on EOMBs themselves ; flag reconciled or not per month
        total_rec = 0.0
        days_in_month = (calendar.monthrange(year, month))[1]
        date_end_current_month = fields.Date.to_string(datetime.datetime(year,month,days_in_month, 23, 59, 59))
        date_start_current_month = fields.Date.to_string(datetime.datetime(year,month,1, 23, 59, 59))
        matches_dummy_rec1 = self.env['account.move'].search([
            ['journal_id.id', '=', journal_id],
            ['is_manual_reconciled_virtual', '=', True],
#            ['date', '<=', date_end_current_month],
#            ['date', '>=', date_start_current_month]
            ])
        print('Matches Y')
        print(len(matches_dummy_rec1))
        matches_dummy_rec2 = self.env['account.move'].search([
            ['journal_id.id', '=', journal_id],
            ['is_manual_reconciled_permanent', '=', True],
#            ['date', '<=', date_end_current_month],
#            ['date', '>=', date_start_current_month]
            ])
        print('Matches Z')
        print(len(matches_dummy_rec2))
        matches_dummy_rec = matches_dummy_rec1 | matches_dummy_rec2
        print('Matches X')
        print(len(matches_dummy_rec))
        for element in matches_dummy_rec:
            total_rec = total_rec + element.dummy_rec
        return total_rec

    @api.model
    def get_reconcile_display_values(self):
        print('***I***')
        matches = self._get_temp_data(self.env.uid)
        current_eomb = matches[0].current_eomb
        prev_eomb = matches[0].prev_eomb
        current_journal_id = current_eomb.journal.id
        if len(matches) == 0:
            raise exceptions.ValidationError('This should never happen. No matches.')
        elif len(matches) > 1:
            raise exceptions.ValidationError('This should never happen. more than one matches.')
        elif len(matches) == 1:
            print(len(matches))
#            reconciled_this_month =  #_get_amount_manual_reconciled_this_month()
            total_debits = self._get_total_debits(current_journal_id)
            total_credits = self._get_total_credits(current_journal_id)
            total_reconciled_debits = self._get_reconciled_total_debits(current_journal_id)
            total_reconciled_credits = self._get_reconciled_total_credits(current_journal_id)
            total_to_reconcile_debits = total_debits - total_reconciled_debits
            total_to_reconcile_credits = total_credits - total_reconciled_credits
            reconciled_this_month = self._get_reconciled_this_month(current_journal_id, current_eomb.date_year, current_eomb.date_month)

            print('***II***')
            result = {
                "prev_eomb_balance" : str(prev_eomb.balance),
#                "prev_eomb_year" : str(prev_eomb.date_year),
#                "prev_eomb_month" : str(prev_eomb.date_month),
#                "prev_eomb_journal_name" : str(prev_eomb.journal.name),
                "current_eomb_balance" : str(current_eomb.balance),
#                "current_eomb_year" : str(current_eomb.date_year),
#                "current_eomb_month" : str(current_eomb.date_month),
#                "current_eomb_journal_name" : str(current_eomb.journal.name),
#                "reconciled_this_month" : str(reconciled_this_month),
                "left_to_reconcile_this_month" : str(current_eomb.balance - prev_eomb.balance - reconciled_this_month),
                "this_month_reconciled" : str(reconciled_this_month), #sum amount reconciled for records 1.reconciled virtual and 2. this month
#                "total_credits" : str(total_credits), #sum amount reconciled for records reconciled virtual
#                "total_debits" : str(total_debits), #current eomb balance, minus total_reconciled
#                "total_reconciled_debits" : str(total_reconciled_debits),
#                "total_reconciled_credits" : str(total_reconciled_credits),
#                "total_to_reconcile_debits" : str(total_to_reconcile_debits),
#                "total_to_reconcile_credits" : str(total_to_reconcile_credits),
                "difference_current_last_balances" : str(current_eomb.balance - prev_eomb.balance)
            }
            print(result)
            return result