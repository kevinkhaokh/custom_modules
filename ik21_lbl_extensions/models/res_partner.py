# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Partner(models.Model):
    _inherit = 'res.partner'

    name_kh = fields.Char(string="Name in Khmer", required=False, select=True)
    address_kh = fields.Text(string="Address in Khmer", required=False, )
    payable_name = fields.Char(string="", required=False, )