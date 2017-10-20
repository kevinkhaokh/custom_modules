# -*- coding: utf-8 -*-

from openerp import models, fields, api

# class ik21_lbl_extensions(models.Model):
#     _name = 'ik21_lbl_extensions.ik21_lbl_extensions'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100