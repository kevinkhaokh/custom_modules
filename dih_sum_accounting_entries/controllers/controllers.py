# -*- coding: utf-8 -*-
from openerp import http

# class DihSumAccountingEntries(http.Controller):
#     @http.route('/dih_sum_accounting_entries/dih_sum_accounting_entries/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/dih_sum_accounting_entries/dih_sum_accounting_entries/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('dih_sum_accounting_entries.listing', {
#             'root': '/dih_sum_accounting_entries/dih_sum_accounting_entries',
#             'objects': http.request.env['dih_sum_accounting_entries.dih_sum_accounting_entries'].search([]),
#         })

#     @http.route('/dih_sum_accounting_entries/dih_sum_accounting_entries/objects/<model("dih_sum_accounting_entries.dih_sum_accounting_entries"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('dih_sum_accounting_entries.object', {
#             'object': obj
#         })