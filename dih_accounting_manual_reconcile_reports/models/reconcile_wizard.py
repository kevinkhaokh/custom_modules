# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import fields, models, api, exceptions
import datetime

class reconcile_wizard(models.TransientModel):

    _name = "dih.reconcile.wizard"
    _description = "Reconcile Wizard"

    select_month = fields.Selection([
        (1,'January'),
        (2,'February'),
        (3,'March'),
        (4,'April'),
        (5,'May'),
        (6,'June'),
        (7,'July'),
        (8,'August'),
        (9,'September'),
        (10,'October'),
        (11,'November'),
        (12,'December')
        ],
        'Select Month', required='True', default=lambda self: self._get_default_month()
        )

    select_year = fields.Integer(string='Select year', required='True', default=lambda self: self._get_default_year())
    select_journal = fields.Many2one('account.journal', string='Select journal', required='True')
    display_previous_eom = fields.Float(string='Previous EOM balance', compute="_compute_get_previous_eom_balance")
    select_current_eom = fields.Float(string='Current balance for end of month')

    @api.model
    def _get_default_month(self):
        return datetime.date.today().month
    
    @api.model
    def _get_default_year(self):
        return datetime.date.today().year

    def _get_temp_data(self, uid):
        matches = self.env['dih.accounting.reconcile.temp.data'].search([
            ['stored_uid', '=', uid]
            ])
        return matches

    def _get_prev_eom(self, year, month, journal_id): #for a given date, returns the previous EOM matches
        return_earlier_year = False
        if(month == 1):
            month_calc = 12
            return_earlier_year = True
        else:
            month = month-1
        if return_earlier_year:
            year = year-1

        matches = self.env['dih.accounting.manual.reconcile.reports.reconcile.eomb'].search([
            ['date_month', '=', month],
            ['date_year', '=', year],
            ['journal.id', '=', journal_id]
            ])
        return matches

    def _get_current_eom(self, year, month, journal_id): #for a given date, returns the matches for EOM of that month
        matches = self.env['dih.accounting.manual.reconcile.reports.reconcile.eomb'].search([
            ['date_month', '=', month],
            ['date_year', '=', year],
            ['journal.id', '=', journal_id]
            ])
        return matches

    @api.depends('select_month', 'select_year', 'select_journal')
    def _compute_get_previous_eom_balance(self):
        matches = self._get_prev_eom(self.select_year, self.select_month, self.select_journal.id)
        if len(matches) > 0:
            self.display_previous_eom = matches[0].balance

    @api.onchange('select_month, select_year', 'select_journal')
    def _onchange_current_eom(self):
        matches = self._get_current_eom(self.select_year, self.select_month, self.select_journal.id)
        if len(matches) == 1:
            self.select_current_eom = matches[0].balance

    def _clear_virtual_reconciles(self, journal_id):
        matches = self.env['account.move'].search([
            ['journal_id.id', '=', journal_id],
            ])
        matches.write({'is_manual_reconciled_virtual' : False})

    @api.multi
    def dih_action_get_view(self):
        for element in self._get_temp_data(self.env.uid):
            element.unlink()

        selected_month = self.select_month
        selected_journal = self.select_journal
        selected_year = self.select_year
        matches = self._get_current_eom(selected_year, selected_month, selected_journal.id)
        matches_prev = self._get_prev_eom(selected_year, selected_month, selected_journal.id)
        #self._clear_virtual_reconciles(selected_journal.id)
        if len(matches) == 0 or len(matches_prev) == 0:
            raise exceptions.ValidationError('Please make sure that the end of month balances exist : for the current month, AND for the previous month.')

        else:
            j_id = selected_journal.id
            domain = ([
                ['journal_id.id', '=', j_id],
                ['journal_id.type', '=', 'bank'],
                ])
            context = "{'search_default_filter_not_reconciled_permanently' : 1, 'some_value' : 'abc'}"
            viewid = self.env.ref('dih_accounting_manual_reconcile_reports.view_move_tree_manual_reconcile_report', False).id
            view = {
                'domain': domain,
#                'views': [(viewid,'tree')],
                'view_id' : viewid, #'view_move_tree_manual_reconcile_report',
                'view_mode' : 'dih_reconcile_tree_with_header',
                'res_model': 'account.move',
                'type': 'ir.actions.act_window',
                'context': context,
                'target': 'current'
            }

            if len(matches) == 1:
                matches[0].write({'balance' : self.select_current_eom})
                self.env['dih.accounting.reconcile.temp.data'].create({     #create the temp data for displaying in next view
                    'stored_uid' : self._context['uid'],
                    'prev_eomb' : (self._get_prev_eom(selected_year, selected_month, selected_journal.id))[0].id,
                    'current_eomb' : matches[0].id,
                    })
            	return view

            else:
            	raise exceptions.ValidationError('There are more than one end of month balances for that month. Please contact the administrator.')