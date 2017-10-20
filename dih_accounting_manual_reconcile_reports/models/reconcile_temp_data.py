# -*- coding: utf-8 -*-

from openerp import models, fields, api
import datetime

class reconcile_temp_data(models.Model):
    _name = "dih.accounting.reconcile.temp.data"

    stored_uid = fields.Integer('UID to be stored')
    prev_eomb = fields.Many2one('dih.accounting.manual.reconcile.reports.reconcile.eomb', 'End of month balance for selected previous month')
    current_eomb = fields.Many2one('dih.accounting.manual.reconcile.reports.reconcile.eomb', 'End of month balane for selected month')