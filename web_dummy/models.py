# -*- coding: utf-8 -*-

from datetime import timedelta, date, datetime

import pytz

from openerp.exceptions import Warning
from openerp.osv import fields, osv, orm

import logging
_logger = logging.getLogger(__name__)

class view(osv.osv):
    _inherit = 'ir.ui.view'

    def __init__(self, pool, cr):
        super(view, self).__init__(pool, cr)
        super(view, self)._columns['type'].selection.append(('dummyview','DummyView'))
        super(view, self)._columns['type'].selection.append(('balancesheet','BalanceSheet'))

        
