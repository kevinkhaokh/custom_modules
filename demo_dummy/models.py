# -*- coding: utf-8 -*-

from datetime import timedelta, date, datetime

import pytz

from openerp import models, fields, api, _, tools
from openerp.exceptions import Warning
from openerp.osv import fields, osv, orm

import logging
_logger = logging.getLogger(__name__)

class dummy(models.Model):
    _name = 'demo_dummy.content'
    _description = 'Dummy content'
