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

from openerp.osv import osv,fields
from openerp.tools.translate import _
from openerp.tools.amount_to_text_en import amount_to_text
from lxml import etree

class account_voucher(osv.osv):
    _inherit = 'account.voucher'

    def _make_journal_search(self, cr, uid, ttype, context=None):
        if context is None: 
            context = {}
        journal_pool = self.pool.get('account.journal')
        if context.get('write_check',False) :
            return journal_pool.search(cr, uid, [('allow_check_writing', '=', True)], limit=1)
        return journal_pool.search(cr, uid, [('type', '=', ttype)], limit=1)

    _columns = {
        'amount_in_word' : fields.char("Amount in Word", readonly=True, states={'draft':[('readonly',False)]}),
        'allow_check' : fields.related('journal_id', 'allow_check_writing', type='boolean', string='Allow Check Writing'),
        'number': fields.char('Number', readonly=True, copy=False),
    }

    def _amount_to_text(self, cr, uid, amount, currency_id, context=None):
        # Currency complete name is not available in res.currency model
        # Exceptions done here (EUR, USD, BRL) cover 75% of cases
        # For other currencies, display the currency code
        currency = self.pool['res.currency'].browse(cr, uid, currency_id, context=context)
        if currency.name.upper() == 'EUR':
            currency_name = 'Euro'
        elif currency.name.upper() == 'USD':
            currency_name = 'Dollars'
        elif currency.name.upper() == 'BRL':
            currency_name = 'reais'
        else:
            currency_name = currency.name
        #TODO : generic amount_to_text is not ready yet, otherwise language (and country) and currency can be passed
        #amount_in_word = amount_to_text(amount, context=context)
        return amount_to_text(amount, currency=currency_name)

    def onchange_amount(self, cr, uid, ids, amount, rate, partner_id, journal_id, currency_id, ttype, date, payment_rate_currency_id, company_id, context=None):
        """ Inherited - add amount_in_word and allow_check_writting in returned value dictionary """
        if not context:
            context = {}
        default = super(account_voucher, self).onchange_amount(cr, uid, ids, amount, rate, partner_id, journal_id, currency_id, ttype, date, payment_rate_currency_id, company_id, context=context)
        if 'value' in default:
            amount = 'amount' in default['value'] and default['value']['amount'] or amount
            amount_in_word = self._amount_to_text(cr, uid, amount, currency_id, context=context)
            default['value'].update({'amount_in_word':amount_in_word})
            if journal_id:
                allow_check_writing = self.pool.get('account.journal').browse(cr, uid, journal_id, context=context).allow_check_writing
                default['value'].update({'allow_check':allow_check_writing})
        return default

    def print_check(self, cr, uid, ids, context=None):
        if not ids:
            raise osv.except_osv(_('Printing error'), _('No check selected '))

        data = {
            'id': ids and ids[0],
            'ids': ids,
        }

        return self.pool['report'].get_action(
            cr, uid, [], 'account_check_writing.report_check', data=data, context=context
        )

    def create(self, cr, uid, vals, context=None):
        if vals.get('amount') and vals.get('journal_id') and 'amount_in_word' not in vals:
            vals['amount_in_word'] = self._amount_to_text(cr, uid, vals['amount'], vals.get('currency_id') or \
                self.pool['account.journal'].browse(cr, uid, vals['journal_id'], context=context).currency.id or \
                self.pool['res.company'].browse(cr, uid, vals['company_id']).currency_id.id, context=context)
        return super(account_voucher, self).create(cr, uid, vals, context=context)

    def copy_data(self, cr, uid, id, default=None, context=None):
        data = super(account_voucher, self).copy_data(cr, uid, id, default=default, context=context)
        if data.get('period_id') and not data.get('date'):
            account_period_obj = self.pool.get('account.period')
            ids = account_period_obj.find(cr, uid, context=context)
            if ids:
                data['period_id'] = ids[0]
        return data

    def write(self, cr, uid, ids, vals, context=None):
        if vals.get('amount') and 'amount_in_word' not in vals:
            voucher = self.browse(cr, uid, ids, context=context)
            currency_id = vals.get('currency_id')
            if not currency_id:
                journal = vals.get('journal_id') and self.pool['account.journal'].browse(cr, uid, vals['journal_id'], context=context) or voucher.journal_id
                currency_id = journal.currency.id
            if not currency_id:
                company = vals.get('company_id') and self.pool['res.company'].browse(cr, uid, vals['company_id'], context=context) or voucher.company_id
                currency_id = company.currency_id.id
            vals['amount_in_word'] = self._amount_to_text(cr, uid, vals['amount'], currency_id, context=context)
        return super(account_voucher, self).write(cr, uid, ids, vals, context=context)

    def fields_view_get(self, cr, uid, view_id=None, view_type=False, context=None, toolbar=False, submenu=False):
        """
            Add domain 'allow_check_writting = True' on journal_id field and remove 'widget = selection' on the same
            field because the dynamic domain is not allowed on such widget
        """
        if not context: context = {}
        res = super(account_voucher, self).fields_view_get(cr, uid, view_id=view_id, view_type=view_type, context=context, toolbar=toolbar, submenu=submenu)
        doc = etree.XML(res['arch'])
        nodes = doc.xpath("//field[@name='journal_id']")
        if context.get('write_check', False) :
            for node in nodes:
                node.set('domain', "[('type', '=', 'bank'), ('allow_check_writing','=',True)]")
                node.set('widget', '')
            res['arch'] = etree.tostring(doc)
        return res


    def recompute_voucher_lines(self, cr, uid, ids, partner_id, journal_id, price, currency_id, ttype, date, context=None):
        """
        Returns a dict that contains new values and context

        @param partner_id: latest value from user input for field partner_id
        @param args: other arguments
        @param context: context arguments, like lang, time zone

        @return: Returns a dict which contains new values, and context
        """
        def _remove_noise_in_o2m():
            """if the line is partially reconciled, then we must pay attention to display it only once and
                in the good o2m.
                This function returns True if the line is considered as noise and should not be displayed
            """
            if _check_line_in_to_pay():
                return False

            if line.reconcile_partial_id:
                if currency_id == line.currency_id.id:
                    if line.amount_residual_currency <= 0:
                        return True
                else:

                    if line.amount_residual <= 0:
                        return True
            return False

        invoice_pool = self.pool.get('account.invoice')
        currency_pool = self.pool.get('res.currency')
        move_line_pool = self.pool.get('account.move.line')
        partner_pool = self.pool.get('res.partner')
        journal_pool = self.pool.get('account.journal')
        line_pool = self.pool.get('account.voucher.line')

        def _check_line_in_to_pay():
            """If the line is associated to a journal entry <- invoice that has status "To Pay", then we're good.
            """
            all_invs_to_pay_ids = invoice_pool.search(cr, uid, [('state', '=', 'to_pay')])
            all_invs_to_pay = invoice_pool.browse(cr, uid, all_invs_to_pay_ids, context=context)
            isInToPay = False

            for inv_to_pay in all_invs_to_pay:
                print '*** treating in loop :  ***' 
                print inv_to_pay.move_id
                if inv_to_pay.move_id == line.move_id:
                    isInToPay = True
                    print inv_to_pay.move_id
                    print ' matches with ' 
                    print line.move_id
                    break
            return isInToPay

        if context is None:
            context = {}
        context_multi_currency = context.copy()

        #set default values
        default = {
            'value': {'line_dr_ids': [], 'line_cr_ids': [], 'pre_line': False},
        }

        # drop existing lines
        line_ids = ids and line_pool.search(cr, uid, [('voucher_id', '=', ids[0])])
        for line in line_pool.browse(cr, uid, line_ids, context=context):
            if line.type == 'cr':
                default['value']['line_cr_ids'].append((2, line.id))
            else:
                default['value']['line_dr_ids'].append((2, line.id))

        if not partner_id or not journal_id:
            return default

        journal = journal_pool.browse(cr, uid, journal_id, context=context)
        partner = partner_pool.browse(cr, uid, partner_id, context=context)
        currency_id = currency_id or journal.company_id.currency_id.id

        total_credit = 0.0
        total_debit = 0.0
        account_type = None
        if context.get('account_id'):
            account_type = self.pool['account.account'].browse(cr, uid, context['account_id'], context=context).type
        if ttype == 'payment':
            if not account_type:
                account_type = 'payable'
            total_debit = price or 0.0
        else:
            total_credit = price or 0.0
            if not account_type:
                account_type = 'receivable'

        if not context.get('move_line_ids', False):
            ids = move_line_pool.search(cr, uid, [('state','=','valid'), ('account_id.type', '=', account_type), ('reconcile_id', '=', False), ('partner_id', '=', partner_id)], context=context)
        else:
            ids = context['move_line_ids']
        invoice_id = context.get('invoice_id', False)
        company_currency = journal.company_id.currency_id.id
        move_lines_found = []

        #order the lines by most old first
        ids.reverse()
        account_move_lines = move_line_pool.browse(cr, uid, ids, context=context)

        #compute the total debit/credit and look for a matching open amount or invoice
        for line in account_move_lines:
            if _remove_noise_in_o2m():
                continue

            if invoice_id:
                if line.invoice.id == invoice_id:
                    #if the invoice linked to the voucher line is equal to the invoice_id in context
                    #then we assign the amount on that line, whatever the other voucher lines
                    move_lines_found.append(line.id)
            elif currency_id == company_currency:
                #otherwise treatments is the same but with other field names
                if line.amount_residual == price:
                    #if the amount residual is equal the amount voucher, we assign it to that voucher
                    #line, whatever the other voucher lines
                    move_lines_found.append(line.id)
                    break
                #otherwise we will split the voucher amount on each line (by most old first)
                total_credit += line.credit and line.amount_residual or 0.0
                total_debit += line.debit and line.amount_residual or 0.0
            elif currency_id == line.currency_id.id:
                if line.amount_residual_currency == price:
                    move_lines_found.append(line.id)
                    break
                line_residual = currency_pool.compute(cr, uid, company_currency, currency_id, abs(line.amount_residual), context=context_multi_currency)
                total_credit += line.credit and line_residual or 0.0
                total_debit += line.debit and line_residual or 0.0

        remaining_amount = price
        #voucher line creation
        for line in account_move_lines:

            if _remove_noise_in_o2m():
                continue

            if line.currency_id and currency_id == line.currency_id.id:
                amount_original = abs(line.amount_currency)
                amount_unreconciled = abs(line.amount_residual_currency)
            else:
                #always use the amount booked in the company currency as the basis of the conversion into the voucher currency
                amount_original = currency_pool.compute(cr, uid, company_currency, currency_id, line.credit or line.debit or 0.0, context=context_multi_currency)
                amount_unreconciled = currency_pool.compute(cr, uid, company_currency, currency_id, abs(line.amount_residual), context=context_multi_currency)
            line_currency_id = line.currency_id and line.currency_id.id or company_currency
            rs = {
                'name':line.move_id.name,
                'type': line.credit and 'dr' or 'cr',
                'move_line_id':line.id,
                'account_id':line.account_id.id,
                'amount_original': amount_original,
                'amount': (line.id in move_lines_found) and min(abs(remaining_amount), amount_unreconciled) or 0.0,
                'date_original':line.date,
                'date_due':line.date_maturity,
                'amount_unreconciled': amount_unreconciled,
                'currency_id': line_currency_id,
            }
            remaining_amount -= rs['amount']
            #in case a corresponding move_line hasn't been found, we now try to assign the voucher amount
            #on existing invoices: we split voucher amount by most old first, but only for lines in the same currency
            if not move_lines_found:
                if currency_id == line_currency_id:
                    if line.credit:
                        amount = min(amount_unreconciled, abs(total_debit))
                        rs['amount'] = amount
                        total_debit -= amount
                    else:
                        amount = min(amount_unreconciled, abs(total_credit))
                        rs['amount'] = amount
                        total_credit -= amount

            if rs['amount_unreconciled'] == rs['amount']:
                rs['reconcile'] = True

            if rs['type'] == 'cr':
                default['value']['line_cr_ids'].append(rs)
            else:
                default['value']['line_dr_ids'].append(rs)

            if len(default['value']['line_cr_ids']) > 0:
                default['value']['pre_line'] = 1
            elif len(default['value']['line_dr_ids']) > 0:
                default['value']['pre_line'] = 1
            default['value']['writeoff_amount'] = self._compute_writeoff_amount(cr, uid, default['value']['line_dr_ids'], default['value']['line_cr_ids'], price, ttype)
        return default
