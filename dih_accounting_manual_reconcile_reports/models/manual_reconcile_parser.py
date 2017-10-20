# -*- coding: utf-8 -*-

from openerp import fields, api, models
import datetime
from openerp.api import Environment
import calendar

class manual_reconcile_parser(object):
    def __init__(self, cr, uid, name, context):
        self.env = Environment(cr, uid, context)
        #Get prev, current eombs and current journal id
        matches = self.env['dih.accounting.reconcile.temp.data'].search([
            ['stored_uid', '=', self.env.uid]
            ])
        self.current_eomb = matches[0].current_eomb
        self.prev_eomb = matches[0].prev_eomb
        self.current_journal_id = self.current_eomb.journal.id
        self.days_in_month = (calendar.monthrange(self.current_eomb.date_year,self.current_eomb.date_month))[1]
        self.start_month_formatted = fields.Date.to_string(datetime.datetime(self.current_eomb.date_year,self.current_eomb.date_month,1, 23, 59, 59))
        self.end_month_formatted = fields.Date.to_string(datetime.datetime(self.current_eomb.date_year,self.current_eomb.date_month,self.days_in_month, 23, 59, 59))
        self.current_date_formatted = fields.Date.to_string(datetime.datetime.today())
        if len(matches) == 0:
            raise exceptions.ValidationError('This should never happen. No matches. manual_reconcile_parser.py')
        elif len(matches) > 1:
            raise exceptions.ValidationError('This should never happen. More than one matches. manual_reconcile_parser.py')

        self.localcontext = {
            'get_beginning_balance' : self._get_beginning_balance,
            'get_cleared_payments' : self._get_cleared_payments,
            'get_cleared_deposit' : self._get_cleared_deposit,
            'get_total_cleared' : self._get_total_cleared,
            'get_cleared_balance' : self._get_cleared_balance,
            'get_end_balance' : self._get_end_balance,
            'get_uncleared_payments' : self._get_uncleared_payments,
            'get_uncleared_deposit' : self._get_uncleared_deposit,
            'get_uncleared_total' : self._get_uncleared_total,
            'get_register_balance_prev' : self._get_register_balance_prev,
            'get_new_payments' : self._get_new_payments,
            'get_new_deposits' : self._get_new_deposits,
            'get_new_total' : self._get_new_total,
            'get_register_balance_curr' : self._get_register_balance_curr,
            'get_end_date' : self._get_end_date,
            'get_start_date' : self._get_start_date,
            'get_current_date' : self._get_current_date,

            'get_cleared_payments_temp' : self._get_cleared_payments_temp,
            'get_cleared_deposit_temp' : self._get_cleared_deposit_temp,
            'get_total_cleared_temp' : self._get_total_cleared_temp,
            'get_cleared_balance_temp' : self._get_cleared_balance_temp,
            'get_uncleared_payments_temp' : self._get_uncleared_payments_temp,
            'get_uncleared_deposit_temp' : self._get_uncleared_deposit_temp,
            'get_uncleared_total_temp' : self._get_uncleared_total_temp,
        }

    def set_context(self, objects, data, ids, report_type = None):
        self.localcontext['data'] = data
        self.localcontext['objects'] = objects

    """
    The values are generated : 

    Beginning Balance : *previous eomb balance
    (Cleared transactions) Checks and payments : *all account.move *permanently reconciled *with a debit *this month
    (Cleared transactions) Deposits and credits : *all account.move *permanently reconciled *with a credit *this month
    Total cleared transactions : *all account.move *permanently reconciled *this month

    Cleared Balance : *current eomb balance

    (Uncleared transactions) Checks and payments : *all account.move *NOT permanently reconciled *with a debit
    (Uncleared transactions) Deposits and credits : *all account.move *NOT permanently reconciled *with a credit
    Total uncleared transactions : *all account.move *NOT permanently reconciled

    Register balance as of (last day of prev eomb) : *all account.moves *with date less or equal to prev eomb

    (New transactions) : Checks and payments : *all account.move *with date greater than prev eomb
    (New transactions) : Deposits and credits : *all account.move *with date greater than prev eomb
    Total new transactions : *sum of 2 above
    
    Ending balance : *^register balance as of (last day of prev eomb) value *^plus total new transactions

    don't forget to include journal ids on all searches ! also verify state of entry.
    """

    def _get_beginning_balance(self):
        return self.prev_eomb.balance

    def _get_cleared_payments(self):
        sum = 0.0
        account_moves = self.env['account.move'].search([
        ['journal_id', '=', self.current_journal_id],
        ['state', '=', 'posted'],
        ['is_manual_reconciled_permanent', '=', True],
        ['is_credit_or_debit', '=', 'credit'],
        ['dih_date_reconciled', '>=', self.start_month_formatted],
        ])
        for entry in account_moves:
            sum += entry.dummy_rec_report
        return sum

    def _get_cleared_payments_temp(self):
        sum = 0.0
        account_moves = self.env['account.move'].search([
        ['journal_id', '=', self.current_journal_id],
        ['state', '=', 'posted'],
        ['is_manual_reconciled_virtual', '=', True],
        ['is_credit_or_debit', '=', 'credit'],
        ['dih_date_virtual_reconciled', '>=', self.start_month_formatted],
        ])
        for entry in account_moves:
            sum += entry.dummy_rec_report
        return sum

    def _get_cleared_deposit(self):
        sum = 0.0
        account_moves = self.env['account.move'].search([
        ['journal_id', '=', self.current_journal_id],
        ['state', '=', 'posted'],
        ['is_manual_reconciled_permanent', '=', True],
        ['is_credit_or_debit', '=', 'debit'],
        ['dih_date_reconciled', '>=', self.start_month_formatted],
        ])
        for entry in account_moves:
            sum += entry.dummy_rec_report
        return sum

    def _get_cleared_deposit_temp(self):
        sum = 0.0
        account_moves = self.env['account.move'].search([
        ['journal_id', '=', self.current_journal_id],
        ['state', '=', 'posted'],
        ['is_manual_reconciled_virtual', '=', True],
        ['is_credit_or_debit', '=', 'debit'],
        ['dih_date_virtual_reconciled', '>=', self.start_month_formatted],
        ])
        for entry in account_moves:
            sum += entry.dummy_rec_report
        return sum
    
    def _get_total_cleared(self):
        sum = 0.0
        account_moves = self.env['account.move'].search([
        ['journal_id', '=', self.current_journal_id],
        ['state', '=', 'posted'],
        ['is_manual_reconciled_permanent', '=', True],
        ['dih_date_reconciled', '>=', self.start_month_formatted],
        ])
        for entry in account_moves:
            sum += entry.dummy_rec_report
        return sum
    
    def _get_total_cleared_temp(self):
        sum = 0.0
        account_moves = self.env['account.move'].search([
        ['journal_id', '=', self.current_journal_id],
        ['state', '=', 'posted'],
        ['is_manual_reconciled_virtual', '=', True],
        ['dih_date_virtual_reconciled', '>=', self.start_month_formatted],
        ])
        for entry in account_moves:
            sum += entry.dummy_rec_report
        return sum

    def _get_cleared_balance(self):
        return self.prev_eomb.balance + self._get_total_cleared()

    def _get_cleared_balance_temp(self):
        return self.prev_eomb.balance + self._get_total_cleared_temp()

    def _get_end_balance(self):
        return self.current_eomb.balance

    def _get_uncleared_payments(self):
        account_moves = self.env['account.move'].search([
        ['journal_id', '=', self.current_journal_id],
        ['state', '=', 'posted'],
        ['is_manual_reconciled_permanent', '=', False],
        ['is_credit_or_debit', '=', 'credit'],
        ])
        sum = 0.0
        for entry in account_moves:
            sum += entry.dummy_rec_report
        return sum

    def _get_uncleared_payments_temp(self):
        account_moves = self.env['account.move'].search([
        ['journal_id', '=', self.current_journal_id],
        ['state', '=', 'posted'],
        ['is_manual_reconciled_virtual', '=', False],
        ['is_credit_or_debit', '=', 'credit'],
        ])
        sum = 0.0
        for entry in account_moves:
            sum += entry.dummy_rec_report
        return sum

    def _get_uncleared_deposit(self):
        account_moves = self.env['account.move'].search([
        ['journal_id', '=', self.current_journal_id],
        ['state', '=', 'posted'],
        ['is_manual_reconciled_permanent', '=', False],
        ['is_credit_or_debit', '=', 'debit'],
        ])
        sum = 0.0
        for entry in account_moves:
            sum += entry.dummy_rec_report
        return sum

    def _get_uncleared_deposit_temp(self):
        account_moves = self.env['account.move'].search([
        ['journal_id', '=', self.current_journal_id],
        ['state', '=', 'posted'],
        ['is_manual_reconciled_virtual', '=', False],
        ['is_credit_or_debit', '=', 'debit'],
        ])
        sum = 0.0
        for entry in account_moves:
            sum += entry.dummy_rec_report
        return sum

    def _get_uncleared_total(self):
        account_moves = self.env['account.move'].search([
        ['journal_id', '=', self.current_journal_id],
        ['state', '=', 'posted'],
        ['is_manual_reconciled_permanent', '=', False],
        ])
        sum = 0.0
        for entry in account_moves:
            sum += entry.dummy_rec_report
        print(sum)
        return sum

    def _get_uncleared_total_temp(self):
        account_moves = self.env['account.move'].search([
        ['journal_id', '=', self.current_journal_id],
        ['state', '=', 'posted'],
        ['is_manual_reconciled_virtual', '=', False],
        ])
        sum = 0.0
        for entry in account_moves:
            sum += entry.dummy_rec_report
        print(sum)
        return sum

    def _get_register_balance_prev(self):
        account_moves = self.env['account.move'].search([
        ['journal_id', '=', self.current_journal_id],
        ['state', '=', 'posted'],
        ['date', '<=', self.start_month_formatted],
        ])
        sum = 0.0
        for entry in account_moves:
            sum += entry.dummy_rec_report
        return sum

    def _get_new_payments(self):
        account_moves = self.env['account.move'].search([
        ['journal_id', '=', self.current_journal_id],
        ['state', '=', 'posted'],
        ['is_credit_or_debit', '=', 'credit'],
        ['date', '>=', self.start_month_formatted],
        ])
        sum = 0.0
        for entry in account_moves:
            sum += entry.dummy_rec_report
        return sum

    def _get_new_deposits(self):
        account_moves = self.env['account.move'].search([
        ['journal_id', '=', self.current_journal_id],
        ['state', '=', 'posted'],
        ['is_credit_or_debit', '=', 'debit'],
        ['date', '>=', self.start_month_formatted],
        ])
        sum = 0.0
        for entry in account_moves:
            sum += entry.dummy_rec_report
        return sum

    def _get_new_total(self):
        sum = 0.0
        account_moves = self.env['account.move'].search([
        ['journal_id', '=', self.current_journal_id],
        ['state', '=', 'posted'],
        ['date', '>=', self.start_month_formatted],
        ])
        for entry in account_moves:
            sum += entry.dummy_rec_report
        return sum

    def _get_register_balance_curr(self):
        sum = 0.0
        account_moves = self.env['account.move'].search([
        ['journal_id', '=', self.current_journal_id],
        ['state', '=', 'posted'],
        ])
        for entry in account_moves:
            sum += entry.dummy_rec_report
        return sum

    def _get_end_date(self):
        end_date = self.end_month_formatted
        return end_date

    def _get_start_date(self):
        start_date = self.start_month_formatted
        return start_date

    def _get_current_date(self):
        current_date = self.current_date_formatted
        return current_date

class report_manual_reconcile_parser(models.AbstractModel):
    _name="report.dih_accounting_manual_reconcile_reports.report_dih_manual_reconcile"
    _inherit='report.abstract_report'
    _template='dih_accounting_manual_reconcile_reports.report_dih_manual_reconcile'
    _wrapped_report_class=manual_reconcile_parser

class report_manual_reconcile_parser(models.AbstractModel):
    _name="report.dih_accounting_manual_reconcile_reports.report_dih_temp_reconcile"
    _inherit='report.abstract_report'
    _template='dih_accounting_manual_reconcile_reports.report_dih_temp_reconcile'
    _wrapped_report_class=manual_reconcile_parser