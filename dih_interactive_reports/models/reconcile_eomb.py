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

from openerp import models, fields, api
import datetime

class reconcile_eomb(models.Model):

    _name = "dih.accounting.manual.reconcile.reports.reconcile.eomb"

    journal = fields.Many2one('account.journal', 'Associated journal', required="True")
    date_month = fields.Selection([
        (1, 'January'),
        (2, 'February'),
        (3, 'March'),
        (4, 'April'),
        (5, 'May'),
        (6, 'June'),
        (7, 'July'),
        (8, 'August'),
        (9, 'September'),
        (10, 'October'),
        (11, 'November'),
        (12, 'December')
        ],
        'Month', required='True', default=lambda self: self._get_default_month())
    date_year = fields.Integer('Year', required='True', default=lambda self: self._get_default_year())
    balance = fields.Float('End of Month Balance') 

    @api.model
    def _get_default_month(self):
        return datetime.date.today().month
    
    @api.model
    def _get_default_year(self):
        return datetime.date.today().year