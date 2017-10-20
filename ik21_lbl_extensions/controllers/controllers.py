# -*- coding: utf-8 -*-
from openerp import http

# class Ik21LblExtensions(http.Controller):
#     @http.route('/ik21_lbl_extensions/ik21_lbl_extensions/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ik21_lbl_extensions/ik21_lbl_extensions/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('ik21_lbl_extensions.listing', {
#             'root': '/ik21_lbl_extensions/ik21_lbl_extensions',
#             'objects': http.request.env['ik21_lbl_extensions.ik21_lbl_extensions'].search([]),
#         })

#     @http.route('/ik21_lbl_extensions/ik21_lbl_extensions/objects/<model("ik21_lbl_extensions.ik21_lbl_extensions"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ik21_lbl_extensions.object', {
#             'object': obj
#         })